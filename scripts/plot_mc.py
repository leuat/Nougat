
import numpy as np
import sys
import os
import math
import matplotlib.pyplot as plt

dir = "../../build-NanoPores-Desktop_Qt_5_5_1_clang_64bit-Release/NanoPores/NanoPores.app/Contents/MacOS/"



#def normalise(data):
#	integralSum = 0;
#	for (i in range(0,data[0].))
#     for(int i=0; i<val.size()-1; i++) {
#       //QPointF &p1 = m_points[i];
#        //QPointF &p2 = m_points[i+1];
#        double dx = index[i+1] - index[i];
#        double dy = val[i+1] + val[i];
#        integralSum += dx*dy;
#    }
#    integralSum *= 0.5;
#    for(int i=0; i<val.size(); i++) {
#        val[i] /= integralSum;
#    }

fc = '#B0B0B0'
fcols = ['#F05020', '#2050F0','#50F030', '#40F0F0']

lineWidth = 2.0


def loadMcFile(filename): 
	if (not os.path.isfile(filename)):
		print "Error: could not find file " + filename
		exit(1)
	with open(filename) as f:
	    data = f.read()

	rawdata = data.split('\n')
#	print data
	while '' in rawdata:
	    rawdata.remove('')

	data = {   }

	header = rawdata[0].split(' ')
	while '' in header:
	    header.remove('')

	for name in header:
		data[name] = []

	rawdata.remove(rawdata[0]);
#	print rawdata
	for d in rawdata:
		# ignore comments
		if (not '#' in d):
			values = d.split(' ')
			for i, value in enumerate(values):
				data[header[i]].append(float(value))

	data["chains"] = np.linspace(0,len(data["step"]),len(data["step"]), endpoint = False)
# 	print data["chains"]

#	print data
#	return

	return data


def getAverage(data):
	avg = np.zeros(len(data[0]))
	for d in data:
		avg += d
	avg/=len(data)
	return avg	

def getSigma(data, average):
	sigma = np.zeros(len(data[0]))
	for d in data:
		sigma += np.power(d - average,2)

	sigma = np.sqrt(sigma/len(data))
	return sigma


def addToPlot(x,y, ax, col, lbl, lw, col2):

#	avg = getAverage(data)
#	sigma = getSigma(data, avg)

	ax.plot(x,y, c=col, label=lbl, linewidth=lw)

	#fillMin = [xx - y for xx, y in zip(avg, sigma)]
	#fillMax = [xx + y for xx, y in zip(avg, sigma)]

	#ax1.fill_between(x, fillMin, fillMax, facecolor=col2, edgecolor=col2, interpolate=True, alpha=0.3)


def addFile(filename, ax, col, lbl, lw, col2):
	global curcol
	print "loading " + filename
	d = load(filename)
	ax.plot(d[0],d[1], c=col, label=filename, linewidth=1 , alpha = 0.5)


def addToPlotSingle(data, ax, col, lbl, lw, col2):

	if (os.path.isdir(path)):
		for filename in os.listdir(path):
			if not os.path.isdir(path + "/" + filename):
				if filename.endswith(".txt"):
					addFile(path + "/" + filename, ax,col,lbl,lw,col2)
			else:
				addToPlot(path + "/" + filename, ax, col, lbl, lw, col2)
	else:
		addFile(path, ax,col,lbl,lw,col2)


def chain(argv):
	if (len(argv)<3):
		print "Error: mcmc must supply filename."
		exit(1)
	filename = sys.argv[2];
	data = loadMcFile(dir + filename)

	fig = plt.figure()

	ax = fig.add_subplot(111)

	ax.set_title("MCMC Chain")    
	ax.set_xlabel('Chain')
	ax.set_ylabel('Value')
	color = 0

	for i, value in enumerate(argv):
		if (i>=3):
			ax.plot(data["chains"], data[value], c=fcols[color], label=value, linewidth=lineWidth)
			color+=1
			if (color==len(fcols)):
				color = 0

	leg = ax.legend()
	plt.savefig('mcmc_chain.eps', format='eps', dpi=1000)
	
	plt.show()
	exit(0)


def likelihood1D(argv):
	if (len(argv)<5):
		print "Error: likelihood must supply filename, parameter and # bins."
		exit(1)

	filename = sys.argv[2];
	data = loadMcFile(dir + filename)

	fig = plt.figure()

	parameter = sys.argv[3];
	bins = int(sys.argv[4]);

	ax = fig.add_subplot(111)

	ax.set_title("Likelihood")    
	ax.set_xlabel('Chain')
	ax.set_ylabel('Value')
	
	n, bins, patches = ax.hist(data[parameter], bins, label=parameter, linewidth=lineWidth, normed=1, histtype='stepfilled', color=fcols[0])

	#print n

	leg = ax.legend()
	plt.savefig('mcmc_1d_ " + parameter  + ".eps', format='eps', dpi=1000)
	
	plt.show()
	exit(0)




if len(sys.argv) < 1:
	print "usage: python plot_mcmc.py [ params ]"
	print "    chain 1D [ parameter ] [ # bins ]"
	print "    chain [ list of parameter names ]"


	sys.exit(1)






if (sys.argv[1] == "mcmc"):
	chain(sys.argv)

if (sys.argv[1] == "1d"):
	likelihood1D(sys.argv)

print "\nInvalid command."

exit(1)

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Likelihood")    
ax1.set_xlabel('Scale')
ax1.set_ylabel('Value')

for path in sys.argv:
	if (i!=0):
		if (os.path.isdir(path)):
			addToPlot(path, ax1, fcols[col], path, 2.0,fcols[col])
		else:
			addToPlotSingle(path, ax1, fcols[col], path, 2.0,fcols[col])
		col+=1
		if (col==len(fcols)):
			col = 0


	i+=1



