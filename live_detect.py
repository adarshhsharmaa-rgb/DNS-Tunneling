import sys, time, joblib, pandas as pd
from scapy.all import sniff, DNS, DNSQR, IP
from features import extract, ClientWindow, FEATURE_NAMES

model = joblib.load("models/rf_model.joblib")
win = ClientWindow()
THRESH = 0.7
stats = {"seen": 0, "alerts": 0, "first_alert": None}
start = time.time()

def handle(p):
    if not (p.haslayer(DNS) and p.haslayer(DNSQR) and p[DNS].qr == 0):
        return
    t0 = time.time()
    q = p[DNSQR]
    client = p[IP].src if p.haslayer(IP) else "x"
    f = extract(q.qname.decode(errors="ignore"), q.qtype, float(p.time), client, win)
    prob = model.predict_proba(pd.DataFrame([f])[FEATURE_NAMES])[0][1]
    stats["seen"] += 1
    if prob >= THRESH:
        stats["alerts"] += 1
        if stats["first_alert"] is None:
            stats["first_alert"] = time.time()
        lat_ms = (time.time() - t0) * 1000
        print(f"[ALERT] {time.strftime('%H:%M:%S')} {client} p={prob:.2f} "
              f"proc={lat_ms:.1f}ms {q.qname.decode()[:60]}")

iface = sys.argv[1] if len(sys.argv) > 1 else "lo"
try:
    sniff(iface=iface, filter="udp port 53 or udp port 5353", prn=handle, store=False)
except KeyboardInterrupt:
    print(stats)
