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

Bulk_5125_Cortex = "5125_cortex_BT_122_L3"
Bulk_5125_Hippocampus = "5125_hippo_BT_139_L3"
Bulk_5125_Liver = "5125_liver_BT_164_L3"

SC_5125_Hippo = sys.argv[1]

Data_Sets = []
Data_Sets.append([SC_5125_Hippo,Bulk_5125_Hippocampus,Bulk_5125_Liver])

for dset in Data_Sets:
    cell = dset[0]
    print cell
    # os.chdir(os.path.join(basepath, cell))
    # for file in glob.glob("*s*__*.png"):
    #     newfile = re.sub("_s\d+__", "-", file)
    #     shutil.move(file, newfile)
    # for file in glob.glob("*-*.png"):
    #     img = Image.open(file)
    #     width = img.size[0]
    #     height = img.size[1]
    #     img2 = img.crop((160,130,width,height))
    #     path = os.path.splitext(file)[0]
    #     basename = os.path.basename(path)
    #     outfile1 = basename + "_cropped.png"
    #     img2.save(outfile1)
        #os.remove(file)

    mergedpeak_data = os.path.join(basepath, cell, cell + peaks_correct_data)
    regions_sml = os.path.join(basepath, cell, cell + peakregions_sml)
    regions_lrg = os.path.join(basepath, cell, cell + peakregions_lrg)

    count=1
    with open(mergedpeak_data) as r0,open(regions_sml) as r_sml,open(regions_lrg) as r_lrg:
        Files= {}
        for rr0,rr_sml,rr_lrg in zip(r0,r_sml,r_lrg):
            line = rr0.strip().split('\t')[0]+"\t"+rr0.strip().split('\t')[1]+"\t"+rr0.strip().split('\t')[2]+"\t"+cell+"_sml-"+rr_sml.strip().split('\t')[0]+"_"+rr_sml.strip().split('\t')[1]+"_"+rr_sml.strip().split('\t')[2]+"_cropped.png"+"\t"+cell+"_lrg-"+rr_lrg.strip().split('\t')[0]+"_"+rr_lrg.strip().split('\t')[1]+"_"+rr_lrg.strip().split('\t')[2]+"_cropped.png"+"\t"+rr0.strip().split('\t')[3]
            Files[str(count)] = line
            count+=1

    a = os.path.join(basepath, cell, cell+"_overlap_0_binary")
    b = os.path.join(basepath, cell, cell+"_overlap_1_binary")
    c = os.path.join(basepath, cell, cell+"_overlap_2_binary")
    d = os.path.join(basepath, cell, cell+"_overlap_3_binary")
    e = os.path.join(basepath, cell, cell+"_overlap_4_binary")
    f = os.path.join(basepath, cell, cell+"_overlap_5_binary")
    count=1
    with open(a) as f1,open(b) as f2,open(c) as f3,open(d) as f4,open(e) as f5,open(f) as f6:
        Peaks = {}
        for aa,bb,cc,dd,ee,ff in zip(f1,f2,f3,f4,f5,f6):
            line = aa.strip().split('\t')[6]+bb.strip().split('\t')[6]+cc.strip().split('\t')[6]+"\t"+dd.strip().split('\t')[6]+ee.strip().split('\t')[6]+ff.strip().split('\t')[6]
            Peaks[str(count)] = line
            count+=1

    a_sml = os.path.join(basepath, cell, cell+"_overlap_sml_0_binary")
    b_sml = os.path.join(basepath, cell, cell+"_overlap_sml_1_binary")
    c_sml = os.path.join(basepath, cell, cell+"_overlap_sml_2_binary")
    d_sml = os.path.join(basepath, cell, cell+"_overlap_sml_3_binary")
    e_sml = os.path.join(basepath, cell, cell+"_overlap_sml_4_binary")
    f_sml = os.path.join(basepath, cell, cell+"_overlap_sml_5_binary")
    count=1
    with open(a_sml) as f1,open(b_sml) as f2,open(c_sml) as f3,open(d_sml) as f4,open(e_sml) as f5,open(f_sml) as f6:
        Small = {}
        for aa,bb,cc,dd,ee,ff in zip(f1,f2,f3,f4,f5,f6):
            line = aa.strip().split('\t')[3]+bb.strip().split('\t')[3]+cc.strip().split('\t')[3]+"\t"+dd.strip().split('\t')[3]+ee.strip().split('\t')[3]+ff.strip().split('\t')[3]
            Small[str(count)] = line
            count+=1

    a_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_0_binary")
    b_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_1_binary")
    c_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_2_binary")
    d_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_3_binary")
    e_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_4_binary")
    f_lrg = os.path.join(basepath, cell, cell+"_overlap_lrg_5_binary")
    count=1
    with open(a_lrg) as f1,open(b_lrg) as f2,open(c_lrg) as f3,open(d_lrg) as f4,open(e_lrg) as f5,open(f_lrg) as f6:
        Large = {}
        for aa,bb,cc,dd,ee,ff in zip(f1,f2,f3,f4,f5,f6):
            line = aa.strip().split('\t')[3]+bb.strip().split('\t')[3]+cc.strip().split('\t')[3]+"\t"+dd.strip().split('\t')[3]+ee.strip().split('\t')[3]+ff.strip().split('\t')[3]
            Large[str(count)] = line
            count+=1

    with open(os.path.join(basepath, cell, cell+"_Input_metadata.txt"),"w") as f8:
        for key in Files:
            encoding = Files[key]+":"+Peaks[key].strip().split('\t')[0]+":"+Small[key].strip().split('\t')[0]+":"+Peaks[key].strip().split('\t')[1]+"\n"
        #for (Fi, Fj),(Pi,Pj),(Si,Sj),(Li,Lj) in zip(Files.items(),Peaks.items(),Small.items(),Large.items()):
            #encoding = Fj+":"+Pj.strip().split('\t')[0]+":"+Sj.strip().split('\t')[0]+":"+Lj.strip().split('\t')[0]+":"+Pj.strip().split('\t')[1]+":"+Sj.strip().split('\t')[1]+":"+Lj.strip().split('\t')[1]+"\n"
            f8.write(encoding)
print "DONE!"
