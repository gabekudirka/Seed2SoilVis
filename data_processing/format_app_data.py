import pandas as pd
import numpy as np
import json 
import re
from geojson import Feature, FeatureCollection, MultiPoint, Point
import uuid
import math
from operator import attrgetter

class Vehicle:
    def __init__(
        self,
        id,
        department,
        make,
        model,
        year,
        vehicle_class
        ):
        self.id = id
        self.department = department
        self.make = make
        self.model = model
        self.year = year
        self.vehicle_class = vehicle_class
        self.trips = []

class Trip:
    def __init__(
        self,
        vehicle,
        start_time,
        end_time,
        date,
        ):
        self.id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.stops = []
        self.num_stops = 0
        self.distance = 0
        self.total_duration = 0
        self.idle_duration = 0
        self.driving_duration = 0
        self.stopped_duration = 0
        self.geojson = []
        self.show = True

    def add_stop(self, stop):
        #self.stops.append(stop.__dict__)
        stop_properties = {
            'vehicle': self.vehicle,
            'stopDuration': stop.stop_duration,
            'idleDuration': stop.idle_duration,
            'startTime': stop.start_time,
            'endTime': stop.end_time,
            'drivingDuration': stop.driving_duration,
            'distance': stop.distance,
            'stopNum': self.num_stops
        }
        point = Point(stop.location)
        feature = Feature(geometry=point, properties=stop_properties)
        self.geojson.append(feature)
        
        self.num_stops += 1
        self.distance += stop.distance
        self.total_duration += (stop.stop_duration + stop.driving_duration)
        self.idle_duration += stop.idle_duration
        self.driving_duration += stop.driving_duration
        self.stopped_duration += stop.stop_duration

class Department:
    def __init__ (
        self,
        name,
        vehicles
    ):
        self.name = name
        self.num_vehicles = len(vehicles);
        self.vehicles = vehicles

class Stop:
    def __init__(
        self,
        location_lat,
        location_long,
        stop_duration,
        idle_duration,
        driving_duration,
        start_time,
        end_time,
        distance
        ):
        self.location = (location_long, location_lat)
        self.stop_duration = stop_duration
        self.idle_duration = idle_duration
        self.driving_duration = driving_duration
        self.start_time = start_time
        self.end_time = end_time
        self.distance = distance
    
if __name__ == '__main__':
    fleet_details_filepath = './raw_data/'
    fleet_details_filename = 'FleetDetails.csv'

    trips_filepath = './raw_data/'
    trips_filename = 'sept-oct_trip_latlng.csv'

    out_filepath = './app_data/'

    fleet_df = pd.read_csv(fleet_details_filepath + fleet_details_filename)

    fleet_df = fleet_df.fillna('')
    #Make sure vehicle names are in correct format
    fleet_df['VehicleName'] = [str(name).split(' ')[0] for name in fleet_df['VehicleName']]
    fleet_df['VehicleName'] = [re.sub('[\W_]+', '', str(name)) for name in fleet_df['VehicleName']]

    #Extract all vehicle objects
    fleet = []
    for idx, row in fleet_df.iterrows():
        vehicle = Vehicle(row['VehicleName'], row['Department'], row['Make'], row['Model'], row['Year'], row['Class'])
        fleet.append(vehicle)

    #Extract all department objects
    depts = []
    groups = fleet_df.groupby('Department')
    for name, rows in groups:
        dept_vehicles = []
        for idx, row in rows.iterrows():
            dept_vehicles.append(row['VehicleName'])
        depts.append(Department(name, dept_vehicles))

    trips_df = pd.read_csv(trips_filepath + trips_filename)

    #Extract all trips
    trip_objs = []
    trips = []
    grouped = trips_df.groupby('TripNum')
    for name, group in grouped:
        trip = Trip(group.iloc[0]['Device'], group.iloc[0]['StopStart'], group.iloc[-1]['StopEnd'], group.iloc[0]['Date'])
        for i, row in group.iterrows():
            # if math.isnan(row.lat) or math.isnan(row.long):
            #     r_row = trips_df.sample(n=1).iloc[0]
            #     while not math.isnan(r_row.lat) and not math.isnan(r_row.long):
            #         r_row = trips_df.sample(n=1).iloc[0]
            #     lat = r_row.lat
            #     lng = r_row.long
            # else:
            #     lat = row.lat
            #     lng = row.long
            if not math.isnan(row.lat) and not math.isnan(row.long):
                stop = Stop(row['lat'], row['long'], row['StopDuration'], row['IdleDuration'], row['DrivingDuration'], row['StopStart'], row['StopEnd'], row['Distance'])
                trip.add_stop(stop)
        trips.append(trip)
        trip_objs.append(trip.__dict__)

    #Assign trips to vehicles
    for vehicle in fleet:
        for trip in trips:
            if vehicle.id == trip.vehicle:
                trip_obj = {
                    'idle_duration': trip.idle_duration,
                    'total_duration': trip.total_duration,
                    'driving_duration': trip.driving_duration,
                    'stopped_duration': trip.stopped_duration,
                    'distance': trip.distance,
                    'start_time': trip.start_time,
                    'end_time': trip.end_time,
                    'num_stops': trip.num_stops,
                }
                vehicle.trips.append(trip_obj)

    #Accumulate vehicle trip statistics
    for vehicle in fleet:
        vehicle.total_trips = 0
        vehicle.total_driving_duration = 0
        vehicle.total_distance = 0
        if len(vehicle.trips) == 0:
            continue
        for trip in vehicle.trips:
            vehicle.total_trips += 1
            vehicle.total_driving_duration += trip['driving_duration']
            vehicle.total_distance += trip['distance']

    #Calculate utilization indicators for vehicles
    max_trips = max(fleet, key=attrgetter('total_trips'))
    max_distance = max(fleet, key=attrgetter('total_distance'))
    max_duration = max(fleet, key=attrgetter('total_driving_duration'))

    for vehicle in fleet:
        vehicle.days_utilization = round(vehicle.total_trips / max_trips.total_trips, 3)
        vehicle.distance_utilization = round(vehicle.total_distance / max_distance.total_distance, 3)
        vehicle.duration_utilization = round(vehicle.total_driving_duration / max_duration.total_driving_duration, 3)
        vehicle.utilization_rate = round((vehicle.days_utilization + vehicle.distance_utilization + vehicle.duration_utilization) / 3, 3)

    #Calculate utilization indicators for departments
    for dept in depts:
        dept_vehicles = []
        for vehicle_id in dept.vehicles:
            vehicle = [vehicle for vehicle in fleet if vehicle.id == vehicle_id]
            dept_vehicles.extend(vehicle)
        dept.avg_days_utilization = 0
        dept.avg_distance_utilization = 0
        dept.avg_duration_utilization = 0
        dept.avg_utilization_rate = 0
        for vehicle in dept_vehicles:
            dept.avg_days_utilization += vehicle.days_utilization
            dept.avg_distance_utilization += vehicle.distance_utilization
            dept.avg_duration_utilization += vehicle.duration_utilization
            dept.avg_utilization_rate += vehicle.utilization_rate
        dept.avg_days_utilization = round(dept.avg_days_utilization / len(dept_vehicles), 3)
        dept.avg_distance_utilization = round(dept.avg_distance_utilization / len(dept_vehicles), 3)
        dept.avg_duration_utilization = round(dept.avg_duration_utilization / len(dept_vehicles), 3)
        dept.avg_utilization_rate = round(dept.avg_utilization_rate / len(dept_vehicles), 3)

    #Make vehicle and department objects serializable
    fleet_obj_arr = []
    for vehicle in fleet:
        fleet_obj_arr.append(vehicle.__dict__)

    dept_obj_arr = []
    for dept in depts:
        dept_obj_arr.append(dept.__dict__)

    fleet_details_obj = {'vehicles': fleet_obj_arr}
    trip_details_obj = {'trips': trip_objs}
    dept_details_obj = {'departments': dept_obj_arr}


    #Process individual stops for heatmap data
    stops_obj_arr = []
    for i, row in trips_df.iterrows():
        if not math.isnan(row.lat) and not math.isnan(row.long):
            stop = Stop(row['lat'], row['long'], row['StopDuration'], row['IdleDuration'], row['DrivingDuration'], row['StopStart'], row['StopEnd'], row['Distance'])
            stop.lat = row['lat']
            stop.lng = row['long']
            stop.device = row['Device']
            stop.group = row['DeviceGroup']
            stops_obj_arr.append(stop.__dict__)

    stops_obj = {'stops': stops_obj_arr}

    #Write all data to files
    with open(out_filepath + "fleet.json", "w") as outfile:
        json.dump(fleet_details_obj, outfile)

    with open(out_filepath + "trips", "w") as outfile:
        json.dump(trip_details_obj, outfile)

    with open(out_filepath + "depts.json", "w") as outfile:
        json.dump(dept_details_obj, outfile)

    with open(out_filepath + "heatmap_data.json", "w") as outfile:
        json.dump(stops_obj, outfile)



