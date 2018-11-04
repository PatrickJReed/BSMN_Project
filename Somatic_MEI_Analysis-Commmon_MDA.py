#!/usr/bin/python2.7
from __future__ import division
import glob, os, gc, sys
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
L1HS_bam_bai = "-L1HS_mapped.bam.bai"
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

SC_Train = sys.argv[1]

Data_Sets = []
Data_Sets.append([SC_Train,Bulk_Brain_Common,Bulk_Fibro_Common])

for dset in Data_Sets:
    cell = dset[0]
    print cell
    tree = ET.parse(IGV)
    root = tree.getroot()
    root[0][0].set('path', os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph)) #L1HS bedgraph
    root[0][1].set('path', os.path.join(basepath,  cell, cell + bam)) #SC Path
    root[0][3].set('path', os.path.join(basepath,  dset[1], dset[1] + bam)) #Bulk Brain Path
    root[0][6].set('path', os.path.join(basepath,  dset[2], dset[2] + bam)) #Bulk Fib Path
    root[1][0].set('id', os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph)) #L1HS bedgraph
    root[2][0].set('id', os.path.join(basepath,  cell, cell + bam)) #SC Path
    root[3][0].set('id', os.path.join(basepath,  dset[1], dset[1] + bam)) #Bulk Brain path
    root[4][0].set('id', os.path.join(basepath,  dset[2], dset[2] + bam)) #Bulk Fib Path
    tree.write(os.path.join(basepath,  cell, cell + igv))



    myinput = open(os.path.join(basepath,  cell, cell + peaks_merged_bed))
    myoutput = open(os.path.join(basepath,  cell, cell + peaks_correct_bed), 'w')
    proc3 = Popen(['grep', '-E', '^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|X|Y)'], stdin=myinput, stdout=myoutput)
    proc3.wait()    

    myinput = os.path.join(basepath,  cell, cell + peaks_correct_bed)
    myoutput1 = os.path.join(basepath,  cell, cell + peakregions_sml)
    myoutput2 = os.path.join(basepath,  cell, cell + peakregions_lrg)
    with open(myoutput1, 'w') as outfile:
        with open(myinput, 'r') as infile:
            data = infile.readlines()
            for string in data:
                line = string.split('\t')
                pos1 = int(line[1])
                pos2 = int(line[2])                  
                center = int((pos1 + pos2)/2)
                pad = 1000
                start = center - pad
                end = center + pad
                row = [line[0], str(start), str(end)]
                outfile.write('\t'.join(row) + '\n')
    outfile.close()
    infile.close()   
    with open(myoutput2, 'w') as outfile:
        with open(myinput, 'r') as infile:
            data = infile.readlines()
            for string in data:
                line = string.split('\t')
                pos1 = int(line[1])
                pos2 = int(line[2])                  
                center = int((pos1 + pos2)/2)
                pad = 10000
                newstart = center - pad
                newend = center + pad
                row = [line[0], str(newstart), str(newend)]
                outfile.write('\t'.join(row) + '\n')
    outfile.close()
    infile.close()

    #make and define L1HS sub sam file here and L1HS read names list


    sc_file = pysam.AlignmentFile(os.path.join(basepath,  cell, cell + bam), "rb")
    bb_file = pysam.AlignmentFile(os.path.join(basepath,  dset[1], dset[1] + bam), "rb")
    bf_file = pysam.AlignmentFile(os.path.join(basepath,  dset[2], dset[2] + bam), "rb")


    myinput = os.path.join(basepath,  cell, cell + peaks_correct_bed)
    myoutput = os.path.join(basepath,  cell, cell + peaks_correct_data)

    with open(myoutput, 'w') as outfile:
        with open(myinput, 'r') as infile:
            data = infile.readlines()
            for region in data:
                sc_iter = sc_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
                bb_iter = bb_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
                bf_iter = bf_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
                sc_i = 0
                bb_i = 0
                bf_i = 0
                for x in sc_iter: sc_i+=1
                for y in bb_iter: bb_i+=1
                for z in bf_iter: bf_i+=1
                sc_count = 1 if sc_i > 0 else 0
                bb_count = 1 if bb_i > 0 else 0 
                bf_count = 1 if bf_i > 0 else 0 
                row = [str(region.strip().split('\t')[0]), str(region.strip().split('\t')[1]), str(region.strip().split('\t')[2])]  
                outfile.write('\t'.join(row) +'\t'+str(sc_count)+str(bb_count)+str(bf_count)+'\n')
    outfile.close()
    infile.close()

    myinput = os.path.join(basepath,  cell, cell + peaks_correct_bed)
    myoutput = open(os.path.join(basepath, cell, cell + L1HS_bam), 'w')
    myoutput2 = os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph)
    p1 = Popen(['samtools', 'view', '-hb', '-@', '1', '-L', L1HS, os.path.join(basepath, cell, cell + bam)], stdout=myoutput)
    p1.wait()
    myoutput.close()
    p2 = Popen(['samtools', 'index', os.path.join(basepath, cell, cell + L1HS_bam)])
    p2.wait()
    L1HS_file = pysam.AlignmentFile(os.path.join(basepath, cell, cell + L1HS_bam), 'rb')
    L1HS_read_names = []
    for read in L1HS_file.fetch(): 
        read_name = str(read).split('\t')[0]#.split('.')[1])
        L1HS_read_names.append(read_name)
    with open(myoutput2, 'w') as outfile:
        with open(myinput, 'r') as infile:
            data = infile.readlines()
            for region in data:
                read_names = ["empty"]
                for read in sc_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2])):
                    read_name = str(read).split('\t')[0]#.split('.')[1])
                    read_names.append(read_name)
                a = len(read_names)
                L1HS_overlap = set(read_names) & set(L1HS_read_names)
                b = len(L1HS_overlap)
                percent = int((b/a)*100)
                row = [str(region.strip().split('\t')[0]), str(region.strip().split('\t')[1]), str(region.strip().split('\t')[2]), str(percent)]  
                outfile.write('\t'.join(row)+'\n')
    outfile.close()
    infile.close()

    filelist =[os.path.join(basepath,  cell, "peaks.bed"),os.path.join(basepath,  dset[1], "peaks.bed"),os.path.join(basepath,  dset[2], "peaks.bed"),L1HS,L1PA2345,L1_Other]
    a = pybedtools.BedTool(os.path.join(basepath, cell, cell + peaks_correct_bed)) ##mergedpeaks2 overlap with loci window or with peak location???
    count = 0
    for fname in filelist:
        b = pybedtools.BedTool(fname)
        a_and_b = a.intersect(b, c=True)
        myoutput = os.path.join(basepath,  cell, cell + overlap + str(count))
        count +=1
        a_and_b.saveas(myoutput)
        myinput = open(myoutput)
        newoutput = open(myoutput+"_binary", 'w')
        #overlap_append
        awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($7 ~ "^[1-9]*$") $7 = "1"; else $7 = $7; }; 1"""
        proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)  
        proc.wait()
        newoutput.flush()
#         peaks = open(os.path.join(basepath, cell, cell + peaks_correct_bed))
#         peaks_sorted = open(os.path.join(basepath, cell, cell + peaks_correct_bed_sorted), 'w')
#         proc = Popen(["sort", "-k1,1", "-k2,2n"], stdin=peaks, stdout=peaks_sorted)  
#         proc.wait()
#         l1_input = open(os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph))
#         l1_sorted = open(os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph_sorted), 'w')
#         proc = Popen(["sort", "-k1,1", "-k2,2n"], stdin=l1_input, stdout=l1_sorted)  
#         proc.wait()
#         a_sorted = pybedtools.BedTool(os.path.join(basepath, cell, cell + peaks_correct_bed_sorted)) ##mergedpeaks2 overlap with loci window or with peak location???
#         l1 = pybedtools.BedTool(os.path.join(basepath,  cell, cell + peaks_L1HS_bedgraph_sorted))
#         a_and_l1 = a_sorted.map(l1, c=4, o='sum')
#         myoutput_l1 = os.path.join(basepath,  cell, cell + overlap + "L1")
#         a_and_l1.saveas(myoutput_l1)

    a_sml = pybedtools.BedTool(os.path.join(basepath,  cell, cell + peakregions_sml)) ##mergedpeaks2 overlap with loci window or with peak location???
    count = 0
    for fname in filelist:
        b = pybedtools.BedTool(fname)
        a_and_b = a_sml.intersect(b, c=True)
        myoutput = os.path.join(basepath,  cell, cell + overlap_sml + str(count))
        count +=1
        a_and_b.saveas(myoutput)
        myinput = open(myoutput)
        newoutput = open(myoutput+"_binary", 'w')
        #overlap_append
        awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($4 >= 2) $4 = "2"; else $4 = $4; }; 1"""
        proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)  
        proc.wait()
        newoutput.flush()

    a_lrg = pybedtools.BedTool(os.path.join(basepath,  cell, cell + peakregions_lrg)) ##mergedpeaks2 overlap with loci window or with peak location???
    count = 0
    for fname in filelist:
        b = pybedtools.BedTool(fname)
        a_and_b = a_lrg.intersect(b, c=True)
        myoutput = os.path.join(basepath,  cell, cell + overlap_lrg + str(count))
        count +=1
        a_and_b.saveas(myoutput)
        myinput = open(myoutput)
        newoutput = open(myoutput+"_binary", 'w')
        #overlap_append
        awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($4 >= 2) $4 = "2"; else $4 = $4; }; 1"""
        proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)  
        proc.wait()
        newoutput.flush()        

    myinput_sml = os.path.join(basepath,  cell, cell + peakregions_sml)
    myoutput_sml = os.path.join(basepath,  cell, cell + loci_sml)
    with open(myoutput_sml, 'w') as outfile:
        with open(myinput_sml, 'r') as infile:
            data = infile.readlines()
            for region in data:
                row = [str(region.strip().split('\t')[0]),":",str(region.strip().split('\t')[1]),"-",str(region.strip().split('\t')[2])]  
                outfile.write("".join(row)+'\n')

    myinput_lrg = os.path.join(basepath,  cell, cell + peakregions_lrg)
    myoutput_lrg = os.path.join(basepath,  cell, cell + loci_lrg)
    with open(myoutput_lrg, 'w') as outfile:
        with open(myinput_lrg, 'r') as infile:
            data = infile.readlines()
            for region in data:
                row = [str(region.strip().split('\t')[0]),":",str(region.strip().split('\t')[1]),"-",str(region.strip().split('\t')[2])]  
                outfile.write("".join(row)+'\n')    

    Popen(['split', '-l', '100', '-d', os.path.join(basepath,  cell, cell + loci_sml), os.path.join(basepath,  cell, cell + ".split_loci_sml_")]).wait()
    Popen(['split', '-l', '100', '-d', os.path.join(basepath,  cell, cell + loci_lrg), os.path.join(basepath,  cell, cell + ".split_loci_lrg_")]).wait()