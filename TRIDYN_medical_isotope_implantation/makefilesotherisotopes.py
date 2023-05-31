# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:18:23 2022

@author: r0750853
"""

import os
import numpy as np

os.chdir("C:/Users/r0750853/linux/Othermedicalisotopes") 
with open('template.in') as f:
    lines = f.readlines()
lijstnamen = []
Energies = [30,60]
isotope ='Tm'
for energy in Energies:
    counter = 0
    for randomchar in np.linspace(10000,50000,10):
        randget = (round(randomchar))
        for whichelnt in ['Al','Zn']:
            name = isotope + whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + ' Othermedicalisotopes; for different energies implantation of in differentfoils\n'
            outfile[1] = 'cdat 0 12. 1\n'
            outfile[2] = 'geom 9000. 100 0\n'
            outfile[3] = 'atda '+ whichelnt  + '  ' + isotope + ' \n'
            outfile[4] = 'comp 1 0\n'
            outfile[5] = 'irra 2 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[6] = 'prec 0.0005\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Othermedicalisotopes/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        for whichelnt in ['NC']:
            name = isotope+ whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + '  Othermedicalisotopes; for different energies implantation of in differentfoils\n'
            outfile[1] = 'cdat 0 12. 1\n'
            outfile[2] = 'geom 9000. 100 0\n'
            outfile[3] = 'atda Na Cl' + '  ' + isotope + ' \n'
            outfile[4] = 'comp 0.5 0.5 0\n'
            outfile[5] = 'irra 3 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[6] = 'prec 0.0005\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Othermedicalisotopes/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        for whichelnt in ['NN']:
            name = isotope + whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + '  Othermedicalisotopes; for different energies implantation of in differentfoils\n'
            outfile[1] = 'cdat 0 12. 1\n'
            outfile[2] = 'geom 9000. 100 0\n'
            outfile[3] = 'atda Na N O' + '  ' + isotope + ' \n'
            outfile[4] = 'comp 0.2 0.2 0.6 0\n'
            outfile[5] = 'irra 4 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[6] = 'prec 0.0005\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Othermedicalisotopes/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        for whichelnt in ['de']:
            name = isotope + whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + ' Othermedicalisotopes; for different energies implantation of in differentfoils\n'
            outfile[1] = 'cdat 0 12. 1\n'
            outfile[2] = 'geom 9000. 100 0\n'
            outfile[3] = 'atda C H O' + '  ' + isotope + ' \n'
            outfile[4] = 'comp 0.3125 0.3125 0.375 0\n'
            outfile[5] = 'irra 4 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[6] = 'prec 0.0005\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Othermedicalisotopes/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        for whichelnt in ['ce']:
            name = isotope + whichelnt +'_'+str(counter) +'_'+ str(round(energy)).zfill(3)
            outfile = lines.copy()
            outfile[0] = name + ' Othermedicalisotopes; for different energies implantation of in differentfoils\n'
            outfile[1] = 'cdat 0 12. 1\n'
            outfile[2] = 'geom 9000. 100 0\n'
            outfile[3] = 'atda C H O' + '  ' + isotope + ' \n'
            outfile[4] = 'comp 0.2858 0.4762 0.238 0\n'
            outfile[5] = 'irra 4 ' + str(energy*1000)+ ' 0. 1.\n'
            outfile[6] = 'prec 0.0005\n'
            outfile[7] = 'rand '+ str(randget) +'\n'
            lijstnamen.append(name+".in")
            f = open("C:/Users/r0750853/linux/Othermedicalisotopes/"+name+".in", "a")
            f.writelines(outfile)
            f.close()
        counter+=1
            
filelist = lijstnamen
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1
