import pandas as pd
import streamlit as st


# Page config
st.set_page_config(
    page_title="Overview (home)",
    page_icon="inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

"""
# Boston Airbnb Pricing Analysis by Team Strong-Side-Left-Side
"""
@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    return df

# load all data first, some is needed for sidebar
boston_NBH = load_csv("inputs/boston_NBH.csv")
boston_tract = load_csv("inputs/boston_tract.csv")

#############################################
# start: sidebar
#############################################

with st.sidebar:
    
    "Select Overview Page"
    page_select = st.selectbox("Select Page", ['Project Overview', 'EDA', 'Methodology', 'Machine Learning/Suggestion'])

    st.button("Rerun")
    '''
    [Template source code here.](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard)
    '''
#############################################
# end: sidebar
#############################################


#####################################################
# Overview Stuff
#####################################################

"""
## Select a Page to Browse Overview
"""
if page_select == 'Project Overview':
    """
    Project Overview
    """
elif page_select == 'EDA':
    """
    EDA
    """
elif page_select == 'Methodology':
    """
    # EXAMPLE TEXT
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
else:
    """
    Discussion of Machine learning and suggestion page
    """


