#!/bin/bash

sudo ifconfig eth0 192.168.1.1 netmask 255.255.255.0 broadcast 192.168.1.255
sudo service isc-dhcp-server start
sudo iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth1 -j MASQUERADE

exit 0
