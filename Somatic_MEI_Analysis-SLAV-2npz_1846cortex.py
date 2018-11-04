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

Bulk_1846_Cerebellum = "1846_cereb_BT_13_L3"
Bulk_1846_Cortex = "1846_cortex_BT_71_L3"
Bulk_1846_Hippocampus = "1846_hippo_BT_19_L3"
Bulk_1846_Liver = "1846_liver_BT_22_L3"



SC_1846_Cortex = ["1846_cortex_SC_72_L3","1846_cortex_SC_73_L3","1846_cortex_SC_74_L3","1846_cortex_SC_75_L3","1846_cortex_SC_78_L3","1846_cortex_SC_79_L3","1846_cortex_SC_80_L3","1846_cortex_SC_81_L3","1846_cortex_SC_82_L3","1846_cortex_SC_83_L3","1846_cortex_SC_84_L3","1846_cortex_SC_85_L3","1846_cortex_SC_86_L3"]


SC_Train = sys.argv[1]

Data_Sets = []
Data_Sets.append([SC_Train,Bulk_1846_Cortex,Bulk_1846_Liver])

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