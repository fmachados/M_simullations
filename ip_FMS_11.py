#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 13:48:05 2018

@author: Fernando Machado
"""
#Define working directory
import os
os.getcwd() #current working directory
#os.chdir("C:\\Users\\Fernando Machado\\Desktop\\Taigo\\Academia\\KU\\Courses\\Simulation & Modeling in Bio (Pyhton)\\ip") #new working directory
os.chdir("C:\\Users\\Fernando Machado\\Documents\\Python\\M_simullations")

import matplotlib.pyplot as plt
from random import choice
import numpy as np
import numpy
import pandas as pd
import time
import csv
from scipy.stats import chi2
import matplotlib.patches as mpatches
import linecache
import scipy

start = time.time() #measuring performance

#Outputs
out1 = open("Report.txt","w")

#Size of matrices (ascii)
metadata = []
for i in range(6): #the first six lines of the ascii file
    metadata.append(linecache.getline("clip_bio1_10m.asc", i+1)) #each line is appended inside the metadata matrix
    metadata[i] = metadata[i].split() #changes from string to list
    metadata[i][1] = float(metadata[i][1]) #changes the values to string elements to floats

#size of environmental matrices
Nrow = int(metadata[1][1])
Ncol = int(metadata[0][1])
out1.write("Size of grid: " + str(Nrow) + " by " + str(Ncol) + "\n" + "\n")

#The variables
bio1 = np.loadtxt("clip_bio1_10m.asc", skiprows = 6)
bio12 = np.loadtxt("clip_bio12_10m.asc", skiprows = 6)

#creates flat lists from the environmental matrices and transform the values to integers
Temp_data = []
Prec_data = []
for row in range(Nrow):
    for col in range(Ncol):
        Temp_data.append(int(bio1[row][col]))
        Prec_data.append(int(bio12[row][col]))

#Presence points of Henicorhina leucosticta (HL) in which temperature & precipitation values were extracted in QGIS and saved as a csv
with open("Nf_Hleucosticta.csv", "r") as f: #has a header
    reader = csv.reader(f)
    HLdata = list(reader) #with these points the fundamental niche ellipse is estimated, see main code below

Temp_list, Prec_list = [], []
Prec_list = []
for row in range(len(HLdata)):
    if (row != 0): 
        Temp_list.append(int(HLdata[row][2]))
        Prec_list.append(int(HLdata[row][3]))

#Nf centroid        ###Fix both for multiple dimensions, just add a loop
centroid = [np.mean(Temp_list), np.mean(Prec_list)]
#var-covar
VC_matrix = np.cov(Temp_list, Prec_list)

#Number of replicates
rep = 4 #10
out1.write("Replicates: " + str(rep) + "\n" + "\n")

#Number of time steps 
steps = 85
out1.write("Generations: " + str(steps) + "\n" + "\n")

#Number of maximum dispersers from a source population for t (e.g., 100 years)
NdMax = 2 #If NdMax = 1: all populations produce the same number of dispersers 
Nd_list = list(range(1, NdMax + 1)) #list of number of dispersers

#The number of dispersers (Nd) could be proportional to S, hence from a pixel with S = 1 the Nd will be NdMax
incNd = 0.5 / NdMax #increment in S range, 0.5 is the minimum value of a pixel to be habitable 
S_list = list(np.arange(0.5 + incNd, 1.0 + incNd, incNd)) #list of S values for each Nd_list element
#Then, if S <= incNd*n: Nd = n

result_vectors = [[[0]*steps for j in range(2)] for r in range(rep)]

#List for vectors of the change in A & C through time (i.e., the dynamic), and a list for headers
dyn = []*2*rep 
titles = []*2*rep

# __Functions__

#def ConfEllipse(x_list, y_list, alfa):
#    "Generates the arguments for building a confidence ellipse"
#    xmean, ymean = np.mean(x_list), np.mean(y_list) #centroid
#    s = chi2.isf(alfa, 2) #chi square constant
#    VC_matrix = np.cov(x_list, y_list) #var-covar matrix
#    lambda_, v = np.linalg.eig(VC_matrix) #eigenvalues & eigenvectors
#    xd = 2 * np.sqrt(s * lambda_[0]) #axis 1
#    yd = 2 * np.sqrt(s * lambda_[1]) #axis 2
#    angle = np.rad2deg(np.arccos(v[0, 0]))
#    return xmean, ymean, xd, yd, angle

#def inside(point, ell_data):
#    "Determines if a point is inside a confidence ellipse"
#    inside = [0, 0]
#    cos_angle = np.cos(np.radians(180 - ell_data[4]))
#    sin_angle = np.sin(np.radians(180 - ell_data[4]))
#    x_trans = (point[0] - ell_data[0]) * cos_angle - (point[1] - ell_data[1]) * sin_angle
#    y_trans = (point[0] - ell_data[0]) * sin_angle + (point[1] - ell_data[1]) * cos_angle
#    norm_d = (x_trans / (ell_data[2]/2))**2 + (y_trans / (ell_data[3]/2))**2 #normalized distance to the centroid
#    if (norm_d <= 1):
#        inside = [1, norm_d]
#    else:
#        inside = [0, norm_d]
#    return inside

def setLoc(coord):
    "Determines the location of a point from the geographic coordinates (lon/lat) of this exercise"
    NWlon, NWlat = round(metadata[2][1], 12), round((158*metadata[4][1] + metadata[3][1]), 12)
    NWvertex = [NWlat, NWlon] #taken from the raster files, the most northwestern point (0,0)
    loc_val, loc = [], []
    if (coord[0] >= 0):
        loc_val.append(NWvertex[0] - coord[0]) #sets y above the Equator 
    else:
        loc_val.append(-coord[0] + NWvertex[0]) #sets y below the Equator
    loc_val.append(-NWvertex[1] + coord[1]) #sets x
    for i in range(2):
        loc.append(int(loc_val[i] / metadata[4][1])) #divided by cell size
    return loc

def setPop(in_list): 
    "Starts populations in a randomly selected 50% subset of the presences that are inside the ellipse"
    C = [[0]*Ncol for i in range(Nrow)] #grid of the number of times a pixel has been accessed & colonized    
    point = []    
    size_l = int(len(in_list)*0.50) #the size of the list based on the percentage parameter
    rowset = np.random.choice(range(1, len(in_list)), size = size_l, replace = False) #creates a random list of "size" presences from in_list    
    for i in range(len(rowset)):
        point = setLoc([float(in_list[rowset[i]][0]), float(in_list[rowset[i]][1])]) #coordinates of the selected rows
        C[point[0]][point[1]] = 1 #then, the firsts populations are established
    return C

def updateA(A, A_now):
    "Updates the accessed pixels matrix each time step"
    for row in range(Nrow):
        for col in range (Ncol):
            if (A_now[row][col] != 0):
                A[row][col] = A[row][col] + A_now[row][col]
    return A

def updateC(C, A_now):
    "Updates the colonized pixels matrix according to the pixels that are visited at each time step"
    for row in range(Nrow):
        for col in range (Ncol):
            if (A_now[row][col] != 0):
                #if the pixels has been visited and are suitable (a threshold could be set here instead of 0)
                if (S[row][col] > 0.5):
                    C[row][col] = C[row][col] + A_now[row][col]
    return C

#def direction():
#    "Sets the direction of dispersal for latitude and longitude"
#    direction = [choice([-1,1]) for i in range(2)]
#    return direction

def howmany(M):
    "Counts the number of cells that are occupied in any matrix M"
    count = 0
    for i in range(len(M)):
        for j in range(len(M[0])):  
            if (M[i][j] > 0): 
                count += 1
    return count                

def maxM4(M4):
    "Returns the max value of a list of four matrices"
    M4_max_list = []
    for r in range(4):
        max_sublist = []
        for i in range(Nrow):
            max_sublist.append(max(M4[r][i]))
        max_list = max(max_sublist)
        M4_max_list.append(max_list)
    max_M4 = max(M4_max_list)
    return max_M4


# __main__

#Nf_ellipse = ConfEllipse(Temp_list, Prec_list, 0.05) #fundamental niche ellipse

#norm_d = [0 for i in range(len(Temp_data))] #list for normalized distances of environmental pixel to the centroid
#for i in range(len(Temp_data)):
#    norm_dist = inside([Temp_data[i], Prec_data[i]], Nf_ellipse)
#    norm_d[i] = norm_dist[1]

#Mahalanobis distances list
Mah_d = [0 for i in range(len(Temp_data))]
for i in range(len(Temp_data)):
    Mah_d[i] = scipy.spatial.distance.mahalanobis([Temp_data[i], Prec_data[i]], 
         centroid, numpy.linalg.inv(VC_matrix))

#the suitability can be proportional to the normalized distance to the centroid of the fundamental niche
#S_data = [0 for i in range(len(Temp_data))]
#for i in range(len(Temp_data)): 
#    S_data[i] = 1 - norm_d[i]
#    if (S_data[i] < 0): #i.e., norm_d > 1 (outside the ellipse)
#        S_data[i] = 0

#the suitability can be proportional to the standarized Mahalanobis distance (to the centroid of the fundamental niche)
S_data = [0 for i in range(len(Temp_data))]
s = chi2.isf(0.05, len(centroid)) #95% confidence
for i in range(len(Temp_data)): 
    if (Mah_d[i] > s): #outside the ellipsoid (S=0)
        S_data[i] = 0
    else: #suitability values inside the ellipsoid
        S_data[i] = 1 - (Mah_d[i] / s)

#The matrix of suitability values is created
S = [[0]*Ncol for i in range(Nrow)] 
S =  [S_data[Ncol * i : Ncol * (i + 1)] for i in range(Nrow)]


#in_list = []
#for i in range(1, len(HLdata)):
#    subset = inside([int(HLdata[i][2]), int(HLdata[i][3])], Nf_ellipse)
#    if (subset[0] == 1):
#        in_list.append([HLdata[i][0], HLdata[i][1], HLdata[i][3], HLdata[i][3], subset[1]])

#which samples are inside the Nf_ellipse? This is used to select the points for the replicates
in_list = []
for i in range(1, len(HLdata)):
    subset = scipy.spatial.distance.mahalanobis([int(HLdata[1][2]), int(HLdata[1][3])], 
                                                 centroid, numpy.linalg.inv(VC_matrix))
    if (subset <= s):
        in_list.append([float(HLdata[i][0]), float(HLdata[i][1]), int(HLdata[i][3]),
                        int(HLdata[i][3]), subset])

###the simulation starts

for r in range(rep):
    C = setPop(in_list) #grid for the number of times a pixel has been colonized 
    #The first accesed pixels matrix (A) starts as the colonized pixel matrix (C)
    A = [[0]*Ncol for i in range(Nrow)]
    for row in range(Nrow):
        for col in range(Ncol):
            if (C[row][col] == 1):
                A[row][col] = 1
                
    for t in range(steps):
        A_now = [[0]*Ncol for i in range(Nrow)] #a list for the accessed pixels on each t
        for row in range(Nrow):
            for col in range(Ncol):            
                if (C[row][col] >= 1): #if there's a population in a pixel (i.e., colonized pixel)
                    if (NdMax != 1):
                    #let's determine how many dispersers will get out from the pixel
                        unkD = True 
                        while unkD:
                            for i in range(len(S_list)):
                                if (S[row][col] <= S_list[i]): 
                                    Nd = Nd_list[i]
                                    unkD = False
                                    break
                    else:
                        Nd = NdMax 
                    to_where = [[0]*2 for i in range(Nd)] #each disperser's movement direction is set randomly
                    for i in range(Nd):                
#                        to_where[i] = direction()
                        #The number of pixels (distance) in latitude and longitude that the disperser will move away from its population are set
                        lat_outside = True
                        while lat_outside:
                            #The distance is taken from a Poisson distribution with lambda = 1
#                            d_lat = np.random.poisson(lam = 1)*to_where[i][0]
                            
                            #The distance is taken from a Normal distribution with mean = 0 & SD = 2
                            d_lat = int(np.random.normal(loc = 0, scale = 2))
                            if (0 <= row + d_lat < Nrow): #if is inside the G grid
                                row_now = row + d_lat
                                lat_outside = False
                        lon_outside = True
                        while lon_outside:
#                            d_lon = np.random.poisson(lam = 1)*to_where[i][1]
                            d_lon = int(np.random.normal(loc = 0, scale = 2))
                            if (0 <= col + d_lon < Ncol):
                                col_now = col + d_lon
                                lon_outside = False
                        A_now[row_now][col_now] += 1 #counts each time a pixel is accessed on time step t
    
        A = updateA(A, A_now) #when all movements have been done, A is updated and stored as a csv
        Amat = np.matrix(A)
        df = pd.DataFrame(data = Amat.astype(int))
        df.to_csv("A_rep"+str(r+1)+".csv", sep = ",", header = False, index = False)
        
        C = updateC(C, A_now) #C needs to be updated before the next t, hence the dispersers will leave just colonized pixels
        Cmat = np.matrix(C)
        df = pd.DataFrame(data = Cmat.astype(int))
        df.to_csv("C_rep"+str(r+1)+".csv", sep = ",", header = False, index = False)            

        result_vectors[r][0][t] = howmany(C) #total number of colonized pixels through time for each rep
        result_vectors[r][1][t] = howmany(A) #total number of accessed pixels through time for each rep
        
    out1.write("For replicate " + str(r+1) + ", " + str(howmany(A)) + 
                   " pixels were accessed and " + str(howmany(C)) + " pixels were colonized" + "\n")
    
    dyn.append(result_vectors[r][0]) #the C vector of change and its title are appended 
    titles.append("C_r" + str(r))
    dyn.append(result_vectors[r][1]) #the A vector of change and its title are appended 
    titles.append("A_r" + str(r))
    
#Finally the vectors of change for A & C (for each replicate) are also stored
dynMat = np.matrix.transpose(np.array(dyn)) 
df = pd.DataFrame(data = dynMat.astype(int))
df.to_csv("change_AC.csv", sep = ",", header = titles, index = False)

out1.close() #close report file

#Plots

################################################# 1) The fundamental niche ellipse

lambda_, v = np.linalg.eig(VC_matrix) #eigenvalues & eigenvectos
plt.figure(0)
ax = plt.gca()
#ellipse = mpatches.Ellipse(xy = (Nf_ellipse[0], Nf_ellipse[1]), width = Nf_ellipse[2], height = Nf_ellipse[3],
#                           angle = Nf_ellipse[4], edgecolor = "r",
#                           fc= "None", lw = 1)
ellipse = mpatches.Ellipse(xy = centroid, width = 2 * np.sqrt(s * lambda_[0]), 
                           height = 2 * np.sqrt(s * lambda_[1]), angle = np.rad2deg(np.arccos(v[0, 0])), #
                           edgecolor = "r", fc= "None", lw = 1) 
ax.add_patch(ellipse)
plt.title("Fundamental Niche 95% ellipse")
plt.xlabel("Temperature (x10)")
plt.xlim(150, 320)
plt.ylabel("Precipitation")
plt.ylim(1000, 4600)
plt.scatter(Temp_list, Prec_list)
plt.savefig("Fundamental_niche.png", dpi = 600, bbox_inches = "tight")
plt.show()

##################################################### 2) Suitability space

plt.figure(1)
plt.imshow(S, interpolation = "none", cmap = "plasma") 
plt.title("S plotted on Geographical space (G)")
plt.colorbar()
plt.savefig("Suitability_space.png", dpi = 600, bbox_inches = "tight")
    
#####################################################Plots for A: 3.1) Binarization

#A way to summarize the information in all replicates of A could be through a sum

rep_names = [] #list of the csv files names
for r in range(rep):
    rep_names.append("A_rep" + str(r+1) + ".csv") #Here, A_rep could be change by C_rep

#Adding replicates
SUM = [[0]*Ncol for i in range(Nrow)]
Final_A = [[0]*Ncol for i in range(Nrow)]

for r in range(rep):
    #importing the list of lists
    with open(rep_names[r], "r") as f:
        reader = csv.reader(f)
        rep_list = list(reader)
        for row in range(Nrow):
            for col in range(Ncol):
                rep_list[row][col] = int(rep_list[row][col]) #transform the list elements to integers
                SUM[row][col] = SUM[row][col] + rep_list[row][col] #sum of replicates

#The matrix of sums can be transformed in a flat list, to exclude the 5% of the pixels with the lowest frequencies
dist_list = []
for row in range(Nrow):
        for col in range(Ncol):
            dist_list.append(SUM[row][col])
            p5 = np.percentile(dist_list, 5) #5th percentile
            if (SUM[row][col] <= p5):
                Final_A[row][col] = 0 #not accessed
            elif (SUM[row][col] > p5):
                Final_A[row][col] = 1 #accessed                

plt.figure(2)
plt.imshow(Final_A, interpolation = "none") 
plt.title("3.1) Summary of A")
plt.colorbar()
plt.savefig("A_summary.png", dpi = 600, bbox_inches = "tight")

#######################################################Plots for A: 3.2) Comparison

list_plotrep = np.random.choice(rep, 4, replace = False) #random list of replicates files
    #But it could be a list of 4 replicates that the user will choose, like: 
#list_plotrep = [0, 3, 7, 8] #remember that it starts with zero
rep_subnames = [] #list of the chosen csv files names for subplots
for r in range(4):
    list_plotrep[r] += 1
    rep_subnames.append("A_rep" + str(list_plotrep[r]) + ".csv") #Here, A_rep could be change by C_rep

M4 = [[[[0]*Ncol for i in range(Ncol)] for j in range(Nrow)] for r in range(4)] #list of replicates to plot
for r in range(4):
    #importing the list of lists
    with open(rep_subnames[r], "r") as f:
        reader = csv.reader(f)
        rep_sublist = list(reader)
        for row in range(Nrow):
            for col in range(Ncol):
                M4[r][row][col] = int(rep_sublist[row][col])
                
plt.figure(3)
for r in range(4):
    plt.subplot(221 + r)
    plt.suptitle("3.2) Comparison of replicates for accessed pixels (A)")
    plt.imshow(M4[r], interpolation = "none", vmin = 0, vmax = maxM4(M4)) #The bars are set to the max value of the 4 rep's
    plt.title("Rep_" + str(list_plotrep[r]))
    plt.colorbar() 
    plt.subplots_adjust(left = 0.1, bottom = 0.05, right = 0.9, top = 0.85, wspace = 0.7, hspace = 0.7)
plt.savefig("A_comparison.png", dpi = 600, bbox_inches = "tight")
    
##################################################change in C and A through time

A_list = [0]*4
for r in range(len(list_plotrep)):
    A_list[r] = result_vectors[list_plotrep[r] - 1][1][steps - 1]
    Amax = max(A_list)
    
plt.figure(4)
for r in range(len(list_plotrep)):
    plt.subplot(221 + r)
    plt.suptitle("Change in C and A through time for each replicate")
    plt.plot(result_vectors[list_plotrep[r] - 1][0], label = "C")
    plt.ylim(0, Amax)
    plt.plot(result_vectors[list_plotrep[r] - 1][1], label = "A")
    plt.title("Rep_" + str(list_plotrep[r]))
    plt.xlabel("Time")
    plt.ylabel("Number of visits")
    plt.subplots_adjust(left = 0.1, bottom = 0.05, right = 0.9, top = 0.85, wspace = 0.7, hspace = 0.7)
    if (r == 2):
        leg = plt.legend(loc = "best", ncol = 1)
plt.savefig("AvsC_change.png", dpi = 600, bbox_inches = "tight")

###

end = time.time()
print("size: ", Nrow, " x ", Ncol, ", rep: ", rep, ", gen: ", steps, ", time: ", end - start, "\n")