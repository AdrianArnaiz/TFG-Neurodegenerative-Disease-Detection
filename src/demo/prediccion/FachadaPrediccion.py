# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 09:29:38 2019

@author: Adrián
"""
import numpy as np
import prediccion.vggish_input as vggish_input
import prediccion.vggish_keras as vggish_keras
import os
import pickle
import matplotlib.pyplot as plot
from scipy.io import wavfile
from matplotlib.figure import Figure

class FachadaPrediccion:
    
    def __init__(self):
        
        #Definimos VGGish para extracción de ccas
        self.model = vggish_keras.get_vggish_keras()
        #Cargamos el checkpoint
        checkpoint_path = 'prediccion/vggish_weights.ckpt'
        self.model.load_weights(checkpoint_path)
        
        self.predictor = pickle.load(open('prediccion/MLP10_vggish_rt.sav', 'rb'))
        
    
    def extraccion_embeddings_audio(self, rutaAudio, embeddings=True):
        ''' Extraemos las características del audio. La manera por defecto es mediante
        la red VGGish. Si embeddings es false saca los espectros definidos en la 
        documentación'''
        #1. Sacamos las ccas MFCC y espectrales
        input_batch  = vggish_input.wavfile_to_examples(rutaAudio)

        #2. producimos los embbeding cn el modelo o los espectros segun se indique
        if embeddings:
            ccas = self.model.predict(input_batch[:,:,:,None])
        else:
            # "Rompemos" los grupos de 0.96s
            ccas = input_batch.reshape(-1, input_batch.shape[-1])
        
        
        #3. Hacemos media y deviación de los embbedings
        media = np.mean(ccas,axis=0)
        desvs = np.std(ccas,axis=0)
        final_ccas = np.append(media,desvs)
        
        return final_ccas
    
    def predecir_parkinson(self, ccas_audio):
        '''Predice el parkinson de las características de un audio.
           Devuelve tanto si tiene parkinos o si no, y la probabilidad de la clasificación
             es decir, la probabilidad de la clase Parkinson.'''
        ccas_audio=[ccas_audio] #Predict y predict_proba reciben un array de 2d
        clase = self.predictor.predict(ccas_audio)
        proba = self.predictor.predict_proba(ccas_audio)[0][1] #clase 1: PD

        return clase, proba
    
    def graficos(self, audio, ventana):
        '''Función encargada de realizar los gráficos de amplitud y de espectros
            de frecuencia de el audio en formato wav, cuya ruta es pasada por parámetro'''
        samplingFrequency, signalData = wavfile.read(audio)
        ventana.ax.clear()
        ventana.bx.clear()
        
        ventana.ax.title.set_text('Amplitud de la onda del audio')
        ventana.ax.set_ylabel('Amplitud')
        ventana.ax.set_xticklabels([])
        ventana.ax.plot(signalData)
        
        ventana.bx.title.set_text('Espectrograma de frecuencias')
        ventana.bx.set_ylabel('Frecuencias')
        ventana.bx.specgram(signalData,Fs=samplingFrequency)
        
        ventana.toolbar.update()
        ventana.graficos.draw()
        #self.ventana.graficos.show()
        
        
        
        
        

        
        
        