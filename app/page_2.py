import streamlit as st

from functions import *


# Load dataframes
df, gdf_zip, gdf_nta, gdf_borough = load_data()

# List the unique boroughs
borough_list = list(gdf_borough["borough"].unique())

# Create a list of species
species_count = df["species_common_name"].value_counts()
top_10_trees = species_count.head(10).index
#top_10_trees = top_10_trees.insert(0, "all trees")

with st.sidebar:
	
	# Show a dropdown selector for borough
	borough_select = st.selectbox("Select a borough:", options=borough_list)
	
	# Show a dropdown selector for tree species
	tree_select = st.selectbox("Select a tree species:", options=top_10_trees, placeholder="Choose an option")

	# Show a slide selector for min_cluster_size
	min_cluster_size_select = st.slider("Select a minimum cluster size:", min_value=40, max_value=100, value=40, step=20)

	# Show a slide selector for min_samples
	min_samples_select = st.slider("Select a minimum samples value:", min_value=1, max_value=10, value=5, step=1)

# Create a filtered geodataframe to retrieve the relevant centroid for the map
gdf_borough_filtered = gdf_borough.loc[gdf_borough["borough"] == borough_select]
centroid_long = gdf_borough_filtered["geometry"].centroid.x.values[0]
centroid_lat = gdf_borough_filtered["geometry"].centroid.y.values[0]

# Filter the main dataframe by borough and tree and convert to a geodataframe
df_filtered = df.loc[(df["borough"] == borough_select) & (df["species_common_name"] == tree_select)].copy()
gs = gpd.GeoSeries.from_wkt(df_filtered['geometry'])
df_filtered_gdf = gpd.GeoDataFrame(df_filtered, geometry=gs, crs="EPSG:32618")

# Create the clusters using HDBSCAN
df_filtered_gdf = cluster_data(df_filtered_gdf, min_cluster_size_select, min_samples_select)

# Calculate the tree density per hectare for each cluster and return a new geodataframe contain that new data
cluster_gdf = calculate_cluster_density(df_filtered_gdf)

# Plot the map with clusters
map = plot_map(cluster_gdf, centroid_lat, centroid_long, "trees_per_hectare", "cluster", zoom=11)
st.plotly_chart(map)

# Create a summary table
summary_table = cluster_gdf[["cluster", "num_trees", "hectares", "trees_per_hectare"]].head()
st.dataframe(summary_table, hide_index=True)