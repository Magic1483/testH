# client.py
import py3stun
import socket
import time
import random

RENDEZVOUS_SERVER = ("83.147.245.51", 50000)  # Replace with actual public IP of the server
STUN_SERVER = "stun.l.google.com"
STUN_PORT = 19302
TTL_VALUES = [1, 2, 3, 4]  # Short TTLs for initial NAT table entries
BREADTH = 5  # Number of nearby ports to test for hole punching

def get_external_ip_port():
    """Query STUN server to get external IP and port."""
    nat_type, external_ip, external_port = py3stun.get_ip_info(
        stun_host=STUN_SERVER, stun_port=STUN_PORT
        )
    return nat_type, external_ip, external_port

def send_udp_probe(target_ip, target_port, ttl):
    """Send a UDP probe to open NAT entries."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        sock.sendto(b"Hello from Client!", (target_ip, target_port))

def register_with_rendezvous(client_id, external_ip, external_port):
    """Send NAT mapping info to the rendezvous server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(RENDEZVOUS_SERVER)
        sock.send(f"REGISTER:{client_id}:{external_ip}:{external_port}".encode())
        response = sock.recv(1024)
        return response == b"OK"

def request_peer_info(peer_id):
    """Request peer's NAT mapping from the rendezvous server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(RENDEZVOUS_SERVER)
        sock.send(f"REQUEST:{peer_id}".encode())
        data = sock.recv(1024).decode()
        return data.split(":") if data != "UNKNOWN" else None

def listen_for_udp():
    """Listen for incoming UDP connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("", 0))
        local_port = sock.getsockname()[1]
        print(f"[*] Listening on UDP Port {local_port}...")

        nat_type, external_ip, external_port = get_external_ip_port()
        register_with_rendezvous("client_b", external_ip, external_port)

        while True:
            data, addr = sock.recvfrom(1024)
            print(f"[+] Received UDP from {addr}: {data.decode()}")

def perform_hole_punching(target_ip, base_port):
    """Send multiple UDP packets with different TTL values to predicted ports."""
    
    for offset in range(-BREADTH, BREADTH+1):
        predicted_port = base_port + offset
        send_udp_probe(target_ip, predicted_port, 2)
        time.sleep(0.1)
    
    for offset in range(-BREADTH, BREADTH+1):
        predicted_port = base_port + offset
        send_udp_probe(target_ip, predicted_port, 128)
        time.sleep(0.1)
    

if __name__ == "__main__":
    print("[*] Starting NAT Traversal...")
    nat_type, external_ip, external_port = get_external_ip_port()
    print(f"[*] Detected NAT: {nat_type}, Public IP: {external_ip}, Public Port: {external_port}")

    is_initiator = input("Are you Client A (initiator)? (y/n): ").lower() == "y"

    if is_initiator:
        register_with_rendezvous("client_a", external_ip, external_port)
        print("[*] Waiting for Client B to register...")

        time.sleep(5)  # Allow time for Client B to register

        peer_info = request_peer_info("client_b")
        if peer_info:
            peer_ip, peer_port = peer_info
            print(f"[+] Received Peer Info: {peer_ip}:{peer_port}")

            print("[*] Performing Two-Stage Hole Punching...")
            perform_hole_punching(peer_ip, int(peer_port))
            perform_hole_punching(peer_ip, int(peer_port))
        else:
            print("[!] Failed to get peer info.")
    else:
        listen_for_udp()
