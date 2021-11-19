import os
import re
import subprocess


class Para():

    def __init__(self,protein,taxon):
        self.protein = protein
        self.taxon = taxon
        self.filename=self.taxon+'_'+self.protein.replace(' ','-')+'.fa'
        self.dic = {}

    def cp(self,fa):
        dic=self.dic
        st=0
        fa = fa.replace('\n', '').lstrip().split(">")
        for i in fa:
            for n, m in enumerate(i):
                if m == '[':
                    st = n
                elif m == ']':
                    dic.setdefault(i[st + 1:n], {})
                    dic[i[st + 1:n]][i[:st]] = i[n + 1:]
                    print('\t'+str(i[:n+1]))
        print('Result: {0} sequences are found, including: {1} species '.format(len(fa)-1,len(dic.keys())))
        return len(fa), dic


    def typefunction(self):

        while True:
            c1="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta > {2}".format(self.taxon, self.protein,self.filename)
            c2="esearch -db protein -query '{0}[organism] AND {1}[PROT]' | efetch -format fasta".format(self.taxon, self.protein)
            yon=input(">> Do you want to save the sequence file? Press n to stop: ").lower()
            print("Input Completed", "\n","Please wait ..............")
            if yon == "y":
                os.system(c1)
                with open(self.filename) as fa:
                    fa = fa.read()
            else:
                fa = subprocess.check_output(c2,shell=True).decode("utf-8")
            length, dic = Para.cp(self, fa)
            if length > 200:
                print('To protect the serve, please search smaller sequence sets')
            else:
                return fa,length,dic


    def clust(self):
        clust = 'clustalo -i merge.fa'
        clust_o=subprocess.check_output(clust,shell=True).decode("utf-8")
        # print(clust_o)
        outputfile=input(">> What is the name of output file [default is 'mod_species name']")
        if outputfile == '':
            outputfile = 'clusted.fa'
        wf=open(outputfile,"w")
        wf.write(clust_o)
        wf.close()
        print(outputfile+' Created!')

    def plotting(self):
        while True:
            try:
                winsize=7
                filename='clusted.fa'
                while winsize > 5:
                    winsize=int(input('>> Do you want the plot curves smooth or not? ["0" for no , "5" for super smooth] '))
                wz=winsize*10+4
                graph = 'svg'
                gdir = input('>> Where do you want to save the plot? [default is the current directory]')
                if gdir == '':
                    gdir = './'
                gofname=input('>> What is the name of the plot? [default is "plot_species name"]')
                if gofname == '':
                    gofname = 'plot_{}'.format(self.taxon)
                plot='plotcon {0} -winsize {1} -graph {2} -gdirectory {3} -goutfile {4}'.format(filename,wz,graph,gdir,gofname)
                os.system(plot)
                break
            except ValueError:
                print(' Please type the correct command !')

def motif_scan():
    c1 = 'patmatmotifs 1.fa -outfile 0.motif'
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
    # print(motif,start,end)
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
    print('{} motif(s) founded!\n'.format(len(mdict)),mdict)
