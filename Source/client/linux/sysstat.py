"""
This script gets system statistics in a linux enviroment:

*   Memory usage
*   CPU usage
*   Total uptime
*   Security event logs
"""

from datetime import datetime

class SysStats:
    """ Returns systems statistics:
    *   Memory usage
    *   CPU usage
    *   Total uptime
    *   Security event logs
    """
    def mem_usage(self):
        ram_usage = {
            "MemTotal": 0,
            "MemFree": 0,
            "MemAvailable": 0,
            "Cached": 0,
            "Date&Time": ""
            }

        with open('/proc/meminfo') as meminfo:
            for line in meminfo:
                for key in ram_usage:
                    if key in line:
                        ram_usage[key] = int(line.split()[1])

        ram_usage["Date&Time"] = datetime.now().ctime()
        return ram_usage

    def cpu_usage(self):
        pass

    def uptime(self):
        pass

    def security_events(self):
        pass


def main():
    """
    module test
    """
    stats = SysStats()
    print(stats.mem_usage())

if __name__ == '__main__':
    main()
