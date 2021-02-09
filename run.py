#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : run.py                             #
# Author         : Rizal F                            #
# Github         : https://github.com/Rizal-XD        #
# Facebook       : https://fb.me/AKUN.KERTASS         #
# Python version : 3.8+                               #
#                                                     #
#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import shutil, platform,os
from src.CLI import (progressBarz)

py_version = platform.python_version()

if py_version < '3.7':
    exit('[WARNING] anda menggunakan python version %s silahkan upgrade ke 3.7++'%(py_version))

cache = ['src/__pycache__', 'src/data/__pycache__']

for path in cache:
    try:
        shutil.rmtree(path)
    except:
        pass
            
os.system('clear')
progressBarz(text='Loading', max=20)
__import__('src.app')
