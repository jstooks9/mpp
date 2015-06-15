# Convert a list of hex values into decimal values

# Update from labview_parse_2
# Trying to fix streaking in data, likely artifacts from the
#	parsing algorithm

# Arguments:
# 1 - unparsed input file name
# 2 - number of columns to keep from the original data file

import sys
from time import time

FILEEXTENSIONLENGTH = 4
NUMBEROFINPUTS = 32 # inherent to the MADC system

dataOrder = [0,1,16,17,8,9,24,25,2,3,18,19,10,11,26,27, \
			4,5,20,21,12,13,28,29,6,7,22,23,14,15,30,31]

filename = sys.argv[1]
if len(sys.argv) == 3:
	numberColumnsKeep = int(sys.argv[2])
else:
	numberColumnsKeep = NUMBEROFINPUTS

outfilename = filename[:-FILEEXTENSIONLENGTH]+'_parsed_TEST.txt'

initialTime = time()

with open(filename) as f:
	with open(outfilename,'w') as of:
		while True:
			currLine = f.readline()
			if currLine == '':
				# print('Output file written to',outfilename)
				break
			if currLine == '4040\n': # marks end of header
				# print(previousLine) # DEBUGGING
				numData = int(previousLine.split()[0][-2:],16) - 1 # convert last 2 bits to decimal,
													   # -1 because of end-header
				# print(numData) # DEBUGGING
				batchData = [0]*NUMBEROFINPUTS
				badBatch = False
				# for i in range(numData):
				for i in range(2):
					# print(f.tell())
					dataLine = f.readline()
					dataidLine = f.readline()
					data = int(dataLine.split()[0],16)
					dataid = int(dataidLine.split()[0][-2:],16)
					if not dataid == dataOrder[i]:
						badBatch = True
						break
					batchData[dataid] = data
				if not badBatch:
					# print(batchData)
					for bd in batchData:
						of.write(str(bd)+'\t')
					of.write('\n')
			previousLine = currLine # store previous line for later reference

elapsedTime = time() - initialTime
print(round(elapsedTime,3),'seconds taken to parse.')