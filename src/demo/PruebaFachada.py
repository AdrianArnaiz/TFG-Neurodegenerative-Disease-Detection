# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:15:37 2019

@author: Adrián
"""
import unittest
from prediccion.FachadaPrediccion import *
import numpy as np

class TestFachada(unittest.TestCase):
    ''' Clase de test para la fachada. Nos basaremos en que tenemos un audio del que sabemos
    y tenemos guardados todos los datos: embeddings, espectros, edad, sexo, clase y probabilidad.
    Probaremos a ver si nos devuelve los datos que ya sabemos.'''
        
    
    def test_extraccion_embd(self):
        ''' Guardamos el objeto fachada prediccion para utilizar sus métodos 
        y la ruta de un audio de ejemplo del que sabemos cual son sus embeddings.
        Comprobamos que son iguales que las guardadas, que sabemos cuales son de manera previa'''
        fachada = FachadaPrediccion()
        audio = 'AVPEPUDEAC0006_readtext.wav'
        ccas = fachada.extraccion_embeddings_audio(audio , embeddings=True)
        self.assertTrue(np.equal(np.load('ccas_test.npy'),ccas).all())
        self.assertTrue(np.equal(256,ccas.shape[0]))
        
    def test_extraccion_espec(self):
        ''' Guardamos el objeto fachada prediccion para utilizar sus métodos 
        y la ruta de un audio de ejemplo del que sabemos cual son sus espectros.
        Comprobamos que son iguales que las guardadas, que sabemos cuales son de manera previa'''
        fachada = FachadaPrediccion()
        audio = 'AVPEPUDEAC0006_readtext.wav'
        ccas = fachada.extraccion_embeddings_audio(audio , embeddings=False)
        self.assertTrue(np.equal(np.load('espec_test.npy'),ccas).all())
        self.assertTrue(np.equal(128,ccas.shape[0]))
        
    def test_predecir(self):
        ''' Hacemos el proceso de prediccion de un audio del que sabemos cual son su probabilidad y clase.
        Evidentemente, tambien sabemos los datos de edad y sexo.'''
        fachada = FachadaPrediccion()
        audio = 'AVPEPUDEAC0006_readtext.wav'
        ccas = fachada.extraccion_embeddings_audio(audio , embeddings=True)
        ccas = np.append(ccas,1)
        ccas = np.append(ccas, 55)
        cl, pr = fachada.predecir_parkinson(ccas)

        self.assertTrue(np.equal(0,cl))
        self.assertTrue(np.isclose(pr,0.341, rtol=0.005))
        

            
            
if __name__=="__main__":

    unittest.main()