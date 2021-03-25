# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 21:09:54 2021

@author: arman
"""

from os import getcwd
import sqlite3 as sq
import pandas as pd
from contextlib import contextmanager 

class SQL(object):
    def __init__(self):
        self.path = getcwd() + "/data/MUSIC_SQL.db"
        
    @contextmanager
    def connect(self):
        try :
            engine = sq.connect(self.path)
            yield engine
        except PermissionError:
            print("can't access to DB")
        except :
            print("Error Connexion to "+self.path)
        finally: 
            engine.commit()
            engine.close()   

        

        
# if __name__ == "__main__":
#     sql = SQL()

#     with sql.connect() as sql_c:
#         req = "select * from musiques"
#         df = pd.read_sql(req,sql_c)
     
 
        
  
      
        
    
 
    
    
    
    