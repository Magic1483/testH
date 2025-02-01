import socket
import time

SERVER_IP = '83.147.245.51'
SERVER_PORT = 54321

def phone_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Register as initiator
    sock.sendto(b"register:initiator", (SERVER_IP, SERVER_PORT))
    
    # Get receiver coordinates
    while True:
        sock.sendto(b"get_receiver", (SERVER_IP, SERVER_PORT))
        data, _ = sock.recvfrom(1024)
        if data != b"NOT_READY":
            peer_ip, peer_port = data.decode().split(':')
            break
        time.sleep(1)
    
    print(f"Attempting connection to {peer_ip}:{peer_port}")
    
    # UDP hole punching - send dummy packet
    sock.sendto(b"PUNCH", (peer_ip, int(peer_port)))
    
    # Communication loop
    while True:
        message = input("Enter message: ")
        sock.sendto(message.encode(), (peer_ip, int(peer_port)))
        data, _ = sock.recvfrom(1024)
        print(f"Received: {data.decode()}")

if __name__ == "__main__":
    phone_client()