# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 07:55:41 2022

@author: r0750853
"""

# program that creates the needed .lay files
numblayers = 4 # aantal layers
aantalsimulaties = 40



import os
ls_files = os.listdir(path="/mnt/c/Users/r0750853/linux/TRIDYN")
layfiles = []
for file in ls_files:
    if file[len(file)-3:len(file)]=='lay':
        layfiles.append(file)
tolookcounters = []
for ii in range(aantalsimulaties):
    if len(layfiles)<(ii+1)*(numblayers):
        tolookcounters.append(ii)
fixcounter = min(tolookcounters)
print('fixcounter = '+ str(fixcounter).zfill(2))
#fixcounter is de hoeveelste simulatie waarnaar we kijken
alllayfilesnuttig = []
for file in ls_files:
    if file[len(file)-3:len(file)]=='lay' and file[6:8]==str(fixcounter).zfill(2):
        alllayfilesnuttig.append(file)
print('alllayfilesnuttig = '+str(alllayfilesnuttig))
if len(alllayfilesnuttig)==0: #als er geen zijn --> maak een 0 lay file die leeg is en niet gebruikt wordt
    print('ik maak een nulde .lay file')
    f = open("/mnt/c/Users/r0750853/linux/TRIDYN/TbGd_l"+str(fixcounter).zfill(2)+"_0.lay", "a")
    f.writelines(" ") #empty file
    f.close()
else: #er is al een .lay file
    vorigelaagnummer = (alllayfilesnuttig[-1])[9:10]
    print('ik maak een .lay file op basis van de laag: '+ vorigelaagnummer)
    os.chdir("/mnt/c/Users/r0750853/linux/TRIDYN/Simulated_data/layeredcolorplotmeerr2/Depth_profile/"+'TbGd_l'+str(fixcounter).zfill(2)+'_'+vorigelaagnummer) 
    with open('TbGd_l'+str(fixcounter).zfill(2)+'_'+vorigelaagnummer+'_pr020.dat') as f:
        lines = f.readlines()
    outfile = lines.copy()
    bla = []
    for ii in range(len(outfile)):
        if ii>=5:
            bla.append(outfile[ii][28:len(outfile[ii])])
    
    os.chdir("/mnt/c/Users/r0750853/linux/TRIDYN/Simulated_data/layeredcolorplotmeerr2/Areal_density") 
    with open('TbGd_l'+str(fixcounter).zfill(2)+'_'+vorigelaagnummer+'_ardn.dat') as f:
        lines = f.readlines()  
    arndat = lines.copy()
    arndatTb = float(arndat[-1][33:45].rstrip("-").lstrip("-"))
    arndatCe = float(arndat[-1][45:59].rstrip("-").lstrip("-"))
    arndatO = float(arndat[-1][60:71].rstrip("-").lstrip("-"))
    arndatGd = float(arndat[-1][71:-1].rstrip("-").lstrip("-"))
    #vanuit arndat
    os.chdir("/mnt/c/Users/r0750853/linux/TRIDYN/Simulated_data/layeredcolorplotmeerr2/Depth_profile/"+'TbGd_l'+str(fixcounter).zfill(2)+'_'+vorigelaagnummer) 
    with open('TbGd_l'+str(fixcounter).zfill(2)+'_'+vorigelaagnummer+'_pr020.dat') as f:
        depthprof = f.readlines()
    depthstep = 10 #in pr files hoeveel er telkens in de diepte gesprongen wordt
    arealdensprTb = 0
    arealdensprCe = 0
    arealdensprO = 0
    arealdensprGd = 0
    for ii in range(5,len(depthprof)):
        arealdensprTb+=depthstep*float(depthprof[ii][13:28].rstrip("-").lstrip("-"))*float(depthprof[ii][35:44].rstrip("-").lstrip("-"))
        arealdensprCe+=depthstep*float(depthprof[ii][13:28].rstrip("-").lstrip("-"))*float(depthprof[ii][44:52].rstrip("-").lstrip("-"))
        arealdensprO+=depthstep*float(depthprof[ii][13:28].rstrip("-").lstrip("-"))*float(depthprof[ii][52:60].rstrip("-").lstrip("-"))
        arealdensprGd+=depthstep*float(depthprof[ii][13:28].rstrip("-").lstrip("-"))*float(depthprof[ii][60:67].rstrip("-").lstrip("-"))
    teveelTb = arealdensprTb-arndatTb
    teveelCe = arealdensprCe-arndatCe
    teveelO = arealdensprO-arndatO
    teveelGd = arealdensprGd-arndatGd
    print(teveelTb,teveelCe,teveelO,teveelGd)
    toaddTb = teveelTb/(100*depthstep)
    toaddCe = teveelCe/(100*depthstep)
    toaddO = teveelO/(100*depthstep)
    toaddGd = teveelGd/(100*depthstep)
    teschrijven = bla.copy()
    for ii in range(len(teschrijven)):
        print('algemene corr factor = '+str(1/float(depthprof[ii+5][13:27])))
        teschrijven[ii] = bla[ii][0:8].rstrip("-").lstrip("-") +'\t'+ str(abs(float(bla[ii][8:16].rstrip("-").lstrip("-"))-toaddTb/float(depthprof[ii+5][13:27].rstrip("-").lstrip("-")))) +'\t' + str(abs(float(bla[ii][16:24].rstrip("-").lstrip("-"))-toaddCe/float(depthprof[ii+5][13:27].rstrip("-").lstrip("-"))))+'\t' + str(abs(float(bla[ii][24:32].rstrip("-").lstrip("-"))-toaddO/float(depthprof[ii+5][13:27].rstrip("-").lstrip("-"))))+'\t' + str(abs(float(bla[ii][32:40].rstrip("-").lstrip("-"))-toaddGd/float(depthprof[ii+5][13:27].rstrip("-").lstrip("-"))))+'\n'
    #print('het lay file noemt' + "/mnt/c/Users/r0750853/linux/TRIDYN/TbGd_l"+str(fixcounter)+'_'+str(int(vorigelaagnummer)+1).zfill(2) +".lay") 
    #f = open("/mnt/c/Users/r0750853/linux/TRIDYN/TbGd_l"+str(fixcounter)+'_'+str(int(vorigelaagnummer)+1).zfill(2) +".lay", "a")
    print('het lay file noemt' + "/mnt/c/Users/r0750853/linux/TRIDYN/TbGd_l"+str(fixcounter).zfill(2)+'_'+str(int(vorigelaagnummer)+1) +".lay") 
    f = open("/mnt/c/Users/r0750853/linux/TRIDYN/TbGd_l"+str(fixcounter).zfill(2)+'_'+str(int(vorigelaagnummer)+1) +".lay", "a")
    f.writelines(teschrijven)
    f.close()

