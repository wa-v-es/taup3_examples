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

###

mpl.rcParams.update({'font.size': 14.5})
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
    lons = np.arange(00, 360.1, spacing)
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

    # ax.legend()
    plt.show()

# def plot_dist_diff():


def cal_dist_time(taupserver):
    phases=('P','S')
    eventdepth=30
    eq_lat,eq_lon=45,0
    evt=(eq_lat,eq_lon)
    params = taup.TimeQuery()
    params.model('iasp91')
    params.sourcedepth(eventdepth)
    params.event(eq_lat,eq_lon)
    stations = make_station_grid(45, 0, spacing=5, max_dist=20)
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
        station_data=cal_dist_time(taupserver)


if __name__ == '__main__':
    main()
###
sys.exit()
with taup.TauPServer(taup_path=taup_path) as taupserver:
    for phase in phases:
        params.phase(phase)
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
####
