
import numpy as np
import sys
import os
import math
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

#dir = "../../build-NanoPores-Desktop_Qt_5_5_1_clang_64bit-Release/NanoPores/NanoPores.app/Contents/MacOS/"
dir = "./"
#filename = "mc.txt"
directory = "figures"
tmpfile = "tmp"
fformat = "png"
bins = "25"

def mcmc(params):
	print "Performing chain on parameters: "
	for p in params:
		print "  - " + p
		os.system("python plot_mc.py -no_display -save_plot -plot_directory=" + directory + " " + filename + " chain " + p)

def mcmc_1d(params):
	global bins

	for p in params:
		print "  - " + p
		os.system("python plot_mc.py -no_display -save_plot -plot_directory=" + directory + " " + filename + " 1d " + p + " " + bins)

def mcmc_2d(params):
	global bins
	print "Performing 2d on parameters: "
	for p in params:
		print "  - " + p[0] + " and " + p[1]
		os.system("python plot_mc.py -no_display -save_plot -plot_directory=" + directory + " " + filename + " 2d " + p[0] +" " + p[1] + " " + bins)


def getfilename(typ, p1):
	global directory
	if (typ=="chain"):
		return directory + "/mcmc_chain_" + p1 + ".eps"
	if (typ=="1d"):
		return directory + "/mcmc_1d_" + p1 + ".eps"
	if (typ=="2d"):
		return directory + "/mcmc_2d_" + p1[0] + "_" + p1[1] + ".eps"


def getAllParams(params, typ):
	allparams = params
	if (typ=="2d"):
		allparams = []
		for i in range(0,len(params)):
			for j in range(i+1,len(params)):
				allparams.append([params[i], params[j]])

	return allparams

def combine(sizex,sizey, params, typ, wx, wy):
	print "Combining..."
	tmp = directory + "/" + tmpfile + "." + fformat
	resultfile = directory + "/" + typ + "." + fformat

	# First, create empty 
	os.system("convert -size "+str(sizex)+"x"+str(sizey)+" xc:white " + tmp)

	grid = []

#	if (params)

	dx=sizex/int(wx)
	dy=sizey/int(wy)


	#print allparams
	#exit(1)

	curP = 0
	shouldBreak = False
	for i in range(int(wx)):
		if (shouldBreak):
			break
		for j in range(int(wy)):
			xx = str(i*dx)
			yy = str(j*dy)
			print xx + ", " + yy + " : " + getfilename(typ, params[curP])
			addstr = "+" +xx + "+" + yy
			os.system("composite -geometry "+str(dx) +"x" + str(dy) + addstr + " " + getfilename(typ, params[curP]) + " " + tmp + " " + tmp)
			curP = curP +1
			if curP>=len(params):
				shouldBreak = True
				break

	os.system("mv " + tmp + " " + resultfile)
	os.system("open " + resultfile)

if len(sys.argv)<6:
	print "usage: python plot_mcmc_all.py [chain/1d/2d] [ ignore ][ x size ] [ y size ] [ list of params ] [ mc.txt ]"
	exit(1)


typ = sys.argv[1];
ignore = sys.argv[2]
x = sys.argv[3]
y = sys.argv[4]
filename = sys.argv[5]
params = getAllParams(sys.argv[5:len(sys.argv)], typ)
if (not ignore == "ignore"):
	if typ=="chain":
		mcmc(params)
	elif typ=="1d":
		mcmc_1d(params)
	elif typ=="2d":
		mcmc_2d(params)
	else:
		print "Unknown command: " + typ
		exit(1)
else:
	print "Ignoring calculations ... "

combine(1024,768, params, typ, x, y)


