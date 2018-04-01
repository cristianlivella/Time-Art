# Control Arduino LEDs from Raspberry PI with webserver and Telegram

## Introduction
We used this test to try the communication with Arduino Ethernet Shield 2, controlling an RGB LED, a green LED and a red LED of two Arduino from a Raspberry PI via Ethernet, configured like explained here:  
***[Raspberry PI as router and server](https://github.com/EsperiaPON/Time-Art/blob/master/Various_tests/001_Raspberry_PI_as_router_and_server/README.md)***.  
The LEDs can be controlled with a web page on the Raspberry and with a Telegram bot.  
You can also use more then two Arduino, just insert all the IPs in the array `$IPs` in `config.php` on Raspberry.

## Circuit
![Circuit](https://i.imgur.com/eXkAa2X.png)

## Arduino sketch
Upload the sketch [controlLedEthernet.ino](https://github.com/EsperiaPON/Time-Art/blob/master/Various_tests/003_Control_Arduino_LEDs_from_Raspberry_webserver_and_Telegram/controlLedEthernet.ino) on each Arduino; **remember to edit** the MAC address (it is printed on a label on the shield) and the IP address (must be different for each device).

## Webserver
Download the folder [html](https://github.com/EsperiaPON/Time-Art/blob/master/Various_tests/003_Control_Arduino_LEDs_from_Raspberry_webserver_and_Telegram/html), put all the files in `/var/www/html/` on your Raspberry PI and edit `config.php` with the IPs of your Arduino.  
You can now open a web browser and insert the IP of your Raspberry in the address bar to access to the dashboard.
![Screenshot](https://i.imgur.com/ottQKz0.png)

## Telegram bot configuration
If you want to control the LEDs also with a Telegram bot, you have to:
* edit `/var/www/html/config.php` with your Telegram bot token (if you haven't got one, you can create it by contacting [@BotFather](http://t.me/BotFather)).
* `crontab -e`, and insert this line at the end of the file:  
`*/1 * * * * /var/www/html/loadtelegrambot.sh >/dev/null 2>&1`
* send a message to your bot with Telegram, you will receive your chatid from it
* insert your chatid in the array `$allowedTelegramChatIds` in `/var/www/html/config.php`, and restart the bot.

## Telegram bot command
```
{ARDUINO_IP}:{LED}:{VALUE}
```
* You can write `all` or `a` instead the Arduino IP to execute the command on all the Arduino set in `config.php`
* `{LED}` could be `rgb`, `led1` or `led2`
* for the RGB LED, `{VALUE}` it must look like this: `R-G-B`
* for the other LEDs it can be only `0`/`off` or `1`/`on`.

Examples:
* `192.168.1.11:led1:1`  
turn on the green LED on the Arduino with the ip 192.168.1.11
* `192.168.1.11:led1:0`  
turn off the green LED on the Arduino with the IP 192.168.1.11
* `all:rgb:255-0-0`  
set red as color of the RGB LED on all the Arduino
* `a:rgb:0-0-0`  
turn off the RGB LED on all the Arduino.

## Video
[![Youtube video](https://img.youtube.com/vi/0QzwFcCa-NE/0.jpg)](https://youtu.be/0QzwFcCa-NE)
