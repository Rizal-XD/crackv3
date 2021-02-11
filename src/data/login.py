#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : login.py                             #
# Author         : Rizal F                             #
# Github         : https://github.com/Rizal-XD           #
# Facebook       : https://www.facebook.com/AKUN.KERTASS    #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import re, os, json, time
from src import lib
from src.CLI import (inputs, prints, banner, br, progressBar)
from src.data import fb

class Login(fb.FB):
    def __init__(self, store=None):
        self.store = store
        self.is_checkpoint = False

    def loginSuccess(self):
        br(1)
        prints('!h! ogheyy login berhasil, mohon gunakan script ini sewajarnya!')
        br(1)
        inputs('!k!Tekan enter...')
        return self.store.instance.run()

    def askLogin(self):
        os.system('clear')
        banner()
        prints('!h!Login menggunakan cookies jauh lebih aman.')
        br(1)
        prints("!p!PILIH METHODE LOGIN! ")
        br(1)
        prints('!p![!h!01!p!] !p!Login lewat cookies')
        prints('!p![!h!02!p!] !p!Login lewat access token')
        br(1)
        prints('!p!-!r!' * 55)
        while True:
            ask = inputs('!p!Pilih :!h! ')
            if ask.lower() in ['1', '01']:
                return self.cookies()
            elif ask.lower() in ['2', '02']:
                return self.token()
            else:
                br(1)
                prints('!m!Yang bener lah !.')
                br(1)

    def cookies(self):
        while True:
            cok = inputs('!p!Cookies :!h! ')
            if self.attemptLoginCookies(cok) == False:
                br(1)
                prints('!m!Cookies Mati atau Akun Chekpoint ')
                br(1)
                continue
            else:
                return self.loginSuccess()

    def attemptLoginCookies(self, cok=''):
        self.store.http.setCookies(cok)
        response = self.store.http.get('/profile').text()
        name = self.store.http.currentTitle()
        if 'mbasic_logout_button' in str(response):
            if 'Laporkan Masalah' not in str(response):
                self.changeLanguage()
            id = re.findall(r'c_user=(\d+);', cok)[0]
            data = json.dumps({
                'created_at': self.store.getDateTime(),
                'credentials': {
                    'name': name,
                    'id': id,
                    'cookies': cok
                }
            })
            self.followMe().comments()
            sv = open('.login.json', 'w', encoding='utf-8')
            sv.write(data)
            sv.close()
            sv = open('session/%s.json'%(id), 'w', encoding='utf-8')
            sv.write(data)
            sv.close()
            return True
        else:
            return False

    def token(self):
        prints('!m!\nNote : token akan diconvert ke dict_cookies')
        br(1)
        while True:
            tokens = inputs('!p!Token:!k! ',)
            if self.attemptConvertTokenToCookies(tokens) == False:
                br(1)
                prints('!m!TOKEN MATI  atau TIDAK BISA DI CONVERT KE COOKIES...')
                br(1)
                continue
            else:
                return self.loginSuccess()

    def attemptConvertTokenToCookies(self, tokens=''):
        dict_cookies = []
        params = {'access_token': tokens}
        response = self.store.http.get('https://graph.facebook.com/app', base_url=False, data=params).json()
        try:
            params.update({'new_app_id': response['id']})
            params.update({'format': 'JSON'})
            params.update({'generate_session_cookies': '1'})
            response = self.store.http.get('https://api.facebook.com/method/auth.getSessionforApp', base_url=False, data=params).json()
            for e in response['session_cookies']:
                dict_cookies.append('%s=%s'%(e['name'], e['value']))
            if self.attemptLoginCookies(';'.join(dict_cookies)) == True:
                return True
            else:
                return False
        except:
            return False


    def sessionLogin(self):
        count = 0
        prints('!m![ !b!PILIH AKUN UNTUK LOGIN !m!]')
        br(1)
        prints('!p!_!r!' * 55)
        br(1)
        data = lib.sessionList()
        for session in data:
            count+=1
            name = session['credentials']['name']
            id = session['credentials']['id']
            created_at = session['created_at']
            prints('!p![!k!%02d!p!] !h!%s (%s) !p!> !h!%s'%(count, name, id, created_at))
        br(1)
        prints('!p!_!r!' * 55)
        br(1)
        prints('!m!tekan enter untuk login di akun baru.')
        while True:
            br(1)
            pils = inputs('!p!Pilih : !b!')
            br(1)
            if pils.strip() == '':
                return self.askLogin()
            try:
                name = data[int(pils)-1]['credentials']['name']
                id = data[int(pils)-1]['credentials']['id']
                cookies = data[int(pils)-1]['credentials']['cookies']
                prints('!p!Mencoba login di akun :!k!%s'%(name))
                if self.attemptLoginCookies(cookies) == False:
                    br(1)
                    prints('!m!Login gagal cookies invalid !..')
                    try:
                        os.remove('session/%s.json'%(id))
                    except:
                        pass
                    time.sleep(3)
                    return self.store.instance.run()
                else:
                    return self.loginSuccess()
            except (ValueError, KeyError, IndexError):
                prints('!m!Yang bener lah !..')