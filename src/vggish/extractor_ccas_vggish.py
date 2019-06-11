import numpy as np
import vggish_input
import vggish_params
import vggish_postprocess
import vggish_keras
import os
    
class Extractor_Caracteristicas_Vggish:

    def __init__(self, rutaCarac, dic_inf_audios=None):
        ''' rutaCcas: ruta donde guardar los archivos de características. '''
        self.rutaCcas = '../'+rutaCarac #i.e.: CaracteristicasExtraidas/Vggish/embeddings||espectros/
        
        try: 
            os.mkdir(self.rutaCcas)
        except FileExistsError:
            print('Directorio de características ya existente, no se crea nuevo.')
        
        self.dic_inf_audios = dic_inf_audios
        
        #Definimos VGGish
        self.model = vggish_keras.get_vggish_keras()
        #Cargamos el checkpoint
        checkpoint_path = 'vggish_weights.ckpt'
        self.model.load_weights(checkpoint_path)
        
        
    def add_target(self, ccas, parkinson):
        ''' Añade la colmuna target. PD: 1, HC: 0. '''
        return np.hstack((ccas,np.ones((ccas.shape[0],1)))) if parkinson else np.hstack((ccas,np.zeros((ccas.shape[0],1))))
    
    def extraccion_embeddings_directorio(self, aud, extra_atribs=None, embeddings = True):
        '''
        Devuelve en numpy las medidas de los audios que saca el VGGish y se guardan en el archivo ccas.npy.
        Recorre para un tipo de audio primero los sanos y los etiqueta y posteriormente hace lo mismo con los PD.
        Finalmente los concatena.

        aud: ruta del directorio de audios a analizar respecto a src/. i.e: 'PC-GITA/read-text/'. Debe subcontener hc y pd.
        extra_atribs: atributos extra a añadir a las caracteriticas. i.e. edad o sexo.
        '''
        rutaAudios = '../'+aud 
        
        rutaAudiosTipo = rutaAudios+'hc/'
        audios = os.listdir(rutaAudiosTipo)
        print('Comienzo extracción HC, quedan:', len(audios)*2,'audios.')        
        ls = np.array( [self.extraccion_embeddings_audio(rutaAudiosTipo+audio, embeddings) for audio in audios] )
        #Borramos los audios de menos de un segundo, cuya salida de vggish es np.array([nan,nan],)
        ls = np.array([instancia for instancia in ls if not np.isnan(instancia).any()])
        ccas_hc = self.add_target(ls, False)
        assert ccas_hc[:,ccas_hc.shape[1]-1].all()==0 #aseguramos que etiquetamos de manera correcta
        
        print('Comienzo extracción PD, quedan:', len(audios),'audios.')
        
        rutaAudiosTipo = rutaAudios+'pd/'
        audios = os.listdir(rutaAudiosTipo)
        ls = np.array( [self.extraccion_embeddings_audio(rutaAudiosTipo+audio, embeddings) for audio in audios] )
        ls = np.array([instancia for instancia in ls if not np.isnan(instancia).any()])
        ccas_pd = self.add_target(ls, True)
        assert ccas_pd[:,ccas_pd.shape[1]-1].all()==1
        
         #Devolvemos todo el conjunto entero junto
        set_datos = np.concatenate((ccas_hc, ccas_pd))
        
        #Añadimos edad o sexo si necesario y si es posible (solo posible para embbedings, no espectros)
        if extra_atribs is not None:
            set_datos = self.add_atribs(set_datos, extra_atribs)

        return set_datos    
        
  
    def extraccion_embeddings_audio(self, rutaAudio, embeddings):
        '''Extrae la media de los 128 embeddings y la deviación poara devolver un vector de 256 ccas por audio
        rutaAudio: ruta relativa del audio desde directorio /src/vggish'''
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
    
    
    def add_atribs(self, ccas, atribs):
        '''Añade los atributos a la matriz ccas cuyos nombres se pasan en formato string y cuyo valor se encuentra en el diccionario dic en 
            la lista atribs.
            Se utiliza para añadir los atributos extra a la hora de extraer todas las características en extraccion_ccas_directorio.
            También se puede utilizar por separado, pasandole un archivo numpy. Esto es útil ya que si hemos sacado las ccas de Disvoice,
               no es necesario volver a invertir el tiempo en volver a sacarlas para añadir dos atributos extra.
        '''
        if self.dic_inf_audios is None:
            raise NameError('No ha pasado ningún diccionario de atributos extra.')
            
        for a in atribs:
            column_atrib = np.array([self.dic_inf_audios[audio][a] for audio in self.dic_inf_audios])
            reps = ccas.shape[0]//100 if ccas.shape[0]>=100 else 1
            column_atrib = np.repeat(column_atrib,reps).reshape(ccas.shape[0],1)
            ccas = np.insert(ccas,[-1],column_atrib,axis=1)
        return ccas
    
    
    