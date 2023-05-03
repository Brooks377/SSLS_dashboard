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
    
    """
    ## Select a Page to Browse Overview
    """
    page_select = st.selectbox("Select Page", ['Project Overview', 'EDA & Methodology', 'Machine Learning/Suggestion'])

    st.button("Rerun")
    '''
    [Website Source Code](https://github.com/Brooks377/SSLS_dashboard)     
    [LeftSide Team Repo](https://github.com/Brooks377/leftside_teamproject)     
    [Template source code (Wall Street Bets)](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard)     
    '''
#############################################
# end: sidebar
#############################################


#####################################################
# Overview Stuff
#####################################################

if page_select == 'Project Overview':
    """
    ## Project Purpose
    Since its inception in 2008, Airbnb has provided travelers with an alternative to staying in hotels or traditional bed and breakfasts. Airbnb has also allowed property owners to gain extra revenue by listing their properties for short or long term. Airbnb properties can range from luxury apartments to quaint places to crash. As a result, there is a large income range for potential renters and property owners. The diversity of properties allows for a variety in property types, locations, and amenities. 

    Due to the variety in properties, an aspiring host may not know how to exactly price their listing. A property owner may not know which amenities will result in the maximum value for their property. Additionally, investors may look to acquire properties to rent as long term Airbnbs, to generate the maximum value. 

    As a result we decided to complete an analysis of what attributes contribute to the price of Airbnb prices in Boston.
    We choose Boston because there are currently 3,864 listings, and many diverse neighborhoods throughout the city. However, the listings are mostly apartments and smaller houses. There are a few limitations of choosing Boston, as some amenities are not represented and there is a lack of similarity in properties in the same neighborhood. Despite this, analyzing boston provides a great indicator to the trends of other cities.

    The goal for this project is to find a suggested Airbnb price based on neighborhood, census tract, property type  and amenities. The end goal is for a prospective Airbnb host to use this dashboard to view data about other listings, then use our models to calculate a suggested price.

    ## Inspiration
    Our group was inspired for this project when watching the Boston Celtics play and seeing Airbnb advertisements across the court. We decided to research [data](http://insideairbnb.com/get-the-data/) regarding Airbnbs in Boston specifically. This site includes data that is the basis of our project.

    Additionally we were inspired for the analysis for this project from this [data science project](https://mohamedirfansh.github.io/Airbnb-Data-Science-Project), which analyzed Airbnb data in Seattle. 
    This project explored how features, location, and textual data affected prices of Airbnbs. The location data helped influence our maps and spatial regression output.




    ## Caveats
    This project reports the **intrinsic** value of Airbnbs in Boston, not the market value. Since the market value can be viewed on the internet easily, this analysis attempts to calculate the intrinsic value based on location, property and amenities. In other words, this report calculates the value that the features of the property provide.



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
    - This section is the culmination of the project, which allows users to put in multiple inputs to determine a suggested Airbnb price.
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
    
    ## Links to raw data:
    - [Inside Airbnb (listings data)](http://insideairbnb.com/get-the-data/)
    - [Neighborhood Map](https://data.boston.gov/dataset/census-2020-block-group-neighborhoods/resource/ed89fab7-aa21-42ce-874b-1b4971ab50fb)
    - [Neighborhood Stats](https://data.boston.gov/dataset/2020-census-for-boston/resource/5800a0a2-6acd-41a3-9fe0-1bf7b038750d)
    - [Tract Map (no longer available)](https://data.boston.gov/dataset/2020-census-for-boston)
    - [Tract Stats](https://data.boston.gov/dataset/2020-census-for-boston/resource/013aba13-5985-4067-bba4-a8d3ca9a34ac)

    # **About Us:**

    #### Brooks Walsh
    """
    st.image('inputs/images/Brooks.png')
    """
    - Major: Finance
    - Year of Graduation: 2024
    - Interests/Hobbies:  Hiking, skiing, watching Liverpool games


    #### Taylor Sheridan
    """
    st.image('inputs/images/Taylor.png')
    """
    - Major: Finance & Business Analytics
    - Year of Graduation: 2024
    - Interests/Hobbies: Golf, working out, visiting the beach

    #### Thomas McDade
    """
    st.image('inputs/images/Tommy.png')
    """
    - Major: Finance & Business Analytics
    - Year of Graduation: 2024
    - Interests/Hobbies: Sports betting, EDM music, nature
    """


elif page_select == 'EDA & Methodology':
    with open('inputs/EDA_Methodology.html', 'r', encoding='utf-8') as f:
        html_file = f.read()
    # Display HTML file
    html(html_file, height = 9300)
else:
    with open('inputs/ML_discussion.html', 'r', encoding='utf-8') as f:
        html_file = f.read()
    # Display HTML file
    html(html_file, height = 7800)

