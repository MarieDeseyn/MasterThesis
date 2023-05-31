# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 12:59:52 2023

@author: r0750853
"""

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
            line_p2 = ionnumber + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mass_fraction)) + "\t" + str("{:e}".format(depth)) + "\t" + str("{:e}".format(0)) + "\t" + str("{:e}".format(0)) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
            g.write(line_p1)
            h.write(line_p2)
    g.close()
    h.close()
      
plt.rcParams.update({'font.size': 22})
os.chdir('C:/Users/r0750853/linux/149Tb/Simulated_data/Depth_profile/149Tbst1Tb')
colspecs = [(2, 13), (15, 26), (28, 35), (36, 43), (44, 51)]
pr100 = np.array(pd.read_fwf('149Tbst1Tb_pr100.dat', colspecs=colspecs, header=1).T)
depthpr = list((pr100[0][3: len(pr100[0])]))
atfracTbpr = list((pr100[3][3: len(pr100[0])]))
atfracAlpr = list((pr100[2][3: len(pr100[0])]))
depth = []
atfracTb=[]
atfracAl=[]
for ii in range(len(depthpr)):
    depth.append(float(depthpr[ii]))
    atfracTb.append(float(atfracTbpr[ii]))
    atfracAl.append(float(atfracAlpr[ii]))
depth=np.array(depth)
atfracTb=np.array(atfracTb)
plt.plot(depth,atfracTb,'gray',linestyle='--',label='3$\AA^{-2}$')

plt.ylabel('Atomic fraction of Tb')
plt.xlabel('Depth [$\AA$]')
plt.plot(depth,atfracAl)

#make info for TRIM
for ii in range(10):
    print(np.mean(atfracTb[ii*6:ii*6+6]))
    print(np.mean(atfracAl[ii*6:ii*6+6]))
    print(' ')

probabilities = []
totat = np.sum(atfracTb[0:60])
numpartperdepth = []
for ii in range(60):
    probabilities.append(atfracTb[ii]/totat)
    numpartperdepth.append(round(90000*atfracTb[ii]/totat))
plt.plot(depth[0:60],probabilities)
plt.figure()
plt.plot(depth[0:60],atfracTb[0:60])
plt.figure()
plt.plot(depth[0:60],numpartperdepth)


alpha_energy = 3.999 * 10**6                                                                               # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "63"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/145.0                          


settings = Settings(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, depth[0:60], numpartperdepth)

save_path = "C:/Users/r0750853/linux/149Tb/"
file_name_out_p1 = "output/Tb_alphas.dat"
file_name_out_p2 = "output/Eu_recoils.dat"

TRYDIN_out_to_SRIM_in(settings, save_path, file_name_out_p1, file_name_out_p2)