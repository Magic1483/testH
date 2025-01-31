import logging
import socket
import sys
import json
import time
import py3stun


logger = logging.getLogger()
CLIENT_LIST = []
PING_BUFFER = 8

"""
MSG TYPE
0 PING
1 PONG
"""
import enum
class MSG_TYPE(enum.Enum):
    Ping = 0
    Pong = 1


def format_addr(addr):
    return '{}:{}'.format(addr[0], str(addr[1]))

def get_addr_from_str(addr_str):
    addr,port = addr_str.split(':')
    return (addr,int(port))

def ImportClients(client_list:list):
    global CLIENT_LIST
    for c in client_list:
        if c not in CLIENT_LIST:
            CLIENT_LIST.append(c)

    print('clients',CLIENT_LIST)


def ConnectToClients(sock:socket.socket):
    global CLIENT_LIST
    for c in CLIENT_LIST:
        sock.sendto(b'',get_addr_from_str(c))

def HandleEntryPoint(sock:socket.socket,addr_to):
    counter = 1
    while True:
        sock.sendto(bytes(MSG_TYPE.Ping.value), addr_to)
        try:
            data,addr = sock.recvfrom(PING_BUFFER)
            # assert data == bytes(MSG_TYPE.Pong.value)

        except socket.timeout:
            print('SERVER NOT RESPONSE!!')
            return

        print('server answer: {} Pong'.format(addr, data),counter)
        counter+=1
        time.sleep(5)




def main(host='83.147.245.51', port=9999):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    # sock.settimeout(15) #timeout 15s

    # send data to server (Entry Point)
    # _,ip,port = py3stun.get_ip_info()
    sock.sendto(b'0', (host, port))


    data, addr = sock.recvfrom(1024)
    print('server answer: {} {}'.format(addr, data.decode('utf-8')))
    ImportClients(json.loads(data.decode('utf-8')))

    print('SEND TO CLIENT ',CLIENT_LIST[0])
    HandleEntryPoint(sock,get_addr_from_str(CLIENT_LIST[0]))

    # sock.sendto(b'0', get_addr_from_str(CLIENT_LIST[0]))
    # data, addr = sock.recvfrom(1024)
    # print('client received: {} {}'.format(addr, data))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
