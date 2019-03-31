#!/usr/bin/env python3

import requests
import json
import flask
from geojson import Point, Feature
from flask import request, url_for, render_template, redirect, jsonify
from flask_cors import CORS

import journey_optimization
import class_point_interest
import User

import numpy as np

app = flask.Flask(__name__)
CORS(app)

MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoibGFmaXVzIiwiYSI6ImNqdHZpZnl2YTFybTAzeWxsbjJvNjY5eW4ifQ.wirxUDiWbhISy5PGNBHp1A'

def retrievePI(lat_deb, lon_deb, lat_fin, lon_fin):
    box = "("+str(min(lat_deb, lat_fin))+","+str(min(lon_deb, lon_fin))+","+str(max(lat_deb, lat_fin))+","+str(max(lon_deb, lon_fin))+")"
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    (node["tourism"="museum"]"""+box+""";
     way["tourism"="museum"]"""+box+""";
     rel["tourism"="museum"]"""+box+""";
    );
    out center;
    """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()

    coord = {}
    for i in range(len(data["elements"])):
        name = data["elements"][i]["tags"].get("name")
        if(name != None):
            lat = data["elements"][i].get("lat")
            lon = data["elements"][i].get("lon")
            if(lat != None or lon != None):
                coord[name] = (lon, lat)
    return coord

@app.route('/',methods=['GET','POST', 'OPTIONS'])
def index():

    classes = ["musée","parc"]

    lat_deb = float(request.args.get("lat_deb"))
    lon_deb = float(request.args.get("lon_deb"))
    lat_fin = float(request.args.get("lat_fin"))
    lon_fin = float(request.args.get("lon_fin"))


    u = User.User(np.array([0.1,0.2]),(lon_deb, lat_deb), (lon_fin, lat_fin),2000000,keep_point_interests=10)

    coord = retrievePI(float(lat_deb), float(lon_deb), float(lat_fin), float(lon_fin))

    points_of_interest = []

    for key in coord:
        lon, lat = coord[key][0], coord[key][1]
        point = class_point_interest.PointOfInterest("musée", (lon,lat), 1.0, 1001, classes)
        points_of_interest.append(point)
    
    arg_interest = u.find_relevant_interest_points(points_of_interest)
    keep_points_interest = [points_of_interest[elem] for elem in arg_interest]
    j = journey_optimization.Journey(u,keep_points_interest)
    interests, journey_time, travel_time, opt_path = j.get_optimal_journey()

    print(opt_path)
    opt_path = opt_path[1:-1]
    print(opt_path)

    coord = {}

    coord["begin"] = (lon_deb, lat_deb)
    for i in opt_path:
        point = interests[i - 1]
        coord["randomName" + str(i)] = point.coord

    coord["end"] = (lon_fin, lat_fin)
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
        "map_size": [float(lon_deb), float(lat_deb), float(lon_fin), float(lat_fin)]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
