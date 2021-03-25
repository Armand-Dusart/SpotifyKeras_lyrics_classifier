# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:10:26 2021

@author: arman
"""
from utils.tools import * 
import pandas as pd
import sqlite3
from sql import *

def generate_data_by_genre(genius):
    dict = {'artist_name':[],'song_name':[],'tag':[]}
    bar = progress_bar(50*6)
    i=1
    for tag in ["rap", "pop", "r-b", "rock", "country", "non-music"] :
        page = 1
        while page :
            print('page :', page,'/50 for',tag )
            res = genius.tag(tag, page=page)
            try :
                dict['artist_name'] += [hit['artists'] for hit in res['hits']] 
                dict['song_name'] += [hit['title'] for hit in res['hits']] 
                dict['tag'] += [tag for i in range(len(res['hits']))]
            except :
                pass
            i+=1
            bar.update(i)
            page = res['next_page']
    df = pd.DataFrame(data=dict)
    
    #checkpoint
    df.to_csv(r'data_tag_checkpoint.csv',sep=";")
    
    lyrics = []
    bar = progress_bar(len(df))
    i=0
    for song,name in df[['song_name','artist_name']].values:
        try :
            l = genius.search_song(name[0], song)
            lyrics.append(l.lyrics)
        except :
            lyrics.append(None)
        i+=1
        bar.update(i)
    df['lyrics'] = lyrics
    return df
   

    
if __name__ == "__main__" :
    # genius = lyricsgenius.Genius(token)
    # df = generate_data_by_genre(genius)
    # df['artist_name'] = df['artist_name'].astype(str)
    # path = r'\data\MUSIC_SQL.db'
    # engine = sqlite3.connect(path)
    # df.to_sql('data_tag',con=engine,if_exists='append',index=False)
    s = SQL()
    with s.connect() as engine:
        req = "select * from data_tag"
        df = pd.read_sql(req,engine)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    