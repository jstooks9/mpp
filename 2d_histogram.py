# create 2D histogram, where histogram height is displayed as color

import numpy as np
import matplotlib.pyplot as plt
import sys

# Arguments:
# 1 - data filename
# 2 - number of bins
# 3 - figure title
# 4 - cutoff for # of stds (default 4)

def make_histogram(data, bins):
	range = max(data) - min(data)
	binWidth = range / float(bins)
	histogram = [0]*bins # initialize histogram
	for d in data:
		index = int(d / binWidth) # calculate which bin to tally
		histogram[index] += 1

	binList = [0] # initialize list of upper bin boundaries
	for i in range(0,bins):
		binList.append(binWidth + binWidth*i) # populate binList with 
											  #  upper bin boundary values
	return binList, histogram # return x,y data for the histogram

def readParsedFile(filename):
	xList = []
	yList = []
	numSTDs = 4
	with open(filename) as f:
		while True:
			currLine = f.readline()
			if currLine == '':
				break
			xList.append(int(currLine.split()[0]))
			yList.append(int(currLine.split()[1]))
	return xList, yList


##################################################
# Main Program
##################################################

FILEEXTENSIONLENGTH = 4
DEFAULTSTDS = 5

#________________________________________________|
# Inputs                                        #| 
inputfilename = sys.argv[1]                     #|
nbins = int(sys.argv[2])                        #|
figureTitle = sys.argv[3]                       #|
if len(sys.argv) == 5:                          #|
	stds = float(sys.argv[4])                   #|
else:                                           #|
	stds = DEFAULTSTDS                          #|
#________________________________________________| 

figureName = inputfilename[:-FILEEXTENSIONLENGTH] + '_plot.png'

x, y = readParsedFile(inputfilename)

stdX = np.std(x)
meanX = np.mean(x)
maxX = meanX + (stdX * stds)
minX = meanX - (stdX * stds)
# maxX = 3600
# minX = 0

stdY = np.std(y)
meanY = np.mean(y)
maxY = meanY + (stdY * stds)
minY = meanY - (stdY * stds)
# maxY = 2500
# minY = 500

trimmedX = []
trimmedY = []
for i, j in zip(x,y):
	if i < minX or i > maxX or j < minY or j > maxY:
		continue
	trimmedX.append(i) 
	trimmedY.append(j)


H, xedges, yedges = np.histogram2d(trimmedX, trimmedY, bins = nbins)

H = np.rot90(H)
H = np.flipud(H)

Hmasked = np.ma.masked_where(H==0,H)

fig = plt.figure()
plt.set_cmap("spectral")
plt.pcolormesh(xedges,yedges,Hmasked)
plt.ylabel('TAC')
plt.xlabel('Amplitude')
plt.title(figureTitle)
cbar = plt.colorbar()

plt.savefig(figureName)
print('Figure saved as', figureName)