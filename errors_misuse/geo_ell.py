# compares geodetic, geocentric, and spherical distances.
# creates Figure 6 of Taup 3.2, 2026, paper.
# Shubh Agrawal
# USC, July 2026

import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
##

taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
###
phases=('P','S')

eventdepth=30
evt=(45,-80)
sta=(85,-80)
params = taup.TimeQuery()
plt.ion()
plt.figure(figsize=(12, 6))
ax = plt.axes()
ax.set_facecolor(to_rgba('mistyrose', alpha=0.1))
plt.style.use('ggplot')
colors=['skyblue','darkseagreen']
with taup.TauPServer(taup_path=taup_path) as taupserver:
    params.model('iasp91')
    params.sourcedepth(eventdepth)
    params.event(*evt)
    for phase in phases:
        params.phase(phase)
        for st_lat in np.arange(-45.0,16,10):
            params.station(st_lat,-80)
            params.geodist('spherical')
            TimeResult_sph = params.calc(taupserver)
            dist=TimeResult_sph.arrivals[0].distdeg
            t_sph=TimeResult_sph.arrivals[0].time
            for i,geod in enumerate(['geocentric','geodetic']):
                    params.geodist(geod)
                    TimeResult = params.calc(taupserver)
                    # cmdLine = params.asCommandLine(taupserver)
                    # print('command line prompt:',cmdLine)
                    for arr in TimeResult.arrivals:
                        # print('phase:',arr.phase,'time:',arr.time,arr.distdeg)
                        # print(TimeResult_sph.arrivals[0].time)
                        t_diff=arr.time-t_sph
                        if arr.phase=='P':
                            plt.scatter(dist, t_diff, marker='o', alpha=1,s=75, color=colors[i],zorder=10)#,label=phase)
                        else:
                            plt.scatter(dist, t_diff, marker='o', alpha=1,s=75, color=colors[i],zorder=10)#,label=phase)

plt.ylabel("$ \Delta $ Time (s)")
plt.xlabel("Distance ($^\\circ$)")
legend_elements = [Line2D([0], [0], marker='o', color='skyblue',
           markersize=8, linestyle='None', label='Geocentric '),
    Line2D([0], [0], marker='o', color='darkseagreen',
           markersize=8, linestyle='None', label='Geodetic')]

ax.set_xlim(27,95)
ax.text(92.5,-3.3,'S',bbox={'facecolor': 'white', 'alpha': 0.85, 'pad': 3.5},fontsize=18,c='maroon')
ax.text(92.5,-1.7,'P',bbox={'facecolor': 'white', 'alpha': 0.85, 'pad': 3.5},fontsize=18,c='maroon')

ax.legend(handles=legend_elements, ncol=2,prop={'family': 'sans-serif', 'size': plt.rcParams['axes.labelsize']})
plt.savefig('sphr_diff.png',dpi=400,bbox_inches='tight', pad_inches=0.1)
