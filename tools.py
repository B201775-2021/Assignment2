from biofunction import Para
def multi(switch):
    '''
    swtich 0: a brand new search;
    switch 1: same protein different species;
    switch 2: different proteins, same specices
    '''
    prt = input("> Please type Protein Name: ").lower()
    txg = input("> Please type Species Name: ").lower().title()
    a = Para(prt, txg)
    file,length,dic=a.typefunction()
    yield a,file,length,dic
    while switch == '0' or switch == '1' or switch=='2':
        if switch =='0':
            prt = input("> Please type another Protein Name: ").lower()
            txg = input("> Please type another Species Name: ").lower().title()
        elif switch == '1':
            txg = input("> Please type another Species Name: ").lower().title()
        else:
            prt = input("> Please type another Protein Name: ").lower()
        a = Para(prt, txg)
        file,length,dic=a.typefunction()
        yield a,file,length,dic


def motif_stool(file):
    file = open(file).read().split('>')
    for i in file[1:]:
        st=list(i)
        st.insert(0,'>')
        sto=''.join(st)
        opf=open('1.fa','w')
        opf.write(sto)
        opf.close()
        yield

def merge(names):
    merge=''
    for i in names:
        merge += i
    a=open('merge.fa','w')
    a.write(merge)
    a.close()
    return 'merge.fa'


