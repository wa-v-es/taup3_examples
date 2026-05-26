# using the taup's amptiude feature, compares amplitude of core phases!

import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import seaborn as sns
from obspy import read, Stream, UTCDateTime,read_events
from obspy.geodetics import gps2dist_azimuth
from collections import defaultdict
from matplotlib.colors import to_rgba
###
def get_dict_amps(TimeResult):
    """
    readfs taup_py output and gets phase names and amplitudes.
    """
    grouped = defaultdict()
    for a in TimeResult.arrivals:
        phase=a.phase
        amp=float(a.amp.factorpsv)
        prev = grouped.get(phase)
        # bit for triplication cases
        if prev is None or abs(amp) > abs(prev):
            if prev != None: #debug step
                pass
                # print(f"prev:{prev}; phase:{phase}; abs amp{abs(amp)}")
            grouped[phase] = amp

    return grouped
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14})

# model="prem" # or 'ak135fcont'
eventdepth=500
phases=['PKJKP','PKIKP','PKP']
plt.ion()
plt.figure(figsize=(14, 6))
ax = plt.axes()
# ax.set_facecolor("whitesmoke")#aliceblue
ax.set_facecolor(to_rgba('darkseagreen', alpha=0.15))
plt.style.use('ggplot')
# plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.5)
dists = []
ratios = []
amps_J=[]
amps_I=[]
amps_K=[]

with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.TimeQuery()
    params.model('prem')
    params.sourcedepth(eventdepth)
    # params.station(*sta)
    # params.degree(np.arange(125,136,10))
    params.amp(True)
    params.mw(8)
    params.phase(phases)
    # params.strikediprake([45,20,45])
    # params.az(20)
    phase_ratios = defaultdict(list)
    # TimeResult = params.calc(taupserver)
    # sys.exit()

    for dist in np.arange(105.0,176,2):
        params.degree([dist])
        # for phase, amp in grouped.items():
        TimeResult = params.calc(taupserver)
        amps = get_dict_amps(TimeResult)
        if len(amps)!= 3:
            continue
        if amps['PKJKP']!=0 and amps['PKIKP']!=0:# and amps['PKP']!=0:
            ratio=np.round(amps['PKJKP']/amps['PKIKP'],5)
            # print(ratio)
            dists.append(dist)
            ratios.append(amps['PKIKP'] / amps['PKJKP'])
            amps_J.append(amps['PKJKP'])
            amps_I.append(amps['PKIKP'])
            amps_K.append(amps['PKP'])


plt.plot(dists, amps_K,c='teal',marker='X',markerfacecolor='cadetblue',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKP')#
plt.plot(dists, amps_I,c='dodgerblue',marker='X',markerfacecolor='skyblue',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKIKP')#
plt.plot(dists, amps_J,c='indigo',marker='X',markerfacecolor='mediumpurple',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKJKP')#


# plt.scatter(dists, ratios, marker='X', alpha=.9,s=99, color='palevioletred',zorder=10)
ax.set_yscale("log")
plt.legend()
plt.ylabel("Amplitude (Psv)")#PKIKP/ PKJKP
plt.xlabel("Distance ($^\\circ$)")
# plt.title(f"Phase amp; Δ20")
# plt.title(f"Inner core P vs S amp for Mw 8")
plt.title(f"Amp comparison for core phases for Mw 8 explosion")


plt.tight_layout()
plt.savefig('mx8_expl_3phases.png',dpi=400,bbox_inches='tight', pad_inches=0.1)
plt.show()
