# rendezvous_server.py
import socket

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 50000      # Fixed communication port

clients = {}

def handle_client(conn, addr):
    global clients
    data = conn.recv(1024).decode()
    if data.startswith("REGISTER:"):
        client_id, ip, port = data.split(":")[1:]
        clients[client_id] = (ip, int(port))
        conn.send(b"OK")
    elif data.startswith("REQUEST:"):
        client_id = data.split(":")[1]
        if client_id in clients:
            conn.send(f"{clients[client_id][0]}:{clients[client_id][1]}".encode())
        else:
            conn.send(b"UNKNOWN")
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print("[*] Rendezvous Server Started")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
