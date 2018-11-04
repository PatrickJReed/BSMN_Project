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

Bulk_1571_Cerebellum = "1571_cereb_BT_40_L3"
Bulk_1571_Hippocampus = "1571_hippo_BT_41_L3"

SC_1571_Hippo = ["1571_hippo_SC_55_L3","1571_hippo_SC_56_L3","1571_hippo_SC_57_L3","1571_hippo_SC_58_L3","1571_hippo_SC_59_L3","1571_hippo_SC_61_L3","1571_hippo_SC_62_L3","1571_hippo_SC_63_L3","1571_hippo_SC_64_L3"]

SC_Train = sys.argv[1]
Data_Sets = []
Data_Sets.append([SC_Train,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])

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