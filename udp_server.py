import logging
import socket
import threading
import sys
import keyboard
import json
from multiprocessing import Process
import enum

class MSG_TYPE(enum.Enum):
    Ping = 0
    Pong = 1

PING_BUFFER = 8

"""
#? ----------- Entry Point Server -----------
Get all connected clients

"""

logger = logging.getLogger()
clients = []

def format_addr(addr):
    return '{}:{}'.format(addr[0], str(addr[1]))

def get_addr_from_str(addr_str):
    addr,port = addr_str.split(':')
    print((addr,int(port)))
    return (addr,int(port))


def SendClientList(sock:socket.socket):
    for client in clients:
        data = [i for i in clients if i != client]
        sock.sendto(json.dumps(data).encode('utf-8'),get_addr_from_str(client))

def HandleClient(sock:socket.socket):
    global MSG_TYPE
    counter = 1
    while True:
        try:
            data,addr = sock.recvfrom(PING_BUFFER)
            print(f'get Ping from {addr}',counter)
            counter+=1
        except socket.timeout:
            print('CLIENT NOT RESPONSE!!\nREMOVE FROM CLIENT LIST')
            clients.remove(format_addr(addr))
            return

        sock.sendto(bytes(MSG_TYPE.Pong.value), addr)

def main(host='0.0.0.0', port=9999):
    global EVENT
    print('start server')
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((host, port))
    # sock.settimeout(30)

    while True:

        
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        logger.info("connection from: %s", addr)
        clients.append(format_addr(addr))

        logger.info(f"NEW CLIENT JOIN {format_addr(addr)}")
        if len(clients) >= 2:
            # send clients to new client
            logger.info(f"SEND INFO TO CLIENTS {len(clients)}")
            SendClientList(sock)
            
            
            


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    proc = Process(target=main)
    proc.start()

    while proc.is_alive():
        if keyboard.is_pressed('q'):
            proc.terminate()
            print('stop server')
            break

