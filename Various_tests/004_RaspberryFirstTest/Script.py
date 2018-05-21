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
        ips.append(line[:-1])

while(True):
	for color in colors:
		for ip in range(0,len(ips)-1):
			print(ips[ip])
			requests.get('http://'+ips[ip]+'?'+color, verify=False, stream=True)
			time.sleep(0.5)
			requests.get('http://'+ips[ip]+'?ledoff')
		for ip in range(len(ips)-1,0,-1):
			print(ips[ip])
			requests.get('http://'+ips[ip]+'?'+color, verify=False, stream=True)
			time.sleep(0.5)
			requests.get('http://'+ips[ip]+'?ledoff')

#for ip in ips:
#	print("Fade to "+ip)
#	requests.get('http://'+ip+'?smooth')
#	time.sleep(1)

#while(True):
#	for color in colors:
#		for ip in ips:
#			print("Sending "+color+" to "+ip)
#			try:
#				requests.get('http://'+ip+'?'+color)
#			except:
#				print("Error at "+ip)
#			time.sleep(0.5)
