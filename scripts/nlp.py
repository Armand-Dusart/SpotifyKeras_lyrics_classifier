# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:11:17 2021

@author: arman
"""


import pandas as pd
import json
import plotly
import plotly.graph_objs as go
from collections import Counter
from random import randrange
from nltk.tokenize import  word_tokenize

class nlp(object):
    def __init__(self,df):
        self.df_v = df
        self.df_v['date'] = self.df_v['release_date'].apply(lambda x: x.split('-')[0]) 
        df_g = self.df_v.groupby('date').sum()
        counter = {}
        for date in df_g.index:
            counter[date] = Counter([word.lower() for word in  word_tokenize(df_g.loc[date,'lyrics_preprocessed']) if len(word) > 2]).most_common()
        word = []
        for date in counter:
            word.extend([w[0] for w in counter[date]])  
        self.df = pd.DataFrame(index=pd.unique(word), columns=[d for d in counter]).fillna(0)
        for d in counter:
            for val in counter[d]:
                self.df.loc[val[0],d] = val[1]




    def create_bar(self):
        graph={}   
        for date in self.df.columns:
            self.df = self.df.sort_values(by=date, ascending=False)
            data = [
                go.Bar(
                    x=[w for w in self.df[date].index[:10]], # assign x as the dataframe column 'x'
                    y=[v for v in self.df[date].values[:10]],
                    marker_color=['#5D23CF','#4823CF','#2623CF','#2344CF','#2366CF','#2385CF','#23A2CF','#23B6CF','#23CECF','#23CFBE'],
                    name="Evolution par an : "+date
                )
            ]
            graph[date] = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graph


    def create_scatter(self):
        graph={}
        
        for word in self.df.index:
            data = [
                go.Scatter(
                    x=[d for d in self.df.columns], # assign x as the dataframe column 'x'
                    y=[v for v in self.df.loc[word]],
                    mode='lines',
                    marker_color='rgb('+str(randrange(0,255))+', '+str(randrange(0,255))+', '+str(randrange(0,255))+')',                
                    name= word 
                )
            ]
            graph[word] = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graph

    

