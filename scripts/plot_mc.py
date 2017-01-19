
import numpy as np
import sys
import os
import re
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
from matplotlib.colors import LogNorm
import scipy.optimize as so
import matplotlib.mlab as mlab

#dir = "../../build-NanoPores-Desktop_Qt_5_5_1_clang_64bit-Release/NanoPores/NanoPores.app/Contents/MacOS/"
dir ="./"


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
DPI = 300
save_dir = ""
display_plot = True
save_plot = False


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
#		print d
		if (not '#' in d):
			values = d.split(' ')
			#print values
			for i, value in enumerate(values):
				#print "before: " + value
				#value = re.sub(r'\W+', '', value)
				value = value.strip()
				value = value.replace("\0x00", "")
				#print "val:" + value + " : " +str(len(value))
				if len(value)==0:
					value = "0"
				#print "after:" + value
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


def chain(argv, data):

	global save_dir
	global save_plot

	fig = plt.figure()

	ax = fig.add_subplot(111)

	ax.set_title("MCMC Chain")    
	ax.set_xlabel('Chain')
	ax.set_ylabel('Value')
	color = 0

	last = 0
	first = ""
	for i, value in enumerate(argv):
		if (i>=0):
			if (first==""):
				first = value
			ax.plot(data["chains"], data[value], c=fcols[color], label=value, linewidth=lineWidth)
			color+=1
			if (color==len(fcols)):
				color = 0
			last = int(i)

	leg = ax.legend()
	if (save_plot):
		plt.savefig(save_dir + 'mcmc_chain_' + first + '.png', format='png', dpi=DPI)
	return True

def likelihood1D(argv, data):
	global save_dir
	global save_plot

	if (len(argv)<2):
		print "Error: likelihood must supply a parameter and # bins."
		return False


	fig = plt.figure()

	parameter = argv[0];
	bins = int(argv[1]);

	ax = fig.add_subplot(111)

	ax.set_title("Likelihood")    
	ax.set_xlabel(parameter)
	ax.set_ylabel('Likelihood')
	
	n, bins, patches = ax.hist(data[parameter], bins, label=parameter, linewidth=lineWidth, normed=1, histtype='stepfilled', color=fcols[0])

	d = data[parameter]

	mu = np.mean(d)
	sigma = np.std(d)

	gauss_x = np.linspace(min(d), max(d), 100)	
	# print gauss_x
	plt.plot(gauss_x,mlab.normpdf(gauss_x, mu, sigma))

	textstr = '$\mu=%.2f$\n$\sigma=%.2f$'%(mu, sigma)
	#print n
	props = dict(boxstyle='round', facecolor='white', alpha=0.5)
	ax.text(0.85, 0.85, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

	plt.axvline(x=mu, ymin=0.0, ymax = max(n)*2, linewidth=2, color='#30FF30')

	leg = ax.legend()
	if (save_plot):
		plt.savefig(save_dir + 'mcmc_1d_' + parameter  + '.png', format='png', dpi=DPI)
	


	return True


def find_confidence_interval(x, pdf, confidence_level):
    return pdf[pdf > x].sum() - confidence_level


def likelihood2D(argv, data):
	global save_dir
	global save_plot

	if (len(argv)<3):
		print "Error: 2d likelihood must supply 2x parameters and # bins."
		exit(1)


	fig = plt.figure()

	parameter1 = argv[0];
	parameter2 = argv[1];
	bins = int(argv[2]);

	ax = fig.add_subplot(111)


	ax.set_title("Likelihood")    
	ax.set_xlabel(parameter1)
	ax.set_ylabel(parameter2)
	
	print "mean x: " + str(np.mean(data[parameter1]))
	print "mean y: " + str(np.mean(data[parameter2]))

	H, xedges, yedges, p = plt.hist2d(data[parameter1], data[parameter2], bins = bins, normed=True)

	x_bin_sizes = (xedges[1:] - xedges[:-1]).reshape((1,bins))
	y_bin_sizes = (yedges[1:] - yedges[:-1]).reshape((bins,1))
	pdf = (H*(x_bin_sizes*y_bin_sizes))

	plt.clf()


	plt.imshow(H, origin = "lower", interpolation = "nearest")#, cmap="CMRmap")

	one_sigma = so.brentq(find_confidence_interval, 0., 1., args=(pdf, 0.68))
	two_sigma = so.brentq(find_confidence_interval, 0., 1., args=(pdf, 0.95))
	X, Y = 0.5*(xedges[1:]+xedges[:-1]), 0.5*(yedges[1:]+yedges[:-1])


	#X, Y = 0.5*(xedges[1:]+xedges[:-1])*bins, 0.5*(yedges[1:]+yedges[:-1]*bins)
 	Z = pdf.T
 	Z = np.swapaxes(Z,0,1)
 	contourcolors = ('yellow', 'yellow', 'white')
	contourlinestyles = ('-', '--', ':')
	contourlinewidths = (1.5, 1.5, 1.5)
	contourlabels = [r'1 $\sigma$', r'2 $\sigma$',r'3 $\sigma$']

# 	contour = plt.contour(Z, levels=[one_sigma, two_sigma], origin="lower", colors=['white', 'white'], linestyles=contourlinestyles)


	plt.title("2D likelihood: " + parameter1 + " and " + parameter2)
	plt.xlabel(parameter2)
	plt.ylabel(parameter1, rotation='horizontal')

	n = 5
	xx = []
	yy = []
	for i in range(0,n):
		xx.append(round(xedges[float(len(xedges)/float(n))*float(i)],2))
		yy.append(round(yedges[float(len(yedges)/float(n))*float(i)],2))


	r = round(np.corrcoef( data[parameter1], data[parameter2] )[1][0],2)

	plt.figtext(0.635, 0.84, "r: "+str(r), color='white')
	plt.yticks(np.linspace(0, int(bins), n, endpoint=False), xx, rotation='horizontal')
	plt.xticks(np.linspace(0, int(bins), n, endpoint=False), yy, rotation='horizontal')

	maxL = np.unravel_index(np.argmax(pdf),pdf.shape)
	xmaxVal= round(X[maxL[0]],2)
	ymaxVal= round(Y[maxL[1]],2)

	print xmaxVal
	print ymaxVal
	xmax = maxL[1]
	ymax = maxL[0]

	plt.axvline(x=xmax, linewidth=1, color='#30FF30')
	plt.axhline(y=ymax, linewidth=1, color='#30FF30')


#	plt.figtext(xmax/float(len(X)),ymax/float(len(Y)),"(" + str(ymaxVal) + "," + str(xmaxVal)+ ")")
	plt.figtext(0.55, 0.80,"maximum: (" + str(ymaxVal) + "," + str(xmaxVal)+ ")", color='white')
#	plt.label(xmax,0, xmaxVal)
#	plt.label(0,ymax, ymaxVal)

#	plt.Circle((30,30),5,color='yellow')
#	print pdf.index(pdf.max())
#	print pdf.argmax(axis=1)
#	print Y.max()


	if (save_plot):
		plt.savefig(save_dir + 'mcmc_2d_' + parameter1 +'_' + parameter2  + '.png', format='png', dpi=DPI)
	
	return True


def set_options(argv):
	i = 0
	global display_plot
	global save_plot
	global save_dir

	for cmd in argv:
		if '-' in cmd:
			i=i+1

			if (cmd=="-save_plot"):
				save_plot = True
				continue
			if (cmd=="-no_display"):
				display_plot = False
				continue

			lst = cmd.split("=")

			if (lst[0].strip()=="-plot_directory"):
				save_dir = lst[1].strip() + "/"
				continue

			print "Error: unknown option: " + cmd
			exit(1)

		else:
			break


	return argv[i:len(argv)]



if len(sys.argv) < 2:
	print "usage: python plot_mcmc.py  [ options ] [ filename ] [ method = chain, 1d, 2d ][ params ] "
	print "  chains: "
	print "    1d [ parameter ] [ # bins ]"
	print "    2d [ parameter1 ] [ parameter2 ] [ # bins ]"
	print "    chain [ list of parameter names ]"
	print "  options: "
	print "    -no_display: Don't display plot"
	print "    -save_plot: Save to disk "
	print "    -plot_directory = [ directory ] : plot save directory "


	sys.exit(1)





params = set_options(sys.argv[1:len(sys.argv)])
filename = params[0]

if (not os.path.isfile(dir + filename)):
	print "Error: could not load file: " + filename
	exit(1)

data = loadMcFile(dir + filename)

# set parameters

ok = False

parseParams = params[2:len(params)]

if (params[1] == "chain"):
	ok = chain(parseParams, data)

if (params[1] == "1d"):
	ok = likelihood1D(parseParams, data)

if (params[1] == "2d"):
	ok = likelihood2D(parseParams, data)

if (ok):
	if (display_plot):
		plt.show()
#	print "K"
else:
	print "\nInvalid command: valid commands are chain, 1d or 2d."

exit(0)

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



