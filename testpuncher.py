import socket
import sys
import time
import logging
import random
import threading
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SymmetricNATPuncher:
    def __init__(self, stun_server, stun_port):
        self.stun_server = stun_server
        self.stun_port = stun_port
        self.sockets = []
        self.port_mappings = defaultdict(list)
        self.running = True
        
    def create_sockets(self, num_ports=10):
        """Create multiple sockets with different source ports"""
        for _ in range(num_ports):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', 0))
            self.sockets.append(sock)
            logger.info(f"Created socket on local port {sock.getsockname()[1]}")
        
    def get_port_predictions(self):
        """Get predicted NAT port allocations"""
        predictions = []
        for sock in self.sockets:
            try:
                # Send multiple packets to STUN server
                for _ in range(3):
                    sock.sendto(b'predict', (self.stun_server, self.stun_port))
                    data, addr = sock.recvfrom(1024)
                    port = int(data.decode().split(':')[1])
                    self.port_mappings[sock.getsockname()[1]].append(port)
            except Exception as e:
                logger.error(f"Error predicting ports: {e}")
                continue
        
        # Analyze port allocation pattern
        for local_port, mapped_ports in self.port_mappings.items():
            if len(mapped_ports) >= 2:
                port_delta = mapped_ports[1] - mapped_ports[0]
                next_predicted = mapped_ports[-1] + port_delta
                predictions.append(next_predicted)
                
        return predictions

    def aggressive_punch(self, peer_address, base_port, num_ports=1000):
        """Attempt to punch through using predicted port range"""
        logger.info(f"Starting aggressive hole punch to {peer_address}")
        
        # Create thread pool for parallel port probing
        threads = []
        port_range = range(base_port, base_port + num_ports)
        
        chunk_size = num_ports // len(self.sockets)
        for i, sock in enumerate(self.sockets):
            start = base_port + (i * chunk_size)
            end = start + chunk_size
            t = threading.Thread(target=self._probe_ports, 
                               args=(sock, peer_address, range(start, end)))
            threads.append(t)
            t.start()
            
        # Start listeners for each socket
        for sock in self.sockets:
            t = threading.Thread(target=self._listen_socket, args=(sock,))
            threads.append(t)
            t.start()
            
        return threads

    def _probe_ports(self, sock, peer_address, port_range):
        """Probe a range of ports on peer"""
        while self.running:
            for port in port_range:
                try:
                    sock.sendto(b'punch', (peer_address, port))
                    time.sleep(0.001)  # Small delay to prevent flooding
                except Exception as e:
                    logger.error(f"Error probing port {port}: {e}")
                    continue

    def _listen_socket(self, sock):
        """Listen for incoming connections on a socket"""
        sock.settimeout(1)
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                if data == b'punch':
                    logger.info(f"Connection established with {addr}!")
                    # Send acknowledgment
                    sock.sendto(b'punch_ack', addr)
                    self.running = False  # Stop other threads once connection is established
                    return addr
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error in listener: {e}")

def main():
    stun_server = "stun.l.google.com"
    stun_port = 19302
    
    puncher = SymmetricNATPuncher(stun_server, stun_port)
    puncher.create_sockets()
    
    # Get port predictions
    predicted_ports = puncher.get_port_predictions()
    if predicted_ports:
        base_port = min(predicted_ports)
        logger.info(f"Predicted base port: {base_port}")
    else:
        base_port = int(input("Enter peer's base port: "))
    
    peer_address = input("Enter peer IP: ")
    
    # Start hole punching
    threads = puncher.aggressive_punch(peer_address, base_port)
    
    # Wait for threads to complete
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        logger.info("Stopping hole punch...")
        puncher.running = False

if __name__ == "__main__":
    main()