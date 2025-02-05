import logging
import socket
import sys


logger = logging.getLogger()
peers = []

def AddrToMsg(addr):
    """
    """
    s = addr[0]+':'+str(addr[1])
    return str(s).encode('utf8')

def MsgToAddr(addr):
    """
    """
    ip,port = addr.decode('utf8').split(':')
    return ip,int(port)


def main(port = 9999):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.bind(('0.0.0.0',port))
    while True:
        data,addr = sock.recvfrom(1024)
        logger.info(f'connection from {addr}')
        peers.append(addr)
        if len(peers) >= 2:
            logger.info(f'send info to client {peers[0]}')
            sock.sendto(AddrToMsg(peers[1]),peers[0])
            logger.info(f'send info to client {peers[0]}')
            sock.sendto(AddrToMsg(peers[0]),peers[1])
            peers.clear()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
