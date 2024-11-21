# Requires overpy, the library that lets us access the Overpass API through python

import overpy
from geopy.geocoders import Nominatim

overApi = overpy.Overpass()
geoLocator = Nominatim(user_agent="crosswalk_locator")
location = geoLocator.geocode("Bloomsbury, London, UK")
geoBoundingBox = (location.latitude - 0.01, location.longitude - 0.01,
                  location.latitude + 0.01, location.longitude + 0.01)  # South, West, North, East

query = f"""
[out:json][timeout:25];
(
  node["highway"="crossing"]({geoBoundingBox[0]},{geoBoundingBox[1]},{geoBoundingBox[2]},{geoBoundingBox[3]});
);
out body;
"""  # Should return all crosswalks within 0.01 longitude/ latitude points,

result = overApi.query(query)

crosswalks = []
for node in result.nodes:
    crosswalks.append((node.lat, node.lon))
    print(f"Crosswalk at latitude: {node.lat}, longitude: {node.lon}")
# Now we have a list of all of the (latitude, longitude) pairs in that area,
# and can use it access the images of those areas for annotation
