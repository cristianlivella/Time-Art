import socket
import fcntl
import struct
from json import load
from urllib2 import urlopen

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

try:
        print "Local IP (eth0): " + get_ip_address('eth0')
except:
        print "Local IP (eth0): 0.0.0.0"
try:
        print "Local IP (eth1): " + get_ip_address('eth1')
except:
        print "Local IP (eth1): 0.0.0.0"
try:
        print "Public IP: " + load(urlopen('https://api.ipify.org/?format=json'))['ip']
except:
        print "Public IP: 0.0.0.0"
