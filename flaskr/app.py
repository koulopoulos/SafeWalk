from flask import Flask, request, redirect, url_for
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
    return """
        <form method="post">
            <input type=text name=from>
            <input type=text name=to>
            <input type=text name=time>
            <input type=submit value=go>
        </form>
    """
