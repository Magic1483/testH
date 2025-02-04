# client.py
import py3stun
import socket
import argparse
import time
import random

STUN_SERVER = "stun.l.google.com"
STUN_PORT = 19302

def get_external_ip_port():
    """Query STUN server to get external IP and port."""
    nat_type, external_ip, external_port = py3stun.get_ip_info(
        stun_host=STUN_SERVER, stun_port=STUN_PORT
        )
    return nat_type, external_ip, external_port



parser = argparse.ArgumentParser()
parser.add_argument('-t','--timeout')
args = parser.parse_args()

print(f'Timeout {args.timeout}s')
for i in range(25):
    _,ip,port = get_external_ip_port()
    print(f'[{i+1}]',ip,port)
    time.sleep(int(args.timeout))


    