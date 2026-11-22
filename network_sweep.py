# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:31:15 2026

@author: dom
"""


import ipaddress
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor


def is_alive(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        capture_output=True, text=True
    )
    return "TTL=" in result.stdout


def check(ip):
    if is_alive(str(ip)):
        return ip
    return None


network = ipaddress.ip_network("192.168.1.0/24")

print(f"Sweeping {network}...")
start_time = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(check, network.hosts())

for ip in results:
    if ip is not None:
        print(f"{ip} is alive")

total_time = time.time() - start_time
print(f"Sweep complete in {total_time:.2f} seconds")
