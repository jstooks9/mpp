# Convert a list of hex values into decimal values

# Update from labview_parse_1
# - now includes the option to keep only the first n columns of the original data file,
#     where n is the second user input

# Arguments:
# 1 - unparsed input file name
# 2 - number of columns to keep from the original data file

import sys
from time import time
import numpy as np
import matplotlib.pyplot as plt

def condense_file(filename,columnsKeep):
	with open(filename) as f:
		data = f.read()
	data = data.split('\n') # parse based on newLines
	newData = ''
	for d in data:
		i = 0
		newLine = ''
		currLine = d.split()

		for curr in currLine:
			i += 1
			if i in columnsKeep:
				newLine = newLine+curr+'\t'
		newData += newLine+'\n'

	with open(filename,'w') as f:
		f.write(newData)

def mesytec_parse(filename):
	FILEEXTENSIONLENGTH = 4
	NUMBEROFINPUTS = 32 # inherent to the MADC system

	dataOrder = [0,1,16,17,8,9,24,25,2,3,18,19,10,11,26,27, \
				4,5,20,21,12,13,28,29,6,7,22,23,14,15,30,31]

	outfilename = filename[:-FILEEXTENSIONLENGTH]+'_parsed_OLD.txt'

	initialTime = time()

	with open(filename) as f:
		with open(outfilename,'w') as of:
			while True:
				currLine = f.readline()
				# print('currLine',currLine)
				if currLine == '':
					# print('Output file written to',outfilename)
					break
				if currLine == '4040\n': # marks end of header

					numData = int(previousLine.split()[0][-2:],16) - 1 # convert last 2 bits to decimal,
														   # -1 because of end-header

					batchData = [0]*NUMBEROFINPUTS
					badBatch = False
					# for i in range(numData):
					for i in range(NUMBEROFINPUTS):

						dataLine = f.readline()
						dataidLine = f.readline()

						if dataidLine == '' or dataLine == '':
							break
						data = int(dataLine.split()[0],16)
						dataid = int(dataidLine.split()[0][-2:],16)
						if not dataid == dataOrder[i]:
							badBatch = True
							break
						batchData[dataid] = data
					if not badBatch:
						for bd in batchData:
							of.write(str(bd)+'\t')
						of.write('\n')
				previousLine = currLine # store previous line for later reference

	elapsedTime = time() - initialTime
	print('File written to',outfilename)
	print(round(elapsedTime,3),'seconds taken to parse.')
	# input('check parsed file')
	return outfilename

# -----------------------------------------------------------------
# create 2D histogram, where histogram height is displayed as color

def readParsedFile(filename,xcol,ycol):
	xList = []
	yList = []
	numSTDs = 4
	with open(filename) as f:
		while True:
			currLine = f.readline()
			if currLine == '' or currLine == '\n':
				break
			xList.append(int(currLine.split()[xcol-1]))
			yList.append(int(currLine.split()[ycol-1]))
	return xList, yList

def histogram_2d(inputfilename,nbins,figureTitle,stds,xcol,ycol,detector):

	FILEEXTENSIONLENGTH = 4
	DEFAULTSTDS = 5

	figureName = inputfilename[:-FILEEXTENSIONLENGTH]+'_'+detector+'_plot_OLD.png'

	x, y = readParsedFile(inputfilename,xcol,ycol)

	stdX = np.std(x)
	meanX = np.mean(x)
	maxX = meanX + (stdX * stds)
	minX = meanX - (stdX * stds)
	# maxX = 3000
	# minX = 0

	stdY = np.std(y)
	meanY = np.mean(y)
	maxY = meanY + (stdY * stds)
	minY = meanY - (stdY * stds)
	# maxY = 3000
	# minY = 0

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
	plt.close(fig)
	print('Figure saved as', figureName)