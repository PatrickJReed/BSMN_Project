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
X2 = np.load('SML_Data.npzdBcMZU-numpy.npy')

r1, g1, b1 = 250, 250, 250 # Original value
r2, g2, b2 = 0, 0, 0 # Value that we want to replace it with

red, green, blue = X2[:,:,:,0], X2[:,:,:,1], X2[:,:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
X2[:,:,:,:3][mask] = [r2, g2, b2]

r1, g1, b1 = 255, 255, 255 # Original value
r2, g2, b2 = 0, 0, 0 # Value that we want to replace it with

red, green, blue = X2[:,:,:,0], X2[:,:,:,1], X2[:,:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
X2[:,:,:,:3][mask] = [r2, g2, b2]

X3 = X2.reshape(X2.shape[0], -1)
X4 = X3.astype(np.float32)
X4 = X4 / 255
rbst_scale = preprocessing.MaxAbsScaler().fit(X4)
X5 = rbst_scale.transform(X4)
X2 = None
X3 = None
X4 = None
c = DeepEmbeddingClustering(n_clusters=10, input_dim=196608)
c.initialize(X5, finetune_iters=1000, layerwise_pretrain_iters=500)
c.cluster(X5)

