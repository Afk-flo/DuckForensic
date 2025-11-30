"""
System analysis - OTO
"""
import platform
import psutil

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
    for p in partitions:
        print(f"--- Partitions : {p.device} ---")
        print(f"Mount point : {p.mountpoint}")
        print(f"Type : {p.fstype}")

        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"Size : {usage.total / (1024 ** 3):.2f} Go")
            print(f"Used : {usage.used / (1024 ** 3):.2f} Go")
            print(f"Free : {usage.free / (1024 ** 3):.2f} Go")
        except PermissionError:
            print("[!] Not enough permissions to access this partition .. [!]")

        print()