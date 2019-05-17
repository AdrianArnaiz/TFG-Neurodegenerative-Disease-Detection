import numpy as np
import pandas as pd
import importlib
from sklearn.base import clone
from sklearn.metrics import SCORERS
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import MinMaxScaler

class Experimenter:
    def __init__(self):
        pass
    
    def get_datos_generales(self, experimento):
        general = experimento["GENERAL"]
        return general["ID"], general["N_FOLDS"]


    def get_datasets(self, experimento, norm=False):
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
        instancias= []
        for algo in experimento["ALGORITMOS"]:
            metodo = algo["ALGO"]
            puntos = [pos for pos, char in enumerate(metodo) if char == "."]
            modulo = importlib.import_module(metodo[:puntos[-1]]) #nombre del modulo
            clase = getattr(modulo, metodo[puntos[-1]+1:]) #nombre de la clase
            instancias.append(clase(**algo["PARAMS"]))

        return [alg["ID_ALG"] for alg in experimento["ALGORITMOS"]],instancias


    def get_output_options(self, experimento):
        if experimento["OUTPUT"]['DISPLAY'] in ["bar","table", "line"]:
            return experimento["OUTPUT"]['METRIC'],experimento["OUTPUT"]['DISPLAY']
        else:
            print("El modelo de representación debe ser table, line o bar")



    def cross_validate_model(self, X, y, model, num_folds, score):
        if score not in SCORERS.keys():
            raise AttributeError("Atributo score debe ser válido. Ver válidos en sklearn.metrics.SCORERS.keys()")
        print('\t'+str(model)[:20], end=' - ')
        mod_scores = cross_val_score(model,X,y,cv=num_folds,scoring=score)
        print('FM')
        return np.array(mod_scores)

    def cross_validate_all_models(self, data_names, data_X, data_y, models, num_folds, score):
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

        # los datos son inventados, no tiene porque devolver los datos de ejemplo
        data = [np.mean(res, axis=1) for res in all_results] 
        data.append(np.mean(data,axis=0))
        df = pd.DataFrame(data,
                      columns = model_names,
                      index = data_names+['MEDIA']) 
        if rep_type == "table":
            return df
        else:
            df.plot(kind=rep_type, ylim=(0,1), figsize=(18,9)).legend(bbox_to_anchor=(1.2, 0.5))
            
    def GridSearchPipe(self, modulo, pipe, pg, verbose=True, normalizar=True):
        mejores=dict()

        for dtst in [ d for d in dir(modulo) if d.startswith('load')]:
            datos = getattr(modulo, dtst)()
            X = datos.data
            y = datos.target
            if normalizar:
                sc = MinMaxScaler()
                X = sc.fit(X).transform(X) #Comentar para no normalizar

            clf = GridSearchCV(pipe, cv=5, param_grid=pg, scoring = 'roc_auc')
            clf.fit(X,y) #crossvalscore(clf,X,y,cv=10,scoring='roc_auc')
            if verbose:
                print('\n------------------------\nDataset:',dtst[5:])
                print("Los mejores parámetros encontrados son:")
                print()
                print(clf.best_params_,end=' - score: ')
                print(clf.best_score_)
                print()
                print("Rejilla de scores de cada una de las combinaciones de parámetros:")
                       
            
            mejores[dtst[5:]]={'score':clf.best_score_, 'params':clf.best_params_, 'results':clf.cv_results_}
                       
            means = clf.cv_results_['mean_test_score']
            stds = clf.cv_results_['std_test_score']
            if verbose:
                for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                    print("%0.3f (+/-%0.03f) for %r"% (mean, std * 2, params))
                print()

        return mejores


