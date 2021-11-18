#!/usr/local/bin/python3
import os
import sys

dic={}
simla={}
length2=[]
length1=[]
def cp(file):
    with open("Tyto.fa") as fa:
        fa=fa.read().replace('\n','').lstrip().split(">")
        for i in fa:
            for n,m in enumerate(i):
                if m == '[':
                    st=n
                elif m == ']':
                    dic.setdefault(i[st+1:n],{})
                    dic[i[st+1:n]][i[:st]]=i[n+1:]
                    length2.append(len(i[n+1:]))
    print(length2)

    with open(file) as sim:
        sim = sim.read().replace('\n','').replace('-','').lstrip().split(">")
        print(sim)
        for i in sim:
            for n,m in enumerate(i):
                if m == '[':
                    st=n
                elif m == ']':
                    simla.setdefault(i[st+1:n],{})
                    length1.append(len(i[n+1:]))
    print(length1)
    for m in range(len(length1)):
        print(length1[m]/length2[m])

#txg="Aves"
cp('2.fa')
#print(dic)
 #with open("Tyto.fa","w") as file:
  #  c=dic.get('Tyto alba')
   # for n,k in c.items():
    #    file.write('>'+n+'[Tyto alba]'+'\n'+k+'\n')

