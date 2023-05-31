# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:09:45 2023

@author: r0750853
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def schemeab(rangeonof,ioncur,timeioncurr):
    #rangeonof = in what range is the onof effect present
    #ioncur = ioncurrent on the foil
    #timeioncurrent = time related to the ioncurrent measurement in minutes    
    plt.plot(timeioncurr,ioncur,'.',color='gray')
    #calculating the surface and laser ionization
    indip = rangeonof 
    for ii in indip:
        plt.axvline(ii,color='gray')
    plt.title('Check the resonances')
    
    aoff = []
    boff = []
    surfandlaser = []
    for indip in rangeonof:
        minnetjea = indip-0.1
        maxetjea = indip
        minnetjeb = indip
        maxetjeb = indip+0.3
        indexentecontrolerena = []
        indexentecontrolerenb = []
        counter = 0
        for tijd in timeioncurr:
            if tijd<= maxetjea and tijd>=minnetjea:
                indexentecontrolerena.append(counter)
            if tijd<= maxetjeb and tijd>=minnetjeb:
                indexentecontrolerenb.append(counter)
            counter+=1
        currtecontrolerena=ioncur[indexentecontrolerena]
        currtecontrolerenb=ioncur[indexentecontrolerenb]
        aoff.append(min(currtecontrolerena)) #at the minimum the laser is put off
        boff.append(min(currtecontrolerenb)) #at the minimum the laser is put off
        plt.plot(timeioncurr[list(ioncur).index(min(currtecontrolerena))],min(currtecontrolerena),'*',color='m')
        plt.plot(timeioncurr[list(ioncur).index(min(currtecontrolerenb))],min(currtecontrolerenb),'*',color='c',alpha=0.5)
    indexenweg = []
    for indip in rangeonof:
        minnetje = indip-0.15
        maxetje = indip+0.2
        indexentecontroleren = []
        counter = 0
        for ii in range(len(timeioncurr)):
            tijd = timeioncurr[ii]
            if tijd<= maxetje and tijd>=minnetje:
                indexenweg.append(ii)
    trendinfo = ioncur.copy()
    trendinfo=list(trendinfo)
    trendinfotime = timeioncurr.copy()
    trendinfotime=list(trendinfotime)
    indices = sorted(indexenweg, reverse=True)
    plt.figure()
    plt.plot(timeioncurr,ioncur,'.')
    for ii in indices:
        trendinfo.pop(ii)
        trendinfotime.pop(ii)
    trendinfotime = np.array(trendinfotime)
    trendinfo = np.array(trendinfo)
    for ii in rangeonof: #ii is een tijd, i een index in 'alle' tijden
        fitindices = [i for i in range(len(trendinfotime)) if trendinfotime[i]>ii-3 and trendinfotime[i]<ii+3]
        z = np.polyfit(trendinfotime[fitindices], trendinfo[fitindices], 20)
        p = np.poly1d(z)
        toapp = p(ii)
        surfandlaser.append(toapp)
        plt.plot(np.arange(ii-3,ii+3,0.5),p(np.arange(ii-3,ii+3,0.5)))
    
    #create plots
    plt.figure()
    plt.plot(timeioncurr,ioncur,'.',color='lightgrey')
    plt.plot(rangeonof,np.array(surfandlaser)-np.array(aoff),'.-',color='m',lw=0.5) #laser ionization scheme a
    plt.plot(rangeonof,np.array(surfandlaser)-np.array(boff),'.-',color='c',lw=0.5) #laser ionization scheme b
    plt.xlabel('Time [min]')
    plt.ylabel('Current [nA]')
    plt.legend(["Total current measured on the foil","Scheme A","Scheme B"])
    plt.xlim(0,1750)
    plt.ylim(-0.1,0.6) 
    
plt.rcParams.update({'font.size': 25})
arraytje = np.arange(22.5,1160,5+1*5/60)
arraytouse = [x for x in arraytje if ((abs(x-891.7499999999998) > 1) and (abs(x-922.25) > 1) and (abs(x-927.33333333) > 1))]
schemeab(arraytouse, ioncurr4july, time4julyioncurrcor)
