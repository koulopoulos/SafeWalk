from flask import Flask, request, redirect, url_for
from . import gcp

app = Flask(__name__)

@app.route('/route')
def route(route):
    return f"Your route is: {route}"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        route = gcp.safest_route(request.form["from"], request.form["to"])
        return redirect(url_for("route", route=route))
    return """
        <form method="post">
            <input type=text name=from>
            <input type=text name=to>
            <input type=submit value=go>
        </form>
    """




#gcp.safest_route("Northeastern University", "Boston University")
