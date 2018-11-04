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

Bulk_1846_Cerebellum = "1846_cereb_BT_13_L3"
Bulk_1846_Cortex = "1846_cortex_BT_71_L3"
Bulk_1846_Hippocampus = "1846_hippo_BT_19_L3"
Bulk_1846_Liver = "1846_liver_BT_22_L3"

SC_1846_Hippo = ["1846_hippo_SC_100_L3","1846_hippo_SC_101_L3","1846_hippo_SC_102_L3","1846_hippo_SC_103_L3","1846_hippo_SC_104_L3","1846_hippo_SC_105_L3","1846_hippo_SC_106_L3","1846_hippo_SC_107_L3","1846_hippo_SC_108_L3","1846_hippo_SC_109_L3","1846_hippo_SC_110_L3","1846_hippo_SC_111_L3","1846_hippo_SC_112_L3","1846_hippo_SC_113_L3","1846_hippo_SC_88_L3","1846_hippo_SC_89_L3","1846_hippo_SC_90_L3","1846_hippo_SC_91_L3","1846_hippo_SC_92_L3","1846_hippo_SC_93_L3","1846_hippo_SC_94_L3","1846_hippo_SC_95_L3","1846_hippo_SC_99_L3"]

Data_Sets = []
Data_Sets.append([SC_1846_Hippo,Bulk_1846_Hippocampus,Bulk_1846_Liver])

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
                        p = Popen(['igv_plotter', '-o', cell+"_sml_", '-L', file, '--max-panel-height', '1000', '--igv-jar-path', '/home/ubuntu/efs/SLAV_Data/IGV_2.4-rc6/igv.jar', '-m', '6G', '-g', 'hg19', os.path.join(basepath, cell, cell + igv)])
                        procs.append(p)
            for pp in procs:
                pp.wait()
                #wait_timeout(pp,300)
