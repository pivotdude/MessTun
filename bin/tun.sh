#!/bin/bash
# Remove interface if exists
sudo ip link del teletun 2>/dev/null

# Create new TUN interface
sudo ip tuntap add teletun mode tun

# Configure point-to-point addresses
sudo ip addr add 10.8.0.1 peer 10.8.0.2 dev teletun

# Bring interface up
sudo ip link set teletun up

# Set device permissions
sudo chmod 666 /dev/net/tun

echo "TUN interface teletun created successfully"
ip addr show teletun
