# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:03:54 2022

@author: r0750853
"""
filelist = []
os.chdir("C:/Users/r0750853/Documents/Effect_of_fractionGd_Tb") 
with open('template.in') as f:
    lines = f.readlines()
lijstnamen = []
for fraction in np.linspace(0.001,0.5,20):
    counter = 0
    for randomchar in np.linspace(10000,50000,10):
        naam = "TbfGd_"+str(counter)+"_"+str(int(round(fraction*100))).zfill(2)
        counter+=1
        randget = (round(randomchar))
        outfile = lines.copy()
        outfile[0]= naam+ ' Tb and Gd on Zn for different relative fractions\n'
        outfile[5] = 'irra 2 '+str(60000)+'. 0. '+str(fraction)+'\n'
        outfile[6] = 'irra 3 '+str(60000)+'. 0. '+str(1-fraction)+'\n'
        outfile[8] = 'rand '+str(randget)+'\n'
        f = open("C:/Users/r0750853/Documents/Effect_of_fractionGd_Tb/"+naam+".in", "a")
        f.writelines(outfile)
        f.close()
        filelist.append(naam+".in")

strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1
    