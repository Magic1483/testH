import py3stun


stun_servers = [
     "stun.l.google.com:19302" ,
     "stun.l.google.com:5349" ,
     "stun1.l.google.com:3478" ,
     "stun1.l.google.com:5349" ,
     "stun2.l.google.com:19302" ,
     "stun2.l.google.com:5349" ,
     "stun3.l.google.com:3478" ,
     "stun3.l.google.com:5349" ,
     "stun4.l.google.com:19302" ,
     "stun4.l.google.com:5349"
]

def analyze_nat_behavior(stun_host,stun_port):
    print(f"[*] Detecting NAT Type from {stun_host}")
    stun_port = int(stun_port)
    # Use a public STUN server (Google STUN servers are commonly used)

    # Get NAT type and external IP/port
    nat_type, external_ip, external_port = py3stun.get_ip_info(
        stun_host=stun_host,
        stun_port=stun_port
    )

    print("\n[+] NAT Analysis Complete:")
    print(f"    NAT Type       : {nat_type}")
    print(f"    Public IP      : {external_ip}")
    print(f"    Public Port    : {external_port}")

    if nat_type == "Blocked":
        print("[!] No UDP traffic allowed. Check firewall settings.")
    elif nat_type == "Open Internet":
        print("[*] No NAT detected. You have a public IP address.")
    elif nat_type in ["Full Cone", "Restricted NAT", "Port Restricted NAT"]:
        print("[*] NAT is manageable for P2P connections.")
    elif nat_type == "Symmetric NAT":
        print("[!] Symmetric NAT detected. P2P is difficult without a relay (TURN server).")

    return nat_type, external_ip, external_port

if __name__ == "__main__":
    for i in stun_servers:
        host,port = i.split(':')
        analyze_nat_behavior(host,port)
