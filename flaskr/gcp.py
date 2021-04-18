import googlemaps
from . import crimedata
from . import config
from datetime import datetime
gmaps = googlemaps.Client(key=config.GCP_API_KEY)

def get_directions(from_d, to_d):
    # Request directions via public transit
    now = datetime.now()
    return gmaps.directions(
        from_d, to_d, mode="walking", departure_time=now, alternatives=True)

def get_routes(g_directions, time):
    routes = []
    count = 0
    for g_route in g_directions:
        route = {
            "danger": 0,
            "danger_level": "",
            "number_steps": 0,
            "steps": [],
            "directions": [],
            "tot_distance": 0,
            "shootings": False,
            "safest_route": False
        }
        for g_leg in g_route["legs"]:
            for g_step in g_leg["steps"]:
                pos = (g_step["start_location"]["lat"], g_step["start_location"]["lng"])
                if count == 0:
                    prev_pos = pos
                crime_data = crimedata.get_data(pos, prev_pos, time)
                route["danger"] += crime_data[0]
                route["number_steps"] += 1
                route["steps"].append(pos)
                route["directions"].append(g_step["html_instructions"])
                route["tot_distance"] += 0.000621371*g_step["distance"]["value"]
                if crime_data[1] > 1:
                    route["shootings"] = True
                prev_pos = pos
                count = count + 1
        if route["danger"] / route["tot_distance"] > 400:
            print(route["danger"] / route["tot_distance"])
            route["danger_level"] = "RED"
        elif route["danger"] / route["tot_distance"] > 150:
            route["danger_level"] = "YELLOW"
        else:
            route["danger_level"] = "GREEN"
        routes.append(route)
        route["tot_distance"] = round(route["tot_distance"], 2)
    min_danger = 9999
    for route in routes:
        if (route["danger"] / route["tot_distance"]) < min_danger:
            print("new safest")
            min_danger = route["danger"] / route["tot_distance"]
            safest = route
    for route in routes:
        if route == safest:
            route["safest"] = True       
    return routes
