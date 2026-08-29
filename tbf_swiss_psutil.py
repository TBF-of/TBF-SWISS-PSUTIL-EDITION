#!/usr/bin/env python3
# ============================================
#   TBF-SWISS v2.1 — PSUTIL EDITION
#   Swiss Army Knife for Linux/PC
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

import os
import sys
import time
import socket
import subprocess
import hashlib
import base64
import random
import string
import requests
import json
import uuid
import platform
import psutil
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# ============================================
#   BANNER
# ============================================
BANNER = """
[bold magenta]╔══════════════════════════════════════════════════════════════════╗
[bold magenta]║                                                                  ║
[bold magenta]║    ████████╗██████╗ ███████╗    ███████╗██╗    ██╗██╗███████╗███████╗
[bold magenta]║    ╚══██╔══╝██╔══██╗██╔════╝    ██╔════╝██║    ██║██║██╔════╝██╔════╝
[bold magenta]║       ██║   ██████╔╝█████╗      ███████╗██║ █╗ ██║██║███████╗███████╗
[bold magenta]║       ██║   ██╔══██╗██╔══╝      ╚════██║██║███╗██║██║╚════██║╚════██║
[bold magenta]║       ██║   ██████╔╝██║         ███████║╚███╔███╔╝██║███████║███████║
[bold magenta]║       ╚═╝   ╚═════╝ ╚═╝         ╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝
[bold magenta]║                                                                  ║
[bold magenta]║           TBF-SWISS v2.1 — PSUTIL EDITION                      ║
[bold magenta]║          by TBFPUMBA — Technology. Security. Efficiency.        ║
[bold magenta]║                                                                  ║
[bold magenta]╚══════════════════════════════════════════════════════════════════╝[bold cyan]"""

# ============================================
#   UTILITY FUNCTIONS
# ============================================

def clear_screen():
    os.system('clear')

def loading_effect(text="Loading", duration=0.5):
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]{text}...", total=100)
        for i in range(100):
            time.sleep(duration / 100)
            progress.update(task, advance=1)

# ============================================
#   SYSTEM FUNCTIONS (PSUTIL)
# ============================================

def system_info():
    loading_effect("Getting system info")
    info = [
        ("OS", platform.system()),
        ("Version", platform.version()),
        ("Hostname", socket.gethostname()),
        ("Python", sys.version.split()[0]),
        ("CPU Cores", psutil.cpu_count()),
        ("Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ]
    for key, value in info:
        console.print(f"[cyan]{key}:[/cyan] {value}")
    input("\n[dim]Press Enter...[/dim]")

def cpu_usage():
    loading_effect("Getting CPU info")
    cpu = psutil.cpu_percent(interval=0.5)
    console.print(f"[green]💻 CPU Usage: {cpu}%[/green]")
    input("\n[dim]Press Enter...[/dim]")

def ram_usage():
    loading_effect("Getting RAM info")
    mem = psutil.virtual_memory()
    console.print(f"[green]🧠 RAM Usage: {mem.percent}% ({mem.used // 1024**2} / {mem.total // 1024**2} MB)[/green]")
    input("\n[dim]Press Enter...[/dim]")

def disk_usage():
    loading_effect("Getting disk info")
    disk = psutil.disk_usage('/')
    console.print(f"[green]💾 Disk Usage: {disk.percent}% ({disk.used // 1024**2} / {disk.total // 1024**2} MB)[/green]")
    input("\n[dim]Press Enter...[/dim]")

def uptime():
    loading_effect("Getting uptime")
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            console.print(f"[green]⏱️ Uptime: {hours}h {minutes}m[/green]")
    except:
        console.print("[red]❌ Could not get uptime[/red]")
    input("\n[dim]Press Enter...[/dim]")

# ============================================
#   NETWORK FUNCTIONS
# ============================================

def ping_host():
    host = Prompt.ask("[bold green]📝 Enter host (e.g., google.com)[/bold green]")
    loading_effect(f"Pinging {host}")
    result = os.system(f"ping -c 4 {host} > /dev/null 2>&1")
    if result == 0:
        console.print("[green]✅ Host is up[/green]")
    else:
        console.print("[red]❌ Host is down[/red]")
    input("\n[dim]Press Enter...[/dim]")

def port_scanner():
    host = Prompt.ask("[bold green]📝 Enter IP or host[/bold green]")
    port_range = Prompt.ask("[bold green]📝 Enter ports (e.g., 80,443 or 20-100)[/bold green]")
    loading_effect(f"Scanning {host}")
    
    ports = []
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        ports = list(range(start, end+1))
    else:
        ports = [int(p.strip()) for p in port_range.split(',')]
    
    open_ports = []
    for port in ports[:20]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
        console.print(f"[cyan]Scanning port {port}...[/cyan]", end="\r")
    
    if open_ports:
        console.print(f"[green]✅ Open ports: {open_ports}[/green]")
    else:
        console.print("[red]❌ No open ports found[/red]")
    input("\n[dim]Press Enter...[/dim]")

def ip_geo():
    ip = Prompt.ask("[bold green]📝 Enter IP address[/bold green]")
    loading_effect(f"Getting location for {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data['status'] == 'success':
            console.print(f"[green]📍 Location: {data['city']}, {data['regionName']}, {data['country']}[/green]")
            console.print(f"[blue]📡 ISP: {data['isp']}[/blue]")
            console.print(f"[blue]🗺️ Coordinates: {data['lat']}, {data['lon']}[/blue]")
        else:
            console.print("[red]❌ IP not found[/red]")
    except:
        console.print("[red]❌ Error fetching data[/red]")
    input("\n[dim]Press Enter...[/dim]")

def dns_lookup():
    domain = Prompt.ask("[bold green]📝 Enter domain[/bold green]")
    loading_effect(f"Looking up {domain}")
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[green]✅ {domain} → {ip}[/green]")
    except:
        console.print("[red]❌ Domain not found[/red]")
    input("\n[dim]Press Enter...[/dim]")

def whois_lookup():
    domain = Prompt.ask("[bold green]📝 Enter domain[/bold green]")
    loading_effect(f"WHOIS for {domain}")
    try:
        result = subprocess.run(f"whois {domain}", shell=True, capture_output=True, text=True)
        lines = result.stdout.split('\n')[:20]
        for line in lines:
            console.print(f"[cyan]{line}[/cyan]")
    except:
        console.print("[red]❌ WHOIS failed[/red]")
    input("\n[dim]Press Enter...[/dim]")

# ============================================
#   GENERATORS
# ============================================

def generate_password():
    length = int(Prompt.ask("[bold green]📝 Length (default 16)[/bold green]", default="16"))
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    password = ''.join(random.choices(chars, k=length))
    console.print(f"[green]🔑 Password: {password}[/green]")
    input("\n[dim]Press Enter...[/dim]")

def generate_hash():
    text = Prompt.ask("[bold green]📝 Enter text to hash[/bold green]")
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha1 = hashlib.sha1(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    console.print(f"[cyan]MD5:[/cyan] {md5}")
    console.print(f"[cyan]SHA1:[/cyan] {sha1}")
    console.print(f"[cyan]SHA256:[/cyan] {sha256}")
    input("\n[dim]Press Enter...[/dim]")

def base64_tool():
    choice = Prompt.ask("[bold green]📝 Encode (e) or Decode (d)[/bold green]")
    text = Prompt.ask("[bold green]📝 Enter text[/bold green]")
    if choice.lower() == 'e':
        encoded = base64.b64encode(text.encode()).decode()
        console.print(f"[green]✅ Encoded: {encoded}[/green]")
    else:
        try:
            decoded = base64.b64decode(text).decode()
            console.print(f"[green]✅ Decoded: {decoded}[/green]")
        except:
            console.print("[red]❌ Invalid Base64[/red]")
    input("\n[dim]Press Enter...[/dim]")

def generate_mac():
    mac = ':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))
    console.print(f"[green]📡 MAC: {mac}[/green]")
    input("\n[dim]Press Enter...[/dim]")

def generate_ip():
    ip = '.'.join(str(random.randint(1, 255)) for _ in range(4))
    console.print(f"[green]🌐 IP: {ip}[/green]")
    input("\n[dim]Press Enter...[/dim]")

def generate_uuid():
    console.print(f"[green]🔢 UUID: {uuid.uuid4()}[/green]")
    input("\n[dim]Press Enter...[/dim]")

def generate_random():
    length = int(Prompt.ask("[bold green]📝 Length (default 16)[/bold green]", default="16"))
    result = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    console.print(f"[green]✅ Random string: {result}[/green]")
    input("\n[dim]Press Enter...[/dim]")

def qr_generator():
    text = Prompt.ask("[bold green]📝 Enter text for QR code[/bold green]")
    try:
        import qrcode
        img = qrcode.make(text)
        img.save("qrcode.png")
        console.print("[green]✅ QR code saved as qrcode.png[/green]")
    except ImportError:
        console.print("[yellow]⚠️ Install qrcode: pip install qrcode[/yellow]")
    input("\n[dim]Press Enter...[/dim]")

def download_file():
    url = Prompt.ask("[bold green]📝 Enter URL to download[/bold green]")
    loading_effect(f"Downloading from {url}")
    try:
        r = requests.get(url, stream=True)
        filename = url.split('/')[-1] or 'download'
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        console.print(f"[green]✅ Downloaded: {filename}[/green]")
    except:
        console.print("[red]❌ Download failed[/red]")
    input("\n[dim]Press Enter...[/dim]")

def check_website():
    url = Prompt.ask("[bold green]📝 Enter URL (e.g., google.com)[/bold green]")
    loading_effect(f"Checking {url}")
    try:
        r = requests.get(f"http://{url}", timeout=5)
        console.print(f"[green]✅ Status: {r.status_code} - {r.reason}[/green]")
    except:
        console.print("[red]❌ Site is down or unreachable[/red]")
    input("\n[dim]Press Enter...[/dim]")

# ============================================
#   MENU
# ============================================

def show_menu():
    clear_screen()
    console.print(Align.center(BANNER))
    console.print()
    console.print("[bold red]┌─────────────────────────────────────────────────────────────┐[/bold red]")
    console.print("[bold red]│[/bold red] [bold yellow]📂 TBF-SWISS v2.1 — PSUTIL EDITION[/bold yellow]                     [bold red]│[/bold red]")
    console.print("[bold red]├─────────────────────────────────────────────────────────────┤[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]1.[/bold cyan] 🌐 Ping host                             [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]2.[/bold cyan] 📡 Port scanner                         [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]3.[/bold cyan] 🌍 IP geolocation                       [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]4.[/bold cyan] 📡 DNS lookup                          [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]5.[/bold cyan] 📋 WHOIS                              [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]6.[/bold cyan] 🖥️ System info                        [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]7.[/bold cyan] 💻 CPU usage                          [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]8.[/bold cyan] 🧠 RAM usage                          [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]9.[/bold cyan] 💾 Disk usage                         [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]10.[/bold cyan] ⏱️ Uptime                             [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]11.[/bold cyan] 🔑 Generate password                  [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]12.[/bold cyan] 🔐 Hash generator (MD5/SHA1/SHA256)   [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]13.[/bold cyan] 🔄 Base64 encode/decode              [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]14.[/bold cyan] 📡 Generate MAC                      [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]15.[/bold cyan] 🌐 Generate IP                       [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]16.[/bold cyan] 🔢 Generate UUID                     [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]17.[/bold cyan] 📊 Generate random string            [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]18.[/bold cyan] 📊 Generate QR code                  [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]19.[/bold cyan] 📥 Download file                     [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]20.[/bold cyan] 🌐 Check website status              [bold red]│[/bold red]")
    console.print("[bold red]│[/bold red] [bold cyan]21.[/bold cyan] 🧹 Clear screen                     [bold red]│[/bold red]")
    console.print("[bold red]├─────────────────────────────────────────────────────────────┤[/bold red]")
    console.print("[bold red]│[/bold red] [bold red]0.[/bold red] ❌ Exit                                [bold red]│[/bold red]")
    console.print("[bold red]└─────────────────────────────────────────────────────────────┘[/bold red]")
    console.print()
    return Prompt.ask("[bold green]TBF-SWISS>[/bold green]")

# ============================================
#   MAIN
# ============================================

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            ping_host()
        elif choice == "2":
            port_scanner()
        elif choice == "3":
            ip_geo()
        elif choice == "4":
            dns_lookup()
        elif choice == "5":
            whois_lookup()
        elif choice == "6":
            system_info()
        elif choice == "7":
            cpu_usage()
        elif choice == "8":
            ram_usage()
        elif choice == "9":
            disk_usage()
        elif choice == "10":
            uptime()
        elif choice == "11":
            generate_password()
        elif choice == "12":
            generate_hash()
        elif choice == "13":
            base64_tool()
        elif choice == "14":
            generate_mac()
        elif choice == "15":
            generate_ip()
        elif choice == "16":
            generate_uuid()
        elif choice == "17":
            generate_random()
        elif choice == "18":
            qr_generator()
        elif choice == "19":
            download_file()
        elif choice == "20":
            check_website()
        elif choice == "21":
            clear_screen()
        elif choice == "0":
            console.print("[green]👋 Goodbye![/green]")
            sys.exit(0)
        else:
            console.print("[red]❌ Invalid choice[/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
