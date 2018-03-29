# Time Art
![Fondi Strutturali Europei](https://i.imgur.com/O4acpw3.png)
This project is a module of [LIVE YOUR TIME](http://poninchiaro.istruzione.it/poninchiaro/progetti/fse/19055/bgtf010003/), a group of 8 workshops organized at [ITIS Pietro Paleocapa](http://www.itispaleocapa.it/) (Bergamo, Italy) in the school year 2017/2018.  
The purpose of the project is to control 8 RGB lights to light up some classroom on the main façade of the school using some Arduino in LAN, creating color effects visible from the street and maybe also from Città Alta.  
In the future the lights might be used in any other situation and controlled also remotely, for example with an Android app or with Telegram.

## Arduino Uno (Rev. 3)
<img align="left" height="200" alt="Arduino Uno" src="https://i.imgur.com/sikbKH4.png">
For this project we'll use 8 Arduino Uno, one for each classroom.  
To every Arduino will be connected an infrared LED, to control the RGB light, and maybe in future also some sensors, for example a PIR sensor to change the color of the light when a movement is detected.

## Ethernet Shield 2
<img align="left" height="200" alt="Ethernet Shield 2" src="https://i.imgur.com/sikbKH4.png">
In each Arduino will be plugged an Ethernet Shield 2 to connect it at the LAN.  
This Ethernet Shield is made by arduino.org, so the library to use in the sketches is not included in the Arduino IDE, if you have downloaded it from arduino.cc.  
In this case you must download the library [Ethernet2](https://github.com/cristianlivella/Time-Art/blob/master/Ethernet2.zip) from [here](https://github.com/cristianlivella/Time-Art/blob/master/Ethernet2.zip) and [install it](https://www.arduino.cc/en/Guide/Libraries#toc2) into your Arduino IDE.

## RGB lights
The RGB lights we will use are natively controlled by an infrared remote control, so to control them from Arduino we will use an infrared LED for every light.
