#!/usr/local/bin/python3
import os
from biofunction import motif_scan
from tools import motif_stool,multi,merge

def run():
    while True:
        try:
            q = input('Welcome to my bioinformatics study programme!\n'
                      'It provides sequence searching and analysis for protein functions and species that YOU WANT.\n '
                      'However, it has a length maximum for 200 sequences.   ''\n'
                      'Type ANYTHING to start the programme ''\n'
                      'Type "q" to quit''\n'
                      '> ').lower()
            if q == 'q':
                break
            while True:
                print('Please choose the searching mode  ')
                switch = input("   0: will repeat and each time is new protein and species;"
                               "\n   1: will repeat for same protein and different species;"
                               "\n   2: will repeat for different proteins and same specices\n "
                               "  others(like q,*,7...) will only search once\n>:")

                names = locals()
                g = multi(switch)
                count = 0
                f0, a0, length, dic = next(g)

                if switch == '0' or switch == '1' or switch == '2':
                    while q != 'q':
                        count += 1
                        names['a' + str(count)], lem, dim = next(g)[1:]
                        length += lem
                        dic.update(dim)
                        if length > 200:
                            print('Too much sequences, think more about the running time.')
                            print('Auto merging started')
                            break
                        q = input('>> Do you want to continue adding? Press q to quit\n> ').lower()
                    print('The total sequences are {0}, including {1} species '.format(length,len(dic.keys())))
                    d=input('>>Do you want to continue? Press n to stop\n> ').lower()
                    if d == 'n':
                        continue
                    print('merging...')
                    mg = merge(list(names['a' + str(i)] for i in range(1, count + 1)))
                    print('merging completed')
                    break
                else:
                    mg = merge(a0)
                    print('merging completed')
                    break

            q = input('>> Do you want to do clusting? Press n to stop\n> ').lower()
            if q != 'n':
                print('clusting...')
                f0.clust()
                print('Similarity plot generating...')
                f0.plotting()
                print('Done')
                q = input('>> Do you want to do motif scanning? Press n to stop\n> ').lower()
                if q != 'n':
                    ms = motif_stool('merge.fa')
                    while True:
                        try:
                            file = next(ms)
                            motif_scan()
                        except StopIteration:
                            print('Scanning finished')
                            os.system('rm -f 1.fa')
                            os.system('rm -f 0.motif')
                            p = input('>> Do you want to save total searching sequence results? Press n to stop\n >').lower()
                            if p !='y':
                                os.system('rm -f merge.fa')
                            break
            else:
                break
        except ValueError:
            print('Please type correctly!')


run()
