# Network Sweep

A Python tool that scans a local network to find live devices, then checks each one for common open ports. It's a basic version of the recon step a network admin or pentester does on a new network, similar to Nmap's ping sweep combined with a port scan.

I built this to learn how local networks work and to practice Python, threads, and Git.

> **Note:** Only sweep networks you own or have permission to scan. Running this on a network you don't control (like a school or work Wi-Fi) can set off security alerts and may break the rules you agreed to.

## How it works

1. **List addresses.** It takes a network range in CIDR notation (like `192.168.1.0/24`) and generates every usable address in it.
2. **Find live devices.** It pings each address. A device that replies is marked as alive. This uses threads so all the pings happen at once instead of one at a time.
3. **Look up names.** For each live device, it does a reverse DNS lookup to find the device's hostname.
4. **Look up MAC addresses.** It reads the system ARP table (`arp -a`) to match each IP to its hardware MAC address.
5. **Scan common ports.** For each live device, it checks a short list of commonly used ports and reports which are open.

## Requirements

* Python 3
* Windows (uses the `ping` and `arp` commands with Windows syntax)
* No extra libraries needed (uses the built in `ipaddress`, `socket`, `subprocess`, `time`, and `concurrent.futures` modules)

## Usage

Set the network range in the script to match your own network, then run it:

```
python network_sweep.py
```

To find your network range, run `ipconfig` and look at your IPv4 address and subnet mask. A mask of `255.255.255.0` means your range is your first three numbers followed by `.0/24` (for example, `192.168.1.0/24`).

## Ports checked

| Port | Service |
|---|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 53 | DNS |
| 80 | HTTP |
| 139 | NetBIOS |
| 443 | HTTPS |
| 445 | SMB (file sharing) |
| 554 | RTSP (cameras) |
| 3389 | RDP (Remote Desktop) |
| 8080 | HTTP alternate |

## Example output

```
Sweeping 192.168.1.0/24...
192.168.1.1 is alive (router.lan) d4-92-5e-xx-xx-xx
    open ports: [53, 80]
192.168.1.50 is alive (printer.lan) 7c-4d-8f-xx-xx-xx
    open ports: [80, 443]
192.168.1.99 is alive (unknown) 40-f6-bc-xx-xx-xx
Sweep complete in 5.78 seconds
```

## What I learned

* How IP addresses, subnet masks, and CIDR notation describe a network
* The difference between ping (ICMP) and port scanning (TCP)
* How MAC addresses and the ARP table work, and why ARP has no built in verification
* Running system commands from Python with `subprocess` and reading their output
* Reverse DNS lookups with `socket`
* Storing lookups in a dictionary
* Speeding up network tasks with threads (`ThreadPoolExecutor`)
* Using Git and GitHub to track and share my code

## Planned features

* [ ] Take the network range as a command line argument instead of editing the code
* [ ] Look up the manufacturer from each MAC address
* [ ] Catch devices that block ping by trying a TCP connection as a backup
* [ ] Save results to a file (kept out of the repo with .gitignore)
