import requests
import time

commands = [
    "on",
    "off",
    "su",
    "giu",
    "flash",
    "fade",
    "smooth"
]

colors = [
    "white",
    "red",
    "red2",
    "green",
    "green2",
    "blue",
    "blue2",
    "blue3",
    "orange",
    "orange2",
    "purple",
    "purple2",
    "ciano",
    "ciano2",
    "yellow",
    "fuchsia"
]

ips = []

with open('ip.txt') as ipFile:
    for line in ipFile:
        ips.append(line.replace('\n', ''))

while(True):
    for x in range(0,7):
        print('LIGHT GAME 1')
        for color in colors:
            for ip in range(0,len(ips)-1):
                try:
                    print('Sending '+color+' at '+ips[ip])
                    requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    print('Delay '+str(1.2-(x*0.1)))
                    time.sleep(1.2-(x*0.1))
                    print('Sending ledoff at '+ips[ip])
                    requests.get('http://'+ips[ip]+'?ledoff')
                except requests.exceptions.RequestException:
                    print('Error at '+ips[ip])
            for ip in range(len(ips)-1,0,-1):
                try:
                    print('Sending '+color+' at '+ips[ip])
                    requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    print('Delay '+str(1.2-(x*0.1)))
                    time.sleep(1.2-(x*0.1))
                    print('Sending ledoff at '+ips[ip])
                    requests.get('http://'+ips[ip]+'?ledoff')
                except requests.exceptions.RequestException:
                    print('Error at '+ips[ip])
        print('LIGHT GAME 2')
        for color in colors:
            for ip in ips:
                try:
                    print('Sending '+color+' at '+ip)
                    requests.get('http://'+ip+'?'+color, timeout=0.1)
                except requests.exceptions.RequestException:
                    print('Error at '+ip)
                time.sleep(1.2-(x*0.1))
