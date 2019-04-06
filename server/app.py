#!/usr/bin/env python3

## -*- coding: utf-8 -*-

import requests
import json
import codecs
import flask
from geojson import Point, Feature
from flask import request, url_for, render_template, redirect, jsonify
from flask_cors import CORS
import csv

import journey_optimization
import class_point_interest
import User

import numpy as np

app = flask.Flask(__name__)
CORS(app)

MAPBOX_ACCESS_KEY = '**MAPBOX ACCESS TOKEN**'

def retrievePI(lat_deb, lon_deb, lat_fin, lon_fin):
    coord = {}
    # if(abs(lat_fin-lat_deb) < 0.1 or abs(lon_fin-lon_deb) < 0.1):
    #    box = "("+str(min(lat_deb, lat_fin)-0.1)+","+str(min(lon_deb, lon_fin)-0.1)+","+str(max(lat_deb, lat_fin)+0.1)+","+str(max(lon_deb, lon_fin)+0.1)+")"
    # else:
    box = "("+str(min(lat_deb, lat_fin))+","+str(min(lon_deb, lon_fin))+","+str(max(lat_deb, lat_fin))+","+str(max(lon_deb, lon_fin))+")"

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query_museum = """
    [out:json];
    (node["tourism"="museum"]"""+box+""";
     way["tourism"="museum"]"""+box+""";
     rel["tourism"="museum"]"""+box+""";
    );
    out center;
    """
    overpass_query_workship = """
    [out:json];
    (node["amenity"="place_of_worship"]"""+box+""";
     way["amenity"="place_of_worship"]"""+box+""";
     rel["amenity"="place_of_worship"]"""+box+""";
    );
    out center;
    """
    overpass_query_market = """
    [out:json];
    (node["amenity"="marketplace"]"""+box+""";
     way["amenity"="marketplace"]"""+box+""";
     rel["amenity"="marketplace"]"""+box+""";
    );
    out center;
    """
    overpass_query_view = """
    [out:json];
    (node["tourism"="viewpoint"]"""+box+""";
     way["tourism"="viewpoint"]"""+box+""";
     rel["tourism"="viewpoint"]"""+box+""";
    );
    out center;
    """
    response_museum = requests.get(overpass_url,
                            params={'data': overpass_query_museum})
    data1 = response_museum.json()
    
    response_workship = requests.get(overpass_url,
                            params={'data': overpass_query_workship})
    data2 = response_workship.json()
    
    response_market = requests.get(overpass_url,
                            params={'data': overpass_query_market})
    data3 = response_market.json()
    
    response_view = requests.get(overpass_url,
                            params={'data': overpass_query_view})
    data4 = response_view.json()

    for i in range(len(data1["elements"])):
        name = data1["elements"][i]["tags"].get("name")
        if(name != None):
            lat = data1["elements"][i].get("lat")
            lon = data1["elements"][i].get("lon")
            if(lat != None or lon != None):
                coord[name] = (lon, lat, "museum")
    for i in range(len(data2["elements"])):
        name = data2["elements"][i]["tags"].get("name")
        if(name != None):
            lat = data2["elements"][i].get("lat")
            lon = data2["elements"][i].get("lon")
            if(lat != None or lon != None):
                coord[name] = (lon, lat, "place_of_worship")
    for i in range(len(data3["elements"])):
        name = data3["elements"][i]["tags"].get("name")
        if(name != None):
            lat = data3["elements"][i].get("lat")
            lon = data3["elements"][i].get("lon")
            if(lat != None or lon != None):
                coord[name] = (lon, lat, "marketplace")
    for i in range(len(data4["elements"])):
        name = data4["elements"][i]["tags"].get("name")
        if(name != None):
            lat = data4["elements"][i].get("lat")
            lon = data4["elements"][i].get("lon")
            if(lat != None or lon != None):
                coord[name] = (lon, lat, "viewpoint")
    return coord

@app.route('/',methods=['GET','POST'])
def index():

    classes = ["museum","viewpoint", "place_of_worship", "marketplace"]

    #Fetch position points
    lat_deb = float(request.args.get("lat_deb"))
    lon_deb = float(request.args.get("lon_deb"))
    lat_fin = float(request.args.get("lat_fin"))
    lon_fin = float(request.args.get("lon_fin"))

    interest_values = [float(request.args.get(classes_name)) for classes_name in classes]

    time = float(request.args.get("free_time"))

    print("User interests %s  free time %f"%(interest_values, time))

    u = User.User(np.array(interest_values),(lon_deb, lat_deb), (lon_fin, lat_fin), time,keep_point_interests=10)

    coord = retrievePI(float(lat_deb), float(lon_deb), float(lat_fin), float(lon_fin))

    points_of_interest = []
    
    museumR = {}

    with open('museum.csv', 'r', encoding='ISO-8859-1') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            museumR[row[0]] = float(row[1])

    for key in coord:
        lon, lat = coord[key][0], coord[key][1]
        if(key in museumR):
            point = class_point_interest.PointOfInterest(coord[key][2], (lon,lat), museumR[key], 1001, classes, name=key)
        else:
            point = class_point_interest.PointOfInterest(coord[key][2], (lon,lat), 0.3, 1001, classes, name=key)
        points_of_interest.append(point)
    
    arg_interest = u.find_relevant_interest_points(points_of_interest)
    keep_points_interest = [points_of_interest[elem] for elem in arg_interest]
    j = journey_optimization.Journey(u,keep_points_interest)
    interests, journey_time, travel_time, opt_path, schedule = j.get_optimal_journey()

    print(schedule)
    #Remove first and last
    opt_path = opt_path[1:-1]

    coord = {}

    places = []
    coord["begin"] = (lon_deb, lat_deb, "Home")
    for i in opt_path:
        point = interests[i - 1]
        coord[point.name] = point.coord
        places.append(point.place_class)

    coord["end"] = (lon_fin, lat_fin, "End")
    print(coord)

    ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/walking/{0}.json?access_token={1}&overview=full&geometries=geojson"
    lat_longs = ";".join(["{0},{1}".format(value[0], value[1]) for key, value in coord.items()])

    url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)

    result = requests.get(url)
    result = result.json()

    geometry = result["routes"][0]["geometry"]

    coord_list = []
    for key in coord:
        coord_list.append([key, coord[key][0], coord[key][1]])

    data = {
        "geometry": geometry,
        "coord": coord_list,
        "map_size": [float(lon_deb), float(lat_deb), float(lon_fin), float(lat_fin)],
        "schedule": schedule.tolist(),
        "places": places
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
