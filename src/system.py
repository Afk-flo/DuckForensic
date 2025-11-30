"""
System analysis - OTO
"""
import platform
from time import sleep

import psutil
from diskinfo import demo
from rich.table import Table
from rich.console import Console

def get_system():
    console = Console()

    table = Table(title="System Information", show_lines=True)

    # Colonnes
    table.add_column("System", style="cyan", no_wrap=True)
    table.add_column("Data", style="magenta")
    table.add_column("Data", style="red")

    table.add_row("Architecture", platform.architecture()[0])
    table.add_row("Machine", platform.machine())
    table.add_row("Operating System", platform.system())
    table.add_row("Processor", platform.processor())
    table.add_row("Uptime", str(psutil.boot_time()))
    table.add_row("CPU Usage", str(psutil.cpu_percent()))
    table.add_row("Memory Usage", str(psutil.virtual_memory().percent))
    table.add_row("Disk Usage", str(psutil.disk_usage('/')))

    """
    uptime = None
    with open("/proc/uptime", "r") as f:
        uptime = f.readline().split(" ")[0].strip()

    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60
    print("[+] Uptime: " + str(uptime_hours) + ":" + str(uptime_minutes) + " hours")

    if uptime_hours < 3:
        print("[!] Server has been started recently .. [!]")
    """

