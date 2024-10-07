import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import folium # DELETE AND UNINSTALL
import streamlit_folium as st_folium # DELETE AND UNINSTALL

import json
import plotly.graph_objects as go
from shapely.geometry import mapping
from sklearn.cluster import HDBSCAN
from shapely.geometry import MultiPoint
from shapely.ops import unary_union


@st.cache_data
def load_data():
	tree_census_path = "../data/clean/tree_data/2015.csv"
	zip_path = "../data/clean/geo_data/zip_data.geojson"
	nta_path = "../data/clean/geo_data/nta_data.geojson"
	borough_path = "../data/clean/geo_data/borough_data.geojson"

	df = pd.read_csv(tree_census_path, dtype={"zip_code": "str"})
	gdfz = gpd.read_file(zip_path)
	gdfn = gpd.read_file(nta_path)
	gdfb = gpd.read_file(borough_path)

	gdfz = gdfz.astype({'zip_code': 'str'})

	gdfz.to_crs(epsg=4326, inplace=True)
	gdfn.to_crs(epsg=4326, inplace=True)
	gdfb.to_crs(epsg=4326, inplace=True)

	return df, gdfz, gdfn, gdfb


def add_metric_columns(df, gdf, scope, area_col_name):
	# Make a copy of the dataframe
	df1 = df.copy()

	# Group the dataframe by the given scope and provide a count
	df_grouped = df1.groupby(by=scope).size().reset_index(name="count")

	# Merge the dataframe with the provided geodataframe
	df_merged = df_grouped.merge(gdf, on=scope, how="right")

	# Add new column representing the tree density
	df_merged["trees_per_hectare"] = df_merged["count"] / df_merged[area_col_name]

	# Convert the dataframe to a geodataframe
	df_geo = gpd.GeoDataFrame(df_merged)
	
	return df_geo


def plot_map(gdf, latitude, longitude, metric, scope, zoom=9.5):

	# Convert the geometries in the GeoDataFrame to a GeoJSON format
	gdf['geometry_json'] = gdf['geometry'].apply(lambda x: mapping(x))

	# Extract the GeoJSON-like structure from the GeoDataFrame
	geojson_data = json.loads(gdf.to_json())

	# Prepare the metric for the map color
	gdf[scope] = gdf[scope].astype(str)  # Ensure it's a string for proper handling

	featureidkey_str = f"properties.{scope}"

	# Create the Plotly Choropleth figure
	fig = go.Figure(go.Choroplethmapbox(
		geojson=geojson_data,
		locations=gdf[scope],  			# The unique identifier for areas
		z=gdf[metric],  				# The data you want to color-code the regions with
		colorscale="Emrld",       		# Define the color scale Viridis
		featureidkey=featureidkey_str,  # Make sure this matches your GeoJSON structure
		marker_opacity=0.5,          	# Opacity for the polygons
		marker_line_width=1,          	# Line width for the boundaries
		hovertemplate = (
				'Trees per hectare: %{z:.0f}<br>' +
				'Location: %{location}<extra></extra>'
			)
	))

#hovertemplate = (
#			'Longitude: %{x:.5f}<br>' +
#			'Latitude: %{y:.5f}<br>' +
#			'Altitude: %{z:.0f} m<br>' +
#			metric_label + ': %{customdata:.0f}<extra></extra>'
#		)

	# Set up the mapbox style and zoom
	fig.update_layout(
		mapbox_style="carto-positron",
		mapbox_zoom=zoom,
		mapbox_center = {"lat": latitude, "lon": longitude},
		margin={"r":0,"t":0,"l":0,"b":0},
		height=700
	)

	# Return the plot
	return fig


def cluster_data(gdf, min_cluster_size, min_samples):

	# Use HBDSCAN to create clusters
	X = gdf[["latitude", "longitude"]].copy()
	hdb = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
	labels = hdb.fit_predict(X)
	gdf["cluster"] = labels

	return gdf


def calculate_cluster_density(gdf, cluster_col="cluster", geo_col="geometry"):

	# Group the data by cluster label (excluding noise, i.e., clusters labeled as -1)
	cluster_groups = gdf[gdf[cluster_col] != -1].groupby(cluster_col)

	# Create an empty list to store the cluster polygons
	polygons = []

	for cluster_id, group in cluster_groups:

		# Calculate the number of trees in each cluster
		num_trees = len(group)

		# Extract the points in the cluster as a Shapely MultiPoint object
		points = MultiPoint(list(group[geo_col]))
		
		# Create a convex hull for the cluster
		# You can replace this with a concave hull for tighter boundaries if desired
		polygon = points.convex_hull
		
		# Store the polygon along with the cluster id
		polygons.append({'cluster': cluster_id, 'geometry': polygon, 'num_trees': num_trees})

	# Convert the polygons into a new GeoDataFrame for visualization
	polygon_gdf = gpd.GeoDataFrame(polygons)
	polygon_gdf.set_crs(epsg=32618, inplace=True)

	# Calculate the area of each polygon in hectares
	polygon_gdf["hectares"] = polygon_gdf.geometry.area / 10000

	# Calculate the number of trees per hectare
	polygon_gdf["trees_per_hectare"] = np.floor(polygon_gdf["num_trees"] / polygon_gdf["hectares"])

	# Sort by trees_per_hectare
	polygon_gdf.sort_values(by="trees_per_hectare", ascending=False, inplace=True)

	# Set CRS back to epsg=4326
	polygon_gdf.to_crs(epsg=4326, inplace=True)

	return polygon_gdf
