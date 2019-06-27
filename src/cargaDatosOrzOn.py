import numpy as np
from sklearn.utils import Bunch

''' 
Modulo de python que contiene las diferentes funciones de carga de datos de las características exactas de orozco en onset.
Todas las funciones funionan de la misma forma, solo cambia el conjunto de datos.
Son funciones que simulan en estilo de los loaders de sklearn (como load_iris en base.py)

En este módulo se cargan las características de disvoice UNA VEZ EXTRAÍDO LAS CCAS ONSET comprendiendo
    Las características de MFCC en onset para frase y vocales.
    6 en total

Atributos
---------
ruta:str
    parametro global al módulo con la ruta en la que encontrar los archivos de características.
    
    
Return de cada funcion
----------------------
Objeto tipo Bunch con 2 elementos
    data: contiene los datos del dataset (sin targets)
    target: la clase de los datos anteriores
''' 

ruta='./CaracteristicasExtraidas/Orozco2016/onset/'

def load_art_rt():
    datos = np.load(ruta+'art_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_atleta():
    datos = np.load(ruta+'art_w_atleta_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_braso():
    datos = np.load(ruta+'art_w_braso_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_campana():
    datos = np.load(ruta+'art_w_campana_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_gato():
    datos = np.load(ruta+'art_w_gato_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_petaka():
    datos = np.load(ruta+'art_w_petaka_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


