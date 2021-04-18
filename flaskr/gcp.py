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
            "shooting": "No shootings on this route"
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
                if crime_data[1] > 0:
                    route["shooting"] = "Shooting on this route"
                prev_pos = pos
                count = count + 1
        if route["danger"] / route["number_steps"] > 100:
            route["danger_level"] = "RED"
        elif route["danger"] / route["number_steps"] > 75:
            route["danger_level"] = "ORANGE"
        elif route["danger"] / route["number_steps"] > 50:
            route["danger_level"] = "YELLOW"
        elif route["danger"] / route["number_steps"] > 25:
            route["danger_level"] = "YELLOW GREEN ISH"
        elif route["danger"] / route["number_steps"] > 0:
            route["danger_level"] = "GREEN"
        routes.append(route)
    
    return routes

def safest_route(from_, to_, time):
    routes = get_routes(get_directions(from_, to_), time)
    lowest = routes[0]
    for route in routes:
        if route["danger"] < lowest["danger"]:
            lowest = route
    return lowest
