#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory
import sys

app = Flask(__name__, static_folder="../build")


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  '''Return index.html for all non-api routes'''
  #pylint: disable=unused-argument
  return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(port=8080)