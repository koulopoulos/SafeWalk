from flask import Flask, request, redirect, url_for, render_template
import datetime
from . import gcp

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        from_l = request.form["starting"]
        to_l = request.form["destination"]
        routes = gcp.get_routes(gcp.get_directions(from_l, to_l), datetime.datetime.now().hour)
        return render_template("routes.html", routes=routes)
    return render_template("index.html")
