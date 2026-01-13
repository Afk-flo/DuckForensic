"""
A simple Linux Forensic tool.
Created in order to retrieve easily important logs for fast investigation.

Author: Afk_flo
Version: 0.1
"""

import os
import platform
from rich.console import Console

from src.system import get_system
from src.user import get_user, history_management
from rich.text import Text

console = Console()

banniere = r"""                                                                                                                    
░███████                         ░██       ░██████████                                                     ░██           
░██   ░██                        ░██       ░██                                                                           
░██    ░██ ░██    ░██  ░███████  ░██    ░██░██         ░███████  ░██░████  ░███████  ░████████   ░███████  ░██ ░███████  
░██    ░██ ░██    ░██ ░██    ░██ ░██   ░██ ░█████████ ░██    ░██ ░███     ░██    ░██ ░██    ░██ ░██        ░██░██    ░██ 
░██    ░██ ░██    ░██ ░██        ░███████  ░██        ░██    ░██ ░██      ░█████████ ░██    ░██  ░███████  ░██░██        
░██   ░██  ░██   ░███ ░██    ░██ ░██   ░██ ░██        ░██    ░██ ░██      ░██        ░██    ░██        ░██ ░██░██    ░██ 
░███████    ░█████░██  ░███████  ░██    ░██░██         ░███████  ░██       ░███████  ░██    ░██  ░███████  ░██ ░███████  
                                                                                                                                                                                                                                                                        
Version 0.8 by @Afk_flo                                                                                                                           
"""


#### Main

if __name__ == '__main__':
    text = Text(banniere)
    text.stylize("bold blue", 0, len(banniere) // 2)
    text.stylize("bold magenta", len(banniere) // 2)

    console.print(text)
    if platform.system() != 'Linux':
        print('[!] This tool only works on Linux systems.')
        print("[!] Exiting...")
        exit(1)

    # System informations
    print("[--] Collecting system configuration [--]")
    get_system()

    print(" ")
    print(" ")

    print("[--] Collecting Users .. [--]")
    get_user()
    history_management()

    """
    @TODO :
    - Create tmp folder + files
    - Identifier l'OS / Plateforme 
    - Get basic data (df, free)
    - Get Users 
        - SSH, history, etc..
    - Get Services 
        - Logs
    """
