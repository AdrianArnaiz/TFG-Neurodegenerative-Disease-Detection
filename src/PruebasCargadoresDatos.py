# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:11:19 2019

@author: Adrián
"""

import unittest
import os
import importlib
import numpy as np

class TestCargaDatos(unittest.TestCase):
    '''
    Clase que testea los módulos de carga de datos.

    Atributos
    ----------
    ruta: str
        ruta de las caracteristicas del modulo.
    modulo: modulo de python
        modulo que contiene las funciones de carga de datos.
    '''
    
    def __init__(self, path, modu):
        ''' Recibimos la ruta de las características y el módulo a cargar
        
        Devuelve la información general del experimento, el cual se ha pasado como diccionario
        y contiene mucha información.

        Parametros
        ----------
        path: str
            ruta de las caracteristicas del modulo.
        modu: modulo de python
            modulo que contiene las funciones de carga de datos.
        '''
        self.ruta = path
        self.modulo = modu
    
    def test_datos(self):
        '''Comprobamos que el archivo numpy que nos devuelve la función es igual
        a el archivo numpy que cargamos nosotros directamente y que sabemos que es 
        el correcto (así se comprueban intrínsecamente valores y dimensiones).
        '''
             
        t = os.listdir(self.ruta)
        sets = [s for s in t if s.endswith('.npy')]
        for cca in sets:
            datosCarpeta = np.load(self.ruta+cca)
            loader = getattr(self.modulo,'load_'+cca[:-9])
            self.assertTrue(np.equal(loader().data, datosCarpeta[:,:-1]).all())
            self.assertTrue(np.equal(loader().target, datosCarpeta[:,-1]).all())
            print('✓ - '+'load_'+cca[:-9]+'()'+' OK')
            
            
if __name__=="__main__":
    ''' Se recorrerán todos los módulos de carga de datos para comprobar que pasan
    el tes de la clase de arriba. Para ello recorremos para cada uno la estructura 
    donde están su conjunto de características. En caso de que no pase el test,
    significará que o la función trabaja mal, o la función no encuentra el archivo.
    No hace falta identificarlo ya que la propia excepciónd e python nos indica cual
    de los dos fallos indicados es.'''
    modulos=list()
    rutas = list()
    #usadas en notebook 1
    modulos.append('cargaDatos')
    rutas.append('./CaracteristicasExtraidas/')
    #usadas en notebook 2a
    modulos.append('cargaDatosEdSx')
    rutas.append('./CaracteristicasExtraidas/EdadYSexo/')
    #usadas en notebook 2b
    modulos.append('cargaDatosHombres')
    rutas.append('./CaracteristicasExtraidas/DivisionSexo/hombres/')
    #usadas en notebook 2c
    modulos.append('cargaDatosMujeres')
    rutas.append('./CaracteristicasExtraidas/DivisionSexo/mujeres/')
    #usadas en notebook 3a
    modulos.append('cargaDatosVggishEmbeddings')
    rutas.append('./CaracteristicasExtraidas/vggish/embbedings/')
    #usadas en notebook 3b
    modulos.append('cargaDatosVggishEspectros')
    rutas.append('./CaracteristicasExtraidas/vggish/espectros/')

    resumen = dict()
    datos = zip(modulos,rutas)
    for mod, ruta in datos:
        print('-------------')
        print(mod)
        print(ruta)
        modulo = importlib.import_module(mod)
        tst = TestCargaDatos(ruta, modulo)
        tst.test_datos()
        resumen[mod]=True

    print('-------------')
    print(resumen)
        
        