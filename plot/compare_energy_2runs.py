## PLOT ENERGY MAPS FOR TWO RUNS
from __future__ import print_function

# path
import os
path = os.path.dirname(os.getcwd()) + '/'   # on level above
os.chdir(path)                              # change working directory

import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
from cmocean import cm

# OPTIONS
runfolder = [1,2]
print('Produce energy mean plots from run ' + str(runfolder))

## read data

runpath1 = path+'data/run%04i' % runfolder[0]
D1 = np.load(runpath1+'/analysis/mean.npy').all()
param1 = np.load(runpath1+'/param.npy').all()

runpath2 = path+'data/run%04i' % runfolder[1]
D2 = np.load(runpath2+'/analysis/mean.npy').all()
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
expo = 1.   # stretching/squeezing for visualization

for v in ['mke','eke']:
    D1[v] = (D1[v]/1e3)**expo
    D2[v] = (D2[v]/1e3)**expo

for v in ['epe','mpe']:
    D1[v] = (D1[v]/1e3)**expo
    D2[v] = (D2[v]/1e3)**expo

## PLOTTING   
levs=[]
for v in ['mke','eke','mpe','epe']:
    maxs = np.max((np.max(D1[v]),np.max(D2[v])))
    levs.append(np.linspace(0,maxs*0.95,64))

fig,axs = plt.subplots(2,4,figsize=(9,5),sharex=True,sharey=True)
plt.tight_layout(rect=[0,.08,1,0.98])
fig.subplots_adjust(wspace=0.03,hspace=0.03)
n = axs.shape[1]
caxs = [0,]*n
for i in range(n):
    pos = axs[-1,i].get_position()
    caxs[i] = fig.add_axes([pos.x0,0.11,pos.width,0.03])

qaxs = np.empty_like(axs)

tiks = [np.array([0,50,100,150,200,250]),np.array([0,250,500,750,1000]),np.array([0,2.5,5,7.5,10]),np.array([0,10,20,30,40,50])]

qaxs[0,0] = axs[0,0].contourf(param1['x_T'],param1['y_T'],h2mat(D1['mke'],param1),levs[0],cmap=cm.thermal,extend='max')
cb1 = fig.colorbar(qaxs[0,0],cax=caxs[0],orientation='horizontal',ticks=tiks[0]**expo)
cb1.set_ticklabels(tiks[0])
cb1.set_label(r'[kJm$^{-2}$]')

qaxs[0,1] = axs[0,1].contourf(param1['x_T'],param1['y_T'],h2mat(D1['eke'],param1),levs[1],cmap=cm.thermal,extend='max')
cb2 = fig.colorbar(qaxs[0,1],cax=caxs[1],orientation='horizontal',ticks=tiks[1]**expo)
cb2.set_ticklabels(tiks[1].astype(np.int))
cb2.set_label(r'[kJm$^{-2}$]')

qaxs[0,2] = axs[0,2].contourf(param1['x_T'],param1['y_T'],h2mat(D1['mpe'],param1),levs[2],cmap=cm.thermal,extend='max')
cb3 = fig.colorbar(qaxs[0,2],cax=caxs[2],orientation='horizontal',ticks=tiks[2]**expo)
cb3.set_ticklabels(tiks[2])
cb3.set_label(r'[kJm$^{-2}$]')

qaxs[0,3] = axs[0,3].contourf(param1['x_T'],param1['y_T'],h2mat(D1['epe'],param1),levs[3],cmap=cm.thermal,extend='max')
cb4 = fig.colorbar(qaxs[0,3],cax=caxs[3],orientation='horizontal',ticks=tiks[3]**expo)
cb4.set_ticklabels(tiks[3])
cb4.set_label(r'[kJm$^{-2}$]')

axs[1,0].contourf(param2['x_T'],param2['y_T'],h2mat(D2['mke'],param2),levs[0],cmap=cm.thermal,extend='max')
axs[1,1].contourf(param2['x_T'],param2['y_T'],h2mat(D2['eke'],param2),levs[1],cmap=cm.thermal,extend='max')    
axs[1,2].contourf(param2['x_T'],param2['y_T'],h2mat(D2['mpe'],param2),levs[2],cmap=cm.thermal,extend='max')    
axs[1,3].contourf(param2['x_T'],param2['y_T'],h2mat(D2['epe'],param2),levs[3],cmap=cm.thermal,extend='max')    

axs[0,0].set_title(r'MKE')
axs[0,1].set_title(r'EKE')
axs[0,2].set_title(r'MPE')
axs[0,3].set_title(r'EPE')

axs[0,0].set_xticks([])
axs[0,0].set_yticks([])

axs[0,0].set_xlim(0,param1['Lx'])
axs[0,0].set_ylim(0,param1['Ly'])

axs[0,0].set_ylabel(r'LR, $\Delta x = 30$km')
axs[1,0].set_ylabel(r'HR, $\Delta x = 7.5$km')

plt.savefig(path+'figs/energy_mean_2runs.png',dpi=150)
plt.close(fig)
