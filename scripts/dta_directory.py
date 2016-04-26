
import numpy as np
import sys
import os
import math
from subprocess import call

if not len(sys.argv) == 4:
	print "usage: [ xyz dir ] [ output dir ] [ # random directions ]"
	exit(1)

path = sys.argv[1]
outDir = sys.argv[2]
noParticles = sys.argv[3]

for filename in os.listdir(path):
	if filename==".DS_Store": continue
	if  not filename.endswith(".xyz"): continue
	if not os.path.isdir(path + "/" + filename):
		inFile = path + "/" + filename
		outFile = outDir + "/" + filename.replace("xyz","txt")
		call(["./nougat", "dta", inFile, outFile, noParticles])

