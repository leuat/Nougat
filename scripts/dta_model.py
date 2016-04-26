
import numpy as np
import sys
import os
import math
import random
from subprocess import call

if not len(sys.argv) == 6:
	print "usage: dta_model [ xyz input file ] [ model parameter file ] [ output directory ] [ # random directions ] [ # runs ]"
	exit(1)

XYZFile = sys.argv[1]
modelFile = sys.argv[2]
outDir = sys.argv[3]
noParticles = sys.argv[4]
noRuns = int(sys.argv[5])


for x in range(0, noRuns):
	seed = str(random.randrange(10000))
	number = str(x).rjust(4, '0')   
	outFile = outDir + "/seed" + number  + ".txt"
	print "Run nr " +str(x) + " to file " + outFile
	call(["./nougat", "dta_model", XYZFile, modelFile, outFile, noParticles, seed])
	
#for filename in os.listdir(path):
#	if filename==".DS_Store": continue
#	if  not filename.endswith(".xyz"): continue
#	if not os.path.isdir(path + "/" + filename):
#		inFile = path + "/" + filename
#
