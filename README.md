# Time Art
![Fondi Strutturali Europei](https://i.imgur.com/O4acpw3.png)
This project is a module of [LIVE YOUR TIME](http://poninchiaro.istruzione.it/poninchiaro/progetti/fse/19055/bgtf010003/), a group of 8 workshops organized at [ITIS Pietro Paleocapa](http://www.itispaleocapa.it/) (Bergamo, Italy) in the school year 2017/2018.  
The purpose of the project is to control 8 RGB lights to light up some classroom on the main façade of the school using some Arduino in LAN, creating color effects visible from the street and maybe also from Città Alta.  
In the future the lights might be used in any other situation and controlled also remotely, for example with an Android app or with Telegram.

## Arduino Uno (Rev. 3)
For this project we'll use 8 Arduino Uno, one for each classroom.  
To every Arduino will be connected an infrared LED, to control the RGB light, and maybe in future also some sensors, for example a PIR sensor to change the color of the light when a movement is detected.

## Ethernet Shield 2
In each Arduino will be plugged an Ethernet Shield 2 to connect it at the LAN.  
This Ethernet Shield is made by arduino.org, so the library to use in the sketches is not included in the Arduino IDE, if you have downloaded it from arduino.cc.  
In this case you must download the library [Ethernet2](Ethernet2.zip) from [here](Ethernet2.zip) and [install it](https://www.arduino.cc/en/Guide/Libraries#toc2) into your Arduino IDE.

## RGB lights
The RGB lights we will use are natively controlled by an infrared remote control, so to control them from Arduino we will use an infrared LED for every light.

## Final result during "Notte al Museo 2018"
[![Youtube video](https://i.imgur.com/vUrBrXx.jpg)](https://youtu.be/6DH9gzSgO6w)  
[Youtube video](https://youtu.be/6DH9gzSgO6w).

## Elettricittà fair 2019
![Raul and Cristian at the project fair booth](https://i.imgur.com/6QTJpVN.jpg)  
_[Raul](https://github.com/Raul178) and [Cristian](https://github.com/cristianlivella) at the project fair booth._

In May 2019 we presented the project at Elettricittà fair, organised by [Barcella Elettroforniture](https://www.barcella.it/).  
[Here](./2019.05%20-%20Project%20Lamp%20Barcella) you can find the software we used in that occasion, and [here](https://youtu.be/QmKffknVNF8) you can watch a short video showing our booth and the dismantling of it at the end of the fair.
