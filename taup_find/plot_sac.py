# plots sac for visualising PP precursors to illustrate use of Taup find
###
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
import datetime
import matplotlib.dates as mdates
import requests
from datetime import datetime, timedelta

def plot_tt_curve(jsonTimes,c1,c2,text='True'):
    i=0
    for phase in jsonTimes.phases:
        time_ph=[]
        dist_ph=[]
        for a in jsonTimes.arrivals:
            if phase==a.phase:
                # tt=(event_time+a.time).matplotlib_date
                # time_ph.append(tt)
                tt=a.time
                time_ph.append(tt)
                dist_ph.append(a.distdeg)
                if 94==a.distdeg:
                    if text == 'True':
                        ax.text(tt, 93.8,phase,horizontalalignment='center', color=c1,fontsize=14)
                    else:
                        ax.text(tt, 93.5+i,phase,horizontalalignment='center', color=c1,fontsize=9)
                        i=i+.1

        # tp_utc = event_time + time_ph
        ax.plot(time_ph, dist_ph, color=c2, lw=1,ls='-', label=phase)

###
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
eq_lat,eq_long,eq_depth=-14.89, -70.20, 252.00
event_time=UTCDateTime('2022-05-26-12:02:23')
plt.ion()
plt.rcParams.update({'font.size': 13})

with taup.TauPServer(taup_path=taup_path) as taupserver:
    params = taup.TimeQuery()
    params.phase(["pP",'sP','PcP','PP','P^410P','P^660P'])
    params.model('iasp91')
    params.degree(np.arange(94,101,1))
    params.sourcedepth(252)
    jsonTimes = params.calc(taupserver)
    params.phase(['Sed660P^410P','P^410P410s','Pv410pP^660P','Sed660P^660P410s','pP^410P'])# Sed660P^660P410s
    # params.phase(['Pv410pP^660P','Sed660P^660P410s'])

    jsonTimes_ = params.calc(taupserver)


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
fig = plt.figure(figsize=(16, 8))
sns.set_style("whitegrid")#, {"axes.facecolor": ".9"} {"grid.color": ".6", "grid.linestyle": ":"}
sns.set_style("whitegrid",{"axes.facecolor": ".2","grid.color": ".6", "grid.linestyle": ":"})
# [left, bottom, width, height]
ax = fig.add_axes([0.07, 0.1, 0.88, 0.8])
for tr in st_all[::4]:
    t = tr.stats.starttime.matplotlib_date + tr.times() / 86400.
    t = tr.times(reftime=event_time)
    ax.plot(t, .5*tr.data/tr.data.max() + tr.stats.distance,lw=.5,c='white')


plot_tt_curve(jsonTimes,'purple','lightpink')
#bin/taup find --max 2 --deg 95 --evdepth 252 --exclude 20,210,moho --time 960 990 --rayparamdeg 4.3 7.8 --mod iasp91
plot_tt_curve(jsonTimes_,'olivedrab','lightgreen',text='False')


ax.set_ylim(94,99.5)
# ax.xaxis_date()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
# t1=UTCDateTime('2022-05-26T12:15:0').matplotlib_date
# t2=UTCDateTime('2022-05-26T12:20:0').matplotlib_date
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.set_ylabel('Distance ($^\\circ$)')
# ax.set_xlim(750,1060)
ax.set_xlim(920,1060)

ax.yaxis.grid(False)

fig.savefig('btw_410_PP.png', dpi=400, pad_inches=0.1)#bbox_inches='tight',

plt.show()
# for
