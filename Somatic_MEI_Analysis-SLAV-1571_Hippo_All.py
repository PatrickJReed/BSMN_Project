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
import pybedtools
import pysam
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
SC_1571_Hippo = ["1571_hippo_SC_43_L3","1571_hippo_SC_45_L3","1571_hippo_SC_46_L3","1571_hippo_SC_47_L3","1571_hippo_SC_48_L3","1571_hippo_SC_50_L3","1571_hippo_SC_51_L3","1571_hippo_SC_52_L3","1571_hippo_SC_53_L3","1571_hippo_SC_55_L3","1571_hippo_SC_56_L3","1571_hippo_SC_57_L3","1571_hippo_SC_58_L3","1571_hippo_SC_59_L3","1571_hippo_SC_61_L3","1571_hippo_SC_62_L3","1571_hippo_SC_63_L3","1571_hippo_SC_64_L3"]


Data_Sets = []
Data_Sets.append([SC_1571_Hippo,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])

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
