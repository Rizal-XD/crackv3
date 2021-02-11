#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : dump.py                             #
# Author         : Rizal F                             #
# Github         : https://github.com/Rizal-XD           #
# Facebook       : https://www.facebook.com/AKUN.KERTASS    #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

from threading import (Thread, Event)
from src.CLI import (color, prints, inputs, write, br)
import re, time, json, os
from datetime import datetime

class Dump:
    def __init__(self, store=None):
        self.store = store
        self.event = Event()
        self.__id__ = []
        self.__filter__ = []
        self.proccess = None

    def reset(self):
        self.__id__ = []
        self.__filter__ = []

    def save(self, saveTo):
        datetimes = self.store.getDateTime()
        self.event.clear()
        time.sleep(2)
        saveTo = re.sub('\s\s+', '_', saveTo.lower())
        save = open('dump/%s.json'%(saveTo), 'w')
        save.write(json.dumps({
            'created_at': datetimes,
            'file_name': '%s.json'%(saveTo),
            'data': self.__id__
        }))
        save.close()
        br(2)
        prints('!p!Hasil tersimpan : !k!dump/%s.json'%(saveTo))
        prints('!p!ID terambil     : !k!%s' %(len(self.__id__)))
        br(1)
        return self.store.instance.back()

    def animate(self):
        while self.event.is_set():
            for i in list('\ |/-•'):
                count = len(self.__id__)
                datetimes = datetime.now().strftime('%H:%M:%S')
                self.proccess = '!p![!h!%s!p!]!ran! Writing ID (%s).. %s !r!'%(datetimes, count, i)
                prints(self.proccess, with_flush=True)
                time.sleep(0.1)

    def run(self):
        self.reset()
        self.event.set()
        th = Thread(target=self.animate)
        th.start()

    def getIDFriedsList(self, stop=False, path='/friends/center/friends', saveTo='friendsList'):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all(style='vertical-align: middle'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'/\?uid=(\d+)&' if '/?uid=' in str(hrefs) else '/(.*?)\?fref=', hrefs['href'])
                    prints(f'\r!p!*!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat selengkapnya' in str(response):
                path = response.find('a', string='Lihat selengkapnya')['href']
            else:
                stop = True

        return self.save(saveTo)

    def friendsList(self):
        th = Thread(target=self.getIDFriedsList, args=(False,))
        th.start()
        self.run()
        return self

    def publicID(self, path=None):
        prints('!h!INGFO:!p!pastikan daftar teman bersifat publik, jika ngedump lebih dari 3k ID')
        prints('!m!mungkin akun anda akan kena limit!, dan tidak dapat menggunakan fitur ini lagi.!p!')
        br(1)
        prints("!p!Contoh : !h!zuck")
        while path == None:
            ids = inputs('!p!USERNAME TARGET :!h! ')
            response = self.store.http.get(f'/{str(ids)}').bs4()
            name = self.store.http.currentTitle()
            for x in response.find_all('a'):
                if '/friends?lst=' in str(x):
                    path = x['href']
                    break
            if path == None:
                br(1)
                prints('!m!Id atau username salah atau teman tidak publik.')
                br(1)
                continue
        br(1)
        prints('!p!Nama akun: !k!%s!r!' %(name))
        br(1)
        th = Thread(target=self.getIDpublic, args=(False, path, ids,))
        th.start()
        self.run()
        return self

    def getIDpublic(self, stop=False, path='/', saveTo='public'):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all(style='vertical-align: middle'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'/\?uid=(\d+)&' if '/?uid=' in str(hrefs) else '/(.*?)\?fref=', hrefs['href'])
                    prints(f'\r!p!*!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Teman Lain' in str(response):
                path = response.find('a', string='Lihat Teman Lain')['href']
            else:
                stop = True

        return self.save(saveTo)

    def search(self):
        query = inputs('!p!Kata kunci : !h!')
        path = f'/search/people/?q={query}&source=filter&isTrending=0'
        while True:
            try:
                max = int(inputs('!p!Limit (!b!100!p!) : !b!'))
                break
            except (ValueError):
                br(1)
                prints('!m! Yang bener lah !')
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDSearch, args=(False, path, query, max))
        th.start()
        self.run()
        return self

    def getIDSearch(self, stop=False, path='/', saveTo='search', max=0, base_url=True):
        while stop == False:
            response = self.store.http.get(path, base_url).bs4()
            for x in response.find_all('a'):
                div = x.find('div')
                if '+' not in str(div) and div != None:
                    name = str(div.text)
                    uid = re.findall(r'/\?id=(\d+)&' if '/?id=' in str(x) else '/(.*?)\?refid=', str(x))
                    prints(f'\r!p!*!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Hasil Selanjutnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Hasil Selanjutnya')['href']
                base_url = False
            else:
                stop = True

        return self.save(saveTo)
  
    def react(self, path=None):
        prints('!p!INPUT LINK POSTINGAN TARGET! ')
        prints('!p!(!h!CONTOH :!h!https://www.facebook.com/4/posts/10112184244817511/?app=fbl!m!)')
        br(1)
        while True:
            try:
                link = inputs('!p!Link postingan : !h!')
                domain = link.split('//')[1].split('/')[0]
                link = link.replace(domain, 'mbasic.facebook.com')
            except IndexError:
                br(1)
                prints('!m!Link salah atau tidak valid...')
                br(1)
                continue
            response = self.store.http.get(link, base_url=False).bs4()
            title = self.store.http.currentTitle().replace(' | Facebook', '')
            for x in response.find_all('a'):
                if '/ufi/reaction/profile/browser/?' in str(x):
                    br(1)
                    prints('!p!TITLE: !k!%s' %(title))
                    br(1)
                    path = x['href']
                    break
            if path != None:
                break
            else:
                br(1)
                prints('!m!Postingan tidak ditemukan...')
                br(1)
                continue
        while True:
            try:
                max = int(inputs('!p!Limit (!k!100!p!) :!h! '))
                break
            except (ValueError):
                br(1)
                prints('!m!Yang bener lah !..')
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDReact, args=(False, path, 'react', max,))
        th.start()
        self.run()
        return self

    def getIDReact(self, stop=False, path='/', saveTo='react', max=0):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all('h3'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(x.text)
                    uid = re.findall(r'\/profile.php\?id=(\d+)$' if 'profile.php?id=' in str(x) else '\/(.*?)$', str(hrefs['href']))
                    prints(f'\r!p!*!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Selengkapnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Selengkapnya')['href']
            else:
                stop = True

        return self.save(saveTo)
 
    def postGroup(self):
        while True:
            id = inputs('!p!ID group : !b!')
            path = f'/groups/{str(id)}'
            response = self.store.http.get(path).text()
            if 'Konten Tidak Ditemukan' in str(response):
                br(1)
                prints('!m!Id group tidak ditemukan')
                br(1)
                continue
            else:
                title = self.store.http.currentTitle()
                br(1)
                prints('!p!Nama group : !k!%s' %(title))
                br(1)
            try:
                max = int(inputs('!p!Limit (!b!100!p!) : !b!'))
                break
            except (ValueError):
                br(1)
                prints('!m!Yang bener lah !...')
                br(1)
                continue
        br(1)
        th = Thread(target=self.getIDPostGroup, args=(False, path, id, max))
        th.start()
        self.run()
        return self

    def getIDPostGroup(self, stop=False, path='/', saveTo='postGroup', max=0):
        while stop == False:
            response = self.store.http.get(path).bs4()
            for x in response.find_all('h3'):
                hrefs = x.find('a')
                if '+' not in str(hrefs) and hrefs != None:
                    name = str(hrefs.text)
                    uid = re.findall(r'content_owner_id_new.(\d+)', hrefs['href'])
                    prints(f'\r!p!*!ran!  {name}', blank_right=int(len(self.proccess)-20))
                    if int(len(self.__id__)) == max or int(len(self.__id__)) > max:
                        stop = True
                        break
                    if len(uid) == 1 and str(uid[0]) not in self.__filter__:
                        self.__filter__.append(str(uid[0]))
                        self.__id__.append({'name': str(name), 'id': str(uid[0])})
            if 'Lihat Postingan Lainnya' in str(response) and stop == False:
                path = response.find('a', string='Lihat Postingan Lainnya')['href']
            else:
                stop = True

        return self.save(saveTo)
