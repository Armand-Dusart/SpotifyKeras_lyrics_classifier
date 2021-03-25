# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 22:51:50 2021

@author: arman
"""

from flask import *
from os import getcwd
import spacy 
from scripts import *
from time import sleep


TEMPLATE_DIR =  getcwd() + '/templates'
STATIC_DIR =  getcwd()+'/static'

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api')
def API():
    return render_template('api.html')

@app.route('/application')
def application():
    return render_template('application.html')


@app.route('/application/playlist', methods=['GET'])
def playlist_app():
    id = request.args.get('url')
    p = Spotify.playlist_sql(id)
    if p.shape[0] < 1 :
        try :
            sp = Spotify(id_token,secret_token)
            play = sp.playlist(id)
        except :
            return redirect("http://localhost:3000/application")
        gen = sp.generator(play,id,fr_nlp,en_nlp)
        [i for i in gen]
    p = Spotify.playlist_sql(id)

    g = nlp(p)
    graph_bar = g.create_bar()
    graph_scatter = g.create_scatter()
    
    return render_template('playlist.html',len=max(p.index),playlist=p,id=id,bar=graph_bar,scatter=graph_scatter)

@app.route('/application/artist', methods=['GET'])
def artist_app():
    nom = request.args.get('nom')
    spotify = Spotify(id_token,secret_token)
    try :
        list_tracks, id = spotify.artist(str(nom))
        if len(list_tracks) == 0:
            return redirect("http://localhost:3000/application")
        p = Spotify.playlist_sql(id)
        if p.shape[0] < 1 :
            gen = spotify.generator(list_tracks,id,fr_nlp,en_nlp)
            [i for i in gen]
    except :
        return redirect("http://localhost:3000/application")
    p = Spotify.playlist_sql(id)
    
    g = nlp(p)
    graph_bar = g.create_bar()
    graph_scatter = g.create_scatter()
    
    predict_graph = model.predict(p)
    
    return render_template('artist.html',len=max(p.index),playlist=p,id=id,bar=graph_bar,scatter=graph_scatter,predict_graph=predict_graph)
    

if __name__ == '__main__':
    print(TEMPLATE_DIR)
    app.run(debug=True,port=3000) 


    
    
      