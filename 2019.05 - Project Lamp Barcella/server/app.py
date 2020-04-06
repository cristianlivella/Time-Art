import eventlet
eventlet.monkey_patch()
import json
import sqlite3
import threading
import time
from flask import Flask, jsonify, g, abort, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
from requests import get
#import telepot, telepot.loop
#from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import telebot

# configuration
DEBUG = True
DATABASE = 'sqlite.db'
ALLOWED_IPS = ['127.0.0.1']
TOTAL_GAME = 4
BOT_TOKEN = 'INSERT_HERE_TELEGRAM_TOKEN'
ALOWED_CHAT_IDS = []

lampCurrentColors = [0]
arduinoStatus = [0]
currentGameId = 0
gameCounter = 0
timeDelay = 500

# istanza dell'applicazione
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ciaoo'
app.config.from_object(__name__)
socketio = SocketIO(app)

# abilita CORS
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.before_request
def allowIp():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)

@app.route('/', methods=['GET'])
def welcome():
    return send_from_directory('', 'welcome.html')

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify('pong')

@app.route('/getLamps', methods=['GET'])
def getLamps():
    sendSocketUpdate()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/getColors', methods=['GET'])
def getColors():
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM colors')
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/changeColor/<lampId>/<colorId>')
def flaskChangeColor(lampId, colorId):
    global currentGameId
    global gameCounter
    currentGameId = 0
    gameCounter = gameCounter + 1
    if lampId == '0':
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM lamps')
        rows = cur.fetchall()
        for row in rows:
            changeColor(row['id'], colorId, 0)
            changeColor(row['id'], colorId, 0)
    else:
        changeColor(lampId, colorId, 0)
    return jsonify('ok')

@app.route('/startGame/<gameId>')
def flaskStartGame(gameId):
    startGame(gameId)
    return jsonify('ok')

@app.route('/setTime/<gameTime>')
def flaskSetTtime(gameTime):
    gameTime = int(gameTime)
    setTime(gameTime)
    return jsonify('ok')

@app.route('/telegramBot/info')
def telegramBot():
    return jsonify({'token': BOT_TOKEN})

@app.route('/telegramBot/checkChatId/<chatId>/<userName>')
def checkChatId(chatId, userName):
    timestamp = time.time()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM allowedChatIds WHERE chatId=' + str(chatId) + ' AND (expire=0 OR expire>' + str(timestamp) + ')')
    rows = cur.fetchall()
    if len(rows)>0:
        return jsonify(1)
    else:
        if userName=='null':
            return jsonify(0)
        cur = con.cursor()
        cur.execute('SELECT * FROM chatIdsRequests WHERE chatId=' + str(chatId) + ' AND status=1')
        rows = cur.fetchall()
        if len(rows)==0:
            cur = con.cursor()
            cur.execute('INSERT INTO chatIdsRequests (name, chatId, status) VALUES ("' + userName + '", ' + chatId + ', 1)')
            con.commit()
        return jsonify(0)

@app.route('/telegramBot/getAuthorizedUsers')
def getAuthorizedUsers():
    timestamp = time.time()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM allowedChatIds WHERE (expire=0 OR expire>' + str(timestamp) + ')')
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/telegramBot/getUsersRequests')
def getUsersRequests():
    timestamp = time.time()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM chatIdsRequests WHERE status=1')
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/telegramBot/add10minutes/<userId>')
def add10minutes(userId):
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('UPDATE allowedChatIds SET expire = expire + 600 WHERE expire!=0 AND id=' + str(userId))
    con.commit()
    return jsonify('ok')

@app.route('/telegramBot/removeUser/<userId>')
def removeUser(userId):
    timestamp = time.time()
    timestamp = timestamp -1
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('UPDATE allowedChatIds SET expire = ' + str(int(timestamp)) + ' WHERE id=' + str(userId))
    con.commit()
    return jsonify('ok')

@app.route('/telegramBot/giveAuth/<requestId>/<permanent>')
def giveAuth(requestId, permanent):
    timestamp = time.time()
    timestamp = timestamp + 600
    if int(permanent)==1:
        timestamp = 0
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM chatIdsRequests WHERE status=1 AND id = ' + str(requestId))
    rows = cur.fetchall()
    name = rows[0]['name']
    chatId = rows[0]['chatId']
    cur = con.cursor()
    cur.execute('UPDATE chatIdsRequests SET status = 0 WHERE chatId = ' + str(chatId))
    cur = con.cursor()
    cur = con.execute('INSERT INTO allowedChatIds (name, chatId, expire) VALUES ("' + name + '", ' + str(chatId) + ', ' + str(int(timestamp)) + ')')
    con.commit()
    return jsonify('ok')

@app.route('/telegramBot/rejectRequest/<requestId>')
def rejectRequest(requestId):
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('UPDATE chatIdsRequests SET status = 0 WHERE id = ' + str(requestId))
    con.commit()
    return jsonify('ok')

@socketio.on('connect', namespace='/')
def testConnect():
    global arduinoStatus
    global lampCurrentColors
    sendSocketUpdate()

def startGame(gameId):
    global currentGameId
    gameId = int(gameId)
    if gameId == currentGameId:
        return
    if gameId == 1:
        gameThread = threading.Thread(target=game1)
        gameThread.start()
    elif gameId == 2:
        gameThread = threading.Thread(target=game2)
        gameThread.start()
    elif gameId == 3:
        gameThread = threading.Thread(target=game3)
        gameThread.start()
    elif gameId == 4:
        gameThread = threading.Thread(target=game4)
        gameThread.start()
    else:
        return
    currentGameId = gameId
    sendSocketUpdate()

def setTime(gameTime):
    global timeDelay
    timeDelay = gameTime

def game1():
    global timeDelay
    global gameCounter
    gameCounter = gameCounter + 1
    myUnicId = gameCounter
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    lamps = cur.fetchall()
    cur.execute('SELECT * FROM colors')
    colors = cur.fetchall()
    while True:
        for color in colors:
            for lamp in lamps:
                if gameCounter != myUnicId:
                    return
                changeColor(lamp['id'], color['id'], 1)
                time.sleep(timeDelay*0.001)
                changeColor(lamp['id'], 0, 1)
            iterLamps = iter(reversed(lamps))
            next(iterLamps)
            prev = next(iterLamps)
            for lamp in iterLamps:
                if gameCounter != myUnicId:
                    return
                changeColor(prev['id'], color['id'], 1)
                time.sleep(timeDelay*0.001)
                changeColor(prev['id'], 0, 1)
                prev = lamp

def game2():
    global timeDelay
    global gameCounter
    gameCounter = gameCounter + 1
    myUnicId = gameCounter
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    lamps = cur.fetchall()
    cur.execute('SELECT * FROM colors')
    colors = cur.fetchall()
    while True:
        for color in colors:
            for lamp in lamps:
                if gameCounter != myUnicId:
                    return
                changeColor(lamp['id'], color['id'], 2)
                time.sleep(timeDelay*0.001)

def game3():
    global timeDelay
    global gameCounter
    gameCounter = gameCounter + 1
    myUnicId = gameCounter
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    lamps = cur.fetchall()
    cur.execute('SELECT * FROM colors')
    colors = cur.fetchall()
    while True:
        for color in colors:
            for i in range(0, len(lamps)-1):
                if gameCounter != myUnicId:
                    return
                changeColor(lamps[i]['id'], color['id'], 3)
                changeColor(lamps[len(lamps)-i-1]['id'], color['id'], 3)
                time.sleep(timeDelay*0.001)
            for i in range(len(lamps)-1, 0, -1):
                if gameCounter != myUnicId:
                    return
                changeColor(lamps[i]['id'], color['id'], 3)
                changeColor(lamps[len(lamps)-i-1]['id'], color['id'], 3)
                time.sleep(timeDelay*0.001)

def game4():
    global timeDelay
    global gameCounter
    gameCounter = gameCounter + 1
    myUnicId = gameCounter
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    lamps = cur.fetchall()
    cur.execute('SELECT * FROM colors')
    colors = cur.fetchall()
    while True:
        if gameCounter != myUnicId:
            return
        changeColor(random.choice(lamps)['id'], random.choice(colors)['id'], 4)
        time.sleep(timeDelay*0.001)

def changeColor(lampId, colorId, gameId):
    global currentGameId
    if gameId != currentGameId:
        return
    lampId = int(lampId)
    colorId = int(colorId)
    if arduinoStatus[lampId-1] == 0:        ## only for debug
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('SELECT ip FROM lamps WHERE id=' + str(lampId))
        ip = cur.fetchone()[0]
        if colorId == 0:
            color = 'ledoff'
        else:
            cur.execute('SELECT command FROM colors WHERE id=' + str(colorId))
            color = cur.fetchone()[0]
        url = 'http://' + ip + '/?' + color
        asyncRequest(url)
        lampCurrentColors[lampId-1] = colorId
        sendSocketUpdate()
        print('hey!')

def asyncRequest(url):
    thread = threading.Thread(target=tryRequest, args=(url,))
    thread.start()

def tryRequest(url):
    try:
        print(url)
        get(url)
    except:
        print('err')

def sendSocketUpdate():
    socketio.emit('projectlamp', {'arduinoStatus': arduinoStatus, 'lampCurrentColors' : lampCurrentColors, 'totalGame' : TOTAL_GAME, 'currentGameId' : currentGameId, 'timeDelay': timeDelay}, broadcast=True)

def updateArduinoStatus():
    global arduinoStatus
    global socketio
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    rows = cur.fetchall()
    for index, row in enumerate(rows):
        try:
            requests.get('http://'+row['ip'], timeout=1)
            arduinoStatus[index] = 1
        except:
            arduinoStatus[index] = 0
            #lampCurrentColors[index] = 1
    sendSocketUpdate()

def threadUpdateArduinoStatus():
    while True:
        updateArduinoStatus()
        time.sleep(10)
        
if __name__ == '__main__':
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM lamps')
    rows = cur.fetchall()
    arduinoStatus = [0] * len(rows)
    lampCurrentColors = [0] * len(rows)
    for index, row in enumerate(rows):
        lampCurrentColors[index] = 0
        arduinoStatus[index] = 0
    thread = threading.Thread(target=threadUpdateArduinoStatus)
    thread.start()
    socketio.run(app, debug=True)
