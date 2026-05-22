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

###
eq_lat,eq_long,eq_depth=-14.89, -70.20, 252.00

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
    # t = tr.times()
    t = tr.stats.starttime.matplotlib_date + tr.times() / 86400.
    ax.plot(t, .5*tr.data/tr.data.max() + tr.stats.distance,lw=.2,c='navy')
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.show()
# for
