import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import matplotlib.patheffects as pe 
import glob
import os
import csv
import numpy as np 
from random import random

# Setting colours specific to each SID
SID4 = ['firebrick','red','darkorange','orangered','gold'] # SID4 Physical assets (n=5)
SID3 = ['limegreen','forestgreen','lightgreen','darkgreen'] # SID3 Financial situation (n=4)
SID2 = ['royalblue','turquoise','steelblue','lightskyblue','blue'] #SID2 Social standing (n=5)        
SID1 = ['purple','magenta','deeppink','fuchsia','violet','hotpink'] #SID1 Critical infrastructure (n=6)
colors = SID4 + SID2 + SID3 + SID1

# Setting angles and wedge widths
# specific to each SID
theta = [9,27,45,63,81,99,117,135,153,171,191.25,213.75,236.25,258.75,277.5,292.5,307.5,322.5,337.5,352.5]
theta_rad = [np.deg2rad(i+90) for i in theta]
width = [18,18,18,18,18,18,18,18,18,18,22.5,22.5,22.5,22.5,15,15,15,15,15,15]
width_rad = [np.deg2rad(i) for i in width]

# Naming each SID
categories = ['Dwelling Type',
            'Waste Disposal',
            'Water Source',
            'Lighting',
            'Cooking',
            'First Marriage',
            'Education',
            'Type',
            'Age Structure',
            'Household-head',
            'Finance Assistance',
            'Income Source',
            'Employment Status',
            'Savings (any)',
            'Transport Assets',
            'Household Size',
            'Occupation Assets',
            'Furniture',
            'Tech Assets',
            'Home Ownership'
            ]

def findCSVs(csvDir):
    # criteria to find the csvs
    search_criteria = '*.csv'
    CSVs = os.path.join(csvDir, search_criteria)
    # taking all the files that match and globbing together
    all_CSVs = glob.glob(CSVs)
    print(len(all_CSVs),'.csv files found')  
    return all_CSVs

maxCSVs = findCSVs('./max/')
sorted_CSVs = sorted(maxCSVs, key=lambda x: int(x[-7:-4]))

# For each of the max R2 cluster files found
for file in sorted_CSVs:
    # reset variables each loop
    print('Processing:',file)
    data_dict = {}
    max = []
    var = []
    with open(file,'r') as csvfile:
        # open figure
        fig = plt.figure(figsize=(5,5))
        # read in data
        data = csv.reader(csvfile, delimiter=',')
        next(data) # skip header
        print('-- Extracting data --')
        for row in data:
            # max R2 value
            max.append(float(row[0]))
            # variable
            var.append(row[1])
        #max_float = [float(i) for i in max]

        # set up polar plot
        print('Plotting',file)
        ax = fig.add_subplot(111, projection='polar')
        # formatting
        ax.grid(color='lightgrey',alpha=0.7,linewidth=0.5)
        ax.set(ylim=(-0.5,1.0), xticklabels=[])
        yticks = np.linspace(0,1.0,num=11)
        yticks_round = [round(i,1) for i in yticks]
        ax.set_yticklabels(yticks_round,ha='left',va='baseline',fontsize=10,fontname='Charter',color='black')
        ax.tick_params(axis='y', labelrotation=270)
        position = 0
        ax.set_rgrids(np.arange(0.0, 1.1, 0.1), angle=position)
        ax.spines["polar"].set_color('black')
        
        # plot data
        bars = ax.bar(theta_rad,max,width=width_rad,color=colors,alpha=0.8,ec='darkgrey')
        
        # adjust the gridlines emphasized
        # to show category divisions (SID1,SID2,SID3,SID4)
        gridlines = ax.xaxis.get_gridlines()
        for inds in [0,2,4,6]:
            # dividers
            gridlines[inds].set_color('black')
            gridlines[inds].set_linewidth(1.75)
        for inds in [1,3,5,7]:
            # absent
            gridlines[inds].set_alpha(0)

        # setting up approriate rotations for the text labels
        rotations = [i+90 for i in theta] # Right side of plot
        adj_rotations = [i+180 if i < 270 else i for i in rotations] # Left side of plot
        bottom = 0.5
        # plot labels per bar
        for x, bar, rotation, label in zip(theta_rad, bars, adj_rotations, var):
            lab = ax.text(x,1.0, label, 
                        ha='center', va='center', rotation=rotation, fontname='Charter',rotation_mode="default", color='black', fontsize=10, path_effects=[pe.withStroke(linewidth=3, foreground="white")])  
    
        # save max R2 class figure
        plt.tight_layout()
        plt.savefig('./max/'+str(file[-7:-4])+'_max_plot.png',transparent=True)
        print('Figure saved')
        plt.close()

###### COLOUR LEGEND ########
# set up figure
fig = plt.figure(figsize=(5,5))
ax1 = fig.add_subplot(111, projection='polar')
ax1.set(ylim=(-0.50,1.0), yticklabels=[], xticklabels=[], rlabel_position=100)

# emphasize SID dividers 
gridlines = ax1.xaxis.get_gridlines()
for inds in [0,2,4,6]:
    gridlines[inds].set_color('black')
    gridlines[inds].set_linewidth(1.75)
for inds in [1,3,5,7]:
    gridlines[inds].set_alpha(0)

# set value as max for completely filled chart
for_key = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
ax1.set_theta_direction(1)
# plot each bar
bars = ax1.bar(theta_rad,for_key,width=width_rad,color=colors,alpha=0.7,ec='darkgrey')
#add category labels
for x, bar, rotation, label in zip(theta_rad, bars, adj_rotations, categories):
    lab = ax1.text(x,0.48,label, 
            ha='center', va='center', rotation=rotation, fontname='Charter', rotation_mode="anchor", color='black', fontsize=10)
# formatting
ax1.yaxis.grid(False)
ax1.spines["polar"].set_color('black')
ax1.spines["polar"].set_linewidth(1.75)
# export
plt.savefig('./max/color_legend.png',transparent=True)
print('Color legend saved')
plt.close()
