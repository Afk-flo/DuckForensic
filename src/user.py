import hashlib
import time
import stat
import datetime
from pathlib import Path

import psutil
import pwd
from rich.table import Table
from rich.console import Console


# Fichiers intéressants pour la forensic utilisateur
FILES_TO_CHECK = [
    ".bash_history",
    ".zsh_history",
    ".sh_history",
    ".mysql_history",
    ".viminfo",
    ".lesshst",
    ".ssh/authorized_keys",
    ".ssh/known_hosts",
    ".bashrc",
    ".profile",
]


def _get_real_users():
    """
    Retourne les "vrais" utilisateurs :
    - root
    - UID >= 1000 (classique Linux)
    """
    users = []
    for entry in pwd.getpwall():
        uid = entry.pw_uid
        if uid == 0 or uid >= 1000:
            users.append(entry)
    return users


def get_user():
    """
    Affiche les infos des vrais users (root + UID >= 1000),
    et marque qq trucs suspects.
    """
    console = Console()

    table = Table(title="Users information", show_lines=True)
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("UID", style="magenta")
    table.add_column("GID", style="magenta")
    table.add_column("Home Directory", style="green")
    table.add_column("Shell", style="yellow")
    table.add_column("Active session", style="blue")
    table.add_column("Suspicious", style="red")

    # Users avec session active (psutil = "who")
    active_usernames = {u.name for u in psutil.users()}

    real_users = _get_real_users()
    console.print(f"[*] Found {len(real_users)} real users\n", style="bold blue")

    for entry in real_users:
        username = entry.pw_name
        uid = entry.pw_uid
        gid = entry.pw_gid
        home = entry.pw_dir
        shell = entry.pw_shell

        home_path = Path(home)
        suspicious = []

        # Home manquant
        if not home_path.exists():
            suspicious.append("No home dir")

        # UID 0 mais pas root → root déguisé
        if uid == 0 and username != "root":
            suspicious.append("UID 0 (fake root?)")

        # Shell chelou
        if shell in ("/usr/sbin/nologin", "/bin/false"):
            suspicious.append("Login disabled shell")
        elif shell not in ("/bin/bash", "/usr/bin/zsh", "/usr/bin/fish"):
            suspicious.append(f"Weird shell: {shell}")

        active = "[green]yes[/green]" if username in active_usernames else "no"

        table.add_row(
            username,
            str(uid),
            str(gid),
            home,
            shell or "N/A",
            active,
            ", ".join(f"[red]{s}[/red]" for s in suspicious) if suspicious else "[green]OK[/green]",
        )

    console.print(table)


def history_management():
    """
    Pour chaque user réel, affiche un tableau listant ses fichiers sensibles :
    - history, .ssh, profils, etc.
    Avec hash, taille, dates, et indicateurs suspects.
    """
    console = Console()

    active_usernames = {u.name for u in psutil.users()}
    real_users = _get_real_users()

    for entry in real_users:
        username = entry.pw_name
        home = Path(entry.pw_dir)

        # Si pas de home, on affiche juste une ligne d'info
        if not home.exists():
            console.print(f"[red]User {username}: home directory {home} does not exist[/red]")
            continue

        # Un tableau PAR user (comme tu voulais)
        table = Table(title=f"User files: {username}", show_lines=True)
        table.add_column("File", style="magenta")
        table.add_column("Size (Bytes)", style="magenta")
        table.add_column("Last modified", style="green")
        table.add_column("Last accessed", style="yellow")
        table.add_column("Suspicious ?", style="red")
        table.add_column("Hash (sha256, 1st 12)", style="cyan")

        has_rows = False  # pour ne pas afficher de tableau vide

        for relpath in FILES_TO_CHECK:
            fpath = home / relpath

            if not fpath.exists():
                continue  # On ignore silencieusement les fichiers absents

            susp = []
            try:
                stat_info = fpath.stat()
            except FileNotFoundError:
                continue

            size = stat_info.st_size
            mtime = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            atime = datetime.datetime.fromtimestamp(stat_info.st_atime)
            perms = oct(stat_info.st_mode & 0o777)

            # Règles "suspect" :

            # Symlink → possible masquage (ex: .bash_history → /dev/null)
            if fpath.is_symlink():
                try:
                    target = fpath.resolve()
                    susp.append(f"symlink → {target}")
                    if "null" in str(target):
                        susp.append("history redirected to null")
                except Exception:
                    susp.append("symlink (unresolved)")

            # Fichier vide → effacement d'historique ?
            if size == 0:
                susp.append("empty")

            # Modifié récemment (< 15 min)
            if time.time() - stat_info.st_mtime < 900:  # 900s = 15min
                susp.append("recent mtime (<15min)")

            # Permissions cheloues
            if perms not in ["0o600", "0o644"]:
                susp.append(f"weird perms: {perms}")
            # World writable
            if stat_info.st_mode & stat.S_IWOTH:
                susp.append("world writable")

            # Hash (pour vérifier si le contenu change dans le temps)
            try:
                file_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()[:12]
            except Exception:
                file_hash = "unreadable"

            suspicious_str = (
                "[green]OK[/green]"
                if not susp
                else ", ".join(f"[red]{s}[/red]" for s in susp)
            )

            table.add_row(
                relpath,
                str(size),
                str(mtime),
                str(atime),
                suspicious_str,
                file_hash,
            )
            has_rows = True

        # Afficher seulement si on a trouvé au moins un fichier intéressant
        if has_rows:
            active_str = (
                "[green]active session[/green]" if username in active_usernames else "no active session"
            )
            console.print(f"\n[bold blue]User: {username}[/bold blue] ({active_str})")
            console.print(table)
