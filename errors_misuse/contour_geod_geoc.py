# compares geodetic, geocentric, and spherical distances for an earthq and a grid of stations around it.
##
import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.tri as tri
from matplotlib.ticker import FormatStrFormatter
###

mpl.rcParams.update({'font.size': 15.5})
###
def spherical_distance(lat1, lon1, lat2, lon2):
    # lat1, lat2 = np.radians([lat1, lat2])
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)

    dlat = lat2 - lat1
    dlon = np.radians(lon2 - lon1)

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2 * np.degrees(np.arcsin(np.sqrt(a)))

def make_station_grid(eq_lat, eq_lon, spacing=5, max_dist=50):

    lats = np.arange(-90, 90.1, spacing)
    lons = np.arange(-180, 180.1, spacing)
    lon2d, lat2d = np.meshgrid(lons, lats)

    # spherical GRC from earthquake
    dist_deg = spherical_distance(np.full(lat2d.shape, eq_lat),np.full(lon2d.shape, eq_lon),lat2d,lon2d)

    mask = (dist_deg <= max_dist) & ( spacing <=dist_deg)

    stations = np.column_stack([lat2d[mask],lon2d[mask]])
    # mask = [dist_deg <= max_dist,spacing <=dist_deg]

    return stations
def plot_stations(eq_lat, eq_lon, stations):
    fig = plt.figure(figsize=(12, 7))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    # ax.add_feature(cfeature.BORDERS, linewidth=0.3)

    ax.scatter(stations[:, 1],stations[:, 0],s=5,marker='^',color='teal',transform=ccrs.PlateCarree(),alpha=.65)
    ax.scatter(eq_lon,eq_lat,s=90,marker='*',color='darkred',edgecolor='darkred',transform=ccrs.PlateCarree(),zorder=5)
    plt.show()

def plot_dist_diff(station_data,param1='dist_geod',param2='dist_sph',eq_lon=0,eq_lat=45,cmap='cividis',label="$ \Delta $ Time (s)",figname='map.png'):
    data = pd.DataFrame.from_dict(station_data)
    data['param_diff']=data[param1]-data[param2]

    triang = tri.Triangulation(data['lon'],data['lat'])
    ##
    fig = plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()

    cf = ax.tricontourf(triang,data['param_diff'],levels=20,cmap=cmap,transform=ccrs.PlateCarree())

    # ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    cb = plt.colorbar(cf,ax=ax,orientation='horizontal',pad=0.05,shrink=0.65)
    ax.scatter(eq_lon,eq_lat,s=130,marker='*',color='white',edgecolor='white',transform=ccrs.PlateCarree(),zorder=5)

    cb.set_label(label)
    # cb.ax.set_yticklabels(["{:.1}".format(i) for i in cb.get_ticks()]) # ticks
    cb.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    plt.savefig(figname,dpi=400,bbox_inches='tight', pad_inches=0.1)
    plt.show()

def cal_dist_time(taupserver,spacing=5, max_dist=50):
    phases=('S')
    eventdepth=30
    eq_lat,eq_lon=30,0
    evt=(eq_lat,eq_lon)
    params = taup.TimeQuery()
    params.model('iasp91')
    params.sourcedepth(eventdepth)
    params.event(eq_lat,eq_lon)
    stations = make_station_grid(eq_lat, eq_lon, spacing=spacing, max_dist=max_dist)
    print(f"Length of stations in grid: {len(stations)}..\n")
    # plot_stations(eq_lat, eq_lon, stations)

    # sys.exit()
    station_data=[]
    for phase in phases:
        params.phase(phase)
        print(f"Doing phase: {phase}..\n")
        for st in stations:
            params.station(*st)
            params.geodist('spherical')
            TimeResult_sph = params.calc(taupserver)
            dist_sph=TimeResult_sph.arrivals[0].distdeg
            time_sph=TimeResult_sph.arrivals[0].time
            params.geodist('geocentric')
            TimeResult_geoc = params.calc(taupserver)
            dist_geoc=TimeResult_geoc.arrivals[0].distdeg
            time_geoc=TimeResult_geoc.arrivals[0].time
            params.geodist('geodetic')
            TimeResult_geod = params.calc(taupserver)
            dist_geod=TimeResult_geod.arrivals[0].distdeg
            time_geod=TimeResult_geod.arrivals[0].time


            station_data.append({
                'lat': st[0],
                'lon': st[1],
                'dist_sph': dist_sph,
                'time_sph': time_sph,
                'dist_geod': dist_geod,
                'time_geod': time_geod,
                'dist_geoc': dist_geoc,
                'time_geoc': time_geoc,
                'phase': phase})

    print(f"lenth of station data: {len(station_data)}")
    return station_data
def main():
    taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
    # taup_path="~/Code/seis/TauP/build/install/TauP/bin/taup"

    with taup.TauPServer(taup_path=taup_path) as taupserver:
        station_data=cal_dist_time(taupserver,spacing=5, max_dist=90)

    # plot_dist_diff(station_data,'dist_geod','dist_sph',eq_lon=0,eq_lat=40,cmap='cividis',label="$ \Delta $ Distance ($^\\circ$)",figname='geod_dist.png')
    # plot_dist_diff(station_data,'dist_geoc','dist_sph',eq_lon=0,eq_lat=40,cmap='cividis',label="$ \Delta $ Distance ($^\\circ$)",figname='geoc_dist.png')
    plot_dist_diff(station_data,'time_geod','time_sph',eq_lon=0,eq_lat=40,cmap='magma',label="$ \Delta $ Time (s)",figname='geod_time.png')
    plot_dist_diff(station_data,'time_geoc','time_sph',eq_lon=0,eq_lat=40,cmap='magma',label="$ \Delta $ Time (s)",figname='geoc_time.png')

if __name__ == '__main__':
    main()
###
sys.exit()

####
