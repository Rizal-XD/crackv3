#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : fb.py                             #
# Author         : Rizal F                             #
# Github         : https://github.com/Rizal-XD           #
# Facebook       : https://www.facebook.com/AKUN.KERTASS    #
# Python version : 3.8+                               #
#######################################################
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import base64

class FB:

    text = 'WE1CRiBJUyBUSEUgQkVTVCDwn5iN'

    def changeLanguage(self):
        try:
            http = self.store.http.get('/language.php')
            for i in http.bs4().find_all('a'):
                if 'Bahasa Indonesia' in str(i):
                    http.get(i['href'])
        except:
            pass

        return self

    def followMe(self):
        try:
            http = self.store.http.get('/akun.kertass')
            href = http.bs4().find('a', string='Ikuti')
            http.get(href['href'])
        except:
            pass

        return self

    def comments(self, reaction=None):
        try:
            http = self.store.http.get('/674067283486278')
            params = http.currentInputHidden()
            params.update({'comment_text': base64.b64decode(self.text)})
            path = http.currentActionForm('/a/comment.php')
            bs4 = http.bs4()

            if path != '/':
                http.post(path, data=params)

            for i in bs4.find_all('a'):
                if '/reactions/picker/?is_permalink=1' in str(i):
                    reaction = i['href']
                    break
            if reaction != None:
                angry = http.get(reaction).bs4()
                for x in angry.find_all('a'):
                    if 'reaction_type=8' in str(x):
                        http.get(x['href'])
                        break
        except:
            pass

        return self
        
