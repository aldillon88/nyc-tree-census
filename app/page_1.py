import streamlit as st
import numpy as np

from functions import *


# Load dataframes
df, gdf_zip, gdf_nta, gdf_borough = load_data()

# Create a list of species
species_count = df["species_common_name"].value_counts()
top_10_trees = species_count.head(10).index
top_10_trees = top_10_trees.insert(0, "all trees")

# Create a list of tree_condition values
tree_conditions = list(df["tree_condition"].unique())
tree_conditions.insert(0, "all conditions")

# Create a list for stewardship_level
stewardship_levels = list(df["stewardship_level"].unique())
stewardship_levels.insert(0, "all levels of stewardship")

# Assign global map variables
city_center = gdf_borough.geometry.unary_union.centroid
latitude = city_center.y
longitude = city_center.x

# Display options in a sidebar
with st.sidebar:

	# Select the appropriate geodataframe and assign additional map variables
	scope_select = st.radio("Choose a scope to analyse:", options=["Borough", "Neighborhood", "ZIP Code"])

	if scope_select == "Borough":
		scope = "borough"
		gdf = gdf_borough
		area_col_name = "area_borough_hectares"
	
	elif scope_select == "Neighborhood":
		scope = "nta_name"
		gdf = gdf_nta
		area_col_name = "area_nta_hectares"
	
	else:
		scope = "zip_code"
		gdf = gdf_zip
		area_col_name = "area_zip_hectares"

	# Show a dropdown selector for tree species
	tree_select = st.selectbox("Select a tree species:", options=top_10_trees, placeholder="Choose an option")

	# Show a dropdown selector for tree condition
	condition_select = st.selectbox("Select a tree condition:", options=tree_conditions, placeholder="Choose an option")

	# Show a dropdown selector for stewardship level
	stewardship_select = st.selectbox("Select a stewardship level:", options=stewardship_levels, placeholder="Choose an option")
	
# Apply filters to the dataframe based on the dropdown selectboxes
if tree_select != "all trees":
	df = df.loc[df["species_common_name"] == tree_select]

if condition_select != "all conditions":
	df = df.loc[df["tree_condition"] == condition_select]

if stewardship_select != "all levels of stewardship":
	df = df.loc[df["stewardship_level"] == stewardship_select]


# Merge main dataframe with correct geodataframe and create metric column
df_geo = add_metric_columns(df, gdf, scope, area_col_name)

# Plot the choropleth map
map = plot_map(df_geo, latitude, longitude, "trees_per_hectare", scope)
st.plotly_chart(map)













