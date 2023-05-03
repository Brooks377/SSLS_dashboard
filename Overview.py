import pandas as pd
import streamlit as st
from streamlit.components.v1 import html



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
    ## Project Purpose
    Since its inception in 2008, Airbnb has provided travelers with an alternative to staying in hotels or traditional bed and breakfasts. Airbnb has also allowed property owners to gain extra revenue by listing their properties for short or long term. Airbnb properties can range from luxury apartments to quaint places to crash. As a result, there is a large income range for potential renters and property owners. The diversity of properties allows for a variety in property types, locations, and amenities. 

    Due to the variety in properties an aspiring host may not know how to exactly price their property. A property owner may not know which amenities will result in the maximum value for their property. Additionally, investors may look to acquire properties to rent as long term Airbnbs, to generate the maximum value. 

    As a result we decided to complete an analysis of what attributes contribute to the price of Airbnb prices in Boston.
    We choose Boston because there are currently 3,864 listings and many diverse neighborhoods, throughout the city. However, the listings are mostly apartments and smaller houses. There are a few limitations of choosing Boston, as many amenities do not apply to a city and the lack of similarity in properties in the same neighborhood that could be seen in suburban areas. However, Boston provides a beneficial example for a city with many diverse neighborhoods.

    The goal for this project is to find a predicted Airbnb price based on neighborhood, census tract, property type  and amenities. The end goal is for a prospective Airbnb host to use this dashboard to generate an estimate of the price 
    of their Airbnb based on these factors. 

    ## Inspiration
    Our group was inspired for this project when watching the Boston Celtics play and seeing Airbnb advertisements across the court. We decided to research [data](http://insideairbnb.com/get-the-data/) regarding Airbnbs in Boston specifically. This site includes data that is the basis of our project.

    Additionally we were inspired for the analysis for this project from this data science project  [data science project](https://mohamedirfansh.github.io/Airbnb-Data-Science-Project), which was analyzed AirBnB data. 


    This project helped inspire us to analyze AirBnB data based on amenities and neighborhoods. The project also
    inspired the wordcloud for top amenities.




    ## Caveats
    This project reports the **intrinsic** value of Airbnbs in Boston, not the market value. Since the market value can be viewed on the internet easily, this analysis attempts to calculate the intrinsic value based on location and amenities. In other words, this report calculates the value that the features of the property provide.



    ## Table of Contents

    1. **Listing Data**
        -  This section allows for users to find the average price of a listing in Boston. 
        -  There is a dropdown menu which allows users to choose desired month, zone type, and neighborhood or census tract
        -  From there, the shapefile of the neighborhood/census tract is highlighted, and the total listings, highest price, average price, and lowest price are outputted
        -  Additionally, there are graphs that output room type distribution, availability of listings, and long versus short term listings.
        -  Additionally, we outputted two world clouds that illustrates the key ammentiies in high price and low price ammenities


    2. **Census Info**
        - This section includes dropdown menus for zone type and neighborhood/census tract data.
        - This reports a shapefile, that highlights the selected neighborhood/tract, and reports the BNB density
        - This section also outputs graphs showing neighborhood demographic breakdown and neighborhood level household vacancy rate

    3. **Spatial Regression**
        - This section hopes to solve the problem of whether Airbnb prices are affected by the prices of nearby listings. Unlike the other sections, this section is a singular analysis and not a customizable graph
        - First we created a regression that takes in variables that are important in determining prices. These variables include number of bathrooms, minimum nights, bedrooms, accommodates, price, latitude, and longitude.
        - Next, we completed a spatial two stage least squares regression taking into account spatial weights
        - We determined that we can assume that there is no relationship with Boston Airbnb listing and nearby listings

    4. **Price Suggestion**
    - This section is the culmination of the project, which allows users to put in multiple inputs to determine the predicted Airbnb price
    - The input choices include:
        - Zone type
        - Neighborhood
        - Month
        - Property Type
        - Room Type
        - Scroll bar for number of bedrooms
        - Scroll bar for number of guests allowed
        - Checkbox for 25 different amenity options
    - This section outputs the intrinsic price for the set of allocations

    # Links and Contribution
    **About Us:**
    #### Brooks Walsh

    #### Taylor Sheridan

    #### Thomas McDade

    **About Us:**
    Brooks Walsh, Taylor Sheridan, and Thomas McDade are students at Lehigh University studying finance with an interests in data science and business analytics. All three took the course Lehigh's Data Science for Finance taught by Don Bowen. This final project represents the culmination of everything they learned in the course 

    """
elif page_select == 'EDA':
    with open('inputs/EDA_Methodology.html', 'r', encoding='utf-8') as f:
        html_file = f.read()
    # Display HTML file
    html(html_file)
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


