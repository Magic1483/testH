import logging
from os import stat
import socket
import sys
import time
import threading
import argparse

logger = logging.getLogger()
peers = []
RUN_EVENT = threading.Event()

def GroupData(arr):
    groups = {}
    for i in arr:
        gr = str(i)[:2]
        if gr not in groups: groups[gr] = []
        groups[gr].append(i)

    return groups

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


def main(server_host = '83.147.245.51', server_port = 9999):
    global RUN_EVENT
    ports = []
    window = 100 # offset for port of peer

    try:
        while True:
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.sendto(b'',(server_host,server_port))      # send req to server
            data,addr = sock.recvfrom(1024)     # rec from server
            logger.info('P: {}'.format(data))
            ports.append(int(data.decode('utf8').split(':')[-1]))
            sock.close()
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info('STOP Service\nShow port scatter')
        print(ports)
        res = GroupData(ports)
        for i in res.keys():
            print('GROUP',i+'***',f'{min(res[i])}-{max(res[i])}')



        # plot(ports)
        RUN_EVENT.set()


def start():
    if len(sys.argv) < 2:
        print('Usage python peer.py server_ip port:optional\ndefault port 9999')
        return

    ip = sys.argv[1]
    port = 9999
    if len(sys.argv) == 3: port = int(sys.argv[2])

    print('Selected server {}:{}'.format(ip,port))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()


if __name__ == '__main__':
    start()
