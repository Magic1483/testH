import socket
import argparse
import random
import os

BUFFER = 1024

    
def RecieveFile(sock: socket.socket):
    expected_seq = 0

    packet,addr = sock.recvfrom(BUFFER+4)
    data = packet[4:]
    filename = data.decode('utf-8')
    print('filename is ',filename)
    file = open(filename,'wb')

    while True:
        packet,addr = sock.recvfrom(BUFFER+4)
        seq_num = int.from_bytes(packet[:4],byteorder='big')
        data = packet[4:]

        if data == b'END':
            print('End of stream')
            break

        if seq_num == expected_seq:
            file.write(data)
            expected_seq += 1
            sock.sendto(seq_num.to_bytes(4,byteorder='big'),addr)
            print(f"Received and wrote packet {seq_num}")
        else:
            sock.sendto((expected_seq - 1).to_bytes(4,byteorder='big'),addr)

    print("File received successfully.")

def SendFile(filename,sock: socket.socket,addr:str):
    seq_num = 0
    file = open(filename,'rb')
    addr = (addr.split(':')[0],int(addr.split(':')[-1]))

    # send filename
    packet = seq_num.to_bytes(4,byteorder='big') + os.path.basename(filename).encode('utf-8')
    sock.sendto(packet,addr)

    while True:
        data = file.read(BUFFER)
        if not data:
            print('End of stream')
            break
        
        # 1st 4 bytes is sequense number
        packet = seq_num.to_bytes(4,byteorder='big') + data
        while True:
            sock.sendto(packet,addr)
            try:
                ack, _ = sock.recvfrom(4)
                ack_num = int.from_bytes(ack, byteorder="big")
                if ack_num == seq_num:
                    print(f"Received ACK for packet {seq_num}")
                    seq_num += 1
                    break  # Move to the next packet
            except socket.timeout:
                print(f"Timeout, resending packet {seq_num}")

    end_packet = seq_num.to_bytes(4,byteorder='big') + b'END'
    sock.sendto(end_packet,addr)
    print('File transfered')


def Peer(mode,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(("",int(port)))

    match mode:
        case 'sender':
            filename = input('filename: ')
            peer_addr = input('peer address: ')
            SendFile(filename,sock,peer_addr)
        case 'reciever':
            RecieveFile(sock)
    
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode')
    parser.add_argument('-p','--port')


    args = parser.parse_args()

    Peer(args.mode)