# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:52:54 2021

@author: arman
"""


from .sql import *
from .spotify import *
from .static_methods import *
from .nlp import *
from .model import *
import spacy

try :
    fr_nlp = spacy.load('fr_core_news_md')
    en_nlp = spacy.load('en_core_web_md')
    secret_token= "your_secret_token"
    id_token ="your_id_token"
except :
    print('Do this cmd')
    print('python -m spacy fr_core_news_md')
    print('python -m spacy en_core_web_md')

if secret_token=="" or id_token=="":
    print('No spotify token')
    print('check __init__.py')


import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(package, 'import')
    

    
install('langdetect')  
install('spotipy') 
install('lyricsgenius') 
install('plotly') 
  
model = model()

print('init')