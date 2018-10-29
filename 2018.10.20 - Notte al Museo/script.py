# -*- coding: utf-8 -*-
 
################ ITIS Paleocapa 2018 ################
# Main developers: Cristian Livella, Matteo Soldini #
#             Project: Esperia Time Art             #
#####################################################
 
import threading, time, telepot, telepot.loop, sys, os, requests, random
 
### CONFIGURAZIONE ###
# Token bot Telegram
botToken = "586571665:AAH6lXEgiiR3iBu_G-CBkA83wM4ndO_CuB4"
 
# Chat id consentiti
allowedChatId = [45395590,296001158,26579149,168562936,478291568,419250460,164062179,213959477,443989610,766297703]

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
 
# IP Arduino
ips = [
	"10.205.0.13",
	"10.205.0.12",
	"10.205.0.11",
	"10.205.0.14",
	"10.205.0.15",
	"10.205.0.16",
	"10.205.0.17",
	"10.205.0.18"
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

telegramChatIdThatWhoStartedTheGame = 0
 
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
 
 
def handle(msg):
    global stato
    global timeDelay
    global bot
    global telegramChatIdThatWhoStartedTheGame
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
            telegramChatIdThatWhoStartedTheGame = chatId
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
            for ip in ips:
                try:
                    requests.get('http://'+ip+'?ledoff', timeout=0.2)
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
        elif (message=='/arcobaleno'):
			if (verbose>=2):
				print('Arcobaleno attivato')
			try:
                		gameThread.stop()
            		except:
                		pass
			requests.get('http://'+ips[0]+'?red', timeout=0.1)
			requests.get('http://'+ips[1]+'?orange', timeout=0.1)
			requests.get('http://'+ips[2]+'?orange2', timeout=0.1)
			requests.get('http://'+ips[3]+'?yellow', timeout=0.1)
			requests.get('http://'+ips[4]+'?green', timeout=0.1)
			requests.get('http://'+ips[5]+'?blue3', timeout=0.1)
			requests.get('http://'+ips[6]+'?blue', timeout=0.1)
			requests.get('http://'+ips[7]+'?purple', timeout=0.1)
			bot.sendMessage(chatId, 'Arcobaleno attivato')
	elif (message=='/rosso_fisso'):
			if (verbose>=2):
				print('Rosso fisso attivato')
			try:
                		gameThread.stop()
            		except:
                		pass
			requests.get('http://'+ips[0]+'?red', timeout=0.1)
			requests.get('http://'+ips[1]+'?red', timeout=0.1)
			requests.get('http://'+ips[2]+'?red', timeout=0.1)
			requests.get('http://'+ips[3]+'?red', timeout=0.1)
			requests.get('http://'+ips[4]+'?red', timeout=0.1)
			requests.get('http://'+ips[5]+'?red', timeout=0.1)
			requests.get('http://'+ips[6]+'?red', timeout=0.1)
			requests.get('http://'+ips[7]+'?red', timeout=0.1)
			bot.sendMessage(chatId, 'Rosso fisso attivato')
	elif (message=='/random'):
			if (verbose>=2):
				print('Random attivato')
			try:
                		gameThread.stop()
            		except:
                		pass
			requests.get('http://'+ips[0]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[1]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[2]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[3]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[4]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[5]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[6]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			requests.get('http://'+ips[7]+'?'+colors[random.randint(0, 16)], timeout=0.1)
			bot.sendMessage(chatId, 'Colori random inviati')
        else:
            bot.sendMessage(chatId, 'Comando non riconosciuto.\n\nScrivi /help per la lista dei comandi.', parse_mode='markdown')
    except:
        pass
 
def lightGame():
    global bot
    global telegramChatIdThatWhoStartedTheGame
    thisStato = stato
    if (stato==0):
        stopGameThread()
        ligthsOff()
        return
    if (stato==1):
        if (verbose>=1):
            print('Partenza ciclo gioco 1')
        for color in colors:
            for ip in range(0,len(ips)-1):
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+color+' a '+ips[ip])
                    requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    if (verbose>=2):
                        print('Delay '+str(timeDelay*0.001))
                    time.sleep(timeDelay*0.001)
                    if (verbose>=2):
                        print('Invio comando di spegnimento a '+ips[ip])
                    requests.get('http://'+ips[ip]+'?ledoff')
                except requests.exceptions.RequestException:
                    print('Errore a '+ips[ip])
                    bot.sendMessage(telegramChatIdThatWhoStartedTheGame, "Errore a " + ips[ip])
            for ip in range(len(ips)-1,0,-1):
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+color+' a '+ips[ip])
                    requests.get('http://'+ips[ip]+'?'+color, timeout=0.1)
                    if (verbose>=2):
                        print('Delay '+str(timeDelay*0.001))
                    time.sleep(timeDelay*0.001)
                    if (verbose>=2):
                        print('Invio comando di spegnimento a '+ips[ip])
                    requests.get('http://'+ips[ip]+'?ledoff')
                except requests.exceptions.RequestException:
                    print('Errore a '+ips[ip])
                    bot.sendMessage(telegramChatIdThatWhoStartedTheGame, "Errore a " + ips[ip])
    if (stato==2):
        if (verbose>=1):
            print('Partenza ciclo gioco 2')
        for color in colors:
            for ip in ips:
                if (stato!=thisStato):
                    break
                try:
                    if (verbose>=2):
                        print('Invio '+color+' a '+ip)
                    requests.get('http://'+ip+'?'+color, timeout=0.1)
                except requests.exceptions.RequestException:
                    print('Errore a '+ip)
                    bot.sendMessage(telegramChatIdThatWhoStartedTheGame, "Errore a " + ips[ip])
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
		    bot.sendMessage(telegramChatIdThatWhoStartedTheGame, "Errore a " + ips[i])
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
		    bot.sendMessage(telegramChatIdThatWhoStartedTheGame, "Errore a " + ips[i])
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
