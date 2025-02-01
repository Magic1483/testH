import socket
import threading

SERVER_IP = '83.147.245.51'  # Replace with your public server IP
SERVER_PORT = 54321

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            print("Received:", data.decode())
        except:
            break

def start_phone_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.sendall(b'phone')  # Identify as phone
        
        # Start receive thread
        receive_thread = threading.Thread(target=receive_messages, args=(sock,))
        receive_thread.start()

        # Send messages
        while True:
            message = input("Enter message to send: ")
            sock.sendall(message.encode())

if __name__ == "__main__":
    start_phone_client()