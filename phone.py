import socket
import threading

SERVER_IP = '83.147.245.51'
SERVER_PORT = 54321

def phone_client():
    # Connect to coordinator
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(b"initiator")
        
        # Get receiver's address
        peer_info = s.recv(1024).decode()
        peer_ip, peer_port = peer_info.split(':')
        print(f"Connecting to {peer_ip}:{peer_port}")

        # Attempt direct connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as direct_conn:
            direct_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            direct_conn.connect((peer_ip, int(peer_port)))
            print("Direct connection established!")
            
            # Start communication
            while True:
                message = input("Enter message: ")
                direct_conn.sendall(message.encode())
                response = direct_conn.recv(1024)
                print(f"Received: {response.decode()}")

if __name__ == "__main__":
    phone_client()