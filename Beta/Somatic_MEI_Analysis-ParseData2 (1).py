#!/usr/bin/python2.7
from __future__ import division
import glob, os, gc, sys
import os.path
import csv
import numpy as np
from time import time
from subprocess import (call, Popen, PIPE)
from itertools import product
#from IPython.display import Image
from PIL import Image
#from IPython.display import Image as IPImage
import shutil
import re
import xml.etree.ElementTree as ET
import time
import pysam



##Path to Data
basepath = "/home/ec2-user/SageMaker/BSMN_Project/"
windows = "hs37d5_windows.bed"
windows_correct = "hs37d5_windows_correct.bed"

L1HS_bedgraph = "_L1HS_mapped.bedgraph"

loci = ".loci"
overlap = "_overlap_"
overlap_sml = "_overlap_sml_"
overlap_lrg = "_overlap_lrg_"
L1HS_bam = "-L1HS_mapped.bam"
bam = "-ready.bam"
igv = "-igv.xml"
bed = ".bed"
## rmask Paths
L1HS = "rmask_L1HS_Final.bed" #keep
L1PA2345 = "rmask_L1PA2345_Final.bed" #keep
L1_Other = "rmask_L1_Other_Final.bed" #keep
##IGV Template
IGV = "igv-template4.xml" #keep
Bulk_1571_Cerebellum = "1571_cereb_BT_40_L3" #keep
Bulk_1571_Hippocampus = "1571_hippo_BT_41_L3" #keep
SC_1571_Hippo = ["1571_hippo_SC_43_L3"] #sys.argv[1]


Data_Sets = []
Data_Sets.append([SC_1571_Hippo,Bulk_1571_Hippocampus,Bulk_1571_Cerebellum])

for dset in Data_Sets:
    for cell in dset[0]:
        print cell
        tree = ET.parse(os.path.join(basepath,IGV))
        root = tree.getroot()
        root[0][0].set('path', os.path.join(basepath, cell + L1HS_bedgraph)) #L1HS bedgraph
        root[0][1].set('path', os.path.join(basepath, cell + bam)) #SC Path
        root[0][3].set('path', os.path.join(basepath,  dset[1], dset[1] + bam)) #Bulk Brain Path
        root[0][6].set('path', os.path.join(basepath,  dset[2], dset[2] + bam)) #Bulk Fib Path
        root[1][0].set('id', os.path.join(basepath, cell + L1HS_bedgraph)) #L1HS bedgraph
        root[2][0].set('id', os.path.join(basepath, cell + bam)) #SC Path
        root[3][0].set('id', os.path.join(basepath,  dset[1], dset[1] + bam)) #Bulk Brain path
        root[4][0].set('id', os.path.join(basepath,  dset[2], dset[2] + bam)) #Bulk Fib Path
        tree.write(os.path.join(basepath, cell + igv))



        myinput = open(os.path.join(basepath, windows))
        myoutput = open(os.path.join(basepath, windows_correct), 'w')
        proc3 = Popen(['grep', '-E', '^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|X|Y)'], stdin=myinput, stdout=myoutput)
        proc3.wait()
        #
        # myinput = os.path.join(basepath,  cell, cell + peaks_correct_bed)
        # myoutput1 = os.path.join(basepath,  cell, cell + peakregions_sml)
        # myoutput2 = os.path.join(basepath,  cell, cell + peakregions_lrg)
        # with open(myoutput1, 'w') as outfile:
        #     with open(myinput, 'r') as infile:
        #         data = infile.readlines()
        #         for string in data:
        #             line = string.split('\t')
        #             pos1 = int(line[1])
        #             pos2 = int(line[2])
        #             center = int((pos1 + pos2)/2)
        #             pad = 1000
        #             start = center - pad
        #             end = center + pad
        #             row = [line[0], str(start), str(end)]
        #             outfile.write('\t'.join(row) + '\n')
        # outfile.close()
        # infile.close()
        # with open(myoutput2, 'w') as outfile:
        #     with open(myinput, 'r') as infile:
        #         data = infile.readlines()
        #         for string in data:
        #             line = string.split('\t')
        #             pos1 = int(line[1])
        #             pos2 = int(line[2])
        #             center = int((pos1 + pos2)/2)
        #             pad = 10000
        #             newstart = center - pad
        #             newend = center + pad
        #             row = [line[0], str(newstart), str(newend)]
        #             outfile.write('\t'.join(row) + '\n')
        # outfile.close()
        # infile.close()

        sc_file = pysam.AlignmentFile(os.path.join(basepath, cell + bam), "rb")
        bb_file = pysam.AlignmentFile(os.path.join(basepath, dset[1] + bam), "rb")
        bf_file = pysam.AlignmentFile(os.path.join(basepath, dset[2] + bam), "rb")
        #
        #
        # myinput = os.path.join(basepath,  cell, cell + peaks_correct_bed)
        # myoutput = os.path.join(basepath,  cell, cell + peaks_correct_data)
        #
        # with open(myoutput, 'w') as outfile:
        #     with open(myinput, 'r') as infile:
        #         data = infile.readlines()
        #         for region in data:
        #             sc_iter = sc_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
        #             bb_iter = bb_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
        #             bf_iter = bf_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2]))
        #             sc_i = 0
        #             bb_i = 0
        #             bf_i = 0
        #             for x in sc_iter: sc_i+=1
        #             for y in bb_iter: bb_i+=1
        #             for z in bf_iter: bf_i+=1
        #             sc_count = 1 if sc_i > 0 else 0
        #             bb_count = 1 if bb_i > 0 else 0
        #             bf_count = 1 if bf_i > 0 else 0
        #             row = [str(region.strip().split('\t')[0]), str(region.strip().split('\t')[1]), str(region.strip().split('\t')[2])]
        #             outfile.write('\t'.join(row) +'\t'+str(sc_count)+str(bb_count)+str(bf_count)+'\n')

        myinput = os.path.join(basepath, windows_correct)
        myoutput = open(os.path.join(basepath, cell + L1HS_bam), 'w')
        myoutput2 = os.path.join(basepath, cell + L1HS_bedgraph)
        p1 = Popen(['samtools', 'view', '-hb', '-@', '1', '-L', os.path.join(basepath,L1HS), os.path.join(basepath, cell + bam)], stdout=myoutput)
        p1.wait()
        p2 = Popen(['samtools', 'index', '-@', '1', os.path.join(basepath, cell + L1HS_bam)])
        p2.wait()
        L1HS_file = pysam.AlignmentFile(os.path.join(basepath, cell + L1HS_bam), 'rb')
        L1HS_read_names =[]
        for read in L1HS_file.fetch():
            read_name = int(str(read).split('\t')[0].split('.')[1])
            L1HS_read_names.append(read_name)
        #print len(L1HS_read_names)
        with open(myoutput2, 'w') as outfile:
            with open(myinput, 'r') as infile:
                data = infile.readlines()
                for region in data:
                    read_names = []
                    for read in sc_file.fetch(region.split('\t')[0], int(region.split('\t')[1]), int(region.split('\t')[2])):
                        read_name = int(str(read).split('\t')[0].split('.')[1])
                        read_names.append(read_name)
                    a = len(read_names)
                    L1HS_overlap = set(read_names) & set(L1HS_read_names)
                    b = len(L1HS_overlap)
                    percent = int((b/(a+1))*100)
                    row = [str(region.strip().split('\t')[0]), str(region.strip().split('\t')[1]), str(region.strip().split('\t')[2]), str(percent)]
                    outfile.write('\t'.join(row)+'\n')

        # filelist =[os.path.join(basepath,  cell, "peaks.bed"),os.path.join(basepath,  dset[1], "peaks.bed"),os.path.join(basepath,  dset[2], "peaks.bed"),L1HS,L1PA2345,L1_Other]
        # a = pybedtools.BedTool(os.path.join(basepath, cell, cell + peaks_correct_bed)) ##mergedpeaks2 overlap with loci window or with peak location???
        # count = 0
        # for fname in filelist:
        #     b = pybedtools.BedTool(fname)
        #     a_and_b = a.intersect(b, c=True)
        #     myoutput = os.path.join(basepath,  cell, cell + overlap + str(count))
        #     count +=1
        #     a_and_b.saveas(myoutput)
        #     myinput = open(myoutput)
        #     newoutput = open(myoutput+"_binary", 'w')
        #     #overlap_append
        #     awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($7 ~ "^[1-9]*$") $7 = "1"; else $7 = $7; }; 1"""
        #     proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)
        #     proc.wait()
        #     newoutput.flush()
        #
        # a_sml = pybedtools.BedTool(os.path.join(basepath,  cell, cell + peakregions_sml)) ##mergedpeaks2 overlap with loci window or with peak location???
        # count = 0
        # for fname in filelist:
        #     b = pybedtools.BedTool(fname)
        #     a_and_b = a_sml.intersect(b, c=True)
        #     myoutput = os.path.join(basepath,  cell, cell + overlap_sml + str(count))
        #     count +=1
        #     a_and_b.saveas(myoutput)
        #     myinput = open(myoutput)
        #     newoutput = open(myoutput+"_binary", 'w')
        #     #overlap_append
        #     awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($4 >= 2) $4 = "2"; else $4 = $4; }; 1"""
        #     proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)
        #     proc.wait()
        #     newoutput.flush()
        #
        # a_lrg = pybedtools.BedTool(os.path.join(basepath,  cell, cell + peakregions_lrg)) ##mergedpeaks2 overlap with loci window or with peak location???
        # count = 0
        # for fname in filelist:
        #     b = pybedtools.BedTool(fname)
        #     a_and_b = a_lrg.intersect(b, c=True)
        #     myoutput = os.path.join(basepath,  cell, cell + overlap_lrg + str(count))
        #     count +=1
        #     a_and_b.saveas(myoutput)
        #     myinput = open(myoutput)
        #     newoutput = open(myoutput+"_binary", 'w')
        #     #overlap_append
        #     awk_cmd = r"""BEGIN { OFS = "\t"; }; { if ($4 >= 2) $4 = "2"; else $4 = $4; }; 1"""
        #     proc = Popen(['awk', awk_cmd], stdin=myinput, stdout=newoutput)
        #     proc.wait()
        #     newoutput.flush()
        #
        # myinput_sml = os.path.join(basepath,  cell, cell + peakregions_sml)
        # myoutput_sml = os.path.join(basepath,  cell, cell + loci_sml)
        # with open(myoutput_sml, 'w') as outfile:
        #     with open(myinput_sml, 'r') as infile:
        #         data = infile.readlines()
        #         for region in data:
        #             row = [str(region.strip().split('\t')[0]),":",str(region.strip().split('\t')[1]),"-",str(region.strip().split('\t')[2])]
        #             outfile.write("".join(row)+'\n')
        #
        # myinput_lrg = os.path.join(basepath,  cell, cell + peakregions_lrg)
        # myoutput_lrg = os.path.join(basepath,  cell, cell + loci_lrg)
        # with open(myoutput_lrg, 'w') as outfile:
        #     with open(myinput_lrg, 'r') as infile:
        #         data = infile.readlines()
        #         for region in data:
        #             row = [str(region.strip().split('\t')[0]),":",str(region.strip().split('\t')[1]),"-",str(region.strip().split('\t')[2])]
        #             outfile.write("".join(row)+'\n')
        #
        # Popen(['split', '-l', '100', '-d', os.path.join(basepath,  cell, cell + loci_sml), os.path.join(basepath,  cell, cell + ".split_loci_sml_")]).wait()
        # Popen(['split', '-l', '100', '-d', os.path.join(basepath,  cell, cell + loci_lrg), os.path.join(basepath,  cell, cell + ".split_loci_lrg_")]).wait()
