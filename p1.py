#!/usr/local/bin/python3
import os
import sys
import subprocess
import numpy as np

def typefunction():
    global txg
    prt = input(">Please type Protein Name : ").lower()
    txg = input(">Please type Species Name: ").lower().title()
    filename=txg+'.fa'
    c1="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta > {0}.fa".format(txg, prt)
    c2="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta".format(txg, prt)
    yon=input(">Do you want to save the sequence file? y or n: ").lower()
    if yon == "y":
        print("Input Completed", "\n", "Please wait ...")
        os.system(c1)
    else:
        print("Input Completed", "\n", "Please wait ...")
        global seqc
        seqc = subprocess.check_output(c2,shell=True)
        print(seqc)
    clust = 'clustalo -i {}'.format(filename)
    clust_o=subprocess.check_output(clust,shell=True)
    print(clust_o)
    outputfile=input("> What is the name of output file (default is 'mod_species name' )")
    if outputfile is None:
        outputfile = 'mod_'+filename
    with open(outputfile,'w') as wf:
        wf.write(clust_o)
typefunction()
