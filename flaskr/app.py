from flask import Flask, request, redirect, url_for, render_template
import datetime
from . import gcp

app = Flask(__name__)

@app.route("/route/<routes>")
def route(routes):
    return render_template("routes.html", routes=routes)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        from_l = request.form["starting"]
        to_l = request.form["destination"]
        route = gcp.get_routes(gcp.get_directions(from_l, to_l), datetime.datetime.now().hour)
        return redirect(url_for("route", route_data=route))
    return render_template("index.html")
