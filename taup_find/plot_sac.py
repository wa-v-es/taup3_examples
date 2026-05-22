# plots sac for visualising PP precursors to illustrate use of Taup find
###
import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from obspy import read, Stream, UTCDateTime,read_events
from obspy.geodetics import gps2dist_azimuth
import datetime
import matplotlib.dates as mdates
import requests
from datetime import datetime, timedelta

###
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
eq_lat,eq_long,eq_depth=-14.89, -70.20, 252.00
event_time=UTCDateTime('2022-05-26-12:02:23')

with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.TimeQuery()
    params.phase(["P","pP",'sP','PcP','PP','P^410P','P^660P'])
    params.model('iasp91')
    params.degree(np.arange(94,101,1))
    params.sourcedepth(252)
    jsonTimes = params.calc(taupserver)

# for a in jsonTimes.arrivals:
#     print(f"{a.phase} {a.distdeg:.2f} {a.time:.2f} {a.rayparam:.2f}")

# sys.exit()
st_all=read('sac_eq_220526_120223/*.sac')
st_all=read('sac_eq_220526_120223/*.sac')

for st in st_all: st.stats.distance=st.stats.sac['gcarc']

startT=UTCDateTime('2022-05-26T12:14:40')
endT=UTCDateTime('2022-05-26T12:20:40')

st_all.trim(starttime=startT,endtime=endT)
st_all.sort(['distance'],reverse=True)
st_all.filter('bandpass',freqmin=.05, freqmax=2)
# print(st_all[11].stats)
    # st.stats.
    # d,v,b=gps2dist_azimuth(eq_lat, eq_long, stlat[j], stlong[j])
# st_all[::5].plot(type='section')
# sys.exit()
fig = plt.figure(figsize=(15, 8))
# [left, bottom, width, height]
ax = fig.add_axes([0.07, 0.1, 0.88, 0.8])
for tr in st_all[::4]:
    t = tr.stats.starttime.matplotlib_date + tr.times() / 86400.
    ax.plot(t, .5*tr.data/tr.data.max() + tr.stats.distance,lw=.2,c='navy')

for phase in jsonTimes.phases:
    time_ph=[]
    dist_ph=[]
    for a in jsonTimes.arrivals:
        if phase==a.phase:
            tt=(event_time+a.time).matplotlib_date
            time_ph.append(tt)
            dist_ph.append(a.distdeg)
            if 94==a.distdeg:
                ax.text(tt, 93.9,phase, color='purple',fontsize=12)

    # tp_utc = event_time + time_ph
    ax.plot(time_ph, dist_ph, color='maroon', lw=1,ls='-', label=phase)

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.show()
# for
