import socket
import threading
import sys
import argparse
from termcolor import colored 


def get_arguments():
    parser = argparse.ArgumentParser(description="TCP port scanner")
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target scan (Ex: -t 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", required=True, help="Victim range to scan (Ex: -p 0-100) or (Ex: -p 22,80,443) or (Ex: 80)")
    options = parser.parse_args()

    return options

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    s.sendall(b'\r\n')  # Envoie un "ping" vide souvent utile
                    banner = s.recv(1024).decode().strip()
                except Exception:
                    banner = "No banner"

                print(colored(f"[+] {port} OPEN - Service: {banner}", "green"))
    except Exception:
        pass

def sort_port(port_int):
    ports = set()

    if "-" in port_int:
        start, end = port_int.split("-")
        ports.update(range(int(start), int(end) + 1))
    
    elif "," in port_int:
        for p in port_int.split(","):
            ports.add(int(p))

    else:
        ports.add(int(port_int))
    
    return sorted(ports)
    

def main():
    
    options = get_arguments()
    target = options.target
    port = sort_port(options.port)
    
    print(f"\n[+] Début du scan de port à: {target}\n")

    try:
        thread_close = []
        for ports in port:
            s = threading.Thread(target=scan_port, args=(target, ports))
            s.start()
            # time.sleep(0.022)
            thread_close.append(s)

        for t in thread_close:
            t.join()

    except KeyboardInterrupt:
        print(colored("\n[!] Scan Stop", "red"))
        sys.exit(1)


if __name__ == "__main__":
    main()
