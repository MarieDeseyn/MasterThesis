# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:14:05 2023

@author: r0750853
"""

lambTb = 1.5*10**(-6)
lambCe = 5.829*10**(-8)

#2
NTb2 = 10**(6)*(3.045389994294287)
NCe2 = 10**(6)*(0.842 - 0.501 * np.exp(-lambCe*(5*60+15)*60))/lambCe
#timestamps[202018]
#timestamps[239936]
np.sum(cur2021[202018:239936])/(2*1.60217663 * 10**(-19))
NGd2 = np.sum(cur2021[202018:239936])/(2*1.60217663 * 10**(-19))-NTb2-NCe2*2

#3
NTb3 = 1.114152394868627
NCe3 = 10**(6)*(0.961 - 0.842 * np.exp(-lambCe*(6*60+45)*60))/lambCe
#timestamps[239936]
#timestamps[288534]
np.sum(cur2021[239936:288534])/(2*1.60217663 * 10**(-19))
NGd3 = np.sum(cur2021[239936:288534])/(2*1.60217663 * 10**(-19))-NTb3-NCe3*2

#4
NTb4 = 1.249216316937183
NCe4 = 10**(6)*(1.045 - 0.961 * np.exp(-lambCe*(40*60+37)*60))/lambCe
#timestamps[288534]
#timestamps[580862]
np.sum(cur2021[288534:580862])/(2*1.60217663 * 10**(-19))
NGd4 = np.sum(cur2021[288534:580862])/(2*1.60217663 * 10**(-19))-NTb4-NCe4*2

#5
NTb5 = 0
NCe5 = 10**(6)*(1.002 - 1.045 * np.exp(-lambCe*(12*60+55)*60))/lambCe
NCe5 = 0
#timestamps[580862]
#timestamps[673858]
np.sum(cur2021[580862:673858])/(2*1.60217663 * 10**(-19))
NGd5 = np.sum(cur2021[580862:673858])/(2*1.60217663 * 10**(-19))-NTb5-NCe5*2

NsTb = [NTb2,NTb3,NTb4,NTb5]
NsCe = [NCe2,NCe3,NCe4,NCe5]
NsGd = [NGd2,NGd3,NGd4,NGd5]
plt.plot(np.array(NsTb)/(np.array(NsTb) + np.array(NsCe)*2 + np.array(NsGd)))
plt.plot(np.array(NsCe)/(np.array(NsTb) + np.array(NsCe)*2 + np.array(NsGd)))
plt.plot(np.array(NsGd)/(np.array(NsTb) + np.array(NsCe)*2 + np.array(NsGd)))

filelist = []
r=4 #mm 

os.chdir("C:/Users/r0750853/Documents/layeredcolorplot_morers2") 
counter = 0
incommingTb = []
with open('template.in') as f:
    lines = f.readlines()

sigma = np.sqrt(0.934*0.816*10**(14))
ren = np.arange(0,3*sigma, sigma/10)
ren = np.arange(3*sigma,4*sigma, sigma/10)
deltar = sigma/10
counter=30-1
for retje in ren:
    counter+=1
    incomingtbper = []
    for ii in range(4):
        naam = "TbGd_l"+str(counter).zfill(2)+'_'+str(ii) # rnumber layernumber
        filelist.append(naam+".in")
        outfile = lines.copy()
        outfile[0]= naam+' Tb,CeO and Gd on Zn layered, incomming energy = 60keV, 2021 collection\n'
        
        tomult = 1/(np.pi*((retje+deltar)**2-retje**2)) * (np.exp(-retje**2/(2*sigma**2))- np.exp(-(retje+deltar)**2 /(2*sigma**2)))
        print(tomult)
        Tb_fluence = NsTb[ii]*tomult
        Gd_fluence = NsGd[ii]*tomult
        Ce_fluence = NsCe[ii]*tomult
        O_fluence = Ce_fluence
        fluence = Tb_fluence+Gd_fluence+Ce_fluence+O_fluence
        print(Tb_fluence)
        incomingtbper.append(Tb_fluence)
        if ii>0:
            outfile[1] = 'cdat 1 ' + "{:.8f}".format(float(fluence)) + ' 1 inputfile\n'
            outfile[4] =''
        else:
            outfile[1] = 'cdat 0 ' +"{:.8f}".format(float(fluence)) + ' 1\n'
        outfile[5] = 'irra 2  60000. 0. '+ str(Tb_fluence/(fluence))+' \n'
        outfile[6] = 'irra 3  53806. 0. '+ str(Ce_fluence/(fluence))+' \n'
        outfile[7] = 'irra 4  6194. 0. '+ str(O_fluence/(fluence))+' \n'
        outfile[8] = 'irra 5  60000. 0. '+ str(Gd_fluence/(fluence))+' \n'
        outfile[10] = 'rand '+str(10000)+'\n'
    incommingTb.append(incomingtbper)
    
        f = open("C:/Users/r0750853/Documents/layeredcolorplot_morers2/"+naam+".in", "a")
        f.writelines(outfile)
        f.close()
        
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1

os.chdir("C:/Users/r0750853/Documents/layeredcolorplot_morers2") 
counter = 0
incommingTb = []
with open('template.in') as f:
    lines = f.readlines()

sigma = np.sqrt(0.934*0.816*10**(14))
ren = np.arange(0,3*sigma, sigma/10)
ren = np.arange(4*sigma,5*sigma, sigma/10)
deltar = sigma/10
counter=40-1
for retje in ren:
    counter+=1
    incomingtbper = []
    for ii in range(4):
        naam = "TbGd_l"+str(counter).zfill(2)+'_'+str(ii) # rnumber layernumber
        filelist.append(naam+".in")
        outfile = lines.copy()
        outfile[0]= naam+' Tb,CeO and Gd on Zn layered, incomming energy = 60keV, 2021 collection\n'
        
        tomult = 1/(np.pi*((retje+deltar)**2-retje**2)) * (np.exp(-retje**2/(2*sigma**2))- np.exp(-(retje+deltar)**2 /(2*sigma**2)))
        print(tomult)
        Tb_fluence = NsTb[ii]*tomult
        Gd_fluence = NsGd[ii]*tomult
        Ce_fluence = NsCe[ii]*tomult
        O_fluence = Ce_fluence
        fluence = Tb_fluence+Gd_fluence+Ce_fluence+O_fluence
        print(Tb_fluence)
        incomingtbper.append(Tb_fluence)
        if ii>0:
            outfile[1] = 'cdat 1 ' + "{:.8f}".format(float(fluence)) + ' 1 inputfile\n'
            outfile[4] =''
        else:
            outfile[1] = 'cdat 0 ' +"{:.8f}".format(float(fluence)) + ' 1\n'
        outfile[5] = 'irra 2  60000. 0. '+ str(Tb_fluence/(fluence))+' \n'
        outfile[6] = 'irra 3  53806. 0. '+ str(Ce_fluence/(fluence))+' \n'
        outfile[7] = 'irra 4  6194. 0. '+ str(O_fluence/(fluence))+' \n'
        outfile[8] = 'irra 5  60000. 0. '+ str(Gd_fluence/(fluence))+' \n'
        outfile[10] = 'rand '+str(10000)+'\n'
    #incommingTb.append(incomingtbper)
    
        f = open("C:/Users/r0750853/Documents/layeredcolorplot_morers2/"+naam+".in", "a")
        f.writelines(outfile)
        f.close()
        
strnamen = ""
ct = 0
for ii in filelist:
    strnamen = strnamen + "\" \"" + filelist[ct]
    ct+=1
