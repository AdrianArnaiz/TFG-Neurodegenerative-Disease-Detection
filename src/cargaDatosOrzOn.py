import numpy as np
from sklearn.utils import Bunch

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


