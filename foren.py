"""
A simple Linux Forensic tool.
Created in order to retrieve easily important logs for fast investigation.

Author: Afk_flo
Version: 0.1
"""

import os
import platform

from src.system import get_system
from src.user import get_user

banniere = """                                                                                                                    
                                                                                                                              
    ,---,                                  ,-.     ,---,.                                                                     
  .'  .' `\                            ,--/ /|   ,'  .' |                                                   ,--,              
,---.'     \          ,--,           ,--. :/ | ,---.'   |   ,---.    __  ,-.             ,---,            ,--.'|              
|   |  .`\  |       ,'_ /|           :  : ' /  |   |   .'  '   ,'\ ,' ,'/ /|         ,-+-. /  | .--.--.   |  |,               
:   : |  '  |  .--. |  | :    ,---.  |  '  /   :   :  :   /   /   |'  | |' | ,---.  ,--.'|'   |/  /    '  `--'_       ,---.   
|   ' '  ;  :,'_ /| :  . |   /     \ '  |  :   :   |  |-,.   ; ,. :|  |   ,'/     \|   |  ,"' |  :  /`./  ,' ,'|     /     \  
'   | ;  .  ||  ' | |  . .  /    / ' |  |   \  |   :  ;/|'   | |: :'  :  / /    /  |   | /  | |  :  ;_    '  | |    /    / '  
|   | :  |  '|  | ' |  | | .    ' /  '  : |. \ |   |   .''   | .; :|  | ' .    ' / |   | |  | |\  \    `. |  | :   .    ' /   
'   : | /  ; :  | : ;  ; | '   ; :__ |  | ' \ \'   :  '  |   :    |;  : | '   ;   /|   | |  |/  `----.   \  : |__ '   ; :__  
|   | '` ,/  '  :  `--'   \   | '.'|'  : |--' |   |  |   \   \  / |  , ; '   |  / |   | |--'  /  /`--'  /|  | '.'|'   | '.'| 
;   :  .'    :  ,      .-./|   :    :;  |,'    |   :  \    `----'   ---'  |   :    |   |/     '--'.     / ;  :    ;|   :    : 
|   ,.'       `--`----'     \   \  / '--'      |   | ,'                    \   \  /'---'        `--'---'  |  ,   /  \   \  /  
'---'                        `----'            `----'                       `----'                         ---`-'    `----'   
                                                                                                                              
Version 0.1 by @Afk_flo                                                                                                                           
"""


#### Main

if __name__ == '__main__':
    print(banniere)

    if platform.system() != 'Linux':
        print('[!] This tool only works on Linux systems.')
        print("[!] Exiting...")
        exit(1)

    # System informations
    print("[--] Collecting system configuration [--]")
    get_system()

    print("[--] Collecting Users .. [--]")
    get_user()

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