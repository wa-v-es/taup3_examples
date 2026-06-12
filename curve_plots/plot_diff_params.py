# ideas for comparing seismic attributes of phases
##
import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import seaborn as sns
from collections import defaultdict
from matplotlib.colors import to_rgba
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from obspy.clients.fdsn import Client

def plot_attribute(ax,jsonCurve,cl):
    for curve in jsonCurve.curves:
        for seg in curve.segments:
            ax.plot(seg.x, seg.y,c=cl,linestyle='-',linewidth=1.5,alpha=.95,label=curve.label)#marker='X',markerfacecolor='skyblue',markersize=12,markeredgewidth=1.15,
            # ax.set_xlabel('Distance ($^\\circ$)')
            ax.set_ylabel(curve.y)
######
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
###
client = Client("USGS")
eq_id='us6000m31m' # afgan eq
eq_id='us6000sasz' # Malaysia deep eq

catalog = client.get_events(eventid=eq_id)
origin=catalog[0].origins[0]
eq_lat,eq_long,eq_depth=origin.latitude,origin.longitude,origin.depth/1000
eq_mw=catalog[0].magnitudes[0].mag
nodal_plane=catalog[0].focal_mechanisms[0].nodal_planes['nodal_plane_1']
strike,dip,rake=nodal_plane.strike,nodal_plane.dip,nodal_plane.rake
# sys.exit()
# https://earthquake.usgs.gov/earthquakes/eventpage/us6000m31m/executive# Afgan eq!
# 336.498°N 70.601°E204.0 km depth

"""
#radian, radian180, degree, degree180, kilometer, kilometer180, rayparamrad, rayparamdeg, rayparamkm,
 time, tau, takeoffangle, incidentangle, turndepth, dpddelta, dpddeg, amp, amppsv, ampsh, phase,
 phasepsv, phasesh, phasedeg, phasedegpsv, phasedegsh, unwrapphasedeg, unwrapphasedegpsv, unwrapphasedegsh,
 geospread, refltran, refltranpsv, refltransh, index, tstar, attenuation, energygeospread, pathlength,
 radiation, radiationpsv, radiationsh, intcaustic
"""

yAxis = ['time',"rayparamdeg", "turndepth", "amppsv", "refltran","attenuation"]
cl=['teal','indianred','slateblue']
vel_mod='ak135fcont'
phase_list=['Smp','ScSP','PKKP'] #Pcp^660P,Pcpv660P
### Scs^660P,ScSP,SP,ScSP,Scs^660P
plt.ion()
fig, axs = plt.subplots(2, 3,figsize=(15, 10),sharex=False,sharey=False)
# sns.set_style("whitegrid")
sns.set_style("whitegrid",{"axes.facecolor": "ghostwhite","grid.color": ".6", "grid.linestyle": ":"})
ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[0, 2]
ax4 = axs[1, 0]
ax5 = axs[1, 1]
ax6 = axs[1, 2]
axx=[ax1,ax2,ax3,ax4,ax5,ax6]
with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.CurveQuery()
    params.model(vel_mod)
    # params.degree([np.arange(90.0,150,10)])
    params.mw(eq_mw)
    params.sourcedepth(eq_depth)
    params.xaxis('degree')
    params.strikediprake(strike,dip,rake)
    params.az(45)
    for j, yAtt in enumerate(yAxis):
        for i, phase in enumerate(phase_list):
            params.yaxis(yAtt)
            params.phase(phase)
            jsonCurve = params.calc(taupserver)
            cmdLine = params.asCommandLine(taupserver)
            print('command line prompt:',cmdLine)
            plot_attribute(axx[j],jsonCurve,cl[i])

ax6.set_xlabel('Distance ($^\\circ$)')
for ax in [ax3,ax6]:
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
ax6.legend()

# plt.savefig('attributes_june12.png',dpi=400,bbox_inches='tight', pad_inches=0.1)

###

###
