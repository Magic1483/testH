import socket
import time

SERVER_IP = '83.147.245.51'
SERVER_PORT = 54321

def pc_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Register as receiver
    sock.sendto(b"register:receiver", (SERVER_IP, SERVER_PORT))
    
    # Get initiator coordinates
    while True:
        data, _ = sock.recvfrom(1024)
        if b':' in data:
            peer_ip, peer_port = data.decode().split(':')
            break
    
    print(f"Expecting connection from {peer_ip}:{peer_port}")
    
    # UDP hole punching - send dummy packet
    sock.sendto(b"PUNCH", (peer_ip, int(peer_port)))
    
    # Communication loop
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received: {data.decode()}")
        response = input("Enter response: ")
        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    pc_client()