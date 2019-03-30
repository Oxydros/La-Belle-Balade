#!/usr/bin/env python3

from flask import Flask, render_template
import sys

app = Flask(__name__, static_folder="static",
                template_folder="templates")

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()