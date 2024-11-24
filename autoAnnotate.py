# Requires overpy, the library that lets us access the Overpass API through python

import overpy
from geopy.geocoders import Nominatim
from owslib.wms import WebMapService
import requests
import json
import matplotlib.pyplot as plt
from PIL import Image as plimg
import numpy as np


def get_cross_walk_location(location_geo_code):
    over_api = overpy.Overpass()
    geo_locator = Nominatim(user_agent="crosswalk_locator")
    location = geo_locator.geocode(location_geo_code)
    geo_bounding_box = (location.latitude - 0.01, location.longitude - 0.01,
                        location.latitude + 0.01, location.longitude + 0.01)  # South, West, North, East

    query = f"""
    [out:json][timeout:25];
    (
      node["highway"="crossing"]({geo_bounding_box[0]},{geo_bounding_box[1]},{geo_bounding_box[2]},{geo_bounding_box[3]});
    );
    out body;
    """  # Should return all crosswalks within 0.01 longitude/ latitude points,

    result = over_api.query(query)

    crosswalks = []
    for node in result.nodes:
        crosswalks.append((node.lat, node.lon))
        # print(f"Crosswalk at latitude: {node.lat}, longitude: {node.lon}")
    # Now we have a list of all the (latitude, longitude) pairs in that area,
    # and can use it access the images of those areas for annotation
    return crosswalks

# # Connect to GIBS WMS Service
# wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
#
# # Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
# img = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
#                  srs='epsg:4326',  # Map projection
#                  bbox=(-180,-90,180,90),  # Bounds
#                  size=(1200, 600),  # Image size
#                  time='2021-09-21',  # Time of data
#                  format='image/png',  # Image format
#                  transparent=True)  # Nodata transparency
#
# # Save output PNG to a file
# out = open('python-examples/MODIS_Terra_CorrectedReflectance_TrueColor.png', 'wb')
# out.write(img.read())
# out.close()
#
# # View image
# Image('python-examples/MODIS_Terra_CorrectedReflectance_TrueColor.png')
#
#
# locations = get_cross_walk_location("Bloomsbury, London, UK")
# for location in locations:
#     get_open_aerial_map_image(location, 0.01)
#     break
