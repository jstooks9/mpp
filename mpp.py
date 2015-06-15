# MPP - Mesytec Post-Process
#	use analysis module to process raw data from the mesytec system

# Input arguments:
#	1. name of raw file
#	2. number of columns to keep from original file
#	3. number of bins for histogram
#	4. histogram figure title
#	5. cutoff # of stds for plotting (default 4)

from mesytec_process import *
import sys

filename = sys.argv[1]
numColumns = int(sys.argv[2])
numBins = int(sys.argv[3])
figureTitle = sys.argv[4]
if len(sys.argv) == 6:
	stds = sys.argv[5]
else:
	stds = 4

outfilename = mesytec_parse(filename,numColumns)
histogram_2d(outfilename,numBins,figureTitle,stds)