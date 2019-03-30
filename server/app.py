#!/usr/bin/env python3

import requests
import json
from flask import Flask, render_template, request
import sys

app = Flask(__name__, static_folder="static",
                template_folder="templates")

def retrievePI(lat_deb, lon_deb, lat_fin, lon_fin):
    box = "("+str(min(lat_deb, lat_fin))+","+str(max(lon_deb, lon_fin))+","+str(max(lat_deb, lat_fin))+","+str(min(lon_deb, lon_fin))+")"
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
        lat = data["elements"][i].get("lat")
        lon = data["elements"][i].get("lon")
        coord[name] = (lat, lon)
    return coord


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        coord = retrievePI(data["lat_deb"], data["lon_deb"], data["lat_fin"], data["lon_fin"])
        return render_template('index.html', route=routes, point=points)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
