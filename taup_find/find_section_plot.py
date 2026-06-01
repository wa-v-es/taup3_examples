# downloads sac files for an event#
from obspy import read, Stream, UTCDateTime,read_events
from obspy.core.event import Origin, Catalog
from obspy.core.inventory.inventory import read_inventory
import numpy as np
from obspy.clients.fdsn import Client
from obspy.clients.fdsn import RoutingClient
import datetime
import os
import sys
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


####
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
client = Client("IRIS")
iris = RoutingClient("iris-federator")
eida = RoutingClient("eida-routing")
# ,RESIF,BGR,INGV,KOERI,IGN,UIB-NORSAR

# starttime= UTCDateTime('2025-07-29T23:24:52') #kamch
starttime= UTCDateTime('2018-08-19T00:19:40') #Fiji

eq_lat,eq_long,eq_depth=52.4948,160.2395,35 #kamch
eq_lat,eq_long,eq_depth=-18.1125,-178.1530,600 #Fiji
endtime= starttime+7000
network_eu="NS,HE,KO,FR,GR,IV"
network_list="II,IM,IU,CU,IC,GT,AK,CN,US,AU,GB,GE"#

try:
    inventory_big=read_inventory("inventory_big_fiji.xml")
except:
    inventory_big = iris.get_stations(network=network_list,starttime=starttime,endtime=endtime)
    # inventory_big += eida.get_stations(network=network_eu,starttime=starttime,endtime=endtime)
    for net in ["NS", "HE", "KO", "FR", "GR", "IV"]:
        try:
            inventory_big += eida.get_stations(network=net,starttime=starttime,endtime=endtime)
            print(net, "OK")
        except Exception:
            print(net, "NO DATA")

    inventory_big.write("inventory_big_fiji.xml",format="STATIONXML")

# # inventory_big.plot(label=False,color_per_network=True,resolution='i',continent_fill_color='honeydew',alpha=.5)
# # download data bit
# stream_all = client.get_waveforms(network=network_list, station='*', location="00",channel= "B*Z", starttime=starttime,endtime=endtime,attach_response=False)
# for net in ["NS", "HE", "KO", "FR", "GR",'IV']:
#     try:
#         stream_all += eida.get_waveforms(network=net, station='*', location="*", channel="B*Z",starttime= starttime,endtime=endtime)#,attach_response=False)
#         print(net, "OK")
#     except Exception:
#         print(net, "NO DATA")
# print('len of stream:',len(stream_all))
# stream_all.resample(20.0)
# stream_all.filter('bandpass',freqmin=.01, freqmax=.2)
#
# # print(len(stream_all))
# for tr in stream_all:
#     if tr.stats.npts>130000:
#         data = os.path.join('sac_fiji_18/')
#         sst='{}.sac'.format(tr.id)
#         tr.write(data+sst,format='sac')
#
# sys.exit()
### read eq data
stream_all=read('sac_fiji_18/*.sac')
stream_all.filter('bandpass',freqmin=.01, freqmax=.1)
stream_all.taper(type='cosine',max_percentage=.1)
### TAUP server
modelname = 'iasp91'
with taup.TauPServer(taup_path=taup_path) as taupserver:
    #Distance query to get garc from earthquake to station
    params = taup.DistazQuery()
    params.model(modelname)
    params.event(eq_lat,eq_long)
    params.sourcedepth(eq_depth)
    for tr in stream_all:
        inv = inventory_big.select(network=tr.stats.network,station=tr.stats.station)
        sta = inv[0][0]
        params.station(sta.latitude,sta.longitude)
        jsondists = params.calc(taupserver)
        tr.stats.distance=jsondists.distances[0].deg
    #### Find query to get phases using earthquake depth and --max
    params_f = taup.FindQuery()
    params_f.model(modelname)
    params_f.max(3)
    params_f.sourcedepth(eq_depth)
    params_f.exclude('20,210,moho,410,660')
    # params_f.pwaveonly()
    jsonfinds = params_f.calcJson(taupserver)
    # Curve query to plot traveltime-dist curve for the phases in find
    params_c = taup.CurveQuery()
    params_c.model(modelname)
    params_c.sourcedepth(eq_depth)
    params_c.phase(jsonfinds['foundphases'])
    jsoncurve = params_c.calc(taupserver)

# sys.exit()
##
stream_all.sort(['distance'],reverse=True)
####
### keep the first trace in a degree bin!
st_bin = Stream()
last_bin = None
for tr in stream_all:
    d_bin = int(tr.stats.distance) # degree bin hack
    if d_bin != last_bin:
        st_bin.append(tr)
        last_bin = d_bin

fig = plt.figure(figsize=(17, 8))
sns.set_style("whitegrid")#, {"axes.facecolor": ".9"} {"grid.color": ".6", "grid.linestyle": ":"}
sns.set_style("whitegrid",{"axes.facecolor": ".2","grid.color": ".6", "grid.linestyle": ":"})
# [left, bottom, width, height]
ax = fig.add_axes([0.07, 0.1, 0.88, 0.8])
for tr in st_bin:#stream_all[::4]
    # t = tr.stats.starttime.matplotlib_date + tr.times() / 86400.
    t = tr.times(reftime=starttime)
    ax.plot(t, 1*tr.data/tr.data.max() + tr.stats.distance,lw=.5,c='white')

for curve in jsoncurve.curves:
    # if curve.label[0]=='p': #useful for shallow eartquakes as depth phases are not well seperated!
    #     continue
    for seg in curve.segments:
        ax.plot(seg.y, seg.x,lw=.35,c='lightgreen',alpha=.75,zorder=2)

# ax.set_ylim(94,99.5)
ax.xaxis.set_minor_locator(MultipleLocator(250))
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_label_position('bottom')
ax.xaxis.tick_bottom()
ax.set_ylabel('Distance ($^\\circ$)')
ax.set_xlim(0,7000)
ax.set_ylim(55,162)
plt.title(f"Fiji August 2018 Mw 8.2")
ax.yaxis.grid(False)
fig.savefig('fiji_55deg_Z.png', dpi=500, pad_inches=0.4)#bbox_inches='tight',
plt.show()
#####
# bin/taup find --max 2 --evdepth 35 --exclude 20,210,moho,410,660 --pwaveonly --mod iasp91
