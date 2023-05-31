# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:17:51 2022

@author: r0750853
"""

import os
import numpy as np

os.chdir("C:/Users/r0750853/linux/Experimentalconfirmation_Tridyn_Yb") 
with open('template.in') as f:
    lines = f.readlines()
lijstnamen = []
Energies = [30,60,100]
for energy in Energies:
    counter = 0
    for randomchar in np.linspace(10000,50000,10):
        randget = (round(randomchar))
        for whichelnt in ['Al','Zn']:
            name = 'ex'+ whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + ' Experimental confirmation, for different energies implantation of Yb in Zn or Al\n'
            outfile[3] = 'atda '+ whichelnt + ' Yb\n'
            outfile[5] = 'irra 2 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Experimentalconfirmation_Tridyn_Yb/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        counter+=1
            
filelist = lijstnamen
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1
