import os

import psutil
from pathlib import Path
import pwd

def get_user():
    """
    Get user informations - list them and try to find malicious one
    """

    users = psutil.users()
    print("[*] Found {} users".format(len(users)))
    for user in users:
        username = user.name
        print("[+] Username: {}".format(username))
        userI = pwd.getpwnam(username)
        print("--> UID: {}".format(userI.pw_uid))
        print("--> GID: {}".format(userI.pw_gid))
        print("--> DIR: {}".format(userI.pw_dir))
        print("--> SHELL: {}".format(userI.pw_shell))


        # Check for /home except root
        if not Path(f"/home/{username}").exists():
            print("[!] User {} don't have a Home - Is this user legit? [!]".format(username))


