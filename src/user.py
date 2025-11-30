import psutil

def get_user():
    """
    Get user informations - list them and try to find malicious one
    """

    users = psutil.users()
    print("[*] Found {} users".format(len(users)))
    for user in users:
        username = user.name
        print("[+] Username: {}".format(username))


