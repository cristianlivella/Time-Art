# Raspberry PI as router and server
![Raspberry PI](https://i.imgur.com/Ck4fJuX.jpg)
By following these steps you will have a Raspberry PI with 2 Ethernet ports:
* **eth0**, the Ethernet port on the Raspberry, it must be connected to an Ethernet hub/switch where will also be connected the Arduino
* **eth1**, the Ethernet port on the external adapter, it must be connected to our existing home/company network.

![Image](https://i.imgur.com/KRMzjIq.png)
The Raspberry PI will create a 192.168.1.x network on the **eth0**, and it will receive a IP from the DHCP of the home/company network on **eth1**.  
The advantages of this setup is that we can be independent, because we can use the Raspberry without connect its **eth1** to a network, and control the Arduino using a PC connected at the same switch, but when we want we can do it, to be able to control our group of Arduino and RGB lights even remotely.

## What you will need
* a Raspberry PI (we use the first generation of model B, but you can use any model)
* an SD/microSD card of at least 4 GB
* an Ethernet - USB adapter
* an Ethernet hub/switch
* some Ethernet cables

## Install Raspbian
* download the image from [here](https://downloads.raspberrypi.org/raspbian_lite_latest)
* write the image to the SD using [Etcher](https://etcher.io/) or your favorite software
* make a text file with name *ssh*, and put in the boot partition of the SD card
* using an Ethernet cable, connect the port **eth1** on the Ethernet adapter to a port on your home/company network
* find the IP of the Raspberry using an [IP scanner](https://www.advanced-ip-scanner.com/), and connect to it with [Putty](https://www.putty.org/), [MobaXterm](https://mobaxterm.mobatek.net/) or any other SSH software
* **CHANGE THE PASSWORD** of the pi account with the command `passwd`

## Configure the Raspberry as router
* `sudo nano /etc/sysctl.conf`  
and uncomment the following line in this file  
`net.ipv4.ip_forward = 1`
* reload sysctl with  
`sudo sysctl -p`
* install a DHCP server  
`sudo apt-get install isc-dhcp-server`  
`sudo service isc-dhcp-server stop`
* replace this file (`/etc/default/isc-dhcp-server`) with [this](isc-dhcp-server)
* replace the DHCP configuration file (`/etc/dhcp/dhcpd.conf`) with [this](dhcpd.conf)
* create in `/home/pi` a file `startnetwork.sh` like [this](startnetwork.sh)
* make the script executable  
`sudo chmod +x /home/pi/startnetwork.sh`
* `sudo nano /etc/rc.local`
and add the following line in the file, above the line `exit 0`:  
`/home/pi/startnetwork.sh`
* connect the port **eth0** to the Ethernet switch, and reboot the Raspberry
`sudo reboot`

## Install and configure the web server
Follow these instructions:  
https://www.raspberrypi.org/documentation/remote-access/web-server/nginx.md
Finally install cURL:  
`sudo apt-get install php-curl`

## Conclusions
If you did everything correctly, now you could connect your computer to the same switch where is connected the port **eth0** of the Raspberry, start an SSH session to the Raspberry with the IP 192.168.1.1 and also surf the Internet.

## Useful links
https://www.raspberrypi.org/documentation/installation/installing-images/  
https://www.raspberrypi.org/forums/viewtopic.php?t=129727  
https://medium.com/linagora-engineering/using-a-pi-3-as-a-ethernet-to-wifi-router-2418f0044819  
https://www.raspberrypi.org/documentation/remote-access/web-server/nginx.md
