import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

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

#############################################
# start: sidebar
#############################################

with st.sidebar:
    
    "Month Selector Test"
    mont_select = st.selectbox("Month", ["3-2023",'4-2023','5-2023'])
    
    "Geography Type Selector Test"
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])
    
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

import geopandas as gpd
import mapclassify
import shapely
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyproj

listings = pd.read_csv('inputs/listings.csv.gz', compression='gzip')

# this step maps each longitude and latitude to a shapely point
listings = gpd.GeoDataFrame(listings, geometry=listings.apply(
        lambda srs: shapely.geometry.Point(srs['longitude'], srs['latitude']), axis='columns'
    ))

# the following if/else uses zone_type selectbox
if zone_type == "Neighborhoods":
    # load map of neighborhoods
    boston_NBH = gpd.read_file("inputs/Census2020_BG_Neighborhoods/Census2020_BG_Neighborhoods.shp")

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

    # this code reprojects the areas into an "equal-area" projection
    # this is so that I can get listings per Kilometer^2
    boston_NBH['BNBDensity'] = (boston_NBH['BNBs'] / boston_NBH['geometry']\
                                .to_crs('epsg:3395')\
                                .map(lambda p: p.area / 10**6))\
                                .fillna(0)
    fig = px.choropleth(boston_NBH, geojson=boston_NBH.geometry, locations=boston_NBH.index,
                        color="BNBDensity", hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)

#####################################################
# load map of census tracts (same steps as above for NBH)

# else implies census tract data
else:
    boston_tract = gpd.read_file("inputs/Census2020_Tracts/Census2020_Tracts.shp")
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
    boston_tract['BNBDensity'] = (boston_tract['BNBs'] / boston_tract['geometry']\
                                .to_crs('epsg:3395')\
                                .map(lambda p: p.area / 10**6))\
                                .fillna(0)
    fig = px.choropleth(boston_tract, geojson=boston_tract.geometry, locations=boston_tract.index,
                        color="BNBDensity", hover_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)

#####################################################
# Create a fake data set that includes desired variables
# then merge it with boston_NBH
# allow user to select desired month
#      - so we need data per month
# this will suffice for proposal
#####################################################

# displaying plot
st.plotly_chart(fig,use_container_width=False)