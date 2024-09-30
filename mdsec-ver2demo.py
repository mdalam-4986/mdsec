#!/usr/bin/env python3
import os
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init()

def clear_console():
    os.system('clear')  # Clear the console

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    centered_lines = [line.center(terminal_width) for line in text.strip().split('\n')]
    return "\n".join(centered_lines)

def print_centered(text):
    print(center_text(Fore.RED + text + Style.RESET_ALL))

# ASCII Art Logo
logo = """
------------------------------------
 ┳┳┓┏┓┏┓┏┓┏┓  ┏┓┓ ┳┏┓┳┓┏┳┓
┃┃┃┏┛┏┛┏┛┃┃  ┃ ┃ ┃┣ ┃┃ ┃
   ┛ ┗┗┛┗┛┗┛┗┻  ┗┛┗┛┻┗┛┛┗ ┻ v2
created by mdalam-4986
and iamgeo1

Make a Selection: 
1. IP Toolkit
2. MaskPhish
3. ZPhisher
4. CamPhish
5. DDoS Attack
6. Port Scanner
7. Simple IP Grabber
8. Exit

-More features coming soon-
mdsec-ver2.py (demo)
------------------------------------
"""

# Demo Functionality Placeholders
def ddos_function():
    print_centered("DDoS attack simulation...")
    print(Fore.LIGHTGREEN_EX + "Simulated DDoS attack finished." + Style.RESET_ALL)

def port_scanner():
    print_centered("Port Scanner simulation...")
    print(Fore.LIGHTGREEN_EX + "Scanned ports: 22 (open), 80 (open), 443 (closed)" + Style.RESET_ALL)

def simple_ip_grabber():
    print_centered("Simple IP Grabber simulation...")
    print(Fore.LIGHTGREEN_EX + "IP grabbed: 192.168.1.100" + Style.RESET_ALL)

def ip_toolkit():
    print_centered("IP Toolkit simulation...")
    print(Fore.LIGHTGREEN_EX + "Local IP: 192.168.1.10\nPublic IP: 203.0.113.1" + Style.RESET_ALL)

def main_menu():
    while True:
        clear_console()
        print_centered(logo)
        choice = input(Fore.RED + "Choose an option: " + Style.RESET_ALL)
        
        if choice == '1':
            ip_toolkit()
        elif choice == '2':
            print_centered("MaskPhish simulation...\nThis is a demo version, no operations performed.")
        elif choice == '3':
            print_centered("ZPhisher simulation...\nThis is a demo version, no operations performed.")
        elif choice == '4':
            print_centered("CamPhish simulation...\nThis is a demo version, no operations performed.")
        elif choice == '5':
            ddos_function()
        elif choice == '6':
            port_scanner()
        elif choice == '7':
            simple_ip_grabber()
        elif choice == '8':
            print_centered("Exiting the application.")
            break
        else:
            print_centered("Invalid choice, please select a valid option.")

        # Wait for user input before going back to the menu
        input(Fore.LIGHTYELLOW_EX + "Press Enter to return to the menu..." + Style.RESET_ALL)

if __name__ == "__main__":
    main_menu()
