import numpy as np
import pandas as pd
import importlib
from sklearn.base import clone
from sklearn.metrics import SCORERS
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

class Experimenter:
    ''' 
    Clase que contiene los métodos que facilitan los experimentos realizados.
    Contiene métodos tanto como para la realización de un experimentador, 
        como métodos de experimentos individuales.
    '''
    def __init__(self):
        pass
    
    def get_datos_generales(self, experimento):
        '''
        Devuelve la información general del experimento, el cual se ha pasado como diccionario
        y contiene mucha información.

        Parametros
        ----------
        experimento: dict
            diccionario que contiene numerosos atributos definiendo el experimento

        Return
        -------
        tupla de tamaño 2
            que contiene str: nombre del experimento, int:numero folds de la CV
        '''
        general = experimento["GENERAL"]
        return general["ID"], general["N_FOLDS"]


    def get_datasets(self, experimento, norm=False):
        '''
        Funcion que importa y devuelve dinamicamente los datasets pasados en el atributo DATASETS
        del diccionario experimenter. El valor de DATASETS es una lista de diccionarios, donde cada
        dataset está definido en un diccionario,  en el que se indica un id y la función en formato string
        para cargarlo. Por ello, lo debemos importar dinámicamente.

        Parametros
        ----------
        experimento: dict
            diccionario que contiene numerosos atributos definiendo el experimento
        norm: boolean
            Booleno si queremos normalizar el dataset

        Return
        -------
        tupla de tamaño 3
            que contiene 3 arrays. El primero con los nombres de los datasets. El segundo es un array de
            matrices con los datos de cada dataset. El tercero es una matriz donde cada fila son las target
            del dataset.
        '''
        data_nombre = [entry["ID_DATA"] for entry in experimento["DATASETS"]]
        datos_X = []
        datos_Y = []
        for dataset in experimento["DATASETS"]:
            #Importamos datos dinámicamente
            origen = dataset["ORIGIN"]
            puntos = [pos for pos, char in enumerate(origen) if char == "."]
            mod = importlib.import_module(origen[:puntos[-1]])
            datos = getattr(mod,origen[puntos[-1]+1:])()
            
            if norm:
                X = datos.data
                sc = MinMaxScaler()
                X_sc = sc.fit(X).transform(X)
                datos_X.append(X_sc)
            else:
                datos_X.append(datos.data)
            datos_Y.append(datos.target)
        return data_nombre,datos_X,datos_Y


    def get_algoritmos(self, experimento):
        '''
        Detecta que algoritmos queremos para nuestro experimenter y devuelve los modelos inicializados.
        Al igual que con los datasets, se importan dinámicamente.

        Parametros
        ----------
        experimento: dict
            diccionario que contiene numerosos atributos definiendo el experimento

        Return
        -------
        tupla de tamaño 2
            primer elemento: array de ids
            segundo elemento: array con las instancias de los modelos
        '''
        
        instancias= []
        for algo in experimento["ALGORITMOS"]:
            metodo = algo["ALGO"]
            puntos = [pos for pos, char in enumerate(metodo) if char == "."]
            modulo = importlib.import_module(metodo[:puntos[-1]]) #nombre del modulo
            clase = getattr(modulo, metodo[puntos[-1]+1:]) #nombre de la clase
            instancias.append(clase(**algo["PARAMS"]))

        return [alg["ID_ALG"] for alg in experimento["ALGORITMOS"]],instancias


    def get_output_options(self, experimento):
        '''
        Devuelve la información sobre la representación de resultados del experimento.
        Tanto la metrica, como la representacion.

        Parametros
        ----------
        experimento: dict
            diccionario que contiene numerosos atributos definiendo el experimento

        Return
        -------
        tupla de tamaño 2
            Metrica del experimento: i.e. accuracy o roc_auc_score
            Representacion: tabla, linea o barra
        '''
        if experimento["OUTPUT"]['DISPLAY'] in ["bar","table", "line"]:
            return experimento["OUTPUT"]['METRIC'],experimento["OUTPUT"]['DISPLAY']
        else:
            print("El modelo de representación debe ser table, line o bar")



    def cross_validate_model(self, X, y, model, num_folds, score):
        '''
        Realiza la validación de un modelo, con los dataset X e y, haciendo CV de numfolds
        y devolviendo la metrica score.

        Parametros
        ----------
        X: numpy.array
            Datos de las instancias del dataset con el que entrenar.
        Y: numpy.array
            Targets de las instancias de X.
        model: scikit_model
            modelo al que entrenar
        num_folds: int
            numero de folds de la validacion cruzada
        score: string 
            métrica que devuelve, de los strings disponibles en valido en sklearn.metrics.SCORERS.keys().
        Return
        -------
        array de resultados
            array con los resultados de cada fold de la CV
        '''
        if score not in SCORERS.keys():
            raise AttributeError("Atributo score debe ser válido. Ver válidos en sklearn.metrics.SCORERS.keys()")
        print('\t'+str(model)[:20], end=' - ')
        mod_scores = cross_val_score(model,X,y,cv=num_folds,scoring=score)
        print('FM')
        return np.array(mod_scores)

    def cross_validate_all_models(self, data_names, data_X, data_y, models, num_folds, score):
        '''
        Realiza la validación cruzada cada modelo que contiene la lista models,
        con tantos dataset como los que se pasen en data_X.

        Parametros
        ----------
        data_names:list(string)
            lista con los nombres de cada dataset.
        X: numpy.array
            array de matrices, cada matriz un conjunto de datos para entrenar el modelo
        Y: numpy.array
            array de arrays, cada array los target de cada matriz de X.
        model: list(scikit_model)
            lista con cada modelo al que entrenar
        num_folds: int
            numero de folds de la validacion cruzada
        score: string 
            métrica que devuelve, de los strings disponibles en valido en sklearn.metrics.SCORERS.keys().
        Return
        -------
        res_exp
            Matriz en la que cada fila es un dataset y cada columna un modelo.
            La intersección de fila y columna es el rendimiento de ese modelo con ese dataset.
        '''
        
        res_exp = []
        for d in range(len(data_names)):
            print(str(d)+' ⟶ '+data_names[d])
            dx = data_X[d]
            dy = data_y[d]
            clone_models = [clone(m) for m in models]
            res_dtset = [self.cross_validate_model(dx,dy,modl,num_folds,score) for modl in clone_models]
            res_exp.append(np.array(res_dtset))    
            print('Fin Data')
        print('-------------Fin Experimentos-----------')
        return res_exp


    def process_results(self, all_results, data_names, model_names, rep_type):
        '''
        Devuelve la información sobre la representación de resultados del experimento.
        Tanto la metrica, como la representacion.

        Parametros
        ----------
        all_results: numpy array
            Matriz en la que cada fila es un dataset y cada columna un modelo.
            La intersección de fila y columna es el rendimiento de ese modelo con ese dataset.
        data_names: list(str)
            lista con los nombres de los datasets
        model_names: list(str)
            lista con los nombres de los modelos
        rep_type: str
            modo de representacion: table, linear o bar

        Return
        -------
         tabla o gráfico linear o de barras con los resultados
        '''        
        data = [np.mean(res, axis=1) for res in all_results] 
        data.append(np.mean(data,axis=0))
        df = pd.DataFrame(data,
                      columns = model_names,
                      index = data_names+['MEDIA']) 
        if rep_type == "table":
            return df
        else:
            df.plot(kind=rep_type, ylim=(0,1), figsize=(18,9)).legend(bbox_to_anchor=(1.2, 0.5))
            
    
    def GridSearchPipe(self,modulo, pipe, pg, verbose=True, normalizar=True):
        '''
        Experimento individual, el que se encarga de realizar un grid search,
        para un modelo pipe pasado (puede incluir más pasos que la clasificación),
        con todos los conjuntos de datos que se pueden cargar desde un determinado
        modulo (i.e modulo = CargaDatos, se genera un grid search para los 18 conjuntos que
        contiene). Habrá una malla de datos, pg, y se podrán normalizar los atributos.
        Se realiza NESTED CROSS VALIDATION.
        
        Parametros
        ----------
        modulo: modulo de python
            modulo de python que contiene loaders de datsets tipo load_...
        pipe: modelo sklearn o Pipeline
            modelo o pipeline con el que realizar los experimentos
        verbose: list(str)
            Si queremos salida por pantalla o no
        normalizar: str
            Si deseamos normalizar los datos o no en el experimento.
            Se hace de manera controlada: no caemos en data snooping.
            Lo añadimos como paso al pipeline.

        Return
        -------
         mejores:
             diccionario con el mejor resultado de cada dataset, resultante de 
             la optimización de parámetros.
        '''
        #Hace n experimentos siendo n el conjunto de datos distintos dentro del modulo pasado como parametro
        mejores=dict()

        #Todo esto es por si queremos normalizar: añadimos paso al pipe
        #El parámetro pipe también puede ser unicamente el clasificador (svm.SVC())
        #   Entonces debemos crear el pipe y renombrar los parametros del param grid.
        if normalizar:
            if isinstance(pipe, Pipeline):
                pipe.steps.insert(0,['norm',MinMaxScaler()])
            else:
                pipe = Pipeline([('norm', MinMaxScaler()), ('clf', pipe)])
                #Si no era pipeline, era clasificador normal:
                #    y hay que añadirle el prefijo clf__ a los parametros del param_grid
                if isinstance(pg, list):
                    #para pasarle a dict: algunos paramgrids les definimos como [dict(params)]
                    pg=pg[0]

                for k in pg:
                    pg['clf__'+k]=pg.pop(k)

        #Hacemos el experimento para cada conjunto de datos
        for dtst in [ d for d in dir(modulo) if d.startswith('load')]:
            datos = getattr(modulo, dtst)()
            X = datos.data
            y = datos.target

            clf = GridSearchCV(pipe, cv=10, param_grid=pg, scoring = 'roc_auc')
            puntuacion = cross_val_score(clf,X,y,cv=10,scoring='roc_auc') #Hacemos nested CV
            mejores[dtst[5:]]=puntuacion.mean()
            if verbose:
                print('\n------------------------\nDataset:',dtst[5:])
                print("Score:",puntuacion.mean())  

        return mejores


