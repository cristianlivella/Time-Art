import requests
import telepot, telepot.loop, time
import socketio
import json
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

HOST = 'http://localhost:5000'

lampCurrentColors = [0]
arduinoStatus = []
currentGameId = 0
timeDelay = 500
nGiochi = 0

socket = socketio.Client()
socket.connect(HOST, namespaces=['/'])
@socket.on('projectlamp')
def projectlamp(data):
    global arduinoStatus
    global lampCurrentColors
    global currentGameId
    global timeDelay
    global nGiochi
    arduinoStatus = data['arduinoStatus']
    lampCurrentColors = data['lampCurrentColors']
    currentGameId = data['currentGameId']
    timeDelay = data['timeDelay']
    nGiochi = data['totalGame']

BOT_TOKEN = ''
ALOWED_CHAT_IDS = []

def checkChatId(chatId, userName):
    response = requests.get(HOST + '/telegramBot/checkChatId/' + str(chatId) + '/' + userName)
    response = response.text
    response = int(response)
    if (response==0):
        return False
    elif (response==1):
        return True

def changeColor(lampId, colorId):
    requests.get(HOST + '/changeColor/' + str(lampId) + '/' + str(colorId))

def startGame(gameId):
    requests.get(HOST + '/startGame/' + str(gameId))

def setTime(timeToSet):
    global timeDelay
    timeDelay = timeToSet
    requests.get(HOST + '/setTime/' + str(timeToSet))

def handle(msg):
    global timeDelay
    chatId = msg['from']['id']
    message = msg['text'].lower()
    nome = msg['from']['first_name'] + ' ' + msg['from']['last_name'] + ' (' + msg['from']['username'] + ')'
    if checkChatId(chatId, nome)==False:
        bot.sendMessage(chatId, '*Ciao!* Attualmente non sei autorizzato ad utilizzare questo bot.\n\nLa tua richiesta è stata *inviata* agli amministratori.', parse_mode='markdown')
        return
    if (message=='/start' or message=='start' or message=='/info' or message=='info' or message=='/help' or message=='help' or message=='menu' or message=='/menu'):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='bianco', callback_data='C-1'), InlineKeyboardButton(text='rosso', callback_data='C-2'), InlineKeyboardButton(text='verde', callback_data='C-4')],
                   [InlineKeyboardButton(text='blu', callback_data='C-5'), InlineKeyboardButton(text='arancione', callback_data='C-7'), InlineKeyboardButton(text='viola', callback_data='C-8')],
                   [InlineKeyboardButton(text='azzurro', callback_data='C-9'), InlineKeyboardButton(text='giallo', callback_data='C-11'), InlineKeyboardButton(text='fucsia', callback_data='C-12')],
                   [InlineKeyboardButton(text='spegni', callback_data='OFF-')],
                   [InlineKeyboardButton(text='gioco 1', callback_data='G-1'), InlineKeyboardButton(text='gioco 2', callback_data='G-2')],
                   [InlineKeyboardButton(text='gioco 3', callback_data='G-3'), InlineKeyboardButton(text='gioco 4', callback_data='G-4')],
                   [InlineKeyboardButton(text='velocità 1', callback_data='S-1'), InlineKeyboardButton(text='velocità 2', callback_data='S-2')],
                   [InlineKeyboardButton(text='velocità 3', callback_data='S-3'), InlineKeyboardButton(text='velocità 4', callback_data='S-4')],
               ])
        bot.sendMessage(chatId, '*Project Lamp* - ITIS Paleocapa', parse_mode='markdown', reply_markup=keyboard)
    else:
        bot.sendMessage(chatId, 'Comando non riconosciuto.\n\nScrivi /menu per visualizzare il menu.', parse_mode='markdown')

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chatId = from_id
    query_data = query_data.split('-', 2)
    if checkChatId(chatId, 'null')==False:
        bot.answerCallbackQuery(query_id, text='Non sei autorizzato ad utilizzare i comandi. Scrivi /start per chiedere l\'autorizzazione.', show_alert=True)
        return
    if query_data[0]=='C':
        changeColor(0, query_data[1])
    elif query_data[0]=='OFF':
        changeColor(0, 0)
    elif query_data[0]=='G':
        startGame(query_data[1])
    elif query_data[0]=='S':
        if query_data[1]=='1':
            setTime(2000)
        elif query_data[1]=='2':
            setTime(1000)
        elif query_data[1]=='3':
            setTime(500)
        elif query_data[1]=='4':
            setTime(250)
    bot.answerCallbackQuery(query_id, text='')

response = json.loads(requests.get(HOST + '/telegramBot/info').text)
BOT_TOKEN = response['token']
bot = telepot.Bot(BOT_TOKEN)
telepot.loop.MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()
print('Telegram bot: ok')

while 1:
    time.sleep(10)
