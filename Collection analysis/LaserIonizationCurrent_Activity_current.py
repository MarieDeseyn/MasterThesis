# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:23:38 2022

@author: marie
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def summarizinggraph(activity,lamb,times, rangeindex, rangeonof,ioncur,timeioncurr,getalletje1,getalletje2,temp,timetemp,use_error=False, error = 0):
    #activity = activity measured in the kromek for Tb line
    #lamb = decayconstant (ln2/t_1/2)
    #times = times at which the activity is measured in minutes
    #rangeindex = in what range is the kromekdata available
    #rangeonof = in what range is the onof effect present
    #ioncur = total ioncurrent on the foil
    #timeioncurrent = time related to the ioncurrent measurement in minutes
    #getalletje1 and getalletje2 = delta t that is used to calculate the collected activity with [#datapoints]
    allcurrentskromek = []
    for ii in rangeindex[getalletje1:len(rangeindex)]:
        Anow = activity[ii] #MBq
        Aprevnow = activity[ii-getalletje1]*np.exp(-lamb*(times[ii]-times[ii-getalletje1])*60) #MBq
        Aadded = Anow - Aprevnow #MBq
        nadded = Aadded/lamb *10**6
        chargeadded = nadded * 1.602*10**(-19) #C
        current = chargeadded/((times[ii]-times[ii-getalletje1])*60) #C/s = A
        allcurrentskromek.append(current*10**9) #nA
    # allcrrentskromek current that is originating from the Tb as for the kromekdata only (Tb) peaks are considered
    allcurrentskromek2 = []
    for ii in rangeindex[getalletje2:len(rangeindex)]:
        Anow = activity[ii] #MBq
        Aprevnow = activity[ii-getalletje2]*np.exp(-lamb*(times[ii]-times[ii-getalletje2])*60) #MBq
        Aadded = Anow - Aprevnow #MBq
        nadded = Aadded/lamb *10**6
        chargeadded = nadded * 1.602*10**(-19) #C
        current = chargeadded/((times[ii]-times[ii-getalletje2])*60) #C/s = A
        allcurrentskromek2.append(current*10**9) #nA
    
    
    #calculating the surface and laser ionization
    indip = rangeonof 
    for ii in indip:
        plt.axvline(ii,color='gray')
    plt.plot(timeioncurr,ioncur,'.')
    plt.title('Check the resonances')
    surfaceionwaarden = []
    surfandlaser = []
    for indip in rangeonof:
        minnetje = indip-0.1
        maxetje = indip+0.1
        indexentecontroleren = []
        counter = 0
        for tijd in timeioncurr:
            if tijd<= maxetje and tijd>=minnetje:
                indexentecontroleren.append(counter)
            counter+=1
        currtecontroleren=ioncur[indexentecontroleren]
        surfaceionwaarden.append(min(currtecontroleren)) #at the minimum the laser is put off
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
    for ii in rangeonof: #ii is a time, i is an index in 'all' times
        fitindices = [i for i in range(len(trendinfotime)) if trendinfotime[i]>ii-3 and trendinfotime[i]<ii+3]
        z = np.polyfit(trendinfotime[fitindices], trendinfo[fitindices], 20)
        p = np.poly1d(z)
        toapp = p(ii)
        surfandlaser.append(toapp)
        plt.plot(np.arange(ii-3,ii+3,0.5),p(np.arange(ii-3,ii+3,0.5)))
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 3]})
    fig.tight_layout()
    
    #create subplots
    ax[0].plot(times,activity,'b.')
    ax[0].set_ylabel('Activity measured\n by the Kromek [MBq]')
    if use_error==True:
        ax[0].errorbar(times,activity,yerr=error, markersize=4, fmt="o", color="blue",
             ecolor="blue", capsize=2, capthick=0.6, linewidth=0.6)
    ax01 = ax[0].twinx()
    ax01.plot(timetemp,temp,'lightgray')
    ax01.set_ylabel('Temperature [A]')
    legend_elements = [Line2D([0], [0], color='lightgray', lw=1, label='Temperature'),
                   Line2D([0], [0], marker='.',color='blue', label='Activity')]
    ax[0].legend(handles=legend_elements, loc='upper left')
    #ax[0].set_xlim(0,1750)
    ax[0].set_xlabel('Time [min]')
    ax[0].set_ylim(-0.1,9)
    ax[1].plot(timeioncurr,ioncur,'.',color='lightgrey')
    ax[1].plot(rangeonof,np.array(surfandlaser)-np.array(surfaceionwaarden),'.',color='red') #laser ionization
    ax[1].plot(times[rangeindex[getalletje1:len(rangeindex)]],allcurrentskromek,'b.')
    z = np.polyfit(times[rangeindex[getalletje1:len(rangeindex)]], allcurrentskromek, 20)
    p = np.poly1d(z)
    ax[1].plot(times[rangeindex[getalletje2:len(rangeindex)]],allcurrentskromek2,'y.',alpha = 0.5)
    ax[1].set_xlabel('Time [min]')
    ax[1].set_ylabel('Current [nA]')
    ax[1].legend(["Total current measured on the foil","Current on the foil originating from laser ionization","Current on the foil coming from 155-Tb with $\Delta t$=" + str(5*getalletje1)+ "minutes","Current on the foil coming from 155-Tb with $\Delta t$=" + str(5*getalletje2)+ "minutes"])
    ax[1].set_xlim(0,1750)
    ax[0].set_xlim(0,1750)
    #ax[1].set_ylim(-0.01,0.17) #15july
    ax[1].set_ylim(-0.1,0.6) #4july
    
plt.figure()
plt.rcParams.update({'font.size': 15})
getalletje1 = 10
getalletje2 = 5
lambdaTb = 1.5*10**(-6)
summarizinggraph(activity4july, lambdaTb, time4julyact, range(19,175), np.arange(22.5,1160,5+1*5/60), ioncurr4july, time4julyioncurrcor, getalletje1,getalletje2, temp4july, time4julytemp, True, erractivity4july)   

getalletje1 = 20
getalletje2 = 10
summarizinggraph(activity15july, lambdaTb, time15julyact,range(0,336), np.arange(69.63,2695,5+1*5/60-0.0005), ioncurr15july, time15julyioncurrcor, getalletje1,getalletje2, temp15july, time15julytemp)   