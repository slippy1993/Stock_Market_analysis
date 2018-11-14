import re
import urllib.request
import requests
import json
import time
import datetime
import os
import csv
import pandas as pd
from alphavantage import getdata_alphavantage
from pandas_datareader import data as web
from stockstats import StockDataFrame as Sdf
from tkinter import *
import numpy as np
from itertools import repeat
from yahoo_finance import Share
import urllib
from lxml import html
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import statistics
from sklearn.cluster import DBSCAN





from bs4 import BeautifulSoup
data=[]
closeprizes=[]
closeprizestemp=[]
temp=[]
MA_three=[]
zeros=[]
sup_res=[]
file = open("DAT_ASCII_EURUSD_M1_201810.csv","r")
for line in file:
    data.append(line)
file.close()

#zeilen aufsplitten und jeweils die closeprizes der liste anhängen
for i in data:
    temp=i.split(';')
    closeprizestemp.append(float(temp[3]))


#spieglen sodass in [0] der aktuellste wert steht
closeprizes=closeprizestemp[::-1]

#MA berechnen
for j in range(0,100):
    three_days_ma=(closeprizes[j]+closeprizes[j+1]+closeprizes[j+2])/3

    MA_three.append(three_days_ma)
    #zeros.append('0')

#find the local turning points and store the price level of these
for k in range(0,len(MA_three)-4):
    if(MA_three[k+1]-MA_three[k]>=0 and MA_three[k+1]-MA_three[k+2]>=0):
        sup_res.append(MA_three[k])
        zeros.append('0')
    elif(MA_three[k+1]-MA_three[k]<=0 and MA_three[k+1]-MA_three[k+2]<=0):
        sup_res.append(MA_three[k])
        zeros.append('0')

twoDarray=np.transpose([zeros, sup_res])



#calculate k dist values to determine epsilon value automated
distances=[]
tempdistance=[]
sorteddistances=[]
sorted_dist=[]
epsilon=0

for v in sup_res:
    tempdistance.clear()
    for z in sup_res:
        tempdistance.append(abs(v-z))
    sorted_dist=tempdistance
    sorted_dist=np.asarray(sorted_dist)
    sorted_dist.sort()

    distances.append(sorted_dist[3])

#calculate epsilon for DBSCAN
distances=np.array(distances)
distances.sort()
SD=np.std(distances)
epsilon=np.mean(distances)



#perform DBSCAN
clustering = DBSCAN(eps=epsilon, min_samples=2).fit(twoDarray)
labels=clustering.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

c_indices=clustering.core_sample_indices_


sup_Res_final=[]

#find support resistance level
for i in range(n_clusters_):
    sup_Res_final.append([])
    for j in range(len(labels)):
        if(labels[j]==i):
            wta=twoDarray[j,1]          #create a n*m list where n is the number ob clusters found and m the price levels which belong to each cluster
            sup_Res_final[i].append(wta) #append the pricelevels of of the turning points to the corresponding cluster



# convert string to float
p=0
s=0
for i in sup_Res_final:

    s=0
    for j in i:
        sup_Res_final[p][s]=float(j)
        s+=1
    p+=1


#calcualte the horizontal lines
sup_res_lines=[]
for i in sup_Res_final:
    mean=sum(i) / float(len(i))
    sup_res_lines.append(mean)


#visualize the support/resistance lines
for i in sup_res_lines:
    plt.hlines(i,0,100,colors='r')

plt.plot(closeprizes[0:100])
plt.show()
