import numpy as np
import os
from scanorama import *
from scipy.sparse import vstack
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize, LabelEncoder

from process import load_names
from experiments import *
from utils import *

np.random.seed(0)

NAMESPACE = 'mouse_brain'
METHOD = 'svd'
DIMRED = 100

data_names = [
    'data/mouse_brain/dropviz/Cerebellum_ALT',
    'data/mouse_brain/dropviz/Cortex_noRep5_FRONTALonly',
    'data/mouse_brain/dropviz/Cortex_noRep5_POSTERIORonly',
    'data/mouse_brain/dropviz/EntoPeduncular',
    'data/mouse_brain/dropviz/GlobusPallidus',
    'data/mouse_brain/dropviz/Hippocampus',
    'data/mouse_brain/dropviz/Striatum',
    'data/mouse_brain/dropviz/SubstantiaNigra',
    'data/mouse_brain/dropviz/Thalamus',
]

if __name__ == '__main__':
    datasets, genes_list, n_cells = load_names(data_names)
    datasets, genes = merge_datasets(datasets, genes_list)

    if not os.path.isfile('data/dimred_{}.txt'.format(NAMESPACE)):
        datasets_dimred, genes = process_data(datasets, genes)
        log('Scanorama integration...')
        datasets_dimred = assemble(datasets_dimred, sigma=50,
                                   batch_size=25000)
        X_dimred = np.concatenate(datasets_dimred)
        np.savetxt('data/dimred_{}.txt'.format(NAMESPACE), X_dimred)
    else:
        X_dimred = np.loadtxt('data/dimred_{}.txt'.format(NAMESPACE))
        
    viz_genes = [
        'Gja1', 'Flt1', 'Gabra6', 'Syt1', 'Gabrb2', 'Gabra1',
        'Meg3', 'Mbp', 'Rgs5', 'Pcp2', 'Dcn', 'Pvalb', 'Nnat',
        'C1qb', 'Acta2', 'Syt6', 'Lhx1', 'Sox4', 'Tshz2', 'Cplx3',
        'Shisa8', 'Fibcd1', 'Drd1', 'Otof', 'Chat', 'Th', 'Rora',
        'Synpr', 'Cacng4', 'Ttr', 'Gpr37', 'C1ql3', 'Fezf2',
    ]

    experiment_srs(X_dimred, NAMESPACE, perplexity=1200,
                   gene_names=viz_genes, genes=genes,
                   gene_expr=vstack(datasets),
                   #visualize_orig=False,
                   kmeans=False)

    log('Done.')
