# This is a python script for plotting cell width profiles along normalized cell length.
#
# REQUIREMENTS:
# This python file must be placed in the same folder as the Oufti csv output file(s).
# You must have python on your computer.
# You must have the Matplotlib and Numpy libraries installed for python.
#
# Directions:
# In the terminal or command prompt, change your directory to the location where
# your exported Oufti csv files and this python script are.
# (for example: "cd /Users/iansparks/Lab_stuff/data/test_2_Hiro")
# Then run this python script (enter: "python mountain_graph.py")

import itertools
import sys
import matplotlib
from matplotlib import pyplot as plt
import math # 'math' needed for 'sqrt'
import csv
import numpy as np
import re
import os
from scipy.stats import kde
from scipy.interpolate import spline
import matplotlib.colors as colors
import random

#gets your current directory
your_directory = os.getcwd()

#set font
afont = {'fontname':'Arial MT'}


#Distance function
def distance(xi,xii,yi,yii):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return math.sqrt(sq1 + sq2)

#first, count how many CSV files are in your directory
CSV_count = 0
for file in os.listdir(your_directory):
    files_name, ext = os.path.splitext(file)
    if ext == ".csv":
        CSV_count += 1


#set up the number of figures
fig, ax = plt.subplots(1, CSV_count, squeeze=False)



#now make a profile figure for each csv file
CSV_count2 = 0
for file in os.listdir(your_directory):
    x = []
    y = []
    Thresh_080 = 0
    Thresh_120 = 0
    Thresh_140 = 0
    Thresh_160 = 0
    files_name, ext = os.path.splitext(file)
    if ext == ".csv":
        #read the cell mesh data from the oufti output csv file
        with open(file, "rb") as inFile:
            csv_reader = csv.reader(inFile, delimiter=',')
            MeshCells = []
            for row in csv_reader:
                if len(row) < 7:
                    continue
                if len(row[6]) < 10:
                    continue
                MeshCells.append(row[6])
            # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
            # Sample size governs the number of cells plotted
            Sample_Size = 150
            if len(MeshCells) < Sample_Size:
                Sample_Size = len(MeshCells)
            #CODE to randomly select n from N
            MeshCells = random.sample(MeshCells, k=Sample_Size)

            for i in MeshCells:
                x = []
                y = []
                CellWidths = []
                mod_i = str(i)
                mod_i = mod_i.translate(None, "['")
                mod_i = mod_i.translate(None, "']")
                CoordinateList = mod_i.split(";")
                x1List = CoordinateList[0].split(" ")
                while ("" in x1List):
                    x1List.remove("")
                y1List = CoordinateList[1].split(" ")
                while ("" in y1List):
                    y1List.remove("")
                x2List = CoordinateList[2].split(" ")
                while ("" in x2List):
                    x2List.remove("")
                y2List = CoordinateList[3].split(" ")
                while ("" in y2List):
                    y2List.remove("")
                for e in range(len(x1List)):
                    CellWidths.append(distance(float(x1List[e]),float(
                    x2List[e]),float(y1List[e]),float(y2List[e])))

                #assign cell widths and normalized cell length values to x and y variables
                count = 0
                for e in range(len(CellWidths)):
                    x.append((float(count))/(float(len(CellWidths)-1)))
                    count = count + 1
                    y.append(CellWidths[e]/13.5135)
                #count how many cells have max widths above certain threshold values
                if max(y) > 0.95:
                    Thresh_080 += 1
                if max(y) > 1.2:
                    Thresh_120 += 1
                if max(y) > 1.4:
                    Thresh_140 += 1
                if max(y) > 1.6:
                    Thresh_160 += 1
                #plot a cell width profile line for each cell
                ax[0,CSV_count2].plot(x,y, c='k', alpha=0.2)

            inFile.close()

        #calculate the percentage of cells that cross each cell width threshold
        percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
        percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
        percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
        percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))
        #set title of subplots to the csv file name
        ax[0,CSV_count2].set_title(files_name, y=1.01)
        #display the percentage of cells above the threshold on the plot
        ax[0,CSV_count2].text((0.003-0.14), 1, str(percentThresh_080) + '%', fontsize=15, color ='g', **afont)
        #display the sample size used for the plot on the plot
        ax[0,CSV_count2].text((0.015-0.14), 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=15, color ='k', **afont)
        #keeps track of which csv file the loop is on in order to assign data to the correct subplot
        CSV_count2 += 1

#plot asthetics adjustment
fig.patch.set_facecolor('w')

#set x and y axis parameters for the plots
for ax in ax.flat:
    ax.set(xlabel='normalized cell length', ylabel='cell width (' + u"\u03BCm" + ')') #changed 'cell profile' to 'normalized cell length'
    ax.plot([-0.15,1.05],[0.95,0.95], 'g--', linewidth=2)
    ax.tick_params(direction='out', axis='both')
    ax.set_ylim([0,1.6])
    ax.set_xlim([-0.15,1.05])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
    ax.set_xticks([0, 0.5, 1])
    ax.set_aspect('equal')
    ax.tick_params(axis='both', which='major', labelsize=15)

#plot asthetics adjustment
fig.subplots_adjust(wspace=0.3, hspace=0.4)
#plot the width profile graphs
plt.show()

exit()
