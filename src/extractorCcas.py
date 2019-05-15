import numpy as np
import os

class ExtractorCaracteristicas:
    ''' Clase encargada de la extracción de características de los audios con la herramienta Disvoice 
    author: Adrián Arnaiz
    '''
    def __init__(self, rutaAud, rutaCarac, dic_inf_audios=None):
        ''' rutaAud: ruta donde se encuentran los audios 
            rutaCcas: ruta donde guardar los archivos de características.
        '''
        self.rutaAudios = '"../../'+rutaAud #i.e.: 'PC-GITA/read-text/'
        try: 
            os.mkdir(rutaCarac)
        except FileExistsError:
            print('Directorio de características ya existente, no se crea nuevo.')
        self.rutaCcas = '"../../'+rutaCarac #i.e.: CaracteristicasExtraidas/
        self.dic_inf_audios = dic_inf_audios
        
    def add_target(self, ccas, parkinson):
        ''' Añade la colmuna target. PD: 1, HC: 0. '''
        return np.hstack((ccas,np.ones((ccas.shape[0],1)))) if parkinson else np.hstack((ccas,np.zeros((ccas.shape[0],1))))
    
    def extraccion_ccas_directorio(self, script, ccashc, ccaspd, extra_atribs=None):
        '''
        Devuelve en numpy las medidas de los audios que saca el script indicado y se guardan en el fichero ccas (txt).
        Recorre para un tipo de audio primero los sanos y los etiqueta y posteriormente hace lo mismo con los PD.
        Finalmente los concatena.

        script: Nombre del script a ejecutar, solo nombre.
        audios: ruta del directorio de audios a analizar respecto a src/.
        ccashc: nombre del fichero que se guardará en el directorio CaracteristicasExtradidas para hc.
        ccaspd: nombre del fichero que se guardará en el directorio CaracteristicasExtradidas para pd.
        '''
        #Extraemos las características para las personas sanas
        comando = 'cd Disvoice\\'+script +' & python '+script+'.py '
        comando+= self.rutaAudios+'hc/" '+self.rutaCcas+ccashc+'" "static" "false"'
        os.system(comando)
        hc = np.loadtxt(self.rutaCcas+ccashc)
        hc = self.add_target(hc, False)
        assert hc[:,hc.shape[1]-1].all()==0 #aseguramos que etiquetamos de manera correcta

        #Extraemos las características para personas con PD
        comando = 'cd Disvoice\\'+script +' & python '+script+'.py '
        comando+= self.rutaAudios+'pd/" '+self.rutaCcas+ccaspd+'" "static" "false"'
        os.system(comando)
        pd = np.loadtxt(self.rutaCcas+ccaspd)
        pd = self.add_target(pd, True)
        assert pd[:,pd.shape[1]-1].all()==1

        #Devolvemos todo el conjunto entero junto
        set_datos = np.concatenate((hc, pd))
        
        #Añadimos edad o sexo si necesario
        if extra_atribs is not None:
            set_datos = self.add_atribs(set_datos, extra_atribs)
            
        return set_datos 

    
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

    def identificadorNan(self, ruta_ccas,verbose=False):
        sets_ccas = [d for d in os.listdir(ruta_ccas) if d.endswith('.npy')]
        dic_nans = dict()
        for ccas in sets_ccas:
            data = np.load(ruta_ccas+ccas)
            if np.isnan(data).any():
                nan = np.argwhere(np.isnan(data))
                audiosconNaN = set(np.argwhere(np.isnan(data))[:,0])
                dic_nans[ccas] =  [audiosconNaN, len(audiosconNaN), len(np.where(np.array(list(audiosconNaN))>49)[0])/len(audiosconNaN),nan]
                if verbose:
                    print('\n--------------\n',ccas)
                    print('\t(Audios, atrib): ',data.shape)
                    print('\tAudios con NaN: ',audiosconNaN)
                    print('\tNumero de audios con NaN: ',len(audiosconNaN))
                    print('\t% de Nan en audios PD: ',dic_nans[ccas][2])

        return dic_nans
    
    def tratamiento_nan(self, ruta_ccas, dic_nan):
        '''Borramos de cada conjunto de caracerísticas las intancias con nan.'''
        for arch in dic_nan:
            data = np.load(ruta_ccas+arch)
            data = np.delete(data, list(dic_nan[arch][0]), 0)
            np.save(ruta_ccas+arch, data)
   
    