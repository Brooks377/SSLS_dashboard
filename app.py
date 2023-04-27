import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import geopandas as gpd
import mapclassify
import shapely
import matplotlib.pyplot as plt
import pyproj
from datetime import datetime, timedelta

pio.renderers.default='browser' # use when doing dev in Spyder (to show figs)

# Page config
st.set_page_config(
    "Boston Airbnb Analysis by SSLS",
    "inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide",
)

"""
# Boston Airbnb Pricing Analysis/Prediction 
- HELLO WORLD
"""

# load all data first, some is needed for sidebar
listings = pd.read_csv('inputs/listings.csv.gz', compression='gzip')
boston_NBH = pd.read_csv("inputs/boston_NBH.csv")
boston_NBH_map = gpd.read_file("inputs/Census2020_BG_Neighborhoods/Census2020_BG_Neighborhoods.shp")
boston_tract = pd.read_csv("inputs/boston_tract.csv")
boston_tract_map = gpd.read_file("inputs/Census2020_Tracts/Census2020_Tracts.shp")

# census data
NBH_data = pd.read_csv("inputs/NBH_census_data.csv")
tract_data = pd.read_csv("inputs/tract_census_data.csv")

# more sidebar prep
start_date = pd.to_datetime('2023-03-19')
end_date = pd.to_datetime('2024-03-18')
dates = pd.date_range(start=start_date, end=end_date, freq='MS')
dates = [d.strftime('%B %Y') for d in dates]

#############################################
# start: sidebar
#############################################

with st.sidebar:
    
    "Select Month"
    month_select = st.selectbox("Month", dates)
    
    "Select Zone Type"
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])
    
    if zone_type == 'Neighborhoods':
        "Select Neighborhood"
        zone_select = st.selectbox("Neighborhood", ['All (Boston)'] + boston_NBH['BlockGr202'].tolist())
    else:
        "Select Census Tract"
        zone_select = st.selectbox("Census Tract", ['All (Boston)'] + boston_tract['NAME20'].tolist())
    '''
    [Template source code here.](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard)
    '''
#############################################
# end: sidebar
#############################################

#######################################################################
# Test: making a working display with our map
#######################################################################

# copied/cleaned from 9th_grade_geography_test

# the following if/else uses zone_type selectbox
if zone_type == "Neighborhoods":

    # selecting desired zone on the map
    if zone_select == "All (Boston)":
        zone_index_select = list(range(len(boston_NBH)))
    else:
        mask = boston_NBH['BlockGr202'] == zone_select
        filtered_df = boston_NBH[mask]

        # select the value in the other column
        zone_index_select = [filtered_df['OBJECTID'].values[0] - 1]

    boston_NBH_map = boston_NBH_map.to_crs('epsg:4326')
    boston_NBH_map.set_index('BlockGr202', inplace=True)
    boston_NBH.set_index('BlockGr202', inplace=True)

    fig = px.choropleth(boston_NBH,
                        geojson=boston_NBH_map.geometry,
                        locations=boston_NBH_map.index,
                        color="BNBDensity",
                        hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>',
                                 selectedpoints=zone_index_select)

#####################################################
# map of census tracts (same steps as above for NBH)
# I have to make changes to match above's speed
#####################################################

# else implies census tract data
else:

    # selecting desired zone on the map
    if zone_select == "All (Boston)":
        zone_index_select = list(range(len(boston_tract)))
    else:
        mask = boston_tract['NAME20'] == zone_select
        filtered_df = boston_tract[mask]

        # select the value in the other column
        zone_index_select = [filtered_df['OBJECTID'].values[0] - 1]

    boston_tract_map = boston_tract_map.to_crs('epsg:4326')
    boston_tract_map.set_index('NAME20', inplace=True)
    boston_tract.set_index('NAME20', inplace=True)

    fig = px.choropleth(boston_tract,
                        geojson=boston_tract_map.geometry,
                        locations=boston_tract_map.index,
                        color="BNBDensity",
                        hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>',
                                 selectedpoints=zone_index_select)

# displaying plot
st.plotly_chart(fig, use_container_width=False)

#####################################################
# Create a fake data set that includes desired variables
# then merge it with boston_NBH
# allow user to select desired month
#      - so we need data per month
# this will suffice for proposal
#####################################################

######################################################
# stats about map
######################################################

# demographic data from census (pie chart)

if zone_type == "Neighborhoods":
    if zone_select == "All (Boston)":
        plot_values = NBH_data.iloc[:, 2:7].sum().values.tolist()
        plot_labels = NBH_data.iloc[:, 2:7].columns.tolist()
        plot_anot = NBH_data['Total:'].sum()
    else:
        # slice the row
        row_to_plot = NBH_data.loc[NBH_data['field concept'] == zone_select]

        # slice the columns
        cols_to_plot = row_to_plot.iloc[:, 2:7]

        # filter out zeros
        mask = cols_to_plot.ne(0)
        cols_to_plot = cols_to_plot.loc[:, mask.values[0]]
        plot_values = cols_to_plot.values.tolist()[0]
        plot_labels = cols_to_plot.columns.tolist()
        plot_anot = row_to_plot['Total:'].values[0]

else:
    # tract pie chart
    if zone_select == "All (Boston)":
        plot_values = tract_data.iloc[:, 2:10].sum().values.tolist()
        plot_labels = tract_data.iloc[:, 2:10].columns.tolist()
        plot_anot = tract_data['Total:'].sum()
    else:
        # slice the row
        selector = boston_tract.loc[zone_select, 'TRACTCE20']
        row_to_plot = tract_data.loc[tract_data['Census Tract'] == selector]

        # slice the columns
        cols_to_plot = row_to_plot.iloc[:, 2:10]

        # filter out zeros
        mask = cols_to_plot.ne(0)
        cols_to_plot = cols_to_plot.loc[:, mask.values[0]]
        plot_values = cols_to_plot.values.tolist()[0]
        plot_labels = cols_to_plot.columns.tolist()
        plot_anot = row_to_plot['Total:'].values[0]


# create a pie chart
fig1, ax = plt.subplots()
ax.pie(plot_values, autopct='%1.1f%%')
ax.set_title('Zone Demographic Breakdown')
ax.legend(labels=plot_labels, loc='center left', bbox_to_anchor=(.95, .5 ))
ax.annotate(f'Total Population of Selected Zone: {plot_anot}' , xy=(1, 1), xytext=(ax.get_xlim()[1] * .96 , ax.get_ylim()[1] * .6), bbox=dict(facecolor='white', boxstyle='round'))

st.pyplot(fig1)

"""
## This section will show stats about the selected neighborhood/tract.
    - Changes based on sidebar inputs
    - Desired Final outputs include:
         - Boston listing prices each month
              - high/low/avg
              - Total available listings / total listings (potentially per price?)
                - Appartments/houses/other
         - NBH/tract listing prices each month
              - high/low/avg
              - Total available listings / total listings (by zone) (potentially per price?)
                - Appartments/houses/other
         - Most common words describing high/low price listings
              - word splatter or short list
         - Total neightborhood/tract household vacancy stats
         - Not necessary for report:
              - would be super easy to add demographic/population data from census
"""
if zone_select == 'All (Boston)':
    'When no zone is selected, only Boston-Level stats will show'
    'Select a zone to produce outputs in this proposal demo'
else:
    if zone_type == 'Neighborhoods':
        example_output = boston_NBH.loc[zone_select,'BNBs']
        example_output2 = boston_NBH.loc[zone_select,'Shape_Leng']
        f'Example Output (# BNBs): {example_output}'
        f'Example Output 2 (Perimeter length): {example_output2}'
    else:
        example_output = boston_tract.loc[zone_select,'BNBs']
        example_output2 = boston_tract.loc[zone_select,'Shape_STLe']
        f'Example Output (# BNBs): {example_output}'
        f'Example Output 2 (Perimeter length): {example_output2}'

######################################################
#: Report Section
######################################################

"""
## This section will show the report file as a markdown document
    - Below is our initial proposal, it's here to ensure markdown files display properly
    - To reiterate:
        - EVERYTHING BELOW THIS POINT IS FROM THE INITIAL PROPOSAL AND IS NO LONGER RELEVANT TO THE CURRENT BUILD

# Research Proposal: Analysis of Boston Airbnb Listings
### Big Picture Question: What attributes about a Boston Airbnb listing are most influential to its list price?

By Tommy McDade, Brooks Walsh, and Taylor Sheridan

## Research Question

After finding correlations and testing different influences, can we predict future Airbnb list prices?
   - This project will be about relationships as well as prediction. 
       - We will do a thorough EDA on our data set (including visuals) to represent the many relationships between different listing attributes and price.
       - After the important relationships are determined, we will use regression models and machine learning to create an accurate predictor of list prices
       - The metrics for success in this project include:
           - A dashboard to visually represent different metrics based on geographic location
           - A maximized R-Squared value (*or a different maximized/minimized measurement statistic, based on our choice of model*)

## Necessary Data

1. The Data will be primarily collected from [kaggle](https://www.kaggle.com/datasets/airbnb/boston):
- sample period: 9/5/2016 - 9/4/2017
    - There are 3 data sets included from Kaggle:
    1. calendar.csv
        - observation: Airbnb listings
        - rows: 1.31 million
        - columns: 4
        - index: "listing_id" and "date"
        - variables: "available (Bool)", "price(continuous)"
            - price is missing 51% of values
    2. listings.csv
        - observation: Airbnb listings
        - rows: 3585
        - columns: 95
        - index: "id", "scrape_id"
        - variables: too many to reasonably include in a proposal
            - a few examples:
                - "host_since", "maximum_nights", "require_guest_profile_picture"
    3. reviews.csv
        - observation: reviews based on Airbnb listings
        - rows: 68.3k
        - columns: 6
        - index: "listing_id", "id", "reviewer_id"
        - variables: "date", "reviewer_name", "comments"

2. To display maps and geographic data, we will need [2020 census tract data](https://data.boston.gov/dataset/census-2020-tracts/resource/1721fbb7-ee56-4a61-9e1b-2f2342d202d1).
    - We will likely be using the shapefile version    

3. The **raw inputs** for this project will be 3 of the 4 data sets described above in .csv format and a shapefile for use in geographic data.
    - All of these data sets will be saved to a folder called "inputs"
    - Any important dataframes/visuals that are created will be saved to a folder called "outputs"

4. High-level data cleaning plan:
- The 3 datasets that are obtained from Kaggle (calendar.csv, listings.csv, reviews.csv) are already fairly clean
    - There are several variables that may need to be a different data type in order to perform analysis
    - Some variables are full of text, and will likely need parsing to be used effectively
    - Some variables are URLs, which likely aren't needed
    - Because there are so many variables, and some are quite specific:
        - There are **a LOT** of NAN values that should be replaced with 0 (or a value that is consistent with the context)
- The last data set (used to create the map) is from 2020 census, and is not in a usable format originally
    - luckily there is a package for python that reads shapefiles effectively:
        - ```import geopandas as gpd```
"""