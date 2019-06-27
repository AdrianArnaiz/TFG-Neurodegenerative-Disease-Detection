import numpy as np
from sklearn.utils import Bunch

''' 
Modulo de python que contiene las diferentes funciones de carga de datos de los espectros obtenidos con VGGish.
Todas las funciones funionan de la misma forma, solo cambia el conjunto de datos.
Son funciones que simulan en estilo de los loaders de sklearn (como load_iris en base.py)

En este módulo se cargan los espectros obtenidos con VGGish comprendiendo
    Espectros para audios de más de 0.975s:
        Espectros para frase y vocales.
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

ruta='./CaracteristicasExtraidas/vggish/espectros/'

def load_vggish_espec_rt():
    datos = np.load( ruta+'vggish_espec_rt_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_espec_v_A():
    datos = np.load( ruta+'vggish_espec_v_A_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_espec_v_E():
    datos = np.load( ruta+'vggish_espec_v_E_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_espec_v_I():
    datos = np.load( ruta+'vggish_espec_v_I_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_espec_v_O():
    datos = np.load( ruta+'vggish_espec_v_O_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


def load_vggish_espec_v_U():
    datos = np.load( ruta+'vggish_espec_v_U_ccas.npy')
    return Bunch(data=datos[:,:-1], target=datos[:,-1])


