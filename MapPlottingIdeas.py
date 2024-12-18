# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:50:18 2024

@author: kayla.green
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, mapping
import numpy as np

# Sample data: coordinates (longitude, latitude) and circle sizes
data = {
    'name': ['Location A', 'Location B', 'Location C'],
    'longitude': [-74.006, -73.935, -73.949],
    'latitude': [40.7128, 40.73061, 40.6782],
    'size': [1000, 500, 1500]  # Circle sizes
}

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))

# Set the coordinate reference system (CRS) to WGS84
gdf.crs = "EPSG:4326"

# Create a base map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world[world.name == "United States"].plot(color='lightgrey', figsize=(10, 10))

# Add circles to the map
for idx, row in gdf.iterrows():
    # Create a circle around the point
    circle = Point(row['longitude'], row['latitude']).buffer(row['size'] / 100000)  # Adjust size for visibility
    plt.plot(*circle.exterior.xy, color='blue', alpha=0.5)  # Plot the circle
    plt.text(row['longitude'], row['latitude'], row['name'], fontsize=12, ha='center')

# Show the plot
plt.title('Circles on Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(-75, -73)
plt.ylim(40.5, 41)
plt.show()
