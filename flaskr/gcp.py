import googlemaps
import config
from datetime import datetime

gmaps = googlemaps.Client(key=config.GCP_API_KEY)

def get_directions(from_d, to_d):
    # Request directions via public transit
    now = datetime.now()
    return gmaps.directions(
        from_d, to_d, mode="walking", departure_time=now, alternatives=True)
    

def routes(g_directions):
    routes = []
    for g_route in g_directions:
        route = {
            "danger": 0,
            "steps": []
        }
        for g_leg in g_route["legs"]:
            for g_step in g_leg["steps"]:
                pos = (g_step["start_location"]["lat"], g_step["start_location"]["lng"])
                route["steps"].append(pos)
        routes.append(route)
    return routes

print(routes(get_directions("Northeastern University", "Boston University")))
