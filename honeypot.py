import socket
import csv
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2323
LOG_FILE = "attempts.csv"

def log_attempt(ip, username, password):
    new_file = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time", "ip", "username", "password"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         ip, username, password])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print("Honeypot listening on port", PORT)

while True:
    conn, addr = server.accept()
    print("Connection from", addr[0])
    conn.sendall(b"Ubuntu 22.04 LTS\r\nlogin: ")
    username = conn.recv(1024).decode(errors="ignore").strip()
    conn.sendall(b"Password: ")
    password = conn.recv(1024).decode(errors="ignore").strip()
    log_attempt(addr[0], username, password)
    print("Tried:", username, password)
    conn.sendall(b"\r\nLogin incorrect\r\n")
    conn.close()
