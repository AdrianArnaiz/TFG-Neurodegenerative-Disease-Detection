# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:57:46 2019

@author: Adrián
"""
from tkinter import *
import os
import tkinter
import time
from prediccion.FachadaPrediccion import FachadaPrediccion
import numpy as np
import matplotlib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class MediadorPrediccion():
    """
    Clase que implementa el mediador de la ventana. Se encarga de la comunicaciónde los elementos de VentanaInicio.
    Concretamente, esta clase actúa para los eventos de predicción y muestra de gráficas de audio.
    Tiene los metodos necesarios para el funcionamiento de esas dos tareas.
    
    author: Adrián Arnaiz
    
    Atributos
    ----------
    ventana  : VentanaInicio
        Objeto tipo la VentanaInicio que sostiene la parte gráfica
    fachadapred : FachadaPrediccion
        Contiene la lógia subyaciente a la prediccion
        
    
    """
    
    
    def __init__(self, ventana):
        """
        Constructor de la clase ventana que nos proporciona las inicializaciones de
        variables y de objetos que vana a ser encesarios para su gestion e implementacion
        de los metodos que va a contener la ventana.
        
        Parametros
        ----------
        ventana: VentanaInicio
            instancia de la clase que de la ventana inicial, la cual tiene el estilo y el tamaño ya predefinido.
        """
        
        self.ventana = ventana
        self.fachadapred = FachadaPrediccion()
        
        
    def prediccion(self):
        """
        Se encarga de sacar las ccas del audio seleccionado,
        añadirle la edad y el sexo introducidos en la pantalla,
        pasarlo a la fachada para que clasifique,
        obtener el resultado y mostrarlo por pantalla
        y mostrar ls gráficas de amplitud y frecuencia.
        
        Throws
        ----------
        ValueError: Formato de edad erroneo
        Exception: por cualquier contratiempo. Si todo el proceso de clasificacion va bien,
            entonces se debe a que no se ha seleccionado ningun audio.
        """
        
        try:
            #Cogemos audio elegido
            selected_audio = self.ventana.playlistbox.curselection()
            selected_audio = int(selected_audio[0])
            selected_audio_path = self.ventana.playlist[selected_audio]
            
            #Añadir sexo y edad
            sexo = self.ventana.sex.get()
            try:
                edad = int(self.ventana.edad.get())
                if edad <0:
                    raise ValueError("El formato de número debe ser adecuado.")
            except:
                raise ValueError("El formato de número debe ser adecuado.")     
            #Extraemos características
            ccas = self.fachadapred.extraccion_embeddings_audio(selected_audio_path)    
            ccas = np.append(ccas,sexo)
            ccas = np.append(ccas,edad)
            #Predecimos
            clase, proba = self.fachadapred.predecir_parkinson(ccas)
            proba = "%.3f" % (proba*100)
            
            #Actualizamos Textos y etiquetas de la pantalla
            self.ventana.statusbar['text'] = "AUDIO ANALIZADO:" + ' - ' + os.path.basename(selected_audio_path)
            self.ventana.predic['text'] = "Predicción de " + os.path.basename(selected_audio_path)
            res = 'Parkinson' if clase ==1 else 'Sano'
            ffg='red' if clase ==1 else 'green'
            res=res+' - Probabilidad de que el paciente tenga parkinson: '+str(proba)+'%'
            self.ventana.predicRes['text'] = 'Predicción: ' + res 
            self.ventana.predicRes['foreground'] = ffg
            
            #Dibujamos graficos            
            self.fachadapred.graficos(selected_audio_path, self.ventana)


        except ValueError as e:
            print(e)
            tkinter.messagebox.showerror('Formato de EDAD erróneo','Introduzca formato de edad válido (enteros>0)')
            
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror('Audio no selecionado', 'No hay ningun audio seleccionado.')
            
            

        
        
        