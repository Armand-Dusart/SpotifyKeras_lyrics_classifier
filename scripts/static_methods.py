# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:40:57 2021

@author: arman
"""

from langdetect import detect
import spacy
from nltk.corpus import stopwords
import pandas as pd
import re
import lyricsgenius

class function(object):
    @staticmethod
    def preprocessing(lyric,fr_nlp,en_nlp):
        if lyric == "" or lyric ==None or type(lyric) != str:
            return None
        lang = detect(lyric)
        lyric = [line for line in lyric.split("\n") if line !='']
        lyric = pd.Series(filter(lambda x : '[' not in x, lyric))
        lyric = [re.sub("\W+"," ",line) for line in lyric]
        lyric = [re.sub("\d+","",line) for line in lyric]
        lyric = " ".join(lyric)
        if lang == 'fr' :
            doc = fr_nlp(lyric)
            stop_words = stopwords.words('french') + ['être','avoir','faire']
            lyric_lem = " ".join([token.lemma_ for token in doc if token.lemma_ not in stop_words]) 
        elif lang == 'en':
            doc = en_nlp(lyric)
            stop_words = stopwords.words('english') + ['i','p','a']
            lyric_lem = " ".join([token.lemma_ for token in doc if token.lemma_ not in stop_words]) 
        else :
            print("Analyse impossible la langue de la musique est autre que le français ou l'anglais :",lang)
            lyric_lem = None
        lyric_lem = lyric_lem.replace('   ',' ').replace('  ',' ').strip()
        return lyric_lem
    
    @staticmethod
    def get_lyrics(artist_name,music_name):
        token = "R1PUL90yUKiH6UEJojWlZ12nxtMdBRSWjoET7Q4got0JN-U44wtD9BeTNFP0tsz0"
        genius = lyricsgenius.Genius(token)
        try:
            l = genius.search_song(music_name,artist_name)
            return l.lyrics
        except : return None
     
    

    