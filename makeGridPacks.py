from sys import argv
E=int(argv[1])
process=argv[2]
sample="%iTeV_%s"%(E,process)
if len(argv)>3: test=bool(int(argv[3]))

import os

definitions="""define p = g u c d s u~ c~ d~ s~ b b~
define j = g u c d s u~ c~ d~ s~ b b~
define l+ = e+ mu+ ta+
define l- = e- mu- ta-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~

define lept = l+ l- vl vl~
define bos = Z W+ W- a
define top = t t~
"""

common='%s $ top bos h'

"""
processes={
"B":
["bos j %s"%common],

"vbf-B":
["bos j j %s QCD=nQCD"%common],

"vbf-H":    
["h j j %s QCD=nQCD"%common],

"BB":
["bos bos %s"%common],

"BBB":
["bos bos bos %s"%common],

"BH":
["bos h %s"%common],

"tB":
["top bos %s"%common],

"t":
["top j %s"%common],

"tt":
["top top %s"%common],

"ttB":
["top top bos %s"%common],

"ttH":    
["top top h %s"%common],

"H":
["h %s HIG=1 HIW=0"%common],

"LL":
["lept lept %s"%common],

"LLB":
["lept lept bos %s"%common],
}
"""

#2013 style
processes={
"B":
["bos j %s"%common],

"vbf":
["bos j j %s QCD=nQCD"%common,
"h j j %s QCD=nQCD"%common],

"BB":
["bos bos %s"%common],

"BBB":
["bos bos bos %s"%common,
"bos h %s"%common],

"tB":
["top bos %s"%common],

"t":
["top j %s"%common],

"tt":
["top top %s"%common],

"ttB":
["top top bos %s"%common,
"top top h %s"%common],

"H":
["h %s HIG=1 HIW=0"%common],
  
"LL":
["lept lept %s"%common],

"LLB":
["lept lept bos %s"%common],
}

xqcut={
    'B':40,
    'vbf':40,
    'BB':40,
    'BBB':40,
    'tB':60,
    't':60,
    'tt':80,
    'ttB':80,
    'H':40,
    'LL':40,
    'LLB':40
}
               
import os
import subprocess
f=open(sample+'.mg','w')
if __name__=='__main__':
    f.write(definitions+'\n')
    f.write('set lhapdf_py2 %s/bin/lhapdf-config\n'%os.environ['prodBase'])
    
    command=processes[process]
    n=len(command[0].split('%')[0].split())

    if process=='H':
        f.write('set auto_convert_model T\n')
        f.write('import model heft\n')
    for i in range(len(command)):
        for j in range(5-n):
            if i==0 and j==0: 
                f.write('generate p p > '+command[i].replace('nQCD',str(j))%('j '*j)+'\n')
            else: 
                f.write('add process p p > '+command[i].replace('nQCD',str(j))%('j '*j)+'\n')
            if test: break
        if test: break

    f.write('output %sTeV_%s\n'%(E,process))
    f.write('launch %sTeV_%s\n'%(E,process))
    #f.write('shower = Pythia8\n')
    f.write('reweight=ON\n')
    #f.write('madspin=ON\n')  #causes crash
    f.write('done\n')
    f.write('%s/Cards/run_card.dat\n'%os.environ['prodBase'])

    f.write('set gridpack = .true.\n')
    f.write('set bias_module HT\n')
    f.write('set bias_parameters = {\'ht_bias_enhancement_power\': 2.0}\n')
    
    if process in ['t','tB','vbf']:
        f.write('set auto_ptj_mjj False\n')
    f.write('set ebeam1 = %i\n'%(1000*E/2))
    f.write('set ebeam2 = %i\n'%(1000*E/2))

    f.write('set xqcut %i\n'%xqcut[process])
    #f.write('set JetMatching:qCut    = %i\n'%xqcut[process])
    #f.write('set JetMatching:nJetMax = %i\n'%j)
    #f.write('set Merging:nJetMax     = %i\n'%j)
    #f.write('set JetMatching:doMerge = 1\n')

    f.write('done\n')
    f.write('\n')

    pythiaCard=open('pythia8_card.dat','w')    
    for line in open(os.environ['prodBase']+'/Cards/pythia8_card.dat'):
        pythiaCard.write(line.replace('Q_CUT',str(xqcut[process])).replace('N_JET_MAX',str(j)))
    pythiaCard.close()
