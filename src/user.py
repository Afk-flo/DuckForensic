import hashlib

import psutil
import pwd
from pathlib import Path
from rich.table import Table
from rich.console import Console
import datetime


def get_user():
    console = Console()

    # Création du tableau
    table = Table(title="Active Users Information", show_lines=True)

    # Colonnes
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("UID", style="magenta")
    table.add_column("GID", style="magenta")
    table.add_column("Home Directory", style="green")
    table.add_column("Shell", style="yellow")
    table.add_column("Suspicious", style="red")

    users = psutil.users()
    console.print(f"[*] Found {len(users)} users\n", style="bold blue")

    for user in users:
        username = user.name
        userI = pwd.getpwnam(username)

        # Home exists ?
        home_path = Path(userI.pw_dir)
        suspicious = ""

        if not home_path.exists():
            suspicious = "[red bold]No home![/red bold]"
        elif userI.pw_uid == 0 and username != "root":
            suspicious = "[red bold]UID 0 (root disguised)[/red bold]"

        # Ajouter au tableau
        table.add_row(
            username,
            str(userI.pw_uid),
            str(userI.pw_gid),
            userI.pw_dir,
            userI.pw_shell,
            suspicious
        )

    console.print(table)


def history_management():
    console = Console()

    users = psutil.users()

    # Création du tableau
    table = Table(title="User files", show_lines=True)

    # Colonnes
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("File", style="magenta")
    table.add_column("Hash", style="magenta")
    table.add_column("Size", style="magenta")
    table.add_column("Last modified", style="green")
    table.add_column("Last accessed", style="yellow")
    table.add_column("Suspicious ?", style="red")

    for user in users:
        username = user.name
        isSuspicious = False

        # Is history ? - get hash
        history_path = Path(f"/home/{username}/.bash_history")

        if not history_path.exists():
            print(f"[-] Can't find {username} history![/]")
        else:
            # hash then metadata
            hash = hashlib.sha256(history_path.read_bytes()).hexdigest()

            if history_path.is_symlink():
                isSuspicious = True

            # Stats metadata for History - is it clean?
            stat = history_path.stat()

            table.add_row(
                username,
                "bash_history",
                hash,
                str(stat.st_size),
                str(datetime.datetime.fromtimestamp(stat.st_mtime)),
                str(datetime.datetime.fromtimestamp(stat.st_atime)),
                str(isSuspicious)
            )

            console.print(table)







