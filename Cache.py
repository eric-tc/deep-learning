#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pickle
import numpy as np

class Cache:

    def __init__(self):
        pass

    def cache_data(self,cache_path,fn,*args,**kwargs):
        """
        Se il file esiste vine caricato dalle cache
        Se il file non esiste viene chiamata la funzione
        
        :param cache_path:
         Path per il file di cache
        :param fn: 
        Funzione o classe che deve essere chiamata
        :param args: 
        Argomenti alla funzione o parametri inizializzazione classe
        :param kwargs: 
        parolechiave
        :return: 
        il risultato della funzione chiamante o crea un istanza dell'oggetto
        """

        if os.path.exists(cache_path):
            with open(cache_path,'rb') as file:
                obj= pickle.load(file)

        else:
            obj=fn(*args,**kwargs)

            with open(cache_path,'wb') as file:
                obj=pickle.dump(obj,file)


        return obj




