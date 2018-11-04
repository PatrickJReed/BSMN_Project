import glob, os, gc, sys
import os.path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from time import time
from subprocess import (call, Popen, PIPE)
from itertools import product
from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)
from sklearn.decomposition import (PCA, RandomizedPCA)
from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle
from sklearn import preprocessing
from IPython.display import Image
from PIL import Image
from IPython.display import Image as IPImage
import shutil
import re
import xml.etree.ElementTree as ET
import time
from keras_dec import DeepEmbeddingClustering
if (sys.version[0] == 2):
    import cPickle as pickle
else:
    import pickle


basepath = "/home/ubuntu/efs/SLAV_Data/SML/"
os.chdir(os.path.join(basepath))
X = np.load('SML_Data.npzdBcMZU-numpy.npy')
X2 = X.reshape(X.shape[0], -1)
X3 = X2.astype(np.float32)
X3 = X3 / 255
X = None
X2 = None
c = DeepEmbeddingClustering(n_clusters=36, input_dim=196608)
c.initialize(X3, finetune_iters=10000, layerwise_pretrain_iters=5000)
c.cluster(X3)

