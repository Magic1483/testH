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
    
    peer_port = int(peer_port)
    for i in range(peer_port-100,peer_port-100):
        # UDP hole punching - send dummy packet
        print(f'sendto {peer_ip}:{i}')
        sock.sendto(b"PUNCH", (peer_ip,i ))
        time.sleep(0.1)

    # while True:
    # data, addr = sock.recvfrom(1024)
    # print(f'answer from {addr} {data}')
        # sock.sendto(b"PUNCH", (peer_ip,))
    
if __name__ == "__main__":
    phone_client()