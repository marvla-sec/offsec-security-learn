import argparse
import pandas as pd
from netportscanner.portscanner import PortScanner
from netportscanner.netscanner import arp_scan, print_scan_results

parser = argparse.ArgumentParser()
parser.add_argument("ip_range", help="the target IP range (e.g., 192.168.10.1)")
parser.add_argument("start_port", type=int, help="the starting port number")
parser.add_argument("end_port", type=int, help="the ending port number")

args = parser.parse_args()

devices_list = arp_scan(args.ip_range)

with open("ip_list.txt", "w") as f:
    for device in devices_list:
        f.write(device["ip"] + "\n")

def scan_ips_from_file():
    with open("ip_list.txt", "r") as f:
        for line in f:
            ip = line.strip()
            if not ip:
                continue
            scanner = PortScanner(ip, args.start_port, args.end_port)
            open_ports = scanner.scan_ports()
            yield {
                "IP Address": ip,
                "Open Ports": ", ".join(map(str, open_ports)) if open_ports else "No open ports"
            }

df = pd.DataFrame(scan_ips_from_file())
print(df)
