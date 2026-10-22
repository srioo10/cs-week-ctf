# Replay - rebuild the telnet conversation from the pcap and print it like a terminal
from scapy.all import rdpcap, TCP, Raw

pkts = rdpcap("../files/replay.pcap")

# 1) The HTTP request on port 80 (a decoy lives in here)
print("=== HTTP (port 80) ===")
for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw) and 80 in (p[TCP].sport, p[TCP].dport):
        print(p[Raw].load.decode(errors="replace"))

# 2) The telnet session on port 23: glue the payloads together in order.
#    Telnet sends one keystroke per packet, so the 'client' bytes are what was typed
#    and the 'server' bytes are what came back.
print("=== TELNET (port 23), as a terminal would show it ===")
session = b"".join(bytes(p[Raw].load) for p in pkts
                   if p.haslayer(TCP) and p.haslayer(Raw) and 23 in (p[TCP].sport, p[TCP].dport))
print(session.decode(errors="replace"))

print("=== just what the user typed ===")
typed = b"".join(bytes(p[Raw].load) for p in pkts
                 if p.haslayer(TCP) and p.haslayer(Raw) and p[TCP].dport == 23)
print(repr(typed.decode()))
