import numpy as np
from sklearn.utils import Bunch

ruta='./CaracteristicasExtraidas/vggish/embbedings/'

def load_vggish_embed_rt():
    datos = np.load( ruta+'vggish_embed_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_embed_v_A():
    datos = np.load( ruta+'vggish_embed_v_A_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_embed_v_E():
    datos = np.load( ruta+'vggish_embed_v_E_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_embed_v_I():
    datos = np.load( ruta+'vggish_embed_v_I_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_embed_v_O():
    datos = np.load( ruta+'vggish_embed_v_O_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_embed_v_U():
    datos = np.load( ruta+'vggish_embed_v_U_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


