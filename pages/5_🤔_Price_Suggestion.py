import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import pickle
import zipfile


# Page config
st.set_page_config(
    page_title="Price Suggestion",
    page_icon="inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

"""
## Use Sidebar Survey to Find Suggested Price
"""
@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    return df
@st.cache_data
def load_gpd(path):
    df = gpd.read_file(path)
    return df


# load all data first, some is needed for sidebar
boston_NBH = load_csv("inputs/boston_NBH.csv")
boston_NBH_map = load_gpd("inputs/Census2020_BG_Neighborhoods/Census2020_BG_Neighborhoods.shp")
boston_tract = load_csv("inputs/boston_tract.csv")
boston_tract_map = load_gpd("inputs/Census2020_Tracts/Census2020_Tracts.shp")

# sidebar prep
start_date = pd.to_datetime('2023-03-19')
end_date = pd.to_datetime('2024-03-18')
dates = pd.date_range(start=start_date, end=end_date, freq='MS')
dates = [d.strftime('%B %Y') for d in dates]

# remove places with 0 listings because it breaks the model
boston_NBH_box = boston_NBH[boston_NBH['BNBs'] != 0]
boston_tract_box = boston_tract[boston_tract['BNBs'] != 0]

# survey items (model variables)
items = ['air_conditioning', 'high_end_electronics', 'bbq', 'balcony', 'nature_and_views', 'bed_linen', 'breakfast', 'tv', 'coffee_machine', 'cooking_basics', 'white_goods', 'elevator', 'gym', 'child_friendly', 'parking', 'outdoor_space', 'host_greeting', 'hot_tub_sauna_or_pool', 'internet', 'long_term_stays', 'pets_allowed', 'private_entrance', 'secure', 'self_check_in', 'smoking_allowed']

room_type_list = ['Entire home/apt', 'Private room', 'Hotel room', 'Shared room']

prop_type_list = ['Entire rental unit', 'Private room in rental unit', 'Entire condo', 'Private room in home', 'Entire serviced apartment', 'Entire home', 'Private room in condo', 'Private room in townhouse', 'Entire townhouse', 'Entire guest suite', 'Private room in bed and breakfast', 'Room in boutique hotel', 'Room in hotel', 'Other']

################################
# sidebar
################################

with st.sidebar:
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])
    if zone_type == 'Neighborhoods':
        
        zone_select = st.selectbox("Neighborhood", ['All (Boston)'] + boston_NBH_box['BlockGr202'].tolist())
    else:
        
        zone_select = st.selectbox("Census Tract", ['All (Boston)'] + boston_tract_box['NAME20'].tolist())
    """
    Neighborhoods/tracts with 0 current listings cannot be selected
    """
    st.button("Rerun")
    
    # lame horizontal line
    st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)
    with st.form("Listing Info Survey"):
        
        month_select = st.selectbox("Month", dates)
        
        prop_type = st.selectbox('Property Type', prop_type_list)
        
        room_type = st.selectbox("Room Type", room_type_list)

        bedroom_num = st.select_slider('Number of Bedrooms', range(1, 16))
        
        guest_num = st.select_slider('Number of Guests Allowed', range(1, 21))

        """
        Check All that Apply:
        """
        # checkbox output
        checkbox_values = {}

        # loop through options and store values
        for option in items:
            checkbox_values[option] = st.checkbox(option)

        submitted = st.form_submit_button('Suggest Price')

    # create a dataframe using the dictionary
    df = pd.DataFrame.from_dict(checkbox_values, orient='index', columns=['Value'])

#######################################################################
# Map of neighborhoods
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

    boston_NBH_map.to_crs('epsg:4326', inplace=True)
    boston_NBH_map.set_index('BlockGr202', inplace=True)
    boston_NBH.set_index('BlockGr202', inplace=True)

    fig = px.choropleth(boston_NBH,
                        geojson=boston_NBH_map.geometry,
                        locations=boston_NBH_map.index,
                        color="BNBDensity",
                        custom_data=['BNBs'],
                        color_continuous_scale= "Oranges")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>' +
                                 '# of BNB listings: %{customdata}',
                                 selectedpoints=zone_index_select)

#####################################################
# map of census tracts (same steps as above for NBH)
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

    boston_tract_map.to_crs('epsg:4326', inplace=True)
    boston_tract_map.set_index('NAME20', inplace=True)
    boston_tract.set_index('NAME20', inplace=True)

    fig = px.choropleth(boston_tract,
                        geojson=boston_tract_map.geometry,
                        locations=boston_tract_map.index,
                        color="BNBDensity",
                        custom_data=['BNBs'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>' +
                                 '# of BNB listings: %{customdata}',
                                 selectedpoints=zone_index_select)

# displaying plot
st.plotly_chart(fig, use_container_width=False)


########################################
# input dataframe and suggested price
########################################

# extract models from zip

@st.cache_data
def load_models(zone_type):
    # name of the NBH models zip
    if zone_type == "Neighborhoods":
        zip_filename = 'inputs/models/zip_models_NBH.zip'
        # create a zipfile object
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            # load models from the pickle files in the zip file
            with zip_file.open('models_NBH.pkl') as f:
                models_NBH = pickle.load(f)
        return models_NBH

    # name of the tract models zip
    else:
        zip_filename = 'inputs/models/zip_models_tract.zip'
        # create a zipfile object
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            # load models from the pickle files in the zip file
            with zip_file.open('models_tract.pkl') as f:
                models_tract = pickle.load(f)
        return models_tract


if submitted:
    # select model based on month
    month_to_model = {
    "April 2023": "model_0",
    "May 2023": "model_1",
    "June 2023": "model_1",
    "July 2023": "model_2",
    "August 2023": "model_2",
    "September 2023": "model_4",
    "October 2023": "model_5",
    "November 2023": "model_6",
    "December 2023": "model_6",
    "January 2024": "model_9",
    "February 2024": "model_9",
    "March 2024": "model_9",
    }

    models = load_models(zone_type)
    model = models[month_to_model[month_select]]

    # add survey data to dataframe
    if zone_select == "All (Boston)":
        st.write("Please Input Neighborhood or Tract for Suggestion")
    else:
        if zone_type == "Neighborhoods":
            survey_columns = {'room_type': room_type, 'property_type': prop_type,
                          'bedrooms': bedroom_num, 'accommodates': guest_num,
                          'census_NBH': zone_select}
        else:
            survey_columns = {'room_type': room_type, 'property_type': prop_type,
                          'bedrooms': bedroom_num, 'accommodates': guest_num,
                          'census_tract': zone_select}
        df = df.astype(int)
        df = df.T.assign(**survey_columns)
        df = df.iloc[:, ::-1]
        # display the dataframe
        st.write(df)
        
        y_pred = model.predict(df)
        st.write(f'Your Suggested List Price for {month_select} is: ${y_pred[0]:.2f}')


# garbage collect manually to help stop memory overload
for name in dir():
    if not name.startswith('_'):
        del globals()[name]

import gc
gc.collect()