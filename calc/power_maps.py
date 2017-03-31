from __future__ import print_function
path = '/home/mkloewer/python/swm/'
import os; os.chdir(path) # change working directory
import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
import time as tictoc
from netCDF4 import Dataset
import glob
from matplotlib.colors import BoundaryNorm,LogNorm
import cmocean

# OPTIONS
runfolder = [3,10]
print('Plots for run ' + str(runfolder))

## read data

runpath1 = path+'data/run%04i' % runfolder[0]
D1 = np.load(runpath1+'/analysis/power_map.npy').all()
param1 = np.load(runpath1+'/param.npy').all()

runpath2 = path+'data/run%04i' % runfolder[1]
D2 = np.load(runpath2+'/analysis/power_map.npy').all()
param2 = np.load(runpath2+'/param.npy').all()

# functions
def h2mat(h,param):
    return h.reshape((param['ny'],param['nx']))

def u2mat(u,param):
    return u.reshape((param['ny'],param['nx']-1))

def v2mat(v,param):
    return v.reshape((param['ny']-1,param['nx']))

def q2mat(q,param):
    return q.reshape((param['ny']+1,param['nx']+1))
##

in1 = h2mat(D1['InPower_T'],param1)
in1 = np.sign(in1)*np.sqrt(abs(in1))

ex1 = h2mat(D1['ExPower_T'],param1)
ex1 = np.sign(ex1)*np.sqrt(abs(ex1))

in2 = h2mat(D2['InPower_T'],param2)
in2 = np.sign(in2)*np.sqrt(abs(in2))

ex2 = h2mat(D2['ExPower_T'],param2)
ex2 = np.sign(ex2)*np.sqrt(abs(ex2))

## PLOTTING   

fig,axs = plt.subplots(2,2,figsize=(9,9),sharex=True,sharey=True)

plt.tight_layout(rect=[0,.08,1,0.98])
fig.subplots_adjust(wspace=0.03,hspace=0.03)

pos = axs[-1,0].get_position()
pos2 = axs[-1,-1].get_position()
cax = fig.add_axes([pos.x0,0.07,pos2.x1-pos.x0,0.03])

levs = np.linspace(-0.3,0.3,64)
tik = np.array([-0.3,-0.2,-0.1,0,0.1,0.2,0.3])

q1 = axs[0,0].contourf(param1['x_T'],param1['y_T'],in1,levs,cmap=cmocean.cm.balance,extend='both')
axs[0,1].contourf(param1['x_T'],param1['y_T'],ex1,levs,cmap=cmocean.cm.balance,extend='both')
cbar = fig.colorbar(q1,cax=cax,orientation='horizontal',ticks=tik)
cbar.set_label(r'Power [Wm$^{-2}$]')
cbar.set_ticklabels(tik**2*np.sign(tik))


axs[1,0].contourf(param2['x_T'],param2['y_T'],in2,levs,cmap=cmocean.cm.balance,extend='both')        
axs[1,1].contourf(param2['x_T'],param2['y_T'],ex2,levs,cmap=cmocean.cm.balance,extend='both')  

axs[0,0].set_title('Energy input: wind forcing')
axs[0,1].set_title('Energy exit: lateral mixing')

axs[0,0].set_xticks([])
axs[0,0].set_yticks([])

axs[0,0].set_ylabel(r'Low resolution, $\Delta x = 30$km')
axs[1,0].set_ylabel(r'High resolution, $\Delta x = 7.5$km')

plt.savefig(path+'compare/power_maps.png')
plt.close(fig)
