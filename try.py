#!/usr/local/bin/python3
import os
import subprocess

filename='Aves.fa'
clust = 'clustalo -i {}'.format(filename)
clust_o=subprocess.check_output(clust,shell=True).decode("utf-8")
print(type(clust_o))
#print(clust_o)
outputfile=input("> What is the name of output file (default is 'mod_species name' )")
if outputfile == '':
   outputfile = 'mod_'+filename
wf=open(outputfile,"w")
wf.write(clust_o)
wf.close()
