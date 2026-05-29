# downloads sac files for an event#
from obspy import read, Stream, UTCDateTime,read_events
from obspy.core.event import Origin, Catalog
import numpy as np
from obspy.clients.fdsn import Client
import datetime
import os
import sys
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

####
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
client = Client("IRIS")

starttime= UTCDateTime('2025-07-29T23:24:52') #2025-07-29 23:24:52
eq_lat,eq_long,eq_depth=52.4948,160.2395,35
endtime= starttime+5000
network_list=['II','IM','IU']
network_list="II,IM,IU,CU,IC,GT"#
inventory_big = client.get_stations(network=network_list,starttime=starttime,endtime=endtime)
# stream_all=client.get_waveforms(network_list, '*', "00", "B*Z", starttime,endtime,attach_response=False)
# stream_all.resample(20.0)
# stream_all.filter('bandpass',freqmin=.01, freqmax=.2)
#
# # print(len(stream_all))
# for tr in stream_all:
#     data = os.path.join('sac_kamch/')
#     sst='{}.sac'.format(tr.id)
#     tr.write(data+sst,format='sac')

###
stream_all=read('sac_kamch/*.sac')
stream_all.filter('bandpass',freqmin=.01, freqmax=.1)
stream_all.taper(type='cosine',max_percentage=.05)
with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.DistazQuery()
    params.model('iasp91')
    params.event(eq_lat,eq_long)
    params.sourcedepth(eq_depth)
    for tr in stream_all:
        inv = inventory_big.select(network=tr.stats.network,station=tr.stats.station)
        sta = inv[0][0]
        params.station(sta.latitude,sta.longitude)
        jsondists = params.calc(taupserver)
        tr.stats.distance=jsondists.distances[0].deg
##
stream_all.sort(['distance'],reverse=True)
fig = plt.figure(figsize=(16, 8))
sns.set_style("whitegrid")#, {"axes.facecolor": ".9"} {"grid.color": ".6", "grid.linestyle": ":"}
sns.set_style("whitegrid",{"axes.facecolor": ".2","grid.color": ".6", "grid.linestyle": ":"})
# [left, bottom, width, height]
ax = fig.add_axes([0.07, 0.1, 0.88, 0.8])
for tr in stream_all:#stream_all[::4]
    t = tr.stats.starttime.matplotlib_date + tr.times() / 86400.
    t = tr.times(reftime=starttime)
    ax.plot(t, 2*tr.data/tr.data.max() + tr.stats.distance,lw=.4,c='white')
# ax.set_ylim(94,99.5)
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.set_ylabel('Distance ($^\\circ$)')
ax.set_xlim(0,4800)
plt.title(f"Kamchatka July 2025 Mw 8.8")
ax.yaxis.grid(False)
# fig.savefig('btw_410_PP.png', dpi=400, pad_inches=0.1)#bbox_inches='tight',
plt.show()
