# client.py
import py3stun
import socket
import time
import random

RENDEZVOUS_SERVER = ("83.147.245.51", 50000)


ports = []
def register_with_rendezvous(client_id, external_ip, external_port):
    """Send NAT mapping info to the rendezvous server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(RENDEZVOUS_SERVER)
        sock.send(f"REGISTER:{client_id}:{external_ip}:{external_port}".encode())
        res = sock.recv(1024)
        ports.append(res.decode('utf8'))
        print(ports)

for i in range(25):
    register_with_rendezvous('a','ip',233)
    time.sleep(5)
