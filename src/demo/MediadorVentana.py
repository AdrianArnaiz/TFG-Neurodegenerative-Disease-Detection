# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:54:36 2019

@author: Adrián
"""

import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as thtk

from mutagen.mp3 import MP3
from pygame import mixer

class MediadorVentana():
    """
    Clase que implementa el mediador de la ventana. Se encarga de la comunicaciónde los elementos de VentanaInicio.
    Concretamente, esta clase actúa para los eventos de carga de audios y reproducción de audios.
    Tiene los metodos necesarios para el funcionamiento de esas dos tareas.
    
    author: Adrián Arnaiz
    
    Atributos
    ----------
    ventana  : VentanaInicio
        Objeto tipo la VentanaInicio que sostiene la parte gráfica

    """
    
    
    def __init__(self, ventana):
        """
        Constructor de la clase ventana que nos proporciona las inicializaciones de
        variables y de objetos que vana a ser encesarios para su gestion e implementacion
        de los metodos que va a contener la ventana.
        
        Parametros
        ----------
        ventana: VentanaInicio
            instancia de la clase que crea la ventana, la cual tiene el estilo y el tamaño ya predefinido.
        """
        
        self.ventana = ventana
        
    
    def browse_file(self):
        """
        Encargada de las funciones para cargar un archivo cuando se clicka en el boton añadir.
        Despliega menú de búsqueda de archivos y perimte la inserccion de varios, siempre tipo wav.
        
        """
        filename_paths = filedialog.askopenfilenames(initialdir = "./",title = "Selecciona archivo",filetypes = (("wav","*.wav"),("all files","*.*")))
        
        if len(filename_paths)>0:
            for filename_path in filename_paths:
                self.add_to_playlist(filename_path)
                mixer.music.queue(filename_path)
        
    
    def add_to_playlist(self,filename):
        """
        Añade la ruta del audio a la playlist para reproducir y a la playlistbox para mostrarla.
        
        Parametros
        ----------
        filename: str
            ruta del audio.
        """
        filename2 = os.path.basename(filename)
        self.ventana.playlistbox.insert(self.ventana.index, filename2)
        self.ventana.playlist.insert(self.ventana.index, filename)
        self.ventana.index += 1
    

    def about_us(self):
        """
        Muestra mensaje de información cuando se clika a about us en Help en el menú.

        """
        tkinter.messagebox.showinfo('Sobre PDD', 'Trabajo de Fin de Grado.\n Alumno: Adrián Arnaiz\n Tutores: Jose Francisco Díez Pastor, Cesar Ignacio García-Osorio')
    

    def del_song(self):
        """
        Borra la ruta del audio clickado en la lista de la playlist de reprodución 
        y de la playlistbox para no mostrarla.

        """
        selected_song = self.ventana.playlistbox.curselection()
        selected_song = int(selected_song[0])
        self.ventana.playlistbox.delete(selected_song)
        self.ventana.playlist.pop(selected_song) 
    
    
    def show_details(self,play_song):
        """
        Muestra la duración total del audio y va mostrando el contador de segundos de reproduccion en tiempo real.
        Para ello se utiza un hilo, para que se vaya actualizando el valor actual del Current Time.
        
        Parametros
        ----------
        play_song: str
            ruta del audio.
        """
        file_data = os.path.splitext(play_song)
    
        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()
    
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.ventana.lengthlabel['text'] = "Duración Total" + ' - ' + timeformat
    
        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()
    
    
    def start_count(self,t):
        """
        Va mostrando el contador de segundos de reproduccion en tiempo real.
        
        Parametros
        ----------
        t: int
            tiempo total de la cancion.
        """
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and mixer.music.get_busy():
            if self.ventana.paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.ventana.currenttimelabel['text'] = "Tiempo Actual " + ' - ' + timeformat
                time.sleep(1)
                current_time += 1
    
    def play_music(self):
        """
        Reacciona a los eventos listener del boton play.
        Si está pausado: lo reanuda.
        Si estaba parado porque no habia nada reproduciendo, empieza a reproducir.
        Muestra los datos de la reproducción y texto informativo en la pantalla.
        """
        if self.ventana.paused:
            mixer.music.unpause()
            self.ventana.statusbar['text'] = "Reproduciendo audio"
            self.ventana.paused = FALSE
        else:
            try:
                self.stop_music()
                time.sleep(1) 
                selected_song = self.ventana.playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_it = self.ventana.playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                self.ventana.statusbar['text'] = "Reproduciendo audio " + ' - ' + os.path.basename(play_it)
                self.show_details(play_it)
            except Exception as e:
                print(e)
                tkinter.messagebox.showerror('Audio no selecionado', 'No hay ningun audio seleccionado.')
    
    
    def stop_music(self):
        """
        Reacciona a los eventos listener del boton stop.
        Para la música.
        Muestra texto informativo en la pantalla.
        """
        mixer.music.stop()
        self.ventana.statusbar['text'] = "Audio parado"
    

    def pause_music(self):
        """
        Reacciona a los eventos listener del boton pause.
        Pausa la música.
        Muestra texto informativo en la pantalla.
        """
        self.ventana.paused = TRUE
        mixer.music.pause()
        self.ventana.statusbar['text'] = "Audio pausado"
    
    
    def rewind_music(self):
        """
        Reacciona a los eventos listener del boton rewind.
        Rebobina la música.
        Muestra texto informativo en la pantalla.
        """
        self.play_music()
        self.ventana.statusbar['text'] = "Audio rebobinadio"
    
    
    def set_vol(self,val):
        """
        Reacciona a los eventos listener del deslizador de volumen.
        Cambia el volumen de la música.
        
        Parametros
        ----------
        val:int
            porcentaje de volumen sobre 100.
        """
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1
    

    def mute_music(self):
        """
        Reacciona a los eventos listener del boton mute.
        Quita el sonido al audio.
        Muestra imagen informativa en la pantalla.
        """
        if self.ventana.muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            self.ventana.volumeBtn.configure(image=self.ventana.volumePhoto)
            self.ventana.scale.set(70)
            self.ventana.muted = FALSE
        else:  # mute the music
            mixer.music.set_volume(0)
            self.ventana.volumeBtn.configure(image=self.ventana.mutePhoto)
            self.ventana.scale.set(0)
            self.ventana.muted = TRUE
    

    def on_closing(self):
        """
        Configura la salida de la aplicación.
        Para la música y 'mata' la ventana.
        """
        self.stop_music()
        self.ventana.root.destroy()
