import numpy as np
from sklearn.utils import Bunch
    
ruta='./CaracteristicasExtraidas/'

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

def load_fon_rt():
    datos = np.load(ruta+'fon_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_v_A():
    datos = np.load(ruta+'fon_v_A_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_v_E():
    datos = np.load(ruta+'fon_v_E_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_v_I():
    datos = np.load(ruta+'fon_v_I_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_v_O():
    datos = np.load(ruta+'fon_v_O_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_v_U():
    datos = np.load(ruta+'fon_v_U_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_w_atleta():
    datos = np.load(ruta+'fon_w_atleta_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_w_braso():
    datos = np.load(ruta+'fon_w_braso_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_w_campana():
    datos = np.load(ruta+'fon_w_campana_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_w_gato():
    datos = np.load(ruta+'fon_w_gato_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_fon_w_petaka():
    datos = np.load(ruta+'fon_w_petaka_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])

def load_prs_rt():
    datos = np.load(ruta+'prs_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])