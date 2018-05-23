# Test Raspberry with 8 lights
## Introduction
We used this test to try the Raspberry with all the Arduino and all the lights.

## What you will need
* a Raspberry PI (configured like explained here: [***Raspberry PI as router and server***](../001_Raspberry_PI_as_router_and_server/README.md)
* 8 Arduino
* 8 Arduino Ethernet Shield
* 8 IR LEDs
* 8 RGB lights
* an Ethernet hub/switch
* some Ethernet cables
* various power supplies

## Circuit and connections
* connect the Raspberry port **eth0** to the Ethernet switch
* connect the Raspberry port **eth1** to your LAN
* put the Ethernet Shields on each Arduino, and connect them to the Ethernet switch
* connect the IR LED to the PIN 3 of each Arduino

## Arduino sketch
Upload the sketch [sketch.ino](sketch.ino) on each Arduino; **remember to edit** the MAC address at the lines 48-49 (it is printed on a label on the shield) and the IP address (must be different for each device).

## Configuration file
Insert in the file `ip.txt` all the Arduino IPs, one for each line.

## Python script
Run this script: [script.py](script.py).

## Video
[![Youtube video](https://img.youtube.com/vi/uyHihy34Fgs/0.jpg)](https://youtu.be/uyHihy34Fgs)
