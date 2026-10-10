# DNS Tunneling Detector

## Quick Start (70% Completion)

This repository contains the code to achieve the 70% requirement for the DNS Tunneling Detector project.

**Note:** For best results with `scapy` packet sniffing, it is recommended to run this on a Linux VM, WSL2, or a native Linux environment.

### 1. Setup Environment
```bash
sudo apt update
sudo apt install -y python3-pip tcpdump wireshark dnsutils iodine
pip3 install scapy scikit-learn pandas numpy matplotlib joblib dnslib
```

### 2. Generate and Capture Normal Traffic
Capture normal DNS requests in the background, whilst randomly simulating visits to a domain list.
```bash
# Terminal 1: Capture traffic
sudo tcpdump -i any -w data/normal.pcap udp port 53

# Terminal 2: Generate normal queries (need a domains.txt list first, e.g. top 4000 domains)
# Example domains file (you can download one or just make a small one)
python3 gen_normal.py domains.txt
```
*(Stop tcpdump with Ctrl+C when you have around 3000 queries)*

### 3. Generate and Capture Tunnel Traffic
Start the local DNS server and generate anomalous subdomains.
```bash
# Terminal 1: Start DNS Server
python3 dns_server.py

# Terminal 2: Capture tunnel traffic & run generator
sudo tcpdump -i lo -w data/tunnel_b32_txt.pcap udp port 5353 &
python3 gen_tunnel.py b32 30 TXT 3000
sudo pkill tcpdump

sudo tcpdump -i lo -w data/tunnel_hex_a.pcap udp port 5353 &
python3 gen_tunnel.py hex 20 A 3000
sudo pkill tcpdump

sudo tcpdump -i lo -w data/tunnel_b32_slow.pcap udp port 5353 &
python3 gen_tunnel.py b32 15 TXT 1500
sudo pkill tcpdump
```

### 4. Build Dataset
Extract features from your captured pcaps into a CSV dataset.
```bash
python3 build_dataset.py
```

### 5. Train Model
Train the Random Forest model and print performance metrics.
```bash
python3 train.py
```

### 6. Run Live Detector
Start sniffing for tunnel patterns in real-time. (Make sure you pass your active interface name e.g., `eth0` or `wlan0` or `lo`)
```bash
sudo python3 live_detect.py lo > results/live_alerts.txt
```

### 7. Run Streamlit Dashboard (The Final 30%)
In a new terminal window, install Streamlit and start the UI dashboard:
```bash
pip3 install streamlit
python3 -m streamlit run app.py
```
*(The dashboard will auto-refresh and display the live alerts and your generated ML plots!)*
