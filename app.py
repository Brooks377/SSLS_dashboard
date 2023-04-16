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

from update_data_cache import get_data

from pypfopt.efficient_frontier import EfficientFrontier

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
"""

# load all data first, some is needed for sidebar
boston_NBH = gpd.read_file("inputs/Census2020_BG_Neighborhoods/Census2020_BG_Neighborhoods.shp")
listings = pd.read_csv('inputs/listings.csv.gz', compression='gzip')
boston_tract = gpd.read_file("inputs/Census2020_Tracts/Census2020_Tracts.shp")

#############################################
# start: sidebar
#############################################

with st.sidebar:
    
    "Select Month"
    month_select = st.selectbox("Month", ["3-2023",'4-2023','5-2023'])
    
    "Select Zone Type"
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])
    
    if zone_type == 'Neighborhoods':
        "Select Neighborhood"
        zone_select = st.selectbox("Neighborhood", ['All (Boston)'] + boston_NBH['BlockGr202'].tolist())
    else:
        "Select Census Tract"
        zone_select = st.selectbox("Census Tract", ['All (Boston)'] + boston_tract['NAME20'].tolist())
    '''
    [Source code and contributors here.](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard)
    '''
#############################################
# end: sidebar
#############################################

######################################################
# start of my contributions
######################################################

######################################################
# redundant note to help me notice where my test starts

#######################################################################
# Test: making a working display with our map
#######################################################################

# copied from 9th_grade_geography_test

# this step maps each longitude and latitude to a shapely point
listings = gpd.GeoDataFrame(listings, geometry=listings.apply(
        lambda srs: shapely.geometry.Point(srs['longitude'], srs['latitude']), axis='columns'
    ))

# the following if/else uses zone_type selectbox
if zone_type == "Neighborhoods":
    # fix for non-stardard coordinates, see notebook for details
    boston_NBH = boston_NBH.to_crs('epsg:4326')

    # function to create a new column based on whether or not a listing is in a neighborhood
    def assign_census_NBH(bnb):
        bools = [geom.contains(bnb['geometry']) for geom in boston_NBH['geometry']]
        if True in bools:
            return boston_NBH.iloc[bools.index(True)]['BlockGr202']
        else:
            return np.nan

    # .apply the function to the listings
    listings['census_NBH'] = listings.apply(assign_census_NBH, axis='columns')

    # use .map() to apply value_counts to each value of 'BlockGr202'
    boston_NBH['BNBs'] = boston_NBH['BlockGr202'].map(listings['census_NBH'].value_counts())
    boston_NBH['BNBs'] = boston_NBH['BNBs'].fillna(0)
    boston_NBH.set_index('BlockGr202', inplace=True)

    # selecting desired zone on the map
    if zone_select == "All (Boston)":
        zone_index_select = list(range(len(boston_NBH)))
    else:
        zone_index_select = [(boston_NBH.loc[zone_select, 'OBJECTID'] - 1)]
    
    # this code reprojects the areas into an "equal-area" projection
    # this is so that I can get listings per Kilometer^2
    boston_NBH['BNBDensity'] = (boston_NBH['BNBs'] / boston_NBH['geometry']\
                                .to_crs('epsg:3395')\
                                .map(lambda p: p.area / 10**6))\
                                .fillna(0)
    fig = px.choropleth(boston_NBH, geojson=boston_NBH.geometry, locations=boston_NBH.index,
                        color="BNBDensity", hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>',
                                 selectedpoints=zone_index_select)

#####################################################
# load map of census tracts (same steps as above for NBH)

# else implies census tract data
else:
    boston_tract = boston_tract.to_crs('epsg:4326')

    def assign_census_tract(bnb):
        bools = [geom.contains(bnb['geometry']) for geom in boston_tract['geometry']]
        if True in bools:
            return boston_tract.iloc[bools.index(True)]['NAME20']
        else:
            return np.nan

    listings['census_tract'] = listings.apply(assign_census_tract, axis='columns')
    boston_tract['BNBs'] = boston_tract['NAME20'].map(listings['census_tract'].value_counts())
    boston_tract['BNBs'] = boston_tract['BNBs'].fillna(0)
    boston_tract.set_index('NAME20', inplace=True)

    # selecting desired zone on the map
    if zone_select == "All (Boston)":
        zone_index_select = list(range(len(boston_tract)))
    else:
        zone_index_select = [(boston_tract.loc[zone_select, 'OBJECTID'] - 1)]

    boston_tract['BNBDensity'] = (boston_tract['BNBs'] / boston_tract['geometry']\
                                .to_crs('epsg:3395')\
                                .map(lambda p: p.area / 10**6))\
                                .fillna(0)
    fig = px.choropleth(boston_tract, geojson=boston_tract.geometry, locations=boston_tract.index,
                        color="BNBDensity", hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                    'BNB Density: %{z}<br>',
                                    selectedpoints=zone_index_select)

# displaying plot
st.plotly_chart(fig,use_container_width=False)

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