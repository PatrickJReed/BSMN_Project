#!/usr/bin/python2.7
from __future__ import print_function
import glob, os, gc, sys
import os.path
import csv
import numpy as np
np.random.seed(1337)  # for reproducibility
from time import time
from subprocess import (call, Popen, PIPE)
from itertools import product
from IPython.display import display
from PIL import Image
from IPython.display import Image as IPImage
import shutil
import re
import xml.etree.ElementTree as ET
import time
basepath = "/home/ubuntu/efs/SLAV_Data/" 

Bulk_5125_Cortex = "5125_cortex_BT_122_L3"
Bulk_5125_Hippocampus = "5125_hippo_BT_139_L3"
Bulk_5125_Liver = "5125_liver_BT_164_L3"

SC_5125_Hippo = ["5125_hippo_SC_140_L3","5125_hippo_SC_141_L3","5125_hippo_SC_142_L3","5125_hippo_SC_143_L3","5125_hippo_SC_144_L3","5125_hippo_SC_145_L3","5125_hippo_SC_147_L3","5125_hippo_SC_149_L3","5125_hippo_SC_150_L3","5125_hippo_SC_151_L3","5125_hippo_SC_152_L3","5125_hippo_SC_153_L3","5125_hippo_SC_154_L3","5125_hippo_SC_155_L3","5125_hippo_SC_156_L3","5125_hippo_SC_157_L3","5125_hippo_SC_158_L3","5125_hippo_SC_159_L3","5125_hippo_SC_160_L3","5125_hippo_SC_161_L3","5125_hippo_SC_162_L3","5125_hippo_SC_163_L3"]

SC_Train = sys.argv[1]

Data_Sets = []
Data_Sets.append([SC_Train,Bulk_5125_Hippocampus,Bulk_5125_Liver])

for dset in Data_Sets:    
    cell = dset[0]
    print(cell)
    os.chdir(os.path.join(basepath, cell))
    if not os.path.isfile(os.path.join(basepath, cell, cell+'_XY.npz')):
        multilabel = os.path.join(basepath, cell, cell +"_Multi-Labels.txt")
        X = []
        Y = []
        with open(multilabel, 'r') as infile:
            data = infile.readlines()    
            X = np.array([np.array(Image.open(string.split('\t')[0])) for string in data if os.path.isfile(os.path.join(basepath, cell, string.split('\t')[0]))])
            print(X.shape)
            Y = np.array([np.array(map(int,onehot.split('\t')[1].split(','))) for onehot in data if os.path.isfile(os.path.join(basepath, cell, onehot.split('\t')[0]))])
            print(Y.shape)
        np.savez(cell+'_XY.npz', X=X, Y=Y)
print("Done with "+cell) 