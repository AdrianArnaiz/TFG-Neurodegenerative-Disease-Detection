import numpy as np
from sklearn.utils import Bunch


''' 
Modulo de python que contiene las diferentes funciones de carga de datos DE LOS HOMBRES.
Todas las funciones funionan de la misma forma, solo cambia el conjunto de datos.
Son funciones que simulan en estilo de los loaders de sklearn (como load_iris en base.py)

En este módulo se cargan las características de disvoice UNA VEZ AÑADIDA EDAD Y SEPARADO POR SEXO comprendiendo
    Las características de fonacion para vocales, frase y palabras.
    Las características de articulacion para frase y pàlabras.
    Las características de prosodia para la frase.
    Las características de MFCC en offset para frase y vocales.
    Las características de MFCC en onset para frase y vocales.
    30 en total

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

ruta='./CaracteristicasExtraidas/DivisionSexo/hombres/'

def load_art_rt():
    datos = np.load(ruta+'art_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_rt_ofset():
    datos = np.load(ruta+'art_rt_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_rt_onset():
    datos = np.load(ruta+'art_rt_onset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_atleta():
    datos = np.load(ruta+'art_w_atleta_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_atleta_ofset():
    datos = np.load(ruta+'art_w_atleta_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_atleta_onset():
    datos = np.load(ruta+'art_w_atleta_onset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_braso():
    datos = np.load(ruta+'art_w_braso_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_braso_ofset():
    datos = np.load(ruta+'art_w_braso_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_braso_onset():
    datos = np.load(ruta+'art_w_braso_onset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_campana():
    datos = np.load(ruta+'art_w_campana_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_campana_ofset():
    datos = np.load(ruta+'art_w_campana_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_campana_onset():
    datos = np.load(ruta+'art_w_campana_onset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_gato():
    datos = np.load(ruta+'art_w_gato_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_gato_ofset():
    datos = np.load(ruta+'art_w_gato_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_gato_onset():
    datos = np.load(ruta+'art_w_gato_onset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_petaka():
    datos = np.load(ruta+'art_w_petaka_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_petaka_ofset():
    datos = np.load(ruta+'art_w_petaka_ofset_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_art_w_petaka_onset():
    datos = np.load(ruta+'art_w_petaka_onset_ccas.npy')
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


