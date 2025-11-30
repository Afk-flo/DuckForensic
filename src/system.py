import platform
import time

import psutil
from rich.table import Table
from rich.console import Console


def format_uptime():
    boot_ts = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_ts)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes or not parts:
        parts.append(f"{minutes}m")

    return " ".join(parts), uptime_seconds


def get_disk_bar(percent, length=20):
    # Petite barre style ███-----
    filled = int(length * percent / 100)
    empty = length - filled
    bar = "█" * filled + "─" * empty
    return bar


def get_system():
    console = Console()

    table = Table(title="System Information", show_lines=True)

    # Colonnes
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Alert", style="red")

    # Infos de base
    table.add_row("Architecture", platform.architecture()[0], "")
    table.add_row("Machine", platform.machine(), "")
    table.add_row("OS", platform.system(), "")
    table.add_row("Processor", platform.processor() or "N/A", "")

    # Uptime
    uptime_str, uptime_seconds = format_uptime()
    uptime_alert = ""
    if uptime_seconds < 3 * 3600:
        uptime_alert = "[bold red]Recently booted (< 3h)[/bold red]"
    table.add_row("Uptime", uptime_str, uptime_alert)

    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_alert = ""
    if cpu_percent > 80:
        cpu_alert = "[bold red]High CPU usage[/bold red]"
    table.add_row("CPU Usage", f"{cpu_percent:.1f} %", cpu_alert)

    # RAM
    mem = psutil.virtual_memory()
    mem_alert = ""
    if mem.percent > 80:
        mem_alert = "[bold red]High memory usage[/bold red]"
    table.add_row("Memory Usage", f"{mem.percent:.1f} %", mem_alert)

    # Disk
    disk = psutil.disk_usage("/")
    disk_bar = get_disk_bar(disk.percent)
    disk_value = f"{disk.percent:.1f} %  [{disk_bar}]"
    disk_alert = ""
    if disk.percent > 90:
        disk_alert = "[bold red]Disk almost full[/bold red]"
    elif disk.percent > 75:
        disk_alert = "[yellow]Disk filling up[/yellow]"

    table.add_row("Disk Usage (/)", disk_value, disk_alert)

    console.print(table)
