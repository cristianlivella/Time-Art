# Ethernet blink

## Introduction
We used this test to try the communication with Arduino Ethernet Shield 2, controlling a LED on the pin 5 of two Arduino from a Raspberry PI via Ethernet, configured like explained here:  
[***Raspberry PI as router and server***](../001_Raspberry_PI_as_router_and_server/README.md).

## Circuit
![Circuit](https://i.imgur.com/GFU5OVK.png)

## Arduino sketch
[ethernetBlink.ino](ethernetBlink.ino)

## PHP script
[ethernetBlink.php](ethernetBlink.php)

## How to use
* put the Ethernet Shield 2 on the two Arduino
* upload the sketch `ethernetBlink.ino` on each Arduino; **remember to edit** the MAC address (it is printed on a label on the shield) and the IP address (must be different for each device)
* put the script `ethernetBlink.php` on the Raspberry and run it:  
`php ethernetBlink.php`

***nb***: *we used the IPs `192.168.1.11` and `192.168.1.12` for the Arduino; if you want to use other IP addresses you should edit `ethernetBlink.php`.*

## Video
[![Youtube video](https://img.youtube.com/vi/PaozKFauqRA/0.jpg)](https://youtu.be/PaozKFauqRA)
