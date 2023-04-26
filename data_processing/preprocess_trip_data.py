import numpy as np
import pandas as pd
import glob
import os
import googlemaps
import geocoder
import folium
import matplotlib.pyplot as plt
import geojsoncontour

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from folium.plugins import MarkerCluster
from scipy.interpolate import griddata

def convert_to_minutes(d):
    if len(d) == 4:
        return int(d[:1])*60 + int(d[2:])
    elif len(d) == 5:
        return int(d[:2])*60 + int(d[3:])
    elif len(d) == 6:
        return int(d[:3])*60 + int(d[4:])

if __name__ == '__main__':
    in_filepath = './raw_data/'
    in_filename = 'sept-oct_trips.csv'

    out_filepath = './raw_data/'
    out_filename = 'sept-oct_trip_latlng.csv'

    #If a vehicle is stopped for this many minutes, indicate that a trip is over
    final_stop_duration = 720

    #Get data fields into correct formats
    df = pd.read_csv(in_filepath + in_filename)
    df = df[df['Device'].notna()]

    df['DrivingDuration'] = df['DrivingDuration'].apply(convert_to_minutes)
    df['StopDuration'] = df['StopDuration'].apply(convert_to_minutes)
    df['IdleDuration'] = df['IdleDuration'].apply(convert_to_minutes)
    df['TripNum'] = 0
    df['NonTripStop'] = False

    trip_num = 0
    for idx, row in df.iterrows():
        if row['StopDuration'] > final_stop_duration:
            df['NonTripStop'].iloc[idx] = True
            trip_num += 1
        else:
            df['TripNum'].iloc[idx] = trip_num

    df = df[df['NonTripStop'] == False]

    #Use geocoding to extract lat and long coordinates from locations
    df['lat'] = np.nan
    df['long'] = np.nan

    #Using us census geocoder
    locations = []
    coords = []
    for index, row in df.iterrows():
        locations.append(row.Location)
        if len(locations) == 9000:
            batch_coords = geocoder.uscensus(locations, method='batch')
            coords.extend(batch_coords)
            locations = []
    batch_coords = geocoder.uscensus(locations, method='batch')
    coords.extend(batch_coords)

    for i, coord in enumerate(coords):
        df.lat.iloc[i] = coord.lat
        df.long.iloc[i] = coord.lng

    #Using ArcGis geocoder
    # for index, row in df.iterrows():
    #     location = row.Location
    #     g = geocoder.arcgis(location)
    #     if g.json is not None:
    #         df.lat.iloc[index] = g.json['lat']
    #         df.long.iloc[index] = g.json['lng']

    df.to_csv(out_filepath + out_filename, encoding='utf-8')