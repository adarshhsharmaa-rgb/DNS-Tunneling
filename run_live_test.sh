#!/bin/bash
cd /mnt/c/Users/Acer/OneDrive/Desktop/DNS_Tunelling/dns-detector

# Start live detector in background and log output
python3 -u live_detect.py lo > results/live_alerts.txt 2>&1 &
LIVE_PID=$!

sleep 3

# Start dns server in background
python3 -u dns_server.py > /dev/null 2>&1 &
DNS_PID=$!

sleep 3

# Send exactly 10 tunnel packets
python3 gen_tunnel.py b32 30 TXT 10

sleep 5

# Kill them
kill $LIVE_PID
kill $DNS_PID

echo "Live test finished, output saved to results/live_alerts.txt"
