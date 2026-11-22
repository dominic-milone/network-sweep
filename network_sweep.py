# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:31:15 2026

@author: dom
"""

import ipaddress
import subprocess

network = ipaddress.ip_network("192.168.1.0/24")

for ip in network.hosts():
    print(ip)


def is_alive(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        capture_output=True, text=True
    )
    return "TTL=" in result.stdout


print(is_alive("192.168.1.1"))
print(is_alive("192.168.1.250"))