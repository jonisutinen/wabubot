#-*- coding: utf-8 -*-

import telepot
import sys
import time
from collections import OrderedDict
from prettytable import PrettyTable
import time
import datetime
import os
import json
import pprint

bot = telepot.Bot('478183515:AAGF0ChUZrya9J0wT0VXoigT9DPEhAGqj5g')

def jsonfileload():
    try:
        pisteet = json.load(open('pisteet.json'))
        pisteet = {int(k):float(v) for k,v in pisteet.items()}
    except IOError:
        pisteet = {}
    print(pisteet)
    return pisteet

pisteet = jsonfileload()

def getname():
    response = bot.getUpdates()
    try:
        nimi = response[0]['message']['from']['first_name'] + ' ' + response[0]['message']['from']['last_name'] + \
        ' ' + response[0]['message']['from']['username']
    except IndexError:
        nimi = ''
    except KeyError:
        try:
            nimi = response[0]['message']['from']['first_name'] + ' ' + response[0]['message']['from']['last_name']
        except KeyError:
            try:
                nimi = response[0]['message']['from']['username']
            except KeyError:
                nimi = ''
    return nimi


def log(string):
    try:
        name = getname()
        logfile = open('log.html', 'r')
        logi = logfile.read()
        logfile.close()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
        logfile = open('log.html', 'w')
        logfile.write('<p>'+ '[' + str(st) + ']: ' + '[' + name + '] ' + str(string) + '<p>' + logi)
        logfile.close()
    except IOError:
        print('Virhe tiedoston luvussa')

def clearlog():
    logfile = open('log.html', 'w')
    logfile.write('')
    logfile.close()
    log('Logi tyhjennetty')
    print('Logi tyhjennetty')

def jsonfilesave(pisteet):
    jsonsave = json.dumps(pisteet)
    f = open('pisteet.json','w')
    f.write(jsonsave)
    print('Kirjoitettu json tiedostoon')
    log('Kirjoitettu json tiedostoon')
    f.close()

def pistelaskuri(key, value):
    if key in pisteet:
        pisteet2 = pisteet.get(key)
        pisteet2 = pisteet2 + value
        pisteet[key] = pisteet2
    else:
        pisteet[key] = value
    pisteetsorted = OrderedDict(sorted(pisteet.items(), key=lambda x: x[0]))
    jsonfilesave(pisteetsorted)
    print(pisteet)
    log(pisteet)

def handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
    	teksti = msg['text']

        if '/add' in teksti.lower():
            if chat_id == -1001330616963:
                piste = teksti.split()
                print(piste[1])
                try:
                    if isinstance(int(piste[1]), (int, float)):
                        try:
                            arvo = float(piste[2].replace(',','.'))
                            print(arvo)
                            log(arvo)
                            if float(arvo) >= 0 and float(arvo) <= 10:
                                pistelaskuri(int(piste[1]), arvo)
                                bot.sendMessage(chat_id, 'Lisäys onnistui ' + str(piste[1]) + ' ' + str(arvo))
                            else:
                                bot.sendMessage(chat_id, 'Lisäys epäonnistui, sallittu pistemäärä 0-10.')

                        except IndexError:
                            bot.sendMessage(chat_id, 'Unohditko lisätä pisteet?\nKomennon käyttö: /add jnro pisteet\nEsim. /add 1 10')
                        except ValueError:
                            bot.sendMessage(chat_id, 'Pisteet jotain muuta kuin numeroita, yritäppäs uudestaan')
                    else:
                        bot.sendMessage('Yritäppäs uudestaan')
                except ValueError:
                    bot.sendMessage(chat_id, 'Joukkuenumero virheellinen, yritäppäs uudestaan')
            else:
                bot.sendMessage(chat_id, 'Väärä chatti urpo')
                log('/add käytettty väärästä chatistä')
                print('/add käytetty väärästä chätistä')

        elif '/tulos' in teksti.lower():
            bot.sendMessage(chat_id, 'Tulokset löytyvät osoitteesta: http://jonisutinen.fi/wabubot/')

        elif '/nollaa' in teksti.lower():
            pisteet.clear()
            for i in range(2):
                jsonfilesave(pisteet)
            print('Sanakirja tyhjennetty')
            log('Sanakirja tyhjennetty')
            bot.sendMessage(chat_id, 'Tuloslista nollattu.')

        elif '/clearlog' in teksti.lower():
            clearlog()

        elif '/komennot' in teksti.lower():
            bot.sendMessage(chat_id, '/add jnro pisteet\n/tulos')

        elif 'getchatid' in teksti.lower():
            print(chat_id)
            log(chat_id)

        else:
            print(teksti)
            log(teksti)

bot.message_loop(handle)
print ('Kuuntelen kylla...')
log('Kuuntelen kylla...')

while 1:
    time.sleep(10)
