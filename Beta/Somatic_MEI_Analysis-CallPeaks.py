#!/usr/bin/python2.7
import glob, os, gc
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
Bulk_1846_Cerebellum = "1846_cereb_BT_13_L3"
Bulk_1846_Cortex = "1846_cortex_BT_71_L3"
Bulk_1846_Hippocampus = "1846_hippo_BT_19_L3"
Bulk_1846_Liver = "1846_liver_BT_22_L3"
Bulk_5125_Cortex = "5125_cortex_BT_122_L3"
Bulk_5125_Hippocampus = "5125_hippo_BT_139_L3"
Bulk_5125_Liver = "5125_liver_BT_164_L3"

SC_1571_Hippo_All = ["1571_hippo_SC_43_L3","1571_hippo_SC_45_L3","1571_hippo_SC_46_L3","1571_hippo_SC_47_L3","1571_hippo_SC_48_L3","1571_hippo_SC_50_L3","1571_hippo_SC_51_L3","1571_hippo_SC_52_L3","1571_hippo_SC_53_L3","1571_hippo_SC_55_L3","1571_hippo_SC_56_L3","1571_hippo_SC_57_L3","1571_hippo_SC_58_L3","1571_hippo_SC_59_L3","1571_hippo_SC_61_L3","1571_hippo_SC_62_L3","1571_hippo_SC_63_L3","1571_hippo_SC_64_L3"]
SC_1846_Cortex_All = ["1846_cortex_SC_72_L3","1846_cortex_SC_73_L3","1846_cortex_SC_74_L3","1846_cortex_SC_75_L3","1846_cortex_SC_78_L3","1846_cortex_SC_79_L3","1846_cortex_SC_80_L3","1846_cortex_SC_81_L3","1846_cortex_SC_82_L3","1846_cortex_SC_83_L3","1846_cortex_SC_84_L3","1846_cortex_SC_85_L3","1846_cortex_SC_86_L3"]
SC_1846_Hippo_All = ["1846_hippo_SC_100_L3","1846_hippo_SC_101_L3","1846_hippo_SC_102_L3","1846_hippo_SC_103_L3","1846_hippo_SC_104_L3","1846_hippo_SC_105_L3","1846_hippo_SC_106_L3","1846_hippo_SC_107_L3","1846_hippo_SC_108_L3","1846_hippo_SC_109_L3","1846_hippo_SC_110_L3","1846_hippo_SC_111_L3","1846_hippo_SC_112_L3","1846_hippo_SC_113_L3","1846_hippo_SC_88_L3","1846_hippo_SC_89_L3","1846_hippo_SC_90_L3","1846_hippo_SC_91_L3","1846_hippo_SC_92_L3","1846_hippo_SC_93_L3","1846_hippo_SC_94_L3","1846_hippo_SC_95_L3","1846_hippo_SC_99_L3"]
SC_5125_Cortex_All = ["5125_cortex_SC_125_L3","5125_cortex_SC_126_L3","5125_cortex_SC_127_L3","5125_cortex_SC_128_L3","5125_cortex_SC_129_L3","5125_cortex_SC_130_L3","5125_cortex_SC_131_L3","5125_cortex_SC_132_L3","5125_cortex_SC_133_L3","5125_cortex_SC_134_L3","5125_cortex_SC_135_L3","5125_cortex_SC_136_L3","5125_cortex_SC_138_L3"]
SC_5125_Hippo_All = ["5125_hippo_SC_140_L3","5125_hippo_SC_141_L3","5125_hippo_SC_142_L3","5125_hippo_SC_143_L3","5125_hippo_SC_144_L3","5125_hippo_SC_145_L3","5125_hippo_SC_147_L3","5125_hippo_SC_149_L3","5125_hippo_SC_150_L3","5125_hippo_SC_151_L3","5125_hippo_SC_152_L3","5125_hippo_SC_153_L3","5125_hippo_SC_154_L3","5125_hippo_SC_155_L3","5125_hippo_SC_156_L3","5125_hippo_SC_157_L3","5125_hippo_SC_158_L3","5125_hippo_SC_159_L3","5125_hippo_SC_160_L3","5125_hippo_SC_161_L3","5125_hippo_SC_162_L3","5125_hippo_SC_163_L3"]

SC_1571_Hippo_Train = ["1571_hippo_SC_45_L3","1571_hippo_SC_48_L3","1571_hippo_SC_50_L3","1571_hippo_SC_51_L3","1571_hippo_SC_52_L3","1571_hippo_SC_55_L3","1571_hippo_SC_56_L3","1571_hippo_SC_57_L3","1571_hippo_SC_58_L3","1571_hippo_SC_59_L3"]
SC_1846_Cortex_Train = ["1846_cortex_SC_73_L3","1846_cortex_SC_78_L3","1846_cortex_SC_79_L3","1846_cortex_SC_82_L3","1846_cortex_SC_83_L3","1846_cortex_SC_85_L3"]
SC_1846_Hippo_Train = ["1846_hippo_SC_102_L3","1846_hippo_SC_103_L3","1846_hippo_SC_108_L3","1846_hippo_SC_112_L3"]
SC_5125_Cortex_Validation = ["5125_cortex_SC_129_L3","5125_cortex_SC_131_L3"]
SC_5125_Hippo_Validation = ["5125_hippo_SC_141_L3","5125_hippo_SC_144_L3","5125_hippo_SC_145_L3","5125_hippo_SC_150_L3","5125_hippo_SC_159_L3","5125_hippo_SC_160_L3","5125_hippo_SC_162_L3"]


Data_Sets_Train = []
Data_Sets_Train.append([SC_1571_Hippo_Train,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])
Data_Sets_Train.append([SC_1846_Cortex_Train,Bulk_1846_Cortex,Bulk_1846_Liver])
Data_Sets_Train.append([SC_1846_Hippo_Train,Bulk_1846_Hippocampus,Bulk_1846_Liver])

Data_Sets_Validation = []
Data_Sets_Validation.append([SC_5125_Cortex_Validation,Bulk_5125_Cortex,Bulk_5125_Liver])
Data_Sets_Validation.append([SC_5125_Hippo_Validation,Bulk_5125_Hippocampus,Bulk_5125_Liver])

Data_Sets_Test = []
SC_1571_Hippo_Test = list(set(SC_1571_Hippo_All) - set(SC_1571_Hippo_Train))
SC_1846_Cortex_Test = list(set(SC_1846_Cortex_All) - set(SC_1846_Cortex_Train))
SC_1846_Hippo_Test = list(set(SC_1846_Hippo_All) - set(SC_1846_Hippo_Train))
SC_5125_Cortex_Test = list(set(SC_5125_Cortex_All) - set(SC_5125_Cortex_Validation))
SC_5125_Hippo_Test = list(set(SC_5125_Hippo_All) - set(SC_5125_Hippo_Validation))



for dset in Data_Sets:
    tissue = dset[1]
    os.chdir(os.path.join(basepath, tissue))
    if not (glob.glob(os.path.join(basepath, tissue, "peaks.txt"))):
        print tissue
        name = os.path.join(basepath, tissue, tissue)
        bamfile = os.path.join(basepath, tissue, tissue+bam)
        #p1 = Popen(['/home/preed/homer/bin/makeTagDirectory', '.', bamfile, '-format', 'sam', '-keepAll', '-single'])
        #p1.wait()
        p2a = Popen(['/home/preed/homer/bin/findPeaks', '.', '-o', 'peaks.txt', '-style', 'dnase', '-F', '0', '-L', '0', '-C', '0', '-tagThreshold', '5'])
        p2a.wait()
        p4 = Popen(['/home/preed/homer/bin/pos2bed.pl', '-bed', os.path.join(basepath, tissue, "peaks.txt")])
        p4.wait()
    tissue = dset[2]
    os.chdir(os.path.join(basepath, tissue))
    if not (glob.glob(os.path.join(basepath, tissue, "peaks.txt"))):
        print tissue
        name = os.path.join(basepath, tissue, tissue)
        bamfile = os.path.join(basepath, tissue, tissue+bam)
        #p1 = Popen(['/home/preed/homer/bin/makeTagDirectory', '.', bamfile, '-format', 'sam', '-keepAll', '-single'])
        #p1.wait()
        p2a = Popen(['/home/preed/homer/bin/findPeaks', '.', '-o', 'peaks.txt', '-style', 'dnase', '-F', '0', '-L', '0', '-C', '0', '-tagThreshold', '5'])
        p2a.wait()
        p4 = Popen(['/home/preed/homer/bin/pos2bed.pl', '-bed', os.path.join(basepath, tissue, "peaks.txt")])
        p4.wait()
        
for dset in Data_Sets:    
    for cell in dset[0]:
        print cell
        os.chdir(os.path.join(basepath, cell))
        name = os.path.join(basepath, cell, cell)
        bamfile = os.path.join(basepath, cell, cell+bam)
        #p1 = Popen(['/home/preed/homer/bin/makeTagDirectory', '.', bamfile, '-format', 'sam', '-keepAll', '-single'])
        #p1.wait()
        p2a = Popen(['/home/preed/homer/bin/findPeaks', '.', '-o', 'peaks.txt', '-style', 'dnase', '-F', '0', '-L', '0', '-C', '0', '-tagThreshold', '5'])
        p2a.wait()
        p4 = Popen(['/home/preed/homer/bin/pos2bed.pl', '-bed', os.path.join(basepath, cell, "peaks.txt")])
        p4.wait()
        p5 = Popen(['/home/preed/homer/bin/mergePeaks', '-code', '-prefix', cell, os.path.join(basepath, cell, "peaks.txt"), os.path.join(basepath, dset[1], "peaks.txt"), os.path.join(basepath,  dset[2], "peaks.txt")])
        p5.wait()
        #myoutput = open(os.path.join(basepath, cell, cell + peaks_merged), 'w')
        #p5 = Popen(['/home/preed/homer/bin/mergePeaks', os.path.join(basepath, cell, "peaks.txt"), os.path.join(basepath, dset[1], "peaks.txt"), os.path.join(basepath,  dset[2], "peaks.txt")], stdout=myoutput)
        #p5.wait()
        myoutput = open(os.path.join(basepath, cell, cell + peaks_merged), 'w')
        p6 = Popen(['/home/preed/homer/bin/mergePeaks', os.path.join(basepath,  cell, cell+"_100"),os.path.join(basepath,  cell, cell+"_110"),os.path.join(basepath,  cell, cell+"_111")], stdout=myoutput)
        p6.wait()
        p7 = Popen(['/home/preed/homer/bin/pos2bed.pl', os.path.join(basepath,  cell, cell + peaks_merged), '-o', os.path.join(basepath,  cell, cell+peaks_merged_bed)])
        p7.wait()        
print "DONE!"
