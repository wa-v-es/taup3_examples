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
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

###
def get_dict_amps(TimeResult):
    """
    reads taup_py output and gets phase names and amplitudes. saves highest amp in case of multiple arrival at a distance..
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
            grouped[phase] = abs(amp)

    return grouped
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})

# model="prem" # or 'ak135fcont'
# M 8.2 - 2018 Fiji Earthquake #
# https://earthquake.usgs.gov/earthquakes/eventpage/us1000gcii/executive
# 2018-08-19 00:19:40 (UTC)18.113°S 178.153°W 600.0 km depth
eventdepth=600
phases=['PKP','PKIKP','SKIKS','PKJKP','SKJKS']
phases=['PKP','PKIKP','PKJKP']

plt.ion()
plt.figure(figsize=(14, 5))
ax = plt.axes()
# ax.set_facecolor("whitesmoke")#aliceblue
ax.set_facecolor(to_rgba('darkseagreen', alpha=0.1))
plt.style.use('ggplot')
# plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.5)
dists = []
ratios = []
amps_J=[]
amps_I=[]
amps_K=[]
colors=['mediumpurple','cadetblue','indianred','skyblue','darkgrey']
params = taup.TimeQuery()
with taup.TauPServer(taup_path=taup_path) as taupserver:
    params.model('prem')
    params.sourcedepth(eventdepth)
    # params.station(*sta)
    # params.degree(np.arange(125,136,10))
    params.amp(True)
    params.mw(8.2)
    # params.phase(phases)
    # params.strikediprake([18,69,-94])# fiji
    params.strikediprake([17,7,-62])# 17°	7°	-62 Brazio
    # params.az(60)
    dist=210
    params.degree(dist)
    phase_ratios = defaultdict(list)
    # TimeResult = params.calc(taupserver)
    # sys.exit()
    for i,phase in enumerate(phases):
        j=0
        # for dist in np.arange(60.0,250,2.5):
        for az in np.arange(0.0,360,6):
            params.az(az)
            # params.degree([dist])
            params.phase(phase)
            # for phase, amp in grouped.items():
            TimeResult = params.calc(taupserver)
            amps = get_dict_amps(TimeResult)
            if len(amps)== 0:
                continue
            if amps[phase]!=0:
                if j==0:
                    plt.scatter(az, amps[phase], marker='X', alpha=.8,s=45, color=colors[i],zorder=10,label=phase)
                    j=+1
                else:
                    plt.scatter(az, amps[phase], marker='X', alpha=.8,s=45, color=colors[i],zorder=10)


#             if amps['PKJKP']!=0 and amps['PKIKP']!=0:# and amps['PKP']!=0:
#                 ratio=np.round(amps['PKJKP']/amps['PKIKP'],5)
#                 # print(ratio)
#                 dists.append(dist)
#                 ratios.append(amps['PKIKP'] / amps['PKJKP'])
#                 amps_J.append(amps['PKJKP'])
#                 amps_I.append(amps['PKIKP'])
#                 amps_K.append(amps['PKP'])
#
# plt.plot(dists, amps_K,c='teal',marker='X',markerfacecolor='cadetblue',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKP')#
# plt.plot(dists, amps_I,c='dodgerblue',marker='X',markerfacecolor='skyblue',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKIKP')#
# plt.plot(dists, amps_J,c='indigo',marker='X',markerfacecolor='mediumpurple',markersize=12,markeredgewidth=1.15,linestyle='-',linewidth=1.25,alpha=.65,label='PKJKP')#


# plt.scatter(dists, ratios, marker='X', alpha=.9,s=99, color='palevioletred',zorder=10)
ax.set_yscale("log")
ax.xaxis.set_minor_locator(MultipleLocator(20))
ax.xaxis.set_major_locator(MultipleLocator(40))
# ax.axvline(x=210,ls='--',lw=1.5,c='darkgrey',zorder=1)
# plt.legend(loc='upper left',fontsize='14')
plt.legend(loc='lower right',fontsize='15')

plt.ylabel("Amplitude ($P_{sv}$)")#PKIKP/ PKJKP
# plt.xlabel("Distance ($^\\circ$)")
plt.xlabel("Azimuth ($^\\circ$)")

# plt.title(f"Phase amp; Δ20")
# plt.title(f"Inner core P vs S amp for Mw 8")
# plt.title(f"Amp comparison for core phases for Mw 8.2 eq dist {dist}: prem")


plt.tight_layout()
# plt.savefig('mx8_fiji_5phs_az_155.png',dpi=400,bbox_inches='tight', pad_inches=0.1)
plt.savefig('mx8.2_3phases_dist_210.png',dpi=400,bbox_inches='tight', pad_inches=0.1)
# plt.savefig('mx8.2_3phases.png',dpi=400,bbox_inches='tight', pad_inches=0.1)

# plt.show()
