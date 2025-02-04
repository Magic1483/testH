# client.py
import py3stun
import socket
import argparse
import time
import random

STUN_SERVER = "stun.l.google.com"
STUN_PORT = 19302

stun_list = [
    "stun.l.google.com:19302",
    "stun1.l.google.com:19302",
    "stun2.l.google.com:19302",
    "stun3.l.google.com:19302",
    "stun4.l.google.com:19302"
]

def get_external_ip_port(host,port):
    """Query STUN server to get external IP and port."""
    nat_type, external_ip, external_port = py3stun.get_ip_info(
        stun_host=host, stun_port=port
        )
    return nat_type, external_ip, external_port



# parser = argparse.ArgumentParser()
# parser.add_argument('-t','--timeout')
# args = parser.parse_args()

# print(f'Timeout {args.timeout}s')
for i,val in enumerate(stun_list):
    stun_host,stun_port = val.split(':')
    nat_type,ip,port = get_external_ip_port(stun_host,int(stun_port))
    print(f'[{stun_host}]',ip,port,nat_type)
    time.sleep(0.1)


    