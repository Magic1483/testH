import socket
import struct

# get ip from announce

server_list = [
    ["retracker.lanta.me",2710],
    ["bandito.byterunner.io",6969],
]




def GetIP(tracker_host,tracker_port,local_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set a timeout for the socket

    protocol_id = 0x41727101980
    action = 0  # Connect action
    transaction_id = 123456

    connect_request = struct.pack(">QII", protocol_id, action, transaction_id)
    sock.sendto(connect_request, (tracker_host, tracker_port))

    connect_response, _ = sock.recvfrom(16)  # Response is 16 bytes
    action_resp, transaction_id_resp, connection_id = struct.unpack(">IIQ", connect_response)
    # Pack the announce request into binary format
    announce_request = struct.pack(
        ">QII20s20sQQQIIIiH",
        connection_id,  # Connection ID from connect response
        1,  # Action (1 for announce)
        transaction_id,  # Transaction ID
        b"03bb57ea1f7e8dc9cc7da349a7c5bc3359",  # Info hash
        b"grt",  # Peer ID
        0,  # Downloaded
        0,  # Left
        0,  # Uploaded
        0,  # Event
        0,  # IP address (0 for default)
        12,  # Key
        1,  # Number of peers wanted
        6070,  # Port
    )


    sock.sendto(announce_request, (tracker_host, tracker_port))
    announce_response, _ = sock.recvfrom(1024)  # Response can be up to 1024 bytes
    # Parse the announce response
    action_resp, transaction_id_resp, interval, leechers, seeders = struct.unpack(
        ">IIIII", announce_response[:20]
    )


    # Extract the list of peers (each peer is 6 bytes: 4 for IP, 2 for port)
    # print(len(announce_response))
    peers = announce_response[20:]
    for i in range(0, len(peers), 6):
        ip = ".".join(str(b) for b in peers[i : i + 4])
        port = struct.unpack(">H", peers[i + 4 : i + 6])[0]
        print(f"{tracker_host} Peer IP: {ip}, Port: {port}")

    # Close the socket
    sock.close()
    return ip,port


if __name__ == '__main__':
    ip,port = GetIP("retracker.lanta.me",2710,5000)
    print(ip,port)
