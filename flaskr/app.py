from flask import Flask
from . import gcp

app = Flask(__name__)

@app.route("/")
def index():
    return gcp.safest_route("Northeastern University", "Boston University")
