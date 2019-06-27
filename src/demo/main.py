from tkinter import ttk
from ttkthemes import themed_tk as thtk
from tkinter import font  as tkfont 
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk

from MediadorVentana import MediadorVentana
from MediadorPrediccion import MediadorPrediccion

import matplotlib
#matplotlib.use("TkAgg")
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg as NavigationToolbar2Tk
except:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class VentanaInicio(object):
   
    
    ''' Clase encargada de definir y sostener todos los elementos gráficos de la aplicación, así como también los listener.
    Tiene toda la estructura de frames, botones, texto y gráficos.
    Únicamente tiene el cosntructor, donde inicializamos los objetos gráficos y listeners.
    
    Código base del reproductor de música: https://github.com/attreyabhatt/Python-Music-Player
    
    author: Adrián Arnaiz
    
    Atributos
    ----------
    //Atributos más importantes para el funcionamiento
    root  : ThemedTk
    mediadorVen : MediadorVentana
    mediadorPred :  MediadorPrediccion
    playlist : List
    index : int
    sex : int
    edad : Entry
    graficos : FigureCanvasTkAgg
    
    //Labels de texto y botones
    statusbar : Label
    menubar : Menu
    audioscargados : Label
    playlistbox : Listbox
    addBtn : Button
    delBtn : Button
    lengthlabel : Label
    currenttimelabel : Label
    paused : Boolean
    muted : Boolean
    playBtn : Button
    stopBtn : Button
    pauseBtn : Button
    predictBtn : Button
    predicRes : Label
    rewindBtn : Button
    rewindBtn : Button
    
    //frames para estructurar la salida por pantalla
    LeftFrame : Frame
    LeftUpFrame : Frame
    LeftDwFrame : Frame
    topframe : Frame
    middleframe : Frame
    bottomframe : Frame
    RightFrame : Frame
    RightupFrame : Frame
    RightdowFrame : Frame
    LeftFrame : Frame
        
        
    '''
    
    
    def __init__(self):
        #Se inicializan todos los menús y elementos para la carga y reproducción de audios
        
        self.root = thtk.ThemedTk()
        self.root.get_themes()                 # Returns a list of all themes that can be set
        self.root.set_theme("radiance")         # Sets an available theme
        self.root.geometry('1366x768')
        self.root.state('zoomed')
        self.root.resizable(0, 0) #Don't allow resizing in the x or y direction
        
        self.mediadorVen = MediadorVentana(self)
        self.mediadorPred = MediadorPrediccion(self)
        
        # Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
        # MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
        #
        # Styles - normal, bold, roman, italic, underline, and overstrike.
        
        self.statusbar = ttk.Label(self.root, text="Bienvenido a Parkinson Disease Detection", relief=SUNKEN, anchor=W, font='Times 10 italic')
        self.statusbar.pack(side=BOTTOM, fill=X)
        
        # Create the menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Create the submenu
        
        subMenu = Menu(self.menubar, tearoff=0)
        
        
        # playlist - contains the full path + filename
        # playlistbox - contains just the filename
        # Fullpath + filename is required to play the music inside play_music load function
        self.playlist = []
        
        
        self.menubar.add_cascade(label="Archivo", menu=subMenu)
        subMenu.add_command(label="Abrir", command=self.mediadorVen.browse_file)
        subMenu.add_command(label="Salir", command=self.mediadorVen.on_closing)
        
        
        subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ayuda", menu=subMenu)
        subMenu.add_command(label="Sobre PDD", command=self.mediadorVen.about_us)
        
        mixer.init()  # initializing the mixer
        
        self.root.title("Parkinon Disease Detection")
        self.root.iconbitmap(r'images/voice.ico')
        
        # 1Root Window - 1.1StatusBar, 1.2LeftUpFrame, 1.3LeftDwFrame
        # 1.2LeftUpFrame - 1.2.1The listbox (playlist) 1.2.2Botones add y delete
        # 1.3LeftDwFrame - 1.3.1TopFrame,1.3.2MiddleFrame and the 1.3.3BottomFrame
        
        #1.2
        self.LeftFrame = Frame(self.root)
        self.LeftFrame.pack(side=LEFT, fill=Y, padx=0,pady=30)#pack(side=LEFT, padx=30padx=30,)
        
        
        self.LeftUpFrame = Frame(self.LeftFrame)
        self.LeftUpFrame.pack(side=TOP, fill=Y)
        #1.2.1
        self.audioscargados = ttk.Label(self.LeftUpFrame, text='Audios cargados:')
        self.audioscargados.pack()
        self.playlistbox = Listbox(self.LeftUpFrame, relief=RAISED, width=30, height=15)
        self.playlistbox.pack(side=TOP)
        self.index = 0 #iniciamos el indice que se usará en la lista
        #1.2.2
        self.addBtn = ttk.Button(self.LeftUpFrame, text="+ Añadir", command=self.mediadorVen.browse_file)
        self.addBtn.pack(side=TOP)    
        self.delBtn = ttk.Button(self.LeftUpFrame, text="- Borrar", command=self.mediadorVen.del_song)
        self.delBtn.pack(side=TOP)
        
        
        
    
        #1.3
        self.LeftDwFrame = Frame(self.LeftFrame)
        self.LeftDwFrame.pack(side=TOP, fill=Y)#.pack(pady=30)
        #1.3.1
        self.topframe = Frame(self.LeftDwFrame)
        self.topframe.pack()
        
        self.lengthlabel = ttk.Label(self.topframe, text='Duración Total : --:--')
        self.lengthlabel.pack(pady=5)
        
        self.currenttimelabel = ttk.Label(self.topframe, text='Tiempo actual : --:--', relief=GROOVE)
        self.currenttimelabel.pack()
        
        self.paused = FALSE
        
        self.muted = FALSE
        
        
        #1.3.2
        self.middleframe = Frame(self.LeftDwFrame)
        self.middleframe.pack(pady=30, padx=30, fill=Y)
        

        self.playPhoto = PhotoImage(file='images/play.png')
		
        self.playBtn = ttk.Button(self.middleframe, image=self.playPhoto, command=self.mediadorVen.play_music)
        self.playBtn.grid(row=0, column=0, padx=10)
        
        self.stopPhoto = PhotoImage(file='images/stop.png')
        self.stopBtn = ttk.Button(self.middleframe, image=self.stopPhoto, command=self.mediadorVen.stop_music)
        self.stopBtn.grid(row=0, column=1, padx=10)
        
        self.pausePhoto = PhotoImage(file='images/pause.png')
        self.pauseBtn = ttk.Button(self.middleframe, image=self.pausePhoto, command=self.mediadorVen.pause_music)
        self.pauseBtn.grid(row=0, column=2, padx=10)
        
        
        
        # Bottom Frame for volume, rewind, mute etc.
        #1.3
        self.bottomframe = Frame(self.LeftDwFrame)
        self.bottomframe.pack(fill=Y)
        
        self.rewindPhoto = PhotoImage(file='images/rewind.png')
        self.rewindBtn = ttk.Button(self.bottomframe, image=self.rewindPhoto, command=self.mediadorVen.rewind_music)
        self.rewindBtn.grid(row=0, column=0)
        
        self.mutePhoto = PhotoImage(file='images/mute.png')
        self.volumePhoto = PhotoImage(file='images/volume.png')
        self.volumeBtn = ttk.Button(self.bottomframe, image=self.volumePhoto, command=self.mediadorVen.mute_music)
        self.volumeBtn.grid(row=0, column=1)
        
        self.scale = ttk.Scale(self.bottomframe, from_=0, to=100, orient=HORIZONTAL, command=self.mediadorVen.set_vol)
        self.scale.set(70)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.7)
        self.scale.grid(row=0, column=2, pady=15, padx=30)
        
        
        #Añadimos la interfaz de la clasificación: texto y Gráfica
        self.RightFrame = Frame(self.root)
        self.RightFrame.pack(side=TOP, anchor=N, fill=X, expand=YES)
        
        self.RightupFrame = Frame(self.RightFrame)
        self.RightupFrame.pack(side=TOP, fill=X)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.predic = ttk.Label(self.RightupFrame, text='Predicción del audio', font=self.title_font)
        self.predic.pack(pady=20)
        #Sexo
        self.sex = IntVar()
        ttk.Radiobutton(self.RightupFrame, text="Hombre", variable=self.sex, value=0).pack(side=TOP)
        ttk.Radiobutton(self.RightupFrame, text="Mujer", variable=self.sex, value=1).pack(side=TOP)
        #Edad
        ttk.Label(self.RightupFrame, text='Edad: ').pack(pady=2) 
        self.edad = ttk.Entry(self.RightupFrame)
        self.edad.pack()
        #Boton para predecir
        self.predictBtn = ttk.Button(self.RightupFrame, text='Predecir audio seleccionado', command=self.mediadorPred.prediccion)
        self.predictBtn.pack(pady=5)
        #Resultado de la prediccion
        self.predicRes = ttk.Label(self.RightupFrame, text='Predicción: --', 
                                font=tkfont.Font(family='Helvetica', size=14, slant="italic"))
        self.predicRes.pack(pady=20)
              
        #El Frame para los gráficos
        self.RightdowFrame = Frame(self.RightFrame)
        self.RightdowFrame.pack(pady=5)
        #Gráfico de ejemplo
        self.f = Figure(figsize=(60,30))
        self.ax = self.f.add_subplot(211)
        self.ax.title.set_text('Amplitud de la onda del audio')
        self.ax.plot([1,2,3,4,5,6,7,8],[0,0,0,0,0,0,0,0])
        self.ax.set_ylabel('Amplitud')
        self.ax.set_xticklabels([])
        self.bx = self.f.add_subplot(212)
        self.bx.title.set_text('Espectrograma de frecuencias')
        self.bx.set_ylabel('Frecuencias')
        self.bx.plot([1,2,3,4,5,6,7,8],[0,0,0,0,0,0,0,0])
        #Canvas para el grafico
        self.graficos = FigureCanvasTkAgg(self.f, self.RightdowFrame)
        #Barra de navegacion del grafico
        self.toolbar = NavigationToolbar2Tk(self.graficos, self.RightdowFrame)
        self.toolbar.update()
        self.graficos._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        #self.graficos.show()
        self.graficos.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.graficos.draw()

        self.root.protocol("WM_DELETE_WINDOW", self.mediadorVen.on_closing)
        self.root.mainloop()
    
    
    
    
if __name__ == '__main__':
    VentanaInicio()
