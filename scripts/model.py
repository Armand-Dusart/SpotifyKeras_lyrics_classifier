# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 16:11:03 2021

@author: arman
"""

import keras
from os import getcwd
import pandas as pd
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import re
from keras.preprocessing.sequence import pad_sequences
from pickle import dump,load
import numpy as np
from collections import Counter
import plotly
import plotly.graph_objs as go
import json


class model():
    def __init__(self):
        self.stop_words = stopwords.words('english') + stopwords.words('french')
        path = getcwd()
        with open(path+'/model/tekonizer.pickle', 'rb') as file:
            self.tokenizer = load(file)
        path = path+"/model/lstm"
        self.model = keras.models.load_model(path)
        
    def stop_word_delete(self,lyric):
      return " ".join([word for word in lyric.split(" ") if word not in self.stop_words])


    def preprocessing_model(self,lyric):
      lyric = [line for line in lyric.split("\n") if line !='']
      lyric = pd.Series(filter(lambda x : '[' not in x, lyric))
      lyric = [re.sub("\d+","",line.lower()) for line in lyric]
      lyric = " ".join([re.sub("\"","",line.lower()) for line in lyric])
      return lyric



    def predict_genre(self,lyric):
        lyric = self.preprocessing_model(lyric)
        lyric = self.stop_word_delete(lyric)
        list_lyrics = [sent for sent in sent_tokenize(lyric) if len(sent) > 10] 
        predict = []
        for l in list_lyrics :
          l = [l]
          seq = self.tokenizer.texts_to_sequences(l)
          padded = pad_sequences(seq, maxlen=70)
          pred = self.model.predict(padded)
          labels = np.array(['rap','pop','r-b','rock'])
          predict.append(labels[np.argmax(pred)])
        return predict
    
    
    def predict(self,df):
        predict_list=[]
        for lyric in df['lyrics']:
            predict_list.extend(self.predict_genre(lyric))
        counter = Counter(predict_list).most_common()
        data = [
            go.Bar(
                x=[w[0] for w in counter], # assign x as the dataframe column 'x'
                y=[w[1] for w in counter],
                marker_color=['#5D23CF','#4823CF','#2623CF','#2344CF'],
                name="Prediction du genre musical"
            )
        ]

        graph = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graph
    
 
          
          
          
          
          
          
          
          
          
          
          
          