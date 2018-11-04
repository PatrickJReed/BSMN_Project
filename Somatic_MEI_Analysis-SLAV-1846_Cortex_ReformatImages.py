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

SC_1846_Cortex_Train = sys.argv[1]

Data_Sets_Train = []
Data_Sets_Train.append([SC_1846_Cortex_Train,Bulk_1846_Cortex,Bulk_1846_Liver])

for dset in Data_Sets_Train:
    cell = dset[0]
    print cell
    os.chdir(os.path.join(basepath, cell))
    for file in glob.glob("*sml*.png"):
        if "mod" not in file or "blk" not in file:
            path = os.path.splitext(file)[0]
            basename = os.path.basename(path)
            outfile1 = basename + "_blk.png"
            if not os.path.isfile(os.path.join(basepath,cell,outfile1)):               
            #newfile = re.sub("_s\d+__", "-", file)
            #shutil.move(file, newfile)
                im = Image.open(file)
                pixelMap = im.load()
                img = Image.new(im.mode, im.size)
                pixelsNew = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        if pixelMap[i,j] == (250,250,250):
                            pixelsNew[i,j] = (0,0,0)
                        elif pixelMap[i,j] == (255,255,255):
                            pixelsNew[i,j] = (0,0,0)
                        else:
                            pixelsNew[i,j] = pixelMap[i,j]
                img.crop((160,130,img.size[0],img.size[1])).resize((512,512)).save(outfile1)
    print "Done!"