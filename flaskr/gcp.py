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
            "steps": []
        }
        for g_leg in g_route["legs"]:
            for g_step in g_leg["steps"]:
                pos = (g_step["start_location"]["lat"], g_step["start_location"]["lng"])
                if count == 0:
                    prev_pos = (pos[0]+0.0001, pos[1]+0.0001)
                route["danger"] += crimedata.get_weight(pos, crimedata.get_distance(prev_pos, pos), time)
                route["steps"].append(pos)
                prev_pos = pos
                count = count + 1
        routes.append(route)
    return routes

def safest_route(from_, to_, time):
    routes = get_routes(get_directions(from_, to_), time)
    lowest = routes[0]
    for route in routes:
        if route["danger"] < lowest["danger"]:
            lowest = route
    return lowest
