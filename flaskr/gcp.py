import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key="AIzaSyACIGGvfWRiZhpb687yWWeDsxHWfp4gtlg")

def routes(from_d, to_d):
    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(from_d, to_d,
                                        mode="walking",
                                        departure_time=now,
                                        alternatives=True)

for route in directions_result:
    print("ROUTE:")
    for leg in route["legs"]:
        for step in leg["steps"]:
            print((step["start_location"], step["end_location"]))