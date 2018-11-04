#!/usr/bin/python2.7
from __future__ import division
import glob, os, gc, sys
import os.path
import csv
import numpy as np
from time import time
from subprocess import (call, Popen, PIPE)
from itertools import product
from IPython.display import Image
from PIL import Image
from IPython.display import Image as IPImage
import shutil
import re
import xml.etree.ElementTree as ET
import time



##Path to Data
basepath = "/home/ubuntu/efs/SLAV_Data/"
narrowpeak = "-ready_peaks.narrowPeak"
peaks_merged = "_peaksMerged.txt"
peaks_merged_bed = "_peaksMerged.bed"
peaks_correct_bed = "_peaksCorrect.bed"
peakregions_sml = ".peakregions_sml"
peakregions_lrg = ".peakregions_lrg"
peaks_correct_data = "_peaksCorrect.data"
peaks_L1HS_bedgraph = "_peaks_L1HS_mapped.bedgraph"
loci_sml = ".loci_sml"
loci_lrg = ".loci_lrg"
overlap = "_overlap_"
overlap_sml = "_overlap_sml_"
overlap_lrg = "_overlap_lrg_"
L1HS_bam = "-L1HS_mapped.bam"
bam = "-ready.bam"
igv = "-igv.xml"
bed = ".bed"
## rmask Paths
L1HS = "/home/ubuntu/efs/SLAV_Data/rmask_L1HS_Final.bed"
L1PA2345 = "/home/ubuntu/efs/SLAV_Data/rmask_L1PA2345_Final.bed"
L1_Other = "/home/ubuntu/efs/SLAV_Data/rmask_L1_Other_Final.bed"
##IGV Template

Bulk_1571_Cerebellum = "1571_cereb_BT_40_L3"
Bulk_1571_Hippocampus = "1571_hippo_BT_41_L3"
Bulk_1846_Cerebellum = "1846_cereb_BT_13_L3"
Bulk_1846_Cortex = "1846_cortex_BT_71_L3"
Bulk_1846_Hippocampus = "1846_hippo_BT_19_L3"
Bulk_1846_Liver = "1846_liver_BT_22_L3"
Bulk_5125_Cortex = "5125_cortex_BT_122_L3"
Bulk_5125_Hippocampus = "5125_hippo_BT_139_L3"
Bulk_5125_Liver = "5125_liver_BT_164_L3"

SC_1571_Hippo = ["1571_hippo_SC_43_L3","1571_hippo_SC_45_L3","1571_hippo_SC_46_L3","1571_hippo_SC_47_L3","1571_hippo_SC_48_L3","1571_hippo_SC_50_L3","1571_hippo_SC_51_L3","1571_hippo_SC_52_L3","1571_hippo_SC_53_L3","1571_hippo_SC_55_L3","1571_hippo_SC_56_L3","1571_hippo_SC_57_L3","1571_hippo_SC_58_L3","1571_hippo_SC_59_L3","1571_hippo_SC_61_L3","1571_hippo_SC_62_L3","1571_hippo_SC_63_L3","1571_hippo_SC_64_L3"]
#SC_1846_Cortex = ["1846_cortex_SC_72_L3","1846_cortex_SC_73_L3","1846_cortex_SC_74_L3","1846_cortex_SC_75_L3","1846_cortex_SC_78_L3","1846_cortex_SC_79_L3","1846_cortex_SC_80_L3","1846_cortex_SC_81_L3","1846_cortex_SC_82_L3","1846_cortex_SC_83_L3","1846_cortex_SC_84_L3","1846_cortex_SC_85_L3","1846_cortex_SC_86_L3"]
#SC_1846_Hippo = ["1846_hippo_SC_100_L3","1846_hippo_SC_101_L3","1846_hippo_SC_102_L3","1846_hippo_SC_103_L3","1846_hippo_SC_104_L3","1846_hippo_SC_105_L3","1846_hippo_SC_106_L3","1846_hippo_SC_107_L3","1846_hippo_SC_108_L3","1846_hippo_SC_109_L3","1846_hippo_SC_110_L3","1846_hippo_SC_111_L3","1846_hippo_SC_112_L3","1846_hippo_SC_113_L3","1846_hippo_SC_88_L3","1846_hippo_SC_89_L3","1846_hippo_SC_90_L3","1846_hippo_SC_91_L3","1846_hippo_SC_92_L3","1846_hippo_SC_93_L3","1846_hippo_SC_94_L3","1846_hippo_SC_95_L3","1846_hippo_SC_99_L3"]
#SC_5125_Cortex = ["5125_cortex_SC_125_L3","5125_cortex_SC_126_L3","5125_cortex_SC_127_L3","5125_cortex_SC_128_L3","5125_cortex_SC_129_L3","5125_cortex_SC_130_L3","5125_cortex_SC_131_L3","5125_cortex_SC_132_L3","5125_cortex_SC_133_L3","5125_cortex_SC_134_L3","5125_cortex_SC_135_L3","5125_cortex_SC_136_L3","5125_cortex_SC_138_L3"]
#SC_5125_Hippo = ["5125_hippo_SC_140_L3","5125_hippo_SC_141_L3","5125_hippo_SC_142_L3","5125_hippo_SC_143_L3","5125_hippo_SC_144_L3","5125_hippo_SC_145_L3","5125_hippo_SC_147_L3","5125_hippo_SC_149_L3","5125_hippo_SC_150_L3","5125_hippo_SC_151_L3","5125_hippo_SC_152_L3","5125_hippo_SC_153_L3","5125_hippo_SC_154_L3","5125_hippo_SC_155_L3","5125_hippo_SC_156_L3","5125_hippo_SC_157_L3","5125_hippo_SC_158_L3","5125_hippo_SC_159_L3","5125_hippo_SC_160_L3","5125_hippo_SC_161_L3","5125_hippo_SC_162_L3","5125_hippo_SC_163_L3"]


Data_Sets = []
Data_Sets.append([SC_1571_Hippo,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])
#Data_Sets.append([SC_1846_Cortex,Bulk_1846_Cortex,Bulk_1846_Liver])
#Data_Sets.append([SC_1846_Hippo,Bulk_1846_Hippocampus,Bulk_1846_Liver])
#Data_Sets.append([SC_5125_Cortex,Bulk_5125_Cortex,Bulk_5125_Liver])
#Data_Sets.append([SC_5125_Hippo,Bulk_5125_Hippocampus,Bulk_5125_Liver])

filelist_sml = []
metadata_sml = []
#metadata2_sml = []

for dset in Data_Sets:
    for cell in dset[0]:
        print cell
        #shutil.copy(os.path.join(basepath, "final", cell, cell+"_Input_metadata.txt"),os.path.join(basepath, diry, cell, cell+"_Input_metadata.txt"))
        os.chdir(os.path.join(basepath, cell))
    ## Load images and meta data from meta files

        with open(os.path.join(basepath, cell, cell+"_Input_metadata.txt")) as f:
            for line in csv.reader(f, delimiter="\t"):
                if os.path.isfile(line[3]):
                    readclass = line[5].split(":")[0]
                    peakclass_sml = line[5].split(":")[1]
                    L1_class = line[5].split(":")[3]
                    #print os.path.join(basepath, diry, cell, line[3])
                    #if peakclass_sml == readclass:
                    class_sml = [readclass,L1_class]
                    filelist_sml.append(os.path.join(basepath, cell, line[3]))
                    metadata_sml.append("".join(class_sml))
                    #metadata2_sml.append("".join(L1_class))

os.chdir(os.path.join(basepath))
X_sml = np.array([np.array(Image.open(fname).resize((200,500))) for fname in filelist_sml])
Y_sml = np.array(metadata_sml).astype(str)
print X_sml.shape
print Y_sml.size
print len(np.unique(Y_sml))
n_classes_sml = Y_sml.size
n_samples_sml = len(X_sml)
np.savez("SLAV_Cells_sml", X_sml=X_sml, Y_sml=Y_sml)
