"""
System analysis - OTO
"""
import platform
from time import sleep

import psutil
import rich
from diskinfo import demo


def get_system():
    # System basics -
    # Architecture
    print("[+] Architecture: " + platform.architecture()[0])

    # Machine
    print("[+] Machine: " + platform.machine())

    # Node
    print("[+] Node: " + platform.node())

    # Distribution
    print("[+] Distribution: " + platform.system())

    # Current configuration (df, free)
    # Memory info - First with proc/meminfo - Next
    print("[+] Memory info : ")
    with open("/proc/meminfo", "r") as meminfo:
        lines = meminfo.readlines()
        meminfo.close()
    print("     " + lines[0].strip())
    print("     " + lines[1].strip())
    sleep(3)

    # Uptime
    uptime = None
    with open("/proc/uptime", "r") as f:
        uptime = f.readline().split(" ")[0].strip()

    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60
    print("[+] Uptime: " + str(uptime_hours) + ":" + str(uptime_minutes) + " hours")

    if uptime_hours < 3:
        print("[!] Server has been started recently .. [!]")

    partitions = psutil.disk_partitions(all=True)

    print("[+] Partitions: ")
    demo.main()
