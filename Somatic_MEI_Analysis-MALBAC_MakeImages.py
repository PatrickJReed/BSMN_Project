#!/usr/bin/python
from __future__ import division
import glob, os, gc
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
basepath = "/home/ubuntu/efs/Common_Experiment/final" 
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

##Common Data
Bulk_Brain_Common = "04132016_mw_Bulk_cor"
Bulk_Fibro_Common = "05252016_mw_Bulk_fib"
SC_MDA_Common = ["04132016_mw_1571_SC_B4_S48","04132016_mw_1571_SC_D4_S49","04132016_mw_L1B1_SC_A2_S43","04132016_mw_L1B1_SC_C1_S45","04132016_mw_L1B1_SC_C2_S46","04132016_mw_L1B1_SC_D2_S50","04132016_mw_L1B1_SC_E2_S51","04132016_mw_L1B1_SC_E3_S52","04132016_mw_L1B1_SC_E3_S52","04132016_mw_L1B1_SC_F2_S53","04132016_mw_L1B1_SC_G1_S54","04132016_mw_L1B1_SC_H1_S55","05252016_mw_L1B1_SC_B4_S47"] 
SC_MALBAC_Common = ["2122_S1","2178_S2","2179_S3","2180_S4","2184_S5","2186_S6","2187_S7","2188_S8","2193_S9","2196_S10","2197_S11","2198_S12","2261_S13","2263_S14","2264_S15","2265_S16"] 



Data_Sets = []
Data_Sets.append([SC_MALBAC_Common,Bulk_Brain_Common,Bulk_Fibro_Common])

for dset in Data_Sets:
    for cell in dset[0]:
        print cell
        os.chdir(os.path.join(basepath, cell))
        locifile = os.path.join(basepath, cell, cell + loci_sml)
        worklist = glob.glob("*.split_loci_sml_*")
        batchsize = 10
        print len(worklist)
        for i in xrange(0, len(worklist), batchsize):
            batch = worklist[i:i+batchsize]
            print i
            index = 1
            procs = []
            for file in batch:
                print file
                with open(os.path.join(basepath, cell, file)) as f0:
                    first = f0.readline()# Read the first line.
                    for last in f0: pass
                    firstpic = cell+"_sml"+"*"+first.strip().split(':')[0]+"_"+first.strip().split(':')[1].split('-')[0]+"_"+first.strip().split(':')[1].split('-')[1]+".png"
                    lastpic = cell+"_sml"+"*"+last.strip().split(':')[0]+"_"+last.strip().split(':')[1].split('-')[0]+"_"+last.strip().split(':')[1].split('-')[1]+".png"
                    if not (glob.glob(os.path.join(basepath, cell, firstpic)) or glob.glob(os.path.join(basepath, cell, lastpic))):
                        p = Popen(['igv_plotter', '-o', cell+"_sml_", '-L', file, '-v', '--max-panel-height', '1000', '--igv-jar-path', '/home/ubuntu/efs/SLAV_Data/IGV_2.4-rc6/igv.jar', '-m', '6G', '-g', 'hg19', os.path.join(basepath, cell, cell + igv)])
                        procs.append(p)
            for pp in procs:
                pp.wait()
                #wait_timeout(pp,300)
