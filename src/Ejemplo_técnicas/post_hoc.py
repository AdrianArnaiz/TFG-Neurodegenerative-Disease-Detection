import scipy.stats as stats
import pandas as pd
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

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
    
    if iman_davenport:
        res = ((d-1)*res)/(d*(k-1)-res)
        if verbose:
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
    dict_clf_avg_rank = {c:r for c, r in zip(name_clfs, average_ranks)}
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
        print(f'# Test de Ivan-Davenport sobre Rankings [F({stat_ImanDaven_ranks:.4f}, {df1}, {df2})] \
              \n\t-> p-val: {pval_ImanDaven_ranks:.4f}')
        one = min(dict_clf_avg_rank, key=dict_clf_avg_rank.get) if control is None else control
        print('\n### Test Hochberg Comparacion {} vs all'.format(one))
        print('# Tabla de comparación de Rankings:')
        print(holm_scores)
    
    return holm_scores, dict_clf_avg_rank



def nemenyi_CD(n_clfs, n_dtsts, alpha=0.05):
    if alpha==0.05:
        q = {2:1.960, 3:2.343, 4:2.569, 5:2.728, 6:2.850, 7:2.949, 8:3.031, 9:3.102, 10:3.164}
    elif alpha==0.1:
        q = {2:1.645, 3:2.052, 4:2.291, 5: 2.459, 6:2.589, 7:2.693, 8:2.780, 9:2.855, 10:2.920}

    return q[n_clfs]*np.sqrt( (n_clfs*(n_clfs+1))/(6*n_dtsts))

def groups_Nemenyi(ranks, CD):
    # Ordenamos los nombres de los rankings de peor a mejor (i>i+1), de izquierda a derecha en el diagrama Nemenyi.
    ordered_lf_rg_keys = sorted(ranks, key=ranks.get, reverse=True)
    #Ordenamos los valores
    coords = [(ranks[k],) for k in ordered_lf_rg_keys]
    
    #Calculamos las distancias entre rankings
    dist = distance.cdist(coords, coords)
    #Calculamos las menores que la distancia critica de Nemenyi
    group = distance.cdist(coords, coords)<CD
    
    #Nos quedamos los indices donde sean menores (solo de triangulo superior para formar grupos de izq a der)
    rows,cols =np.where(np.triu(group, k=1))
    #Calculamos los vecinos, dict donde estan los extremos de los grupos (1:4 representa 1-2-3-4)
    neighbours = dict(zip(rows,cols))
    
    #Nos quedamos con grupos unicos: "2:4" esta incluido en "1:4"
    sets_same_classifiers = dict()
    for k in neighbours:
            if neighbours[k] not in sets_same_classifiers.values():
                sets_same_classifiers[k]=neighbours[k]
    #Tenemos los grupos con el nombre del clf            
    grupos = [(ordered_lf_rg_keys[k:sets_same_classifiers[k]+1]) for k in sets_same_classifiers]
    
    return grupos

def plot_nemenyi(ranks, CD, groups, fsize=(13,4)):
    n_clfs = len(ranks)
    limits=(n_clfs,1) #Limite a ranking maximo
    
    fig, ax = plt.subplots(figsize=fsize)
    plt.subplots_adjust(left=0.2, right=0.8)
    
    # set up plot
    ax.set_xlim(limits)
    ax.set_ylim(0,1)
    ax.spines['top'].set_position(('axes', 0.6))

    #ax.xaxis.tick_top()
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_visible(False)
    for pos in ["bottom", "left", "right"]:
        ax.spines[pos].set_visible(False)
        
    # CD bar
    ax.plot([limits[0],limits[0]-CD], [.9,.9], color="k")
    ax.plot([limits[0],limits[0]], [.9-0.03,.9+0.03], color="k")
    ax.plot([limits[0]-CD,limits[0]-CD], [.9-0.03,.9+0.03], color="k") 
    ax.text(limits[0]-CD/2., 0.92, f"CD {CD:.2f}", ha="center", va="bottom") 

    
    # annotations
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="-",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, va="center")
    
    
    # Pintamos lineas de los grupos
    x = 0.55
    y = 0.55
    for g in groups:
        ax.plot([ranks[g[0]],ranks[g[-1]]],[x,y], color="k", lw=3)
        x=x-0.07
        y=y-0.07
    
    
    
    # Escribir cada ranking
    x = 0
    #y = 0.4
    ha_val = 'right'
    change = True
    for i,k in enumerate(sorted(ranks, key=ranks.get, reverse=True)):
        if i >= n_clfs/2 and change:
            x = 1
            ha_val = 'left'
            change = False
            y = y + 0.15
        ax.annotate(k, xy=(ranks[k], 0.6), xytext=(x,y),ha="left",  **kw)
        
        if i >= n_clfs/2:
            y = y + 0.15
        else:
            y = y - 0.15    
        
    
 
    plt.show()