# NYC Tree Census 2015

#### Introduction
This project is an analysis of NYC Tree Census data collected in 2015. Further information on the data can be found on Kaggle, where the data files were sourced: [Kaggle](https://www.kaggle.com/datasets/nycparks/tree-census)

#### Environment and packages
##### Python Interpreter
- Python 3.9.6
##### Main Packages Used
- geopandas==1.0.1
- matplotlib==3.9.1
- notebook==7.2.1
- numpy==2.0.1
- pandas==2.2.2
- plotly==5.23.0
- scikit-learn==1.5.1
- shapely==2.0.5
- streamlit==1.38.0

#### Installation
1. Clone this repository:
	1. `git clone https://github.com/aldillon88/nyc-tree-census`.
2. Create a virtual environment and activate it:
	1. `python -m venv [venv-name]`
	2. `source [venv-name]/bin/activate`.
3. Install the required packages:
	1. `pip install -r requirements.txt`.
4. Run the Streamlit app:
	1. `streamlit run app.py`

#### App usage
**Tab 1 - Tree Density**\n
This tab allows the user to view tree density by borough, neighborhood and zip code, and filter based on characteristics such as species, the condition of the tree 
and and the level of public stewardship that may have been provided for each tree.

**Tab 2 - Tree Clusters**\n
This tab allows the user to visualize clusters of trees by borough and species. This is achieved through the use of the HDBSCAN clustering algorithm 
and user defined hyperparameter values.