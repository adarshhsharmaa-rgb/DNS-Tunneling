#!/bin/bash

# Convert to Linux paths just in case
cd /mnt/c/Users/Acer/OneDrive/Desktop/DNS_Tunelling/dns-detector

echo "Capturing normal traffic..."
tcpdump -i any -w data/normal.pcap udp port 53 > /dev/null 2>&1 &
TCPDUMP_PID=$!
sleep 2
python3 gen_normal.py domains.txt
sleep 2
kill $TCPDUMP_PID

echo "Starting DNS server..."
python3 dns_server.py > /dev/null 2>&1 &
DNS_PID=$!
sleep 2

echo "Capturing tunnel_b32_txt..."
tcpdump -i lo -w data/tunnel_b32_txt.pcap udp port 5353 > /dev/null 2>&1 &
TPID=$!
sleep 1
python3 gen_tunnel.py b32 30 TXT 3000
sleep 1
kill $TPID

echo "Capturing tunnel_hex_a..."
tcpdump -i lo -w data/tunnel_hex_a.pcap udp port 5353 > /dev/null 2>&1 &
TPID=$!
sleep 1
python3 gen_tunnel.py hex 20 A 3000
sleep 1
kill $TPID

echo "Capturing tunnel_b32_slow..."
tcpdump -i lo -w data/tunnel_b32_slow.pcap udp port 5353 > /dev/null 2>&1 &
TPID=$!
sleep 1
python3 gen_tunnel.py b32 15 TXT 1500
sleep 1
kill $TPID

echo "Stopping DNS server..."
kill $DNS_PID

echo "Building dataset..."
python3 build_dataset.py

echo "Training model..."
python3 train.py
