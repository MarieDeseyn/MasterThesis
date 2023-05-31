# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:00:40 2022

@author: r0750853
"""

import os
import numpy as np

#on Al
os.chdir("C:/Users/r0750853/Documents/firstGdimplanted") 
with open('template.in') as f:
    lines = f.readlines()
lijstnamen = []
incE = 60
counter = 0
Gdfluencen = np.linspace(0.1,4,20)


for Gdfl in Gdfluencen:
    counter = 0
    print(str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2))
    for randomchar in np.linspace(10000,50000,10):
        naam = 'GdAl_'+str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2)+'_'+str(counter)
        counter+=1
        randget = (round(randomchar))
        incv = np.sqrt(2*incE/(139+16))
        #Energy is distributed evenly according to conservation of momentum
        ECe = 0.5*139*(incv)**2
        EO = 0.5*16*(incv)**2       
        outfile = lines.copy()
        outfile[0]= naam+ ' Gd on Al different fluences \n'
        outfile[1]= 'cdat 0 '+str(Gdfl)+' 1\n'     
        outfile[7] = 'rand '+str(randget)+'\n'
        f = open("C:/Users/r0750853/Documents/firstGdimplanted/"+naam+".in", "a")
        f.writelines(outfile)
        f.close()
        lijstnamen.append(naam+".in")

filelist = lijstnamen
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1


# make Tb implant files
with open('templateTb.in') as f:
    lines = f.readlines()
lijstnamen = []
incE = 60
counter = 0
Gdfluencen = np.linspace(0.1,4,20)
for Gdfl in Gdfluencen:
    counter = 0
    print(str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2))
    for randomchar in np.linspace(10000,50000,10):
        naam = 'Tbna_'+str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2)+'_'+str(counter)
        lijstnamen.append(naam+".in")
        counter+=1
        randget = (round(randomchar))
        incv = np.sqrt(2*incE/(139+16))
        #speed is distributed evenly
        ECe = 0.5*139*(incv)**2
        EO = 0.5*16*(incv)**2       
        outfile = lines.copy()
        outfile[0]= naam+ ' Tb on Al that has allready been irradiated with Gd with different fluences \n'
        outfile[6] = 'rand '+str(randget)+'\n'
        f = open("C:/Users/r0750853/Documents/firstGdimplanted/"+naam+".in", "a")
        f.writelines(outfile)
        f.close()
        

filelist = lijstnamen
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1


# make .lay files files
for Gdfl in Gdfluencen:
    counter = 0
    print(str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2))
    for randomchar in np.linspace(10000,50000,10):
        naam = 'GdAl_'+str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2)+'_'+str(counter)
        print(naam)
        os.chdir('C:/Users/r0750853/linux/3TRIDYN/Simulated_data/firstGdimplanted/Depth_profile/'+ str(naam))
        with(open(str(naam)+'_pr100.dat')) as f:
            lines = f.readlines()
        outfile = lines.copy()
        bla = []
        for ii in range(len(outfile)):
            if ii>=5:
                bla.append(outfile[ii][28:len(outfile[ii])])
        f = open("C:/Users/r0750853/linux/3TRIDYN/" + 'Tbna_'+str(round(Gdfl,2))[0]+str(round(Gdfl,2))[2:4].zfill(2)+'_'+str(counter) +".lay", "a")
        f.writelines(bla)
        f.close()
        counter+=1
