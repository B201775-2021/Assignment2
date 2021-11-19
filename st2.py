#!/usr/local/bin/python3
import os
import sys
import subprocess
import numpy as np
import re

class Para():

    def __init__(self,protein,taxon):
        self.protein = protein
        self.taxon = taxon
        self.filename=self.taxon+'.fa'
        self.dic = {}

    def cp(self,fa):
        dic=self.dic
        st=0
        fa = fa.replace('\n', '').lstrip().split(">")
        print('Result: {} sequences are found, including: '.format(len(fa)))
        for i in fa:
            for n, m in enumerate(i):
                if m == '[':
                    st = n
                elif m == ']':
                    dic.setdefault(i[st + 1:n], {})
                    dic[i[st + 1:n]][i[:st]] = i[n + 1:]
                    print('\t'+str(i[:n]))
        return len(fa), dic


    def typefunction(self):

        while True:
            c1="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta > {0}.fa".format(self.taxon, self.protein)
            c2="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta".format(self.taxon, self.protein)
            yon=input("> Do you want to save the sequence file? y or n: ").lower()
            print(" Input Completed", "\n", "Please wait ......")
            if yon == "y":
                os.system(c1)
                with open(self.filename) as fa:
                    fa = fa.read()
            else:
                fa = subprocess.check_output(c2,shell=True).decode("utf-8")
            length, dic = Para.cp(self, fa)
            if length > 1000:
                print('To protect the serve, please search smaller sequence sets')
            else:
                break


    def clust(self):
        clust = 'clustalo -i {}'.format(self.filename)
        clust_o=subprocess.check_output(clust,shell=True).decode("utf-8")
        print(clust_o)
        outputfile=input("> What is the name of output file [default is 'mod_species name']")
        if outputfile == '':
            outputfile = 'mod_'+self.filename
        wf=open(outputfile,"w")
        wf.write(clust_o)
        wf.close()
        print(outputfile+'Created!''\n')

    def plotting(self):
        while True:
            try:
                winsize=7
                filename=self.filename
                while winsize > 5:
                    winsize=int(input('> Do you want the plot curves smooth or not? ["0" for no , "5" for super smooth] '))
                wz=winsize*10+4
                graph = 'svg'
                gdir = input('> Where do you want to save the plot? [default is the current directory]')
                if gdir == '':
                    gdir = './'
                gofname=input('> What is the name of the plot? [default is "plot_species name"]')
                if gofname == '':
                    gofname = 'plot_{}'.format(self.taxon)
                plot='plotcon {0} -winsize {1} -graph {2} -gdirectory {3} -goutfile {4}'.format(filename,wz,graph,gdir,gofname)
                os.system(plot)
                break
            except ValueError:
                print('> Please type the correct command')

def motif_scan(file=''):
    c1 = 'patmatmotifs {} -outseq 0.motif'.format(file)
    c2='rm -f 0.motif'
    os.system(c1)
    mdict={}
    st=0
    ed=0
    name=0
    a=open('0.motif').read()
    print(type(a))
    motif=list(re.finditer(r'Motif = ',a))
    start=list(re.finditer('Start = position',a))
    end=list(re.finditer('End = position',a))
    print(motif,start,end)
    for m in range(len(motif)):
        ax=[motif[m], start[m], end[m]]
        for i in range(len(ax)):
            b = e = ax[i].end()
            if i == 1:
                b += 1
                while a[b] != ' ':
                    b += 1
                st=a[e+1:b]
            elif i == 2:
                b += 1
                while a[b] != ' ':
                    b += 1
                ed=a[e+1:b]
            else:
                while a[b] != '\n':
                    b += 1
                name=a[e:b]
        mdict.setdefault('{} ~ {}'.format(st,ed),0)
        mdict['{} ~ {}'.format(st,ed)] = name
    print(mdict)
    os.system(c2)


def multi(switch):
    '''
    swtich 0: a brand new search;
    switch 1: same protein different species;
    switch 2: different proteins, same specices
    '''
    prt = input("> Please type Protein Name: ").lower()
    txg = input("> Please type Species Name: ").lower().title()
    a = Para(prt, txg)
    a.typefunction()

    while True:
        if switch =='0':
            prt = input("> Please type another Protein Name: ").lower()
            txg = input("> Please type another Species Name: ").lower().title()
        if switch == '1':
            txg = input("> Please type another Species Name: ").lower().title()
        if switch == '2':
            prt = input("> Please type another Protein Name: ").lower()
        a = Para(prt, txg)
        a.typefunction()
        yield a
while True:
    q=input('Welcome to my bioinfo study programme!''\n'
            'Type "s" to start the programme ''\n'
            'Type "q" to quit''\n'
            '> ')
    switch = input("swtich 0: a brand new search;"
                   "\nswitch 1: same protein different species;"
                   "\nswitch 2: different proteins, same specices\n >:")
    g = multi(switch)   
    
    while q != 'q':
        a = next(g)
        print(a.dic)
        q = input('Do you want to continue adding? > ')
