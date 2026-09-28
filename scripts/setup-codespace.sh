#!/bin/bash
echo "Configuring Docker container forwarding..."
sudo iptables-legacy -P FORWARD ACCEPT
echo "Docker forwarding configured."