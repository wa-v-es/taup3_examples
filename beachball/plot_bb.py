import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from scipy.interpolate import griddata
from obspy.imaging.beachball import beach
from matplotlib.colors import LinearSegmentedColormap
# from cmcrameri import cm


taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 13})
########
neg = "lightgray"
pos = "seagreen"
cmap_bb = LinearSegmentedColormap.from_list("custom_bb",[neg, "white", pos],N=256)

strike,dip,rake=17,7,-62

phases=['PKP','PKIKP','PKJKP']
eventdepth=607
params = taup.BeachballQuery()
dist=210
# dist=-150
azi=90
clip= False

with taup.TauPServer(taup_path=taup_path) as taupserver:
    params.model('prem')
    params.sourcedepth(eventdepth)
    params.phase(phases)
    params.degree(dist)
    params.az(azi)

    # params.station(*sta)
    params.strikediprake(strike,dip,rake)
    cmdLine = params.asCommandLine(taupserver)
    print('command line prompt:',cmdLine)
    BB = params.calc(taupserver)

r_phases=[]
for arr in BB.arrivals:
    take_off_rad=np.radians(arr.takeoff)
    r_ph=np.sqrt(2) * np.sin(take_off_rad / 2)
    r_phases.append([r_ph,arr.phase])
print(r_phases)

####
# sys.exit()
takeoff=np.asarray([list[0] for list in BB.radiationPattern])
azimuth=np.asarray([list[1] for list in BB.radiationPattern])
P_amp=np.asarray([list[2] for list in BB.radiationPattern])

##
theta = np.radians(takeoff)
phi = np.radians(azimuth)

r = np.sqrt(2) * np.sin(theta / 2)
x = r * np.sin(phi)
y = r * np.cos(phi)

N = 500
gx = np.linspace(-1.02, 1.02, N)
gy = np.linspace(-1.02, 1.02, N)
GX, GY = np.meshgrid(gx, gy)

GZ = griddata((x, y),P_amp,(GX, GY),method='linear')

fig, ax = plt.subplots(figsize=(6,6))
clip_c = plt.Circle((0, 0), 0.5, transform=ax.transData)
levels = np.linspace(-np.nanmax(np.abs(GZ)), np.nanmax(np.abs(GZ)),51)
cf = ax.contourf(GX,GY,GZ,levels=levels,cmap=cmap_bb,extend='both')
if clip:
    cf.set_clip_path(clip_c)
    # for c in cf.collections:
    #     c.set_clip_path(clip)
    circle = plt.Circle((0,0),.5,fill=False,lw=.5,color='k')

else:
    circle = plt.Circle((0,0),1,fill=False,lw=.5,color='k')

ax.add_patch(circle)
###
# circles for phases
ax.add_patch(plt.Circle((0,0),r_phases[1][0],fill=False,lw=1.75,ls='--',color='mediumpurple',label=r_phases[1][1]))
ax.add_patch(plt.Circle((0,0),r_phases[0][0],fill=False,lw=1.75,ls='--',color='cadetblue',label=r_phases[0][1]))
ax.add_patch(plt.Circle((0,0),r_phases[3][0],fill=False,lw=1.75,ls='--',color='indianred',label=r_phases[3][1]))


# ax.plot(xP, yP, 'ko', ms=7)
# ax.plot(xT, yT, 'wo', ms=7, mec='k')
# plt.scatter(dist, t_diff, marker='o', alpha=1,s=75, color=colors[i],zorder=10)#,label=phase)
# plt.colorbar(cf,label='P amplitude')
title = f" Strike = {strike}°   Dip = {dip}°   Rake = {rake}°"
ax.set_title(title, pad=12)

if clip:
    offset = .52
else:
    offset = 1.02

ax.text(0,  offset, 'N', ha='center', va='bottom', fontweight='bold')
ax.text(offset, 0, 'E', ha='left',   va='center', fontweight='bold')
ax.text(0, -offset, 'S', ha='center', va='top'  , fontweight='bold')
ax.text(-offset, 0, 'W', ha='right',  va='center', fontweight='bold')
ax.set_aspect('equal')

if clip:
    ax.set_xlim(-.65,.65)
    ax.set_ylim(-.65,.65)
else:
    ax.set_xlim(-1.15,1.15)
    ax.set_ylim(-1.15,1.15)

plt.legend(loc='lower right',fontsize='13')

ax.axis('off')
plt.savefig('bb_amp_phases_d210.png',dpi=400,bbox_inches='tight', pad_inches=0.1)

plt.show()
