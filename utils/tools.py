# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:24:32 2021

@author: arman
"""


from IPython import get_ipython
import pandas as pd

def clear():
    get_ipython().magic('clear')
 
def table(df,by,columns,function):
   if type(by) != list or type(columns) != list :
       print("By and Colmuns need to be a list")
   elif len(by) != 1 :
       print('By needs to be 1 col not several')
   elif False in [True for col in columns+by if col in df.columns]+[False for col in columns+by if col not in df.columns] or type(df) != pd.core.frame.DataFrame:
       print("Value not in columns or df not a DataFrame")
   else:
       try :
           if function == "sum" :
               return df.groupby(by=by).sum()[columns]
           elif function == "mean" :
               return df.groupby(by=by).mean()[columns]
       except KeyError:
           print("Values need to be integer or float")
       




class progress_bar():
    def __init__(self,liste):
        self.pourcentage = -1
        if type(liste) != int :
            self.liste = list(liste)
            self.type = 'liste'
        else :
            self.liste = liste
            self.type = 'int'
        
    def update(self,i):
        if self.type != "int" :
            i = int(self.liste.index(i))
            pourcentage_temps = round((i/len(self.liste))*100)
            if self.pourcentage != pourcentage_temps :
                self.pourcentage = pourcentage_temps
                print(self.pourcentage,"%")
        else:
            pourcentage_temps = round((i/self.liste)*100)
            if self.pourcentage != pourcentage_temps :
                self.pourcentage = pourcentage_temps
                print(self.pourcentage,"%")
                
