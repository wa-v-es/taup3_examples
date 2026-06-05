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
######
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
###
eq_id='us6000m31m'
# https://earthquake.usgs.gov/earthquakes/eventpage/us6000m31m/executive# Afgan eq!
# 36.474°N 70.746°E203.0 km depth

vel_mod='ak135fcont'
phase_list=['PKKP','SKKS','PKJKP']
phase_list=['PKKP']
"""
#adian, radian180, degree, degree180, kilometer, kilometer180, rayparamrad, rayparamdeg, rayparamkm,
 time, tau, takeoffangle, incidentangle, turndepth, dpddelta, dpddeg, amp, amppsv, ampsh, phase,
 phasepsv, phasesh, phasedeg, phasedegpsv, phasedegsh, unwrapphasedeg, unwrapphasedegpsv, unwrapphasedegsh,
 geospread, refltran, refltranpsv, refltransh, index, tstar, attenuation, energygeospread, pathlength,
 radiation, radiationpsv, radiationsh, intcaustic
"""
with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.CurveQuery()
    params.phase(phase_list)
    params.model(vel_mod)
    # params.degree([np.arange(90.0,150,10)])
    # params.degree([np.arange(90.0,150,10)])

    # params.eid(eq_id)
    # params.amp(True)
    # params.mw(6.4)
    params.sourcedepth(203)
    params.yaxis('attenuation')
    params.xaxis('degree')
    jsonCurve = params.calc(taupserver)
    cmdLine = params.asCommandLine(taupserver)
    print('command line prompt:',cmdLine)

###
plt.ion()
fig, axs = plt.subplots(2, 3,figsize=(15, 10),sharex=False,sharey=False)
ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[0, 2]
ax4 = axs[1, 0]
ax5 = axs[1, 1]
ax6 = axs[1, 2]
###
for curve in jsonCurve.curves:
    for seg in curve.segments:
        ax1.plot(seg.x, seg.y,c='dodgerblue',linestyle='-',linewidth=1.25,alpha=.85,label=curve.label)#marker='X',markerfacecolor='skyblue',markersize=12,markeredgewidth=1.15,
        ax1.set_xlabel('Distance ($^\\circ$)')
        ax1.set_ylabel('Attenuation (?)')
