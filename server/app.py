#!/usr/bin/env python3

import requests
import json
import flask
from geojson import Point, Feature
from flask import request, url_for, render_template, redirect, jsonify
from flask_cors import CORS

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
    lat_deb = request.args.get("lat_deb")
    lon_deb = request.args.get("lon_deb")
    lat_fin = request.args.get("lat_fin")
    lon_fin = request.args.get("lon_fin")

    coord = retrievePI(float(lat_deb), float(lon_deb), float(lat_fin), float(lon_fin))
    ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/walking/{0}.json?access_token={1}&overview=full&geometries=geojson"
    lat_longs = ";".join(["{0},{1}".format(value[0], value[1]) for key, value in coord.items()])

    url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)

    result = requests.get(url)
    result = result.json()

    geometry = result["routes"][0]["geometry"]
    return jsonify(geometry)

if __name__ == '__main__':
    app.run(debug=True)
