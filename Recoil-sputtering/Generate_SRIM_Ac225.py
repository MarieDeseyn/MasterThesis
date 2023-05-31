# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 18:38:10 2023

@author: r0750853
"""

#Zn

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import math
import os.path

# Define the settings class
class Settings:
    def __init__(self, alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, depthvector, numberofparticles):
        self.alpha_energy = alpha_energy                        # Energy of alpha particle
        self.atomic_number_p1 = atomic_number_p1                # Atomic number of emitted particle
        self.atomic_number_p2 = atomic_number_p2                # Atomic number of recoil particle
        self.mass_fraction = mass_fraction                      # Mass of emitted/recoil
        self.depthvector = depthvector                          # Vector containing the different depths at which the recoil particle should recoil from
        self.numberofparticles = numberofparticles              # Number of particles at each depth (same as depthvector) that recoil

# Generates information lines
def generate_toptext(string_alpha, string_recoil):
    line1 = "=========== TRIM with various Incident Ion Energies/Angles and Depths ========= \n"
    line2 = "= This file tabulates the kinetics of incident ions or atoms.                 = \n"
    line3 = "= Col.#1: Ion Number, Col.#2: Z of atom leaving, Col.#3: Atom energy (eV).    = \n"
    line4 = "= Col.#4-6: Last location:  Col.#4: X= Depth into target.                     = \n"
    line5 = "= Col.#7-9: Cosines of final trajectory.                                      = \n"
    line6 = "================ Typical Data File is shown below  ============================ \n"
    line7_1 = string_alpha
    line7_2 = string_recoil
    line8 = "Event  Atom  Energy  Depth   Lateral-Position   ----- Atom Direction ---- \n"
    line9 = "Name   Numb   (eV)    _X_(A)   _Y_(A)  _Z_(A)   Cos(X)   Cos(Y)   Cos(Z) \n"
    line10 = "\n"

    text_alpha = line1+line2+line3+line4+line5+line6+line7_1+line8+line9+line10
    text_recoil = line1+line2+line3+line4+line5+line6+line7_2+line8+line9+line10
    
    return [text_alpha, text_recoil]

# Program that takes a reformed TRIDYN output to generate new .dat files to be used as input for SRIM
def TRYDIN_out_to_SRIM_in(settings, save_path, file_name_out_p1, file_name_out_p2):
    alpha_energy = settings.alpha_energy
    atomic_number_p1 = settings.atomic_number_p1
    atomic_number_p2 = settings.atomic_number_p2
    mass_fraction = settings.mass_fraction
    depthvector = settings.depthvector
    numberofparticles = settings.numberofparticles

    complete_name_out_p1 = os.path.join(save_path, file_name_out_p1)
    complete_name_out_p2 = os.path.join(save_path, file_name_out_p2)
    
    g = open(complete_name_out_p1, 'w')
    h = open(complete_name_out_p2, 'w')
    text = generate_toptext("alpha particles\n ", "recoiling particles\n")
    g.write(text[0])
    h.write(text[1])
    
    for ii, depth in enumerate(depthvector):
        N = numberofparticles[ii]
        # Generate isotropic distribution
        phi = np.random.uniform(0, 2 * math.pi, N)
        theta = np.arccos(1 - 2 * np.random.random(N))
        energy_p1 = [alpha_energy]*N
        vec_x = np.cos(phi) * np.sin(theta)
        vec_y = np.sin(phi) * np.sin(theta)
        vec_z = np.cos(theta)
        ionnumber = str(int(depth)).zfill(5)
        for i in range(N):
            line_p1 = ionnumber + "\t" + atomic_number_p1 + "\t" + str("{:e}".format(energy_p1[i])) + "\t" + str("{:e}".format(depth)) + "\t" + str("{:e}".format(0)) + "\t" + str("{:e}".format(0)) + "\t" + str(vec_x[i]) + "\t" + str(vec_y[i]) + "\t" + str(vec_z[i]) + "\n"
            #line_p1 = ion_number[i] + "\t" + atomic_number_p1 + "\t" + str("{:e}".format(energy_p1[i])) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(vec_x[i]) + "\t" + str(vec_y[i]) + "\t" + str(vec_z[i]) + "\n"
            line_p2 = ionnumber + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mass_fraction)) + "\t" + str("{:e}".format(depth)) + "\t" + str("{:e}".format(0)) + "\t" + str("{:e}".format(0)) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
            #line_p2 = ion_number[i] + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mass_fraction)) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
            g.write(line_p1)
            h.write(line_p2)
    #f.close()
    g.close()
    h.close()
    
    
import os.path
import re
# this function reforms ion range SRIM output to a more convenient form for processing
def reform_R(save_path, name_in, name_out):
    complete_name_in = os.path.join(save_path, name_in) 
    complete_name_out = os.path.join(save_path, name_out) 
    fin = open(complete_name_in, "r")
    fout = open(complete_name_out, "w")
    
    start_data = False                                                                                  # Check if actual data has started
    for line in fin:
        if start_data:
            fout.write(re.sub(',', '.', re.sub('\s+', ' ', re.sub('E', 'e', line))) + "\n")             # Change "," to "."; change multiple spaces to a single space; change E to e
        elif line.startswith("-------"):
            start_data = True
            
    print("reformed SRIM file with single space separation: ion x y z")
    fin.close()
    fout.close()


# Define the settings class
class SettingsM:
    def __init__(self, alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness):
        self.alpha_energy = alpha_energy                        # Energy of alpha particle
        self.atomic_number_p1 = atomic_number_p1                # Atomic number of emitted particle
        self.atomic_number_p2 = atomic_number_p2                # Atomic number of recoil particle
        self.mass_fraction = mass_fraction                      # Mass of emitted/recoil
        self.sample_width = sample_width                        # Width of the sample
        self.sample_thickness = sample_thickness                # Total thickness of the sample
      

# Program that takes a reformed SRIM output to generate new .dat files to be used as input for SRIM again
def srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2):
    alpha_energy = settings.alpha_energy
    atomic_number_p1 = settings.atomic_number_p1
    atomic_number_p2 = settings.atomic_number_p2
    mass_fraction = settings.mass_fraction
    sample_width = settings.sample_width
    sample_thickness = settings.sample_thickness

    ion_number = []
    x = []
    y = []
    z = []
    complete_name_in = os.path.join(save_path, file_name_in)
    complete_name_out_p1 = os.path.join(save_path, file_name_out_p1)
    complete_name_out_p2 = os.path.join(save_path, file_name_out_p2)
    
    # Open and read input file
    with open(complete_name_in, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        
        for row in reader:
            # Check if the particle is still on the sample
            if -sample_width/2 < float(row[2]) < sample_width/2 and -sample_width/2 < float(row[3]) < sample_width/2 and float(row[1]) < sample_thickness:
                # Add position to output arrays
                ion = row[0].lstrip("0")
                while len(ion) < 5:
                    ion = "0" + ion
                ion_number.append(ion)
                y.append(float(row[2]))
                z.append(float(row[3]))
                x.append(abs(float(row[1])))

    
    N = len(ion_number)
    # Generate isotropic distribution
    phi = np.random.uniform(0, 2 * math.pi, N)
    theta = np.arccos(1 - 2 * np.random.random(N))
    energy_p1 = [alpha_energy]*N
    vec_x = np.cos(phi) * np.sin(theta)
    vec_y = np.sin(phi) * np.sin(theta)
    vec_z = np.cos(theta)
    
    g = open(complete_name_out_p1, 'w')
    h = open(complete_name_out_p2, 'w')
    
    text = generate_toptext("alpha particles", "recoiling particles")
    g.write(text[0])
    h.write(text[1])
    
    # For all events still in the system write dat file entry
    for i in range(N):   
        line_p1 = ion_number[i] + "\t" + atomic_number_p1 + "\t" + str("{:e}".format(energy_p1[i])) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(vec_x[i]) + "\t" + str(vec_y[i]) + "\t" + str(vec_z[i]) + "\n"
        line_p2 = ion_number[i] + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mass_fraction)) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
        g.write(line_p1)
        h.write(line_p2)

    f.close()
    g.close()
    h.close()

    print("Created .dat files for alphas and recoils")







####10MBq --> pr100
# Ac-->Fr
plt.rcParams.update({'font.size': 22})
os.chdir('C:/Users/r0750853/linux/Actinium_Jake_Zn/Simulated_data/Depth_profile/225Ac_Jake')
colspecs = [(2, 13), (15, 26), (28, 35), (36, 43), (44, 51)]
pr100 = np.array(pd.read_fwf('225Ac_Jake_pr100.dat', colspecs=colspecs, header=1).T)
depthpr = list((pr100[0][3: len(pr100[0])]))
atfracLapr = list((pr100[4][3: len(pr100[0])]))
atfracZnpr = list((pr100[2][3: len(pr100[0])]))
atfracAcpr = list((pr100[3][3: len(pr100[0])]))
depth = []
atfracAc=[]
atfracZn=[]
atfracLa = []
for ii in range(len(depthpr)):
    depth.append(float(depthpr[ii]))
    atfracAc.append(float(atfracAcpr[ii]))
    atfracLa.append(float(atfracLapr[ii]))
    atfracZn.append(float(atfracZnpr[ii]))
depth=np.array(depth)
atfracAc=np.array(atfracAc)
plt.plot(depth,atfracAc,'gray',linestyle='--',label='3$\AA^{-2}$')
plt.plot(depth,atfracLa,'blue',linestyle='--',label='3$\AA^{-2}$')
plt.ylabel('Atomic fraction of Ac')
plt.xlabel('Depth [$\AA$]')
plt.twinx()
plt.plot(depth,atfracZn)

#make info for TRIM
for ii in range(10):
    print('Zn')
    print(np.mean(atfracZn[ii*10:ii*10+10]))
    print('Ac')
    print(np.mean(atfracAc[ii*10:ii*10+10]))
    print('La')
    print(np.mean(atfracLa[ii*10:ii*10+10]))
    print(' ')

probabilities = []
totat = np.sum(atfracAc[0:100])
numpartperdepth = []
for ii in range(100):
    probabilities.append(atfracAc[ii]/totat)
    numpartperdepth.append(round(90000*atfracAc[ii]/totat))
plt.plot(depth[0:100],probabilities)
plt.figure()
plt.plot(depth[0:100],atfracAc[0:100])
plt.figure()
plt.plot(depth[0:100],numpartperdepth)

alpha_energy = 5935.1*10**3/(1+4/221) #3.999 * 10**6 #Q = 5935.1 kev, T_alpha = Q/(1+malpha/mdaugther), mdaughter = 221                                                                       # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "87"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/221                          


settings = Settings(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, depth[0:100], numpartperdepth)

save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/"
file_name_out_p1 = "output/Ac_alphas.dat"
file_name_out_p2 = "output/Fr_recoils.dat"

TRYDIN_out_to_SRIM_in(settings, save_path, file_name_out_p1, file_name_out_p2)




# Fr--> At
save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/output/"

name_in = "range_Ac_implant_1.txt"
name_out = "easyread_range_Ac_implant_1.txt"
reform_R(save_path, name_in, name_out)


alpha_energy = 6457.7*10**3/(1+4/217)                                                                        # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "85"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/217                                                                               #Ac225 - Fr221 - At217 - Bi213 - Tl209 - Pb209
sample_width = 1.95*10**8
sample_thickness = 5 * 10**3 
settings = SettingsM(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness)

save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/"
file_name_out_p1 = "output/Ac_alphas2.dat"
file_name_out_p2 = "output/At_recoils.dat"
file_name_in = "output/easyread_range_Ac_implant_1.txt"

srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2)

#At --> Bi
save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/output/"

name_in = "range_Ac_implant_2.txt"
name_out = "easyread_range_Ac_implant_2.txt"
reform_R(save_path, name_in, name_out)

alpha_energy = 2701.4*10**3/(1+4/213)                                                                        # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "83"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/213                                                                               #Ac225 - Fr221 - At217 - Bi213 - Tl209 - Pb209
sample_width = 1.95*10**8
sample_thickness = 5 * 10**3 
settings = SettingsM(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness)

save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/"
file_name_out_p1 = "output/Ac_alphas3.dat"
file_name_out_p2 = "output/Bi_recoils.dat"
file_name_in = "output/easyread_range_Ac_implant_2.txt"

srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2)



#Bi --> Po --> Pb
save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/output/"

name_in = "range_Ac_implant_3.txt"
name_out = "easyread_range_Ac_implant_3.txt"
reform_R(save_path, name_in, name_out)

alpha_energy = 8536.1*10**3/(1+4/209)                                                                        # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "82"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/209                                                                               #Ac225 - Fr221 - At217 - Bi213 - Tl209 - Pb209
sample_width = 1.95*10**8
sample_thickness = 5 * 10**3 
settings = SettingsM(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness)

save_path = "C:/Users/r0750853/linux/Actinium_Jake_Zn/"
file_name_out_p1 = "output/Ac_alphas4.dat"
file_name_out_p2 = "output/Pb_recoils.dat"
file_name_in = "output/easyread_range_Ac_implant_3.txt"

srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2)
