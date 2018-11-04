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
peakregions_sml = ".peakregions_sml"
peaks_correct_data = "_peaksCorrect.data"
peaks_L1HS_bedgraph = "_peaks_L1HS_mapped.bedgraph"
loci_sml = ".loci_sml"
loci_sml = ".loci_sml"
overlap = "_overlap_"
overlap_sml = "_overlap_sml_"
overlap_sml = "_overlap_sml_"
L1HS_bam = "-L1HS_mapped.bam"
bam = "-ready.bam"
igv = "-igv.xml"
bed = ".bed"
## rmask Paths
L1HS = "/home/ubuntu/efs/SLAV_Data/rmask_L1HS_Final.bed"
L1PA2345 = "/home/ubuntu/efs/SLAV_Data/rmask_L1PA2345_Final.bed"
L1_Other = "/home/ubuntu/efs/SLAV_Data/rmask_L1_Other_Final.bed"
##IGV Template
IGV = "/home/ubuntu/efs/SLAV_Data/igv-template4.xml"

Bulk_1571_Cerebellum = "1571_cereb_BT_40_L3"
Bulk_1571_Hippocampus = "1571_hippo_BT_41_L3"
Bulk_1846_Cerebellum = "1846_cereb_BT_13_L3"
Bulk_1846_Cortex = "1846_cortex_BT_71_L3"
Bulk_1846_Hippocampus = "1846_hippo_BT_19_L3"
Bulk_1846_Liver = "1846_liver_BT_22_L3"
Bulk_5125_Cortex = "5125_cortex_BT_122_L3"
Bulk_5125_Hippocampus = "5125_hippo_BT_139_L3"
Bulk_5125_Liver = "5125_liver_BT_164_L3"

SC_1571_Hippo_Train = sys.argv[1]




Data_Sets_Train = []
Data_Sets_Train.append([SC_1571_Hippo_Train,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])
#Data_Sets_Train.append([SC_1846_Cortex_Train,Bulk_1846_Cortex,Bulk_1846_Liver])
#Data_Sets_Train.append([SC_1846_Hippo_Train,Bulk_1846_Hippocampus,Bulk_1846_Liver])

Data_Sets_Validation = []
#Data_Sets_Validation.append([SC_5125_Cortex_Validation,Bulk_5125_Cortex,Bulk_5125_Liver])
#Data_Sets_Validation.append([SC_5125_Hippo_Validation,Bulk_5125_Hippocampus,Bulk_5125_Liver])

Data_Sets_Test = []
#SC_1571_Hippo_Test = list(set(SC_1571_Hippo_All) - set(SC_1571_Hippo_Train))
#SC_1846_Cortex_Test = list(set(SC_1846_Cortex_All) - set(SC_1846_Cortex_Train))
#SC_1846_Hippo_Test = list(set(SC_1846_Hippo_All) - set(SC_1846_Hippo_Train))
#SC_5125_Cortex_Test = list(set(SC_5125_Cortex_All) - set(SC_5125_Cortex_Validation))
#SC_5125_Hippo_Test = list(set(SC_5125_Hippo_All) - set(SC_5125_Hippo_Validation))

for dset in Data_Sets_Train:
    cell = dset[0]
    print cell
    os.chdir(os.path.join(basepath, cell))
    for file in glob.glob("*_sml_s*__*.png"):
        newfile = re.sub("_s\d+__", "-", file)
        shutil.move(file, newfile)
        img = Image.open(newfile)
        width = img.size[0]
        height = img.size[1]
        img2 = img.crop((160,130,width,height))
        path = os.path.splitext(newfile)[0]
        basename = os.path.basename(path)
        outfile1 = basename + "_cropped.png"
        img2.save(outfile1)
print "Done_A!"
for dset in Data_Sets_Train:
    cell = dset[0]
    print cell
    with open(os.path.join(basepath, cell, cell+"_Input_metadata.txt")) as f:
        for line in csv.reader(f, delimiter="\t"):
            if os.path.isfile(os.path.join(basepath, cell,line[3])):
                #print line[3]
                filename = line[3]
                readclass = line[5].split(":")[0]
                peakclass_peak = line[5].split(":")[1]
                L1_class_peak = line[5].split(":")[2]
                peakclass_sml = line[5].split(":")[3]
                L1_class_sml = line[5].split(":")[4]
                class_sml = [readclass,peakclass_peak,L1_class_peak,peakclass_sml,L1_class_sml]
                dst = "".join(class_sml)
                if not os.path.exists(os.path.join(basepath, "Train_Small", dst)):
                    os.makedirs(os.path.join(basepath, "Train_Small", dst))
                if os.path.isfile(os.path.join(basepath, cell,filename)):
                    if not os.path.isfile(os.path.join(basepath, "Train_Small", dst,filename)):
                        shutil.move(os.path.join(basepath, cell,filename), os.path.join(basepath, "Train_Small", dst))
print "Done_B!"
