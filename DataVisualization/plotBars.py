import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from random import randint

def plotBars(tupla,x_subtitle,y_subtitle):
	x = [tupla[i][0] for i in range(len(tupla))]
	y = [tupla[i][1] for i in range(len(tupla))]
	plt.axes([0.0,0.0,1,1])
	maxValue = max(y)

	if(type(y[0]) == int):
		textformat = "%d"
	else:
		textformat = "%.2f"

	for i in range(len(x)):
		if(y[i] == maxValue):
			plt.bar(i,y[i],facecolor='#8b0a50',edgecolor = 'white',align='center')
		else:
			plt.bar(i,y[i],facecolor='#cccccc',edgecolor = 'white',align='center')
		plt.text(i, y[i], x[i], ha='center', va= 'bottom',fontsize=7)
		if(y[i] / float(maxValue) > 0.25):
			plt.text(i,y[i] / 2,textformat % y[i],ha='center',va='bottom',fontsize=9)


	plt.text(-len(x) * 0.1,maxValue / 2,y_subtitle,ha='center',va='baseline',fontsize=15,rotation='vertical')
	plt.text(len(x) / 2, -max(y) * 0.15,x_subtitle,ha='center',va='bottom',fontsize=15)

	plt.xlim(-len(x) * 0.15, len(x) + len(x) * 0.15)
	plt.xticks(())
	plt.ylim( max(y) * -0.15, max(y) + max(y) * 0.15)
	plt.yticks(())	
	plt.show()

def plotDualBars(tupla,x_subtitle,y_subtitle):
	n = len(tupla)
	X = np.arange(n)
	Y1 = [ x[1] for x in tupla ]#(1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
	Y2 = [ -x[2] for x in tupla ]#(1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
	plt.bar(X, Y1, facecolor='#90ee90', edgecolor='white')
	plt.bar(X, Y2, facecolor='#ff9999', edgecolor='white')

	for x, y in zip(X, Y1):
	    plt.text(x + 0.4, y / 2, '%d' % y, ha='center', va= 'bottom')
	    plt.text(x + 0.4, y, tupla[x][0], ha='center', va= 'bottom',fontsize=7)
	for x, y in zip(X, Y2):
	    plt.text(x + 0.4, y / 2, '%d' % (y * -1), ha='center', va= 'top')
	
        plt.text((-0.25 * n) - 0.25,len(y_subtitle)/ 2 + 0,y_subtitle,ha='center',va='baseline',fontsize=15,rotation='vertical')
        plt.text(n / 2, min(Y2) + ( min(Y2)* 0.15),x_subtitle,ha='center',va='bottom',fontsize=15)

	plt.xlim((-0.25 * n), n + (n* 0.25))
	plt.xticks(())
	plt.yticks(())
	plt.ylim( min(Y2) - ( max(max(Y1), abs(min(Y2))) * 0.25 ),max(Y1) + (max(max(Y1),abs(min(Y2))) * 0.25)   )
	plt.show()
