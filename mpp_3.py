# MPP - Mesytec Post-Process
#	use analysis module to process raw data from the mesytec system

# Input arguments:
#	1. name of raw file
#	2. name of input file for settings
#	3. title for the plot

# Input file instructions:
#	Lines with multiple entries use any standard delimiters as specified in
#		the documentation for the split() method. When in doubt, just use
#		spaces.
#	Line 1. Channel numbers with data
#	Line 2. Number of bins for the 2d histogram
#	Line 3. List of detectors used to collect data in ascending MPD-4
#			channel

# Limitations on input:
#	- Only accepts pairs of Ampl/TAC data (in that order)
#	- If you enter an odd number of channels, program will exit

from mesytec_process_3_1 import *
import sys

filename = sys.argv[1]
inputfilename = sys.argv[2]
figureTitle = sys.argv[3]

with open(inputfilename) as f:
	keepColumns = f.readline().split('\n')[0].split()
	keepColumns = [int(x)-1 for x in keepColumns]
	numBins = int(f.readline().split()[0])
	detectors = f.readline().split()
	detectors = detectors[0].split(',')

numPlots = len(keepColumns) / 2
if len(keepColumns) % 2:
	raise Exception('Error: Must enter an even number of channels.')

if len(sys.argv) == 6:
	stds = sys.argv[5]
else:
	stds = 4

parsedfilename = mesytec_parse(filename,keepColumns)
# condense_file(parsedfilename,properKeepColumns)

i = 0
it = []
for c in keepColumns:
	it.append(i)
	i += 1

columns = iter(it)

i = 0
for c in columns:
	histogram_2d(parsedfilename,numBins,figureTitle,stds,c,next(columns),detectors[i])
	i += 1