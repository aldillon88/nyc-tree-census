import streamlit as st


st.set_page_config(page_title="NYC Tree Census 2015", layout="wide")

st.title('NYC Tree Census 2015')

density_page = st.Page("page_1.py", title="Tree Density")
clusters_page = st.Page("page_2.py", title="Tree Clusters")
project_page = st.Page("page_3.py", title="Project Description")


pg = st.navigation([density_page, clusters_page, project_page])

pg.run()