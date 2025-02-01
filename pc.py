import socket
import threading

SERVER_IP = '83.147.245.51'
SERVER_PORT = 54321

def pc_client():
    # Connect to coordinator
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(b"receiver")
        
        # Create listening socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(('0.0.0.0', 0))  # Auto-select port
            listener.listen(1)
            
            # Send external port to coordinator
            external_port = listener.getsockname()[1]
            s.sendall(f"{socket.gethostbyname(socket.gethostname())}:{external_port}".encode())
            s.recv(1024)  # Wait for READY signal

            # Accept direct connection
            conn, addr = listener.accept()
            print(f"Direct connection from {addr} established!")

            # Start communication
            while True:
                data = conn.recv(1024)
                print(f"Received: {data.decode()}")
                response = input("Enter response: ")
                conn.sendall(response.encode())

if __name__ == "__main__":
    pc_client()