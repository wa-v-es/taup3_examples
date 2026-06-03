#downloads and saves ea data as sac files
from obspy import read, Stream, UTCDateTime,read_events
from obspy.core.event import Origin, Catalog
from obspy.core.inventory.inventory import read_inventory
import numpy as np
from obspy.clients.fdsn import Client
from obspy.clients.fdsn import RoutingClient
import datetime
####
iris = RoutingClient("iris-federator")
eida = RoutingClient("eida-routing")

starttime= UTCDateTime('2018-08-19T00:19:40') #Fiji

eq_lat,eq_long,eq_depth=-18.1125,-178.1530,600 #Fiji
endtime= starttime+7000
network_eu="NS,HE,KO,FR,GR,IV"
network_list="II,IM,IU,CU,IC,GT,AK,CN,US,AU,GB,GE"#

try:
    inventory_big=read_inventory("inventory_big_fiji.xml")
except:
    inventory_big = iris.get_stations(network=network_list,starttime=starttime,endtime=endtime)
    for net in ["NS", "HE", "KO", "FR", "GR", "IV"]:
        try:
            inventory_big += eida.get_stations(network=net,starttime=starttime,endtime=endtime)
            print(net, "OK")
        except Exception:
            print(net, "NO DATA")
    inventory_big.write("inventory_big_fiji.xml",format="STATIONXML")

# inventory_big.plot(label=False,color_per_network=True,resolution='i',continent_fill_color='honeydew',alpha=.5)
# download data bit
stream_all = client.get_waveforms(network=network_list, station='*', location="00",channel= "B*Z", starttime=starttime,endtime=endtime,attach_response=False)
for net in ["NS", "HE", "KO", "FR", "GR",'IV']:
    try:
        stream_all += eida.get_waveforms(network=net, station='*', location="*", channel="B*Z",starttime= starttime,endtime=endtime)#,attach_response=False)
        print(net, "OK")
    except Exception:
        print(net, "NO DATA")
print('len of stream:',len(stream_all))
stream_all.resample(20.0)
stream_all.filter('bandpass',freqmin=.01, freqmax=.2)

# print(len(stream_all))
for tr in stream_all:
    if tr.stats.npts>130000: # to remove spurious traces with less npts
        data = os.path.join('sac_fiji_18/')
        sst='{}.sac'.format(tr.id)
        tr.write(data+sst,format='sac')
####
