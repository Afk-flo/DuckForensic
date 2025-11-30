import hashlib
import time

import psutil
import pwd
from pathlib import Path
from rich.table import Table
from rich.console import Console
import datetime

# Will be update soon - Files for User forensic
FILES_TO_CHECK = [
    ".bash_history",
    ".zsh_history",
    ".mysql_history",
    ".viminfo",
    ".lesshst",
    ".ssh/authorized_keys",
]

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
    table.add_column("Size (Bytes)", style="magenta")
    table.add_column("Last modified", style="green")
    table.add_column("Last accessed", style="yellow")
    table.add_column("Suspicious ?", style="red")

    for user in users:
        username = user.name
        isSuspicious = False

        for filename in FILES_TO_CHECK:
            fpath = Path(f"/home/{username}/{filename}")

            if not fpath.exists():
                continue
                 # Fail silently

            # hash then metadata
            file_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()[:12]
            stat = fpath.stat()
            suspicious = []

            if stat.st_size == 0:
                suspicious.append("Empty file")

            if time.time() - stat.st_mtime < 2000:
                suspicious.append("Recently modified (<15 min)")

            # weird permissions
            perms = oct(stat.st_mode & 0o777)
            if perms not in ["0o600", "0o644"]:
                suspicious.append(f"Weird perms: {perms}")

            table.add_row(
                username,
                filename,
                file_hash,
                str(stat.st_size),
                str(datetime.datetime.fromtimestamp(stat.st_mtime)),
                str(datetime.datetime.fromtimestamp(stat.st_atime)),
                ", ".join(suspicious) if suspicious else "[green]OK[/green]"
            )

            console.print(table)







