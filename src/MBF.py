#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : MBF.py                             #
# Author         : Rizal F                             #
# Github         : https://github.com/Rizal-XD           #
# Facebook       : https://www.facebook.com/AKUN.KERTASS    #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from src import lib
from src.store import Store
from src.CLI import (inputs, prints, banner, br, progressBar)
from time import sleep
import os ,requests

class MBF:
    def __init__(self, store=None):
        self.store = store
        store.instance = self

    def run(self):
        banner()
        if lib.isLogin() == False:
            if len(lib.sessionList()) == 0:
                return self.store.login.askLogin()
            else:
                return self.store.login.sessionLogin()
        if lib.isActive(self) == False:
            br(1)
            prints('!m! cookies mati. silahkan login ulang')
            br(1)
            inputs('!k!Tekan enter untuk login kembali..')
            return self.run()
        id = self.store.object['credentials']['id']
        ip = requests.get('https://api.ipify.org').text
        name = self.store.object['credentials']['name']
        prints('!p!_!r!' * 55)
        prints('!p![!h!•!p!] !p!NAMA AKUN !p!:!k! %s!r!' %(name))
        prints('!p![!h!•!p!] !p!UID       !p!:!k! %s!r!' %(id))
        prints('!p![!h!•!p!] !p!IP        !p!:!k! %s!r!' %format(ip))
        prints('!p!_!r!' * 55)
        for index in self.store.menu:
            prints(self.store.menu[index]['name'])
        try:
            br(1)
            prints('!p!-!r!' * 55)
            pils = int(inputs('!p!RizalXd/>:!h! '))
            pils = '%02d'%(pils,)
            function = self.store.menu[pils]['func']
        except (ValueError, KeyError, IndexError):
            br(1)
            prints('!m!Isi Yang bener...')
            sleep(2)
            return self.run()

        br(1)

        progressBar(text='loading...', max=20)

        return function()

    def back(self):
        inputs('!k!Tekan enter untuk kembali..')
        return self.run()

    def clearDumpCache(self, count=0):
        list = lib.cacheDumpList()
        if len(list) == 0:
            br(1)
            prints('!m!Belum ada cache...')
            br(1)
            return self.back()
        br(2)
        prints('!m![ !h!LIST SEMUA CACHE DARI HASIL DUMP!r! !m!]')
        br(1)
        for cache in list:
            count+=1
            num = '%02d'%(count,)
            prints('!p![!h!%s!p!] !p!%s'%(num, cache['name']))
        prints('!p!_!r!' * 55)
        br(1)
        prints('!p!Guanakan (,)(comma) untuk pilihan selanjutnya, contoh: 1,2,3')
        prints('!p!Ketik !m!\'all\'!p! untuk menghapus semua cache.')
        prints('!p!Sayangi penyimpanan anda lort untuk menyimpan ocep :v !')
        br(1)
        prints('!k! tekan enter untuk kembali.')
        br(1)
        select = inputs('!p!Pilih : !k!')
        if select.lower() in ["all", "'all'"]:
            for delete in list:
                try:
                    name = delete['name']
                    path = delete['path']
                    os.remove(path)
                    prints('!h! - %s - Dihapus!r!' %(name))
                except:
                    pass
            br(1)
            return self.back()
        br(1)
        for e in select.strip().split(','):
            try:
                name = list[int(e)-1]['name']
                path = list[int(e)-1]['path']
                os.remove(path)
                prints('!h! - %s - Dihapus!r!' %(name), blank_left=6)
            except:
                pass
        br(1)
        return self.back()
    
    def resultCrack(self):
        while True:
            ask = inputs('!p!Ingin melihat hasil CP/OK? !m![!p!CP/OK!m!]!p! : !p!')
            if ask.lower() == 'cp':
                data = lib.resultCrack(name='CP')
                break
            elif ask.lower() == 'ok':
                data = lib.resultCrack(name='OK')
                break
            else:
                br(1)
                prints('!m!Input salah...')
                br(1)
        if len(data) == 0:
            br(1)
            prints('!m!Belum ada hasil...')
            br(1)
            return self.back()
        br(1)
        prints('!m![ !b!LIST SEMUA HASIL %s!r! !m!]'%(ask.upper()))
        for res in data:
            br(2)
            prints('!p!_!r!' * 55)
            prints('!m!> !p!Tanggal !h!%s !p!: !k!%s'%(res['created_at'], res['total']))
            prints('!p!_!r!' * 55)
            for e in res['list']:
                prints('!m!- !p!%s'%(e))
        br(2)
        type = inputs('!m!Ketik \'delete\' untuk menghapus semua hasil atau enter untuk batal !p!: !b!')
        if type.lower() in ["delete","'delete'"]:
            os.remove('result/%s.json'%(ask.upper()))
            br(1)
            prints('!h!Semua hasil \'%s\' berhasil dihapus!'%(ask))
            br(1)
            return self.back()

        return self.run()

    def changeAccount(self):
        try:
            os.remove('.login.json')
        except:
            pass
        self.store.http.cookies.clear()
        return self.run()
        
    def updet(self):
        os.system('git pull')
        sleep(2)
        return self.run()