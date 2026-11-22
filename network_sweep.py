# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:31:15 2026

@author: dom
"""

import ipaddress
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [21, 22, 23, 53, 80, 139, 443, 445, 554, 3389, 8080]

def is_alive(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        capture_output=True, text=True
    )
    return "TTL=" in result.stdout


def get_name(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "unknown"

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def scan_common_ports(ip):
    open_ports = []
    for port in COMMON_PORTS:
        if scan_port(ip, port):
            open_ports.append(port)
    return open_ports

def check(ip):
    ip = str(ip)
    if is_alive(ip):
        return ip, get_name(ip)
    return None


def get_mac_table():
    output = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout
    macs = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1].count("-") == 5:
            macs[parts[0]] = parts[1]
    return macs




network = ipaddress.ip_network("192.168.1.0/24")

print(f"Sweeping {network}...")
start_time = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(check, network.hosts())

macs = get_mac_table()

for result in results:
    if result is not None:
        ip, name = result
        mac = macs.get(ip, "unknown")
        print(f"{ip} is alive ({name}) {mac}")
        ports = scan_common_ports(ip)
        if ports:
            print(f"    open ports: {ports}")
            

total_time = time.time() - start_time
print(f"Sweep complete in {total_time:.2f} seconds")