import streamlit as st

st.header("Introduction")
st.markdown("""
	The goal of this project is to provide a simple way to visulize the tree density of New York City based on data collected in the 2015 Tree Census. There are two tabs in this data app:

	**Tab 1 - Tree Density**\n
	This tab allows the user to view tree density by borough, neighborhood and zip code, and filter based on characteristics such as species, the condition of the tree 
	and and the level of public stewardship that may have been provided for each tree.

	**Tab 2 - Tree Clusters**\n
	This tab allows the user to visualize clusters of trees by borough and species. This is achieved through the use of the HDBSCAN clustering algorithm 
	and user defined hyperparameter values.
	""")

st.divider()
st.header("Real World Use")
st.subheader("Tree Density")
st.markdown("""
	By combining the filters available, users can easily locate which areas have the highest (or lowest) density of trees for any chosen characteristic. This helps to answer questions
	such as, for example, which neighborhood has the highest density of trees that appear to be cared for by the public (stewardship level), or which borough has the highest density of
	trees in poor condition that may be in need of care or replacement?

	This tab utilizes a choropleth map with color coding to give the user quick insight into the answers to these and many other questions. When combined with other census data or domain knowledge,
	the user may discover potential connections between, for example, average rental prices and tree density, or average household income and tree stewardship.
	""")

st.subheader("Tree Clusters")
st.markdown("""
	Both research and maintenance teams who are interested in the health and wellbeing of trees in New York City may use this tab to define clusters of various sizes and characteristics
	in order to, for example, find areas that could be potential epicenters of pest and disease outbreaks. Through knowing this information, researches and maintenance teams may be able to
	anticipate and prevent major issues to ensure the ongoing health of the trees and ecosystems within the city.
	""")