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

bot = telepot.Bot('478183515:AAGF0ChUZrya9J0wT0VXoigT9DPEhAGqj5g')
#pisteet = {}


def jsonfileload():
    try:
        pisteet = json.load(open('pisteet1.json'))
        pisteet = {int(k):float(v) for k,v in pisteet.items()}
    except IOError:
        pisteet = {}
    print(pisteet)
    return pisteet


pisteet = jsonfileload()

def log(string):
    try:
        logfile = open('log.html', 'r')
        logi = logfile.read()
        logfile.close()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
        logfile = open('log.html', 'w')
        logfile.write('<p>'+ '[' + str(st) + ']: ' + str(string) + '<p>' + logi)
        logfile.close()
    except IOError:
        print('Virhe tiedoston luvussa')


def clearlog():
    logfile = open('log.html', 'w')
    logfile.write('')
    logfile.close()
    log('Logi tyhjennetty')
    print('Logi tyhjennetty')


def jsonfilesave(pisteet, i):
    #pisteetnew = jsonfileload()
    #print(pisteetnew)
    #print(pisteet)
    #pisteetnew.update(pisteet)
    jsonsave = json.dumps(pisteet)
    if i == 0:
        f = open('pisteet1.json','w')
    else:
        f = open('pisteet2.json','w')
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
    for i in range(2):
        if i == 0:
            pisteetsorted = OrderedDict(sorted(pisteet.items(), key=lambda x: x[1], reverse=True))
            jsonfilesave(pisteetsorted, i)
        else:
            pisteetsorted = OrderedDict(sorted(pisteet.items(), key=lambda x: x[0]))
            jsonfilesave(pisteetsorted, i)
    #jsonfilesave(pisteet)
    print(pisteet)
    log(pisteet)
    #return pisteet

def htmltable(taulukko, m):
    html_string = taulukko.get_html_string(attributes={'class': 'table table-striped header-fixed'})
    if m == 1:
        html_file = open('pisteittain.html', 'w')
    else:
        html_file = open('joukkuettain.html', 'w')

    html_alku = open('htmlkoodialku.html', 'r')
    html_loppu = open('htmlkoodiloppu.html', 'r')
    htmlalku = html_alku.read()
    htmlloppu = html_loppu.read()
    html_file.write(htmlalku + '\n' + html_string + '\n' + htmlloppu)
    if m ==1:
        print('Kirjoitettu html-tiedostoon.')
        log('Kirjoitettu html-tiedostoon.')
    html_file.close()
    html_alku.close()
    html_loppu.close()

def tulos(chat_id):
    for m in range(1,-1,-1):
        #eka taulukko
        if m == 1:
            taulukko = PrettyTable(['Sijoitus', 'Joukkuenro', 'Pisteet'])
        #toka taulukko
        else:
            taulukko = PrettyTable(['Joukkuenro', 'Pisteet'])
        if m == 1:
            pisteetsortedvalue = OrderedDict(sorted(pisteet.items(), key=lambda x: x[1], reverse=True))
        else:
            pisteetsortedvalue = OrderedDict(sorted(pisteet.items(), key=lambda x: x[0]))
        n = 1

        for k,v in pisteetsortedvalue.items():
            avain = str(k)
            arvo = str(v)
            if m == 1:
                taulukko.add_row([n, avain, arvo])
            else:
                taulukko.add_row([avain,arvo])
            n += 1

        if taulukko:
            if m == 1:
                bot.sendMessage(chat_id, 'Tulokset tallennettu ja löytyvät osoitteesta http://jonisutinen.fi/wabubot')
                print(str(taulukko))
                log(str(taulukko))

            htmltable(taulukko, m)

        else:
            bot.sendMessage(chat_id, 'Tuloslista tyhjä.')


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

        '''
        if '/tulos' in teksti.lower():
            tulos(chat_id)
        '''

        if '/nollaa' in teksti.lower():
            pisteet.clear()
            #tulos(chat_id)
            for i in range(2):
                jsonfilesave(pisteet, i)
            print('Sanakirja tyhjennetty')
            log('Sanakirja tyhjennetty')
            bot.sendMessage(chat_id, 'Tuloslista nollattu.')

        if '/clearlog' in teksti.lower():
            clearlog()

        if '/komennot' in teksti.lower():
            bot.sendMessage(chat_id, '/add jnro pisteet\n/tulos')

        if '/getchatid' in teksti.lower():
            print(chat_id)
            log(chat_id)

bot.message_loop(handle)
print ('Kuuntelen kylla...')
log('Kuuntelen kylla...')

while 1:
    time.sleep(10)
