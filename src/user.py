import psutil
import pwd
from pathlib import Path
from rich.table import Table
from rich.console import Console


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
