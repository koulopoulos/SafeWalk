from flask import Flask, request, redirect, url_for, render_template
from . import gcp

app = Flask(__name__)

@app.route("/route/<route_data>")
def route(route_data):
    return f"""
        <div>{route_data}</div>
    """

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        route = gcp.safest_route(request.form["from"], request.form["to"], request.form["time"])
        return redirect(url_for("route", route_data=route))
    return render_template("index.html")
