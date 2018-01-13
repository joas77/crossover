"""
Script to collect machine statistics in an intranet environment
"""
import xml.etree.ElementTree as ET
import paramiko
import socket

def get_clients_cfg():
    """
    Reads client's settins from ./config/clients_config.xml and
    returns a list of dictionaries with clients configurations
    """
    #TODO
    cfgtree = ET.parse("./config/clients_config.xml")
    return [{'ip':'127.0.0.1',
            'port':2222,
            'username': 'vagrant',
            'password':'vagrant',
            }]

def send_script(hostname, username, port, password, script_file, remote_path):
    """" send systat.py script to client"""
    transport = paramiko.Transport((hostname, port))
    transport.connect(hostkey=None,
                      username=username,
                      password=password,
                      gss_host=socket.getfqdn(hostname)
                     )
    sftp = paramiko.SFTPClient.from_transport(transport)

    # copy this demo onto the client
    print('creating ' +  remote_path + ' file in client '+ username +'@' + hostname + ' ...')
    try:
        sftp.mkdir("crossover_tmp_folder")
    except IOError:
        print('(assuming temporal folder already exists)')

    sftp.put(script_file, remote_path)
    transport.close()

def exec_client_script(hostname, username, port, password, remote_path):
    """"execute systat.py script in client and receives data"""
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname, port, username, password)
    print("executing client script in client {0}@{1}".format(username, hostname))
    stdin, stdout, stderr = client.exec_command('python3 ' + remote_path)
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()

def main():
    """main function """
    print(get_clients_cfg())
    # ssh conection test: ssh vagrant@127.0.0.1 -p 2222
    script_path = '../client/linux/sysstat.py'
    remote_path = 'crossover_tmp_folder/sysstat.py'
    for clientcfg in get_clients_cfg():
        ip = clientcfg['ip']
        port = clientcfg['port']
        username = clientcfg['username']
        password = clientcfg['password']

        send_script(ip, username, port, password, script_path, remote_path)

        exec_client_script(ip, username, port, password, remote_path)



if __name__ == '__main__':
    main()
