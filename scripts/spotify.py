# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 21:08:48 2021

@author: arman
"""
import spotipy 
from spotipy.oauth2 import SpotifyOAuth 
from scripts.static_methods import *
from scripts.sql import *
import spacy 
import pandas as pd



class Spotify:
    def __init__(self,id_token,secret_token):
        uri_app = 'http://localhost:3000/'
        scope = "playlist-read-private"
        self.__sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                       client_id=id_token,
                                                       client_secret=secret_token,
                                                       redirect_uri=uri_app))

    def playlist(self,id):
        playlists = self.__sp.playlist(id,fields=['tracks'])
        list_tracks = [i['track'] for i in playlists['tracks']['items']]
        return list_tracks
    
    def artist(self,id):
        artist= id
        artist = self.__sp.search(q='artist:' + artist, type='artist')
        artist = artist['artists']['items'][0]['id']
        albums = self.__sp.artist_albums(artist,album_type='album')
        list_id_album = [al['id'] for al in albums['items']]
        list_tracks = []
        for alb in list_id_album:
            alb = self.__sp.album_tracks(alb)
            list_tracks.extend([self.__sp.track(i['id']) for i in alb['items']])
        return list_tracks, artist
    
    @staticmethod
    def processing(track,id,fr_nlp,en_nlp):
        dict = {}
        dict['name'] = track['name']
        dict['album'] = track['album']['name']
        dict['release_date'] = track['album']['release_date']
        dict['artists'] = "|".join([art['name'] for art in track['artists']])
        dict['id'] = track['id']
        dict['href'] = track['href']
        dict['uri'] = track['uri']
        dict['playlist_id'] = id
        dict['lyrics'] =  function.get_lyrics(dict['artists'].split("|")[0],track['name'].split("-")[0])
        dict['lyrics_preprocessed'] = function.preprocessing(dict['lyrics'],fr_nlp,en_nlp)
        sql = SQL()
        with sql.connect() as engine:
            cur = engine.cursor()
            cur.execute('INSERT INTO musiques (name, album, release_date, artists, id, href, uri, playlist_id, lyrics, lyrics_preprocessed) VALUES (:name, :album, :release_date, :artists, :id, :href, :uri, :playlist_id, :lyrics, :lyrics_preprocessed);', dict)
        
    
    
    @staticmethod    
    def playlist_sql(id):
        req = "select * from musiques where playlist_id = '%s'" %id
        sql = SQL()
        with sql.connect() as engine:
            df = pd.read_sql(req,engine)
            df = df.drop_duplicates(subset=['name', 'artists'])
            df = df.dropna()
        return df
 

    @staticmethod
    def generator(play,id,fr_nlp,en_nlp):
        for i in range(len(play)):
            Spotify.processing(play[i], id, fr_nlp, en_nlp)
            yield i
        
    


# if __name__ == "__main__":
#     id = "https://open.spotify.com/playlist/6WUuFEQsXqkbBLn4MjHLLf?si=2d915ee7bf634f4c"
#     secret_token= "2b92db3122a943fb992bdf9e496b42d1"
#     id_token ="04d7777a9aad4c6d93731ad08fff2811"
#     fr_nlp = spacy.load('fr_core_news_md')
#     en_nlp = spacy.load('en_core_web_md')
#     print("model loaded")
    
#     spotify = Spotify(id_token,secret_token)
    
#     artist, id = spotify.artist("qalf")
    

    

    
    
    
   
    
    
    