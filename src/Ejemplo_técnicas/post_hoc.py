import scipy.stats as stats
import pandas as pd
import numpy as np


def friedman_ranking_chi(d, k, r, iman_davenport = False, verbose=True):
    '''
    d: numero de datasets
    k: numero de clasificadores
    r: np.array de rankings medios
    iman_davenport: devolver estadístico con corrección o normal
    '''
    first = (12*d) / (k*(k+1))
    sumat = np.sum(r**2)
    second = (k*((k+1)**2)) / 4
    res = first*(sumat-second)
    
    if iman_davenport and verbose:
        res = ((d-1)*res)/(d*(k-1)-res)
        print('Friedman IVAN-Davenport Chi Square - Datasets: {} - Clasificadores {}'.format(d,k))
        print('-- Chi_sq^2_f = {:.3f}'.format(res))
        
    elif verbose:
        print('Friedman Chi Square - Datasets: {} - Clasificadores {}'.format(d,k))
        print('-- Chi_sq^2_f = {:.3f}'.format(res))
        
    return res




def hochberg_test(ranks, n_datasets, control=None, alpha=0.05):
    """
        Parameters
        ----------
        ranks : dictionary
            A dictionary with format 'Classifier':'mean_rank' 
        control : string optional
            The name of the control method (one vs all) 
            
        Returns
        ----------
        Comparions : np.array-like
            Strings identifier of each comparison with format 'group_i_control vs group_j'
            
        Z-values : np.array-like
            The computed Z-value statistic for each comparison.
            
        p-values : np.array-like
            The associated p-value from the Z-distribution wich depends on the index of the comparison
            
        adj_sigmas : np.array-like
            The associated adjusted sigma according HOCHBERG test alpha/i, being i the reverse of the position in ranking.
            
        References
        ----------
        Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. Journal of Machine learning research, 7(Jan), 1-30.
    """
    k = len(ranks) # numero de tests
    values = list(ranks.values())
    keys = list(ranks.keys())

    control_i = values.index(min(values)) if not control else keys.index(control)

    # Strings de comparaciones
    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    
    # Estadísticos y pval
    # Estadisticos son la diferencia de rankings medios
    # Error estandar según Demsar
    se = np.sqrt((k*(k+1))/(6*n_datasets)) 

    z_values = [abs(values[control_i] - values[i])/se for i in range(k) if i != control_i]
    p_values = [2*(1-stats.norm.cdf(abs(z))) for z in z_values]
    #p_values = [2*(1-stats.norm.cdf(abs(z))) for z in z_values]
    
    # Ordenarmos por pval
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    
    # Ajustamos sigma según Hochner
    adj_sigmas = [alpha/i for i in range(k-1,0,-1)]
    
    return np.asarray(comparisons), np.asarray(z_values), np.asarray(p_values), np.asarray(adj_sigmas)

def posthoc_Friedman_Davenport_Hochbertest(results, alpha=0.05, obj='max', control=None, verbose=True):
    '''
    results: DataFrame like
        Each row a dataset, each column a classifiers. Column of datasets names calles 'Dataset'
    '''
    
    # Preparamos resultados en numpy, array de nombres y datos del experimento
    name_clfs = results.drop('Dataset', axis=1).columns
    results_np = results[name_clfs].values
    n_datasets = results_np.shape[0]
    n_clfs = results_np.shape[1]
    
    #1. Realizamos friedman sobre los resultados de evaluación
    stat_fried_metric, pval_fried_metric = stats.friedmanchisquare(*results_np.transpose())
    
    #2. Realizamos test de friedman sobre los rankings
    #Calculamos rankings y rankings medios en np y dict
    all_ranks = np.array([stats.rankdata(-p) for p in results_np]) if obj=='max' else np.array([stats.rankdata(p) for p in results_np])
    average_ranks = np.mean(all_ranks, axis=0)
    dict_clf_avg_rank = {c:r for c, r in zip(name_clfs, average_ranks.round(3))}
    #Calculamos el estadistico de Iman-Davenport
    stat_ImanDaven_ranks = friedman_ranking_chi(n_datasets, #numero datasets
                                                n_clfs, #numero de clfs
                                                average_ranks, 
                                                iman_davenport=True,
                                                verbose= False)
    df1 = n_clfs-1
    df2 = (n_clfs-1)*(n_datasets-1)
    pval_ImanDaven_ranks = stats.f.sf(stat_ImanDaven_ranks, df1, df2)
    
    #3. Test de Hochberg
    comparisons_h, z_values_h, p_values_h, adj_sigmas_h = hochberg_test(dict_clf_avg_rank,
                                                        n_datasets = n_datasets,
                                                        control=control,
                                                        alpha=alpha)

    holm_scores = pd.DataFrame({"z":z_values_h.round(3),"p": p_values_h.round(3),
                                'alpha/i':adj_sigmas_h.round(3) ,"sig": p_values_h < adj_sigmas_h}, 
                               index=comparisons_h)

    if verbose:
        print(f'### Experimento')
        print(f'# Number of classifiers: {n_clfs}')
        print(f'# Number of datasets: {n_datasets}')
        print('# Name of classifiers: {}'.format(', '.join(name_clfs.format())))
        print(f'# Alpha: {alpha}')
        
        print(f'\n### Métricas')
        print(f'# Test de Friedman sobre métricas \n\t-> p-val: {pval_fried_metric:.4f}')
        
        print(f'\n### Rankings')
        mx_string = len(max(name_clfs, key=lambda x: len(x)))
        for k in sorted(dict_clf_avg_rank, key=dict_clf_avg_rank.get):
            print('# {:{}} ranking medio:  {}'.format(k,mx_string,dict_clf_avg_rank[k]))
        print(f'# Test de Friedman sobre Rankings [F({stat_ImanDaven_ranks:.4f}, {df1}, {df2})] \
              \n\t-> p-val: {pval_ImanDaven_ranks:.4f}')
        one = min(dict_clf_avg_rank, key=dict_clf_avg_rank.get) if control is None else control
        print('\n### Test Hochberg Comparacion {} vs all'.format(one))
        print('# Tabla de comparación de Rankings:')
        print(holm_scores)
    
    return holm_scores

