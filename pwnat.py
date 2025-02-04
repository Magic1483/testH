#!/usr/bin/env python3
# pwnat.py
import os
import socket
import struct
import select
import time

MAGIC_ID = 0x1337  # Shared identifier between client/server
DUMMY_IP = '1.2.3.4'
ICMP_ECHO_REQUEST = 8
ICMP_TIME_EXCEEDED = 11

def checksum(data):
    sum = 0
    for i in range(0, len(data), 2):
        sum += (data[i] << 8) + data[i+1]
    sum = (sum >> 16) + (sum & 0xffff)
    return ~sum & 0xffff

def create_icmp_packet(icmp_type, code, id, seq, payload=b''):
    header = struct.pack('!BBHHH', icmp_type, code, 0, id, seq)
    data = header + payload
    calc_checksum = checksum(data)
    header = struct.pack('!BBHHH', icmp_type, code, calc_checksum, id, seq)
    return header + payload

def server_mode(local_port):
    # Create raw ICMP socket
    icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, 1)
    
    # Create UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('0.0.0.0', local_port))
    
    print(f"[*] Server mode listening on UDP:{local_port}")
    
    while True:
        # Send ICMP echo requests to dummy IP
        icmp_pkt = create_icmp_packet(ICMP_ECHO_REQUEST, 0, MAGIC_ID, 1)
        icmp_sock.sendto(icmp_pkt, (DUMMY_IP, 0))
        
        # Check for incoming ICMP time exceeded
        rlist, _, _ = select.select([icmp_sock, udp_sock], [], [], 1)
        
        for sock in rlist:
            if sock == icmp_sock:
                pkt, addr = icmp_sock.recvfrom(1024)
                if pkt[20] == ICMP_TIME_EXCEEDED:
                    print(f"[+] Received ICMP time exceeded from {addr[0]}")
            elif sock == udp_sock:
                data, addr = udp_sock.recvfrom(1024)
                print(f"[+] UDP message from {addr}: {data.decode()}")
                udp_sock.sendto(b"ACK: " + data, addr)

def client_mode(server_ip, server_port):
    # Create raw ICMP socket
    icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
    # Create spoofed ICMP time exceeded packet
    original_ip_header = struct.pack('!BBHHHBBH4s4s', 
        0x45, 0, 40, 0, 0, 64, 1, 0, 
        socket.inet_aton(DUMMY_IP), socket.inet_aton(server_ip))
    
    original_icmp = create_icmp_packet(ICMP_ECHO_REQUEST, 0, MAGIC_ID, 1)
    time_exceeded = create_icmp_packet(ICMP_TIME_EXCEEDED, 0, 0, 0, 
                                      original_ip_header + original_icmp[:8])
    
    print(f"[*] Client mode punching hole to {server_ip}:{server_port}")
    
    # Send spoofed ICMP time exceeded
    icmp_sock.sendto(time_exceeded, (server_ip, 0))
    
    # UDP communication
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('0.0.0.0', 0))
    
    for i in range(3):
        udp_sock.sendto(f"PWNAT test {i}".encode(), (server_ip, server_port))
        time.sleep(1)
    
    while True:
        data, addr = udp_sock.recvfrom(1024)
        print(f"[+] Received UDP response: {data.decode()}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='pwnat-style NAT traversal')
    parser.add_argument('-s', '--server', action='store_true', help='Server mode')
    parser.add_argument('-c', '--client', metavar='SERVER_IP', help='Client mode')
    parser.add_argument('-p', '--port', type=int, default=MAGIC_ID, help='Port number')
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        print("Error: This script requires root privileges")
        exit(1)
        
    if args.server:
        server_mode(args.port)
    elif args.client:
        if not args.client:
            print("Error: Client mode requires server IP")
            exit(1)
        client_mode(args.client, args.port)
    else:
        parser.print_help()