import sys, pandas as pd
from scapy.all import rdpcap, DNSQR, DNS, IP
from features import extract, ClientWindow

def pcap_to_rows(path, label, source):
    rows, win = [], ClientWindow()
    for p in rdpcap(path):
        if p.haslayer(DNS) and p.haslayer(DNSQR) and p[DNS].qr == 0:
            q = p[DNSQR]
            client = p[IP].src if p.haslayer(IP) else "x"
            f = extract(q.qname.decode(errors="ignore"), q.qtype, float(p.time), client, win)
            f["label"], f["source"] = label, source
            rows.append(f)
    return rows

rows = []
rows += pcap_to_rows("data/normal.pcap", 0, "normal")
for name in ["tunnel_b32_txt", "tunnel_hex_a", "tunnel_b32_slow"]:
    rows += pcap_to_rows(f"data/{name}.pcap", 1, name)
pd.DataFrame(rows).to_csv("data/dataset.csv", index=False)
print("rows:", len(rows))
