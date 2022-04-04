# import matplotlib.pyplot as plt
# from drawnow import drawnow, figure
import numpy as np
from pylab import *
from drawnow import drawnow, figure
import matplotlib

# matplotlib.use('Qt5Agg')
matplotlib.use('QtAgg')


def plot_now():
    plot(x,y)

x = np.linspace(0,5,50)

for i in np.linspace(0,10,1000):
    y = np.sin(i*x)
    drawnow(plot_now)



print('end of file')