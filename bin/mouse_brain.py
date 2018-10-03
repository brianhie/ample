import numpy as np
from scanorama import *
from scipy.sparse import vstack
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize, LabelEncoder

from process import load_names
from sketch import srs, reduce_dimensionality, test
from utils import log

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

    log('Scanorama integration...')
    datasets_dimred, genes = process_data(datasets, genes)
    datasets_dimred = assemble(datasets_dimred, sigma=50)
    X_dimred = np.concatenate(datasets_dimred)
    #log('Dimension reduction with {}...'.format(METHOD))
    #X = vstack(datasets)
    #X_dimred = reduce_dimensionality(X, method=METHOD, dimred=DIMRED)
    #if METHOD == 'jl_sparse':
    #    X_dimred = X_dimred.toarray()
    #log('Dimensionality = {}'.format(X_dimred.shape[1]))

    test(X_dimred, 'mouse_brain', perplexity=1200)

    log('Done.')
