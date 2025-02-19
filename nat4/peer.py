import logging
from os import stat
import socket
import sys
import time
import threading
import argparse
import struct

logger = logging.getLogger()
peers = []
RUN_EVENT = threading.Event()


def AddrToMsg(addr):
    """
    """
    s = addr[0]+':'+str(addr[1])
    return str(s).encode('utf8')

def MsgToAddr(addr):
    """
    """
    ip,port = addr.decode('utf8').split(':')
    return (ip,int(port))


def Listen(sock:socket.socket):
    global RUN_EVENT
    while  not RUN_EVENT.is_set():
        data,addr = sock.recvfrom(1024)
        logger.info('REC '+str(data))

def Send(sock:socket.socket,addr,window,mode):
    global RUN_EVENT
    ttl_values = [1,2,3,4,5,6,7]

    while not RUN_EVENT.is_set():
        if mode == 'r':logger.info(f'SEND SHORT TTL TO PORT [ {addr[1]} - {addr[1]+window} ]')
        if mode == 'i':logger.info(f'SEND LONG TTL TO PORT [ {addr[1]} - {addr[1]+window} ]')

        for offset in range(window+1):
            msg = b'test request'
            if mode == 'r': # reciever mode
                for t in ttl_values:
                    sock.setsockopt(socket.IPPROTO_IP,socket.IP_TTL,struct.pack('I', t))
                    sock.sendto(msg,(addr[0],addr[1]+offset))
            else: # sender mode
                sock.sendto(msg,(addr[0],addr[1]+offset))

        time.sleep(0.5)


def main(mode,server_host = '83.147.245.51', server_port = 9999):
    # Peer 1 send short TTL packets
    # Peer 2 send long TTL packets

    global RUN_EVENT
    window = 100 # offset for port of peer
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(b'',(server_host,server_port))      # send req to server

    data,addr = sock.recvfrom(1024)     # rec from server
    logger.info('Get client from server {} {}'.format(addr,data))
    addr = MsgToAddr(data) # peer info
    logger.info('[ * ] Get Client '+str(addr))

    send_th   = threading.Thread(target=Send,args=(sock,addr,window,mode))
    listen_th = threading.Thread(target=Listen,args=(sock,))
    send_th.start()
    listen_th.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('STOP Service')
        RUN_EVENT.set()


def start():
    if len(sys.argv) < 3:
        print('Usage python peer.py server_ip mode i-initiator\nr-reciever')
        return

    ip = sys.argv[1]
    mode = sys.argv[2]
    port = 9999
    # if len(sys.argv) == 3: port = int(sys.argv[2])

    print('Selected server {}:{}'.format(ip,port))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(mode)


if __name__ == '__main__':
    start()
