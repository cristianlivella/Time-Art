# -*- coding: utf-8 -*-

################ ITIS Paleocapa 2018 ################
# Main developers: Cristian Livella, Matteo Soldini #
#             Project: Esperia Time Art             #
#####################################################

import threading, time, telepot, telepot.loop, sys, os, requests, random
from Tkinter import *

### CONFIGURAZIONE ###
# Token bot Telegram
botToken = "0123456789:BOT_TOKEN"

# Chat id consentiti
allowedChatId = []

# Colori
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

hex_colors = [
    "#eeeeff",
    "#d81f0d",
    "#bf3c82",
    "#11b12e",
    "#02811f",
    "#0426ff",
    "#003bff",
    "#0058eb",
    "#f577c8",
    "#c07c33",
    "#1a2fff",
    "#8229b8",
    "#009ad8",
    "#005deb",
    "#c6b16e",
    "#ad24dd"
    ]

# IP Arduino
ips = [
	"10.205.0.11",
	"10.205.0.12",
	"10.205.0.13",
	"10.205.0.14",
	"10.205.0.15",
	"10.205.0.16",
	"10.205.0.17",
	"10.205.0.18",
	]

# Numero di giochi disponibili
nGiochi = 4

verbose = 2

#########################################
### NON MODIFICARE SOTTO QUESTA LINEA ###
#########################################

arduinoOnline = [0] * len(ips)
timeDelay = 500
stato = 0

finestre_gui = list()
canvas_gui = 0
window_gui = 0

class ThreadManager(threading.Thread):
    def __init__(self, function):
        self.running = False
        self.function = function
        super(ThreadManager, self).__init__()
    def start(self):
        self.running = True
        super(ThreadManager, self).start()
    def run(self):
        while self.running:
            try:
                self.function()
            except:
                pass
    def stop(self):
        self.running = False

def checkArduinoOnline():
    global arduinoOnline
    if (verbose>=2):
        print('INIZIO CHECK ARDUINO ONLINE..')
    for x in range(len(ips)):
        try:
            requests.get('http://'+ips[x], timeout=0.5)
            arduinoOnline[x] = 1
            if (verbose>=2):
                print('Arduino a '+ips[x]+': ONLINE')
        except:
            arduinoOnline[x] = 0
            if (verbose>=2):
                print('Arduino a '+ips[x]+': OFFLINE')
    time.sleep(10)

def countArduinoOnline():
    count = 0
    for x in range(len(ips)):
        if (arduinoOnline[x]==1):
            count += 1
    return count

def getStato():
    if (stato==0):
        return 'off'
    else:
        return 'gioco '+str(stato)

def startGameThread():
    global gameThread
    if (verbose>=1):
        print('AVVIO GAME THREAD...')
    try:
        gameThread = ThreadManager(function = lightGame)
        gameThread.start()
        if (verbose>=2):
            print('Game thread avviato')
    except:
        if (verbose>=2):
            print('Impossibile avviare il game thread (potrebbe essere già attivo)')

def stopGameThread():
    global gameThread
    if (verbose>=1):
        print('STOP GAME THREAD...')
    try:
        gameThread.stop()
        if (verbose>=2):
            print('Game thread stoppato')
    except:
        if (verbose>=2):
            print('Impossibile stoppare il game thread (potrebbe essere già stoppato')

def lightsOff():
    errorCount = 0
    if (verbose>=1):
        print('INVIO COMANDO SPEGNIMENTO ALLE LAMPADE...')
    for ip in ips:
        try:
            requests.get('http://'+ip+'?ledoff', timeout=0.2)
            if (verbose>=2):
                print("Comando di spegnimento inviato correttamente a "+ip)
        except:
            if (verbose>=2):
                print("ERRORE nell\'invio del comando di spegnimento a "+ip)
            errorCount += 1
    return errorCount

def createWindow():
    global canvas_gui
    global window_gui
    global finestre_gui
    global hex_colors
    window_gui = Tk()
    window_gui.geometry(str(len(ips)*150) + 'x300')
    window_gui.title("Esperia Time Art")
    window_gui.update_idletasks()
    window_gui.update()
    canvas_1 = Canvas(window_gui, width=len(ips)*100, height=20)
    canvas_1.pack()
    text_1 = Label(window_gui, text="Esperia Time Art", font=("AldotheApache", 60))
    text_1.pack()
    canvas_gui = Canvas(window_gui, width=len(ips)*150, height=250)
    canvas_gui.pack()
    for x in range(len(ips)):
        obj = canvas_gui.create_rectangle((150*x)+10, 20, (150*(x+1))-10, 150, fill="#222222")
        finestre_gui.append(obj)
    window_gui.update_idletasks()
    window_gui.update()

def changeWindowColor(windowId, colorId):
    global canvas_gui
    global window_gui
    global finestre_gui
    global hex_colors
    canvas_gui.itemconfigure(finestre_gui[windowId], fill=hex_colors[colorId])
    window_gui.update_idletasks()
    window_gui.update()

def sendColorCommand(windowId, colorId):
    print 'ciao'
    if (colorId>=0):
        try:
            requests.get('http://'+ips[windowId]+'?'+colors[colorId], timeout=0.1)
            changeWindowColor(windowId, colorId)
        except requests.exceptions.RequestException:
            print('Errore a '+ips[windowId])
    else:
        requests.get('http://'+ips[windowId]+'?ledoff', timeout=0.2)
        changeWindowColor(windowId, "#222222")


def handle(msg):
    global stato
    global timeDelay
    global bot
    try:
        if (verbose>=2):
            print('Ricevuto messaggio Telegram da '+str(msg['from']['id'])+': '+msg['text'])
        chatId = msg['from']['id']
        message = msg['text'].lower()
        if (not chatId in allowedChatId):
            bot.sendMessage(chatId, '*Ciao!*\nNon sei autorizzato ad utilizzare questo bot.\n\nQuesto è il tuo *chatId*: '+str(chatId)+'.', parse_mode='markdown')
            return
        if (message=='/start' or message=='start' or message=='/info' or message=='info' or message=='/help' or message=='help'):
            text = '*- TIME ART BOT -*\n\nArduino list:\n'
            for x in range(len(ips)):
		text += ips[x]+': '
	    	if arduinoOnline[x]==1:
    		    text += 'online'
		else:
                    text += 'offline'
		text += '\n'
            text += '\nTime delay: '+str(timeDelay)+' ms\n\n*Comandi:*\n/off -> spegne tutte le lampade\n/game \[ID] -> avvia il gioco di luce [ID] da 1 a 4\n/setTime \[TEMPO] -> imposta il delay tra ogni azione del gioco (millisecondi)'
            bot.sendMessage(chatId, text, parse_mode='markdown')
	elif (message=='/off' or message=='off'):
	    stopGameThread()
            stato = 0
            errorCode = lightsOff()
            if (errorCode==0):
                bot.sendMessage(chatId, 'Comando di spegnimento inviato correttamente a tutte le lampade.')
            else:
                bot.sendMessage(chatId, 'Problema con l\'invio del comando di spegnimento a '+str(errorCode)+' lampade.')
        elif (message[0:5]=='/game' or message[0:4]=='game'):
            try:
                lightGame = int(message.replace('/', '').replace('game', ''))
            except:
                bot.sendMessage(chatId, 'Id gioco non valido.', parse_mode='markdown')
                return
            if (not lightGame in range(1, nGiochi+1)):
                bot.sendMessage(chatId, 'Id gioco non valido.', parse_mode='markdown')
                return
            try:
                gameThread.stop()
            except:
                pass
            for ip in range(len(ips)):
                try:
                    #requests.get('http://'+ip+'?ledoff', timeout=0.2)
                    sendColorCommand(ip, -1)
                except:
                    pass
            try:
                stato = lightGame
                startGameThread()
                bot.sendMessage(chatId, 'Gioco di luce '+str(lightGame)+' avviato!')
            except:
                bot.sendMessage(chatId, 'Errore con l\'avvio del thread.')
                stato = 0
        elif (message[0:8]=='/settime' or message[0:7]=="settime"):
            try:
                time = int(message.replace('/', '').replace('settime', ''))
            except:
                bot.sendMessage(chatId, 'Tempo non valido.', parse_mode='markdown')
                return
            if (not time in range (0, 100000)):
                bot.sendMessage(chatId, 'Tempo non valido.', parse_mode='markdown')
                return
            timeDelay = time
            bot.sendMessage(chatId, 'Delay impostato a '+str(timeDelay)+' ms.', parse_mode='markdown')
        else:
            bot.sendMessage(chatId, 'Comando non riconosciuto.\n\nScrivi /help per la lista dei comandi.', parse_mode='markdown')
    except:
        pass

def lightGame():
    thisStato = stato
    if (stato==0):
        stopGameThread()
        ligthsOff()
        return
    if (stato==1):
        if (verbose>=1):
            print('Partenza ciclo gioco 1')
        for color in range(0, len(colors)-1):
            for ip in range(0,len(ips)-1):
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+colors[color]+' a '+ips[ip])
                    #requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    sendColorCommand(ip, color)
                    if (verbose>=2):
                        print('Delay '+str(timeDelay*0.001))
                    time.sleep(timeDelay*0.001)
                    if (verbose>=2):
                        print('Invio comando di spegnimento a '+ips[ip])
                    #requests.get('http://'+ips[ip]+'?ledoff')
                    sendColorCommand(ip, -1)
                except requests.exceptions.RequestException:
                    print('Errore a '+ips[ip])
            for ip in range(len(ips)-1,0,-1):
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+colors[color]+' a '+ips[ip])
                    #requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    sendColorCommand(ip, color)
                    if (verbose>=2):
                        print('Delay '+str(timeDelay*0.001))
                    time.sleep(timeDelay*0.001)
                    if (verbose>=2):
                        print('Invio comando di spegnimento a '+ips[ip])
                    #requests.get('http://'+ips[ip]+'?ledoff')
                    sendColorCommand(ip, -1)
                except requests.exceptions.RequestException:
                    print('Errore a '+ips[ip])
    if (stato==2):
        if (verbose>=1):
            print('Partenza ciclo gioco 2')
        for color in range(len(colors)):
            for ip in range(len(ips)):
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+colors[color]+' a '+ips[ip])
                    #requests.get('http://'+ip+'?'+color, timeout=0.1)
                    sendColorCommand(ip, color)
                except requests.exceptions.RequestException:
                    print('Errore a '+ips[ip])
                if (verbose>=2):
                    print('Delay '+str(timeDelay*0.001))
                time.sleep(timeDelay*0.001)
    if (stato==3):
        if (verbose>=1):
            print('Partenza ciclo gioco 3')
        for color in colors:
	    for i in range(0,len(ips)-1):
		if (stato!=thisStato):
		    break
		try:
		    print('Sending '+random.choice(colors)+' at '+ips[i])
		    requests.get('http://'+ips[i]+'?'+color, timeout=0.1)
		    print('Sending '+random.choice(colors)+' at '+ips[len(ips)-i-1])
		    requests.get('http://'+ips[len(ips)-i-1]+'?'+color, timeout=0.1)
		    time.sleep(timeDelay*0.001)
		    requests.get('http://'+ips[i]+'?off', timeout=0.1)
		    requests.get('http://'+ips[len(ips)-i-1]+'?off', timeout=0.1)
		    print('Sending off')
		except requests.exceptions.RequestException:
		    print('Error sending command')
	    for i in range(len(ips)-1,0,-1):
                if (stato!=thisStato):
                    break
		try:
		    print('Sending '+random.choice(colors)+' at '+ips[i])
		    requests.get('http://'+ips[i]+'?'+color, timeout=0.1)
		    print('Sending '+random.choice(colors)+' at '+ips[len(ips)-i-1])
		    requests.get('http://'+ips[len(ips)-i-1]+'?'+color, timeout=0.1)
		    time.sleep(timeDelay*0.001)
		    requests.get('http://'+ips[i]+'?off', timeout=0.1)
                    requests.get('http://'+ips[len(ips)-i-1]+'?off', timeout=0.1)
                    print('Sending off')
		except requests.exceptions.RequestException:
		    print('Error sending command')
    if (stato==4):
        if (verbose>=1):
            print('Partenza ciclo gioco 4')
	try:
	    requests.get('http://'+random.choice(ips)+'?'+random.choice(colors), timeout=0.1)
            time.sleep(timeDelay*0.001)
	except requests.exceptions.RequestException:
	    print('Error sending command')

print("TIME ART DAEMON - V. 1.0.0")

# AVVIO BOT TELEGRAM #
bot = telepot.Bot(botToken)
telepot.loop.MessageLoop(bot, handle).run_as_thread()
print("Telegram bot: ok")

# THREAD PER CONTROLLO CONTINUO STATO ARDUINO #
checkThread = ThreadManager(function = checkArduinoOnline)
checkThread.start()

createWindow()
