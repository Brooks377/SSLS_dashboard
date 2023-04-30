import pandas as pd
import plotly.express as px
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Census Info",
    page_icon="inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

"""
# Select a Neighborhood/Tract to View Stats
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

# more sidebar prep
start_date = pd.to_datetime('2023-03-19')
end_date = pd.to_datetime('2024-03-18')
dates = pd.date_range(start=start_date, end=end_date, freq='MS')
dates = [d.strftime('%B %Y') for d in dates]

# census data
NBH_data = load_csv("inputs/NBH_census_data.csv")
tract_data = load_csv("inputs/tract_census_data.csv")

#############################################
# start: sidebar
#############################################

with st.sidebar:

    "Select Zone Type"
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])

    if zone_type == 'Neighborhoods':
        "Select Neighborhood"
        zone_select = st.selectbox("Neighborhood", ['All (Boston)'] + boston_NBH['BlockGr202'].tolist())
    else:
        "Select Census Tract"
        zone_select = st.selectbox("Census Tract", ['All (Boston)'] + boston_tract['NAME20'].tolist())

    st.button("Rerun")
#############################################
# end: sidebar
#############################################

#######################################################################
# map of neighborhoods
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
                        hover_data=['BNBs'],
                        color_continuous_scale= "Oranges")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>' +
                                 'BNB Density: %{z}<br>',
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

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

######################################################
# demographic pie chart
######################################################

if zone_type == "Neighborhoods":
    if zone_select == "All (Boston)":
        plot_values = NBH_data.iloc[:, 2:7].sum().values.tolist()
        plot_labels = NBH_data.iloc[:, 2:7].columns.tolist()
        plot_anot = NBH_data['Total:'].sum()

        # title variable
        type_lab = "Boston"

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
        
        # title variable
        type_lab = "Neighborhood"

else:
    # tract pie chart
    if zone_select == "All (Boston)":
        plot_values = tract_data.iloc[:, 2:10].sum().values.tolist()
        plot_labels = tract_data.iloc[:, 2:10].columns.tolist()
        plot_anot = tract_data['Total:'].sum()
        
        # title variable
        type_lab = "Boston"

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
        
        # title variable
        type_lab = "Census Tract"


# create a pie chart
fig1, ax = plt.subplots()
ax.pie(plot_values, autopct='%1.1f%%')
ax.set_title(f'{type_lab} Demographic Breakdown')
ax.legend(labels=plot_labels, loc='center left', bbox_to_anchor=(.95, .5 ))
ax.annotate(f'Total Population of {type_lab}: {plot_anot}' , xy=(1, 1), xytext=(ax.get_xlim()[1] * .96 , ax.get_ylim()[1] * .6), bbox=dict(facecolor='white', boxstyle='round'))

st.pyplot(fig1)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

######################
# vacancy pie chart
######################
if not zone_select == "All (Boston)":
    households_in_zone = row_to_plot['Occupied'].values[0] + row_to_plot['Vacant'].values[0]
else:
    households_in_zone = NBH_data['Occupied'].sum() + NBH_data['Vacant'].sum()

if households_in_zone > 0:
    if zone_type == "Neighborhoods":
        if zone_select == "All (Boston)":
            plot_values = NBH_data.iloc[:, 7:].sum().values.tolist()
            plot_labels = NBH_data.iloc[:, 7:].columns.tolist()
            plot_anot = households_in_zone

            # title variable
            type_lab = "Boston"

        else:
            # slice the row
            row_to_plot = NBH_data.loc[NBH_data['field concept'] == zone_select]

            # slice the columns
            cols_to_plot = row_to_plot.iloc[:, 7:]

            # filter out zeros
            mask = cols_to_plot.ne(0)
            cols_to_plot = cols_to_plot.loc[:, mask.values[0]]
            plot_values = cols_to_plot.values.tolist()[0]
            plot_labels = cols_to_plot.columns.tolist()
            plot_anot = households_in_zone

            # title variable
            type_lab = "Neighborhood"

    else:
        # tract pie chart
        if zone_select == "All (Boston)":
            plot_values = tract_data.iloc[:,10:].sum().values.tolist()
            plot_labels = tract_data.iloc[:,10:].columns.tolist()
            plot_anot = households_in_zone

            # title variable
            type_lab = "Boston"

        else:
            # slice the row
            selector = boston_tract.loc[zone_select, 'TRACTCE20']
            row_to_plot = tract_data.loc[tract_data['Census Tract'] == selector]

            # slice the columns
            cols_to_plot = row_to_plot.iloc[:,10:]

            # filter out zeros
            mask = cols_to_plot.ne(0)
            cols_to_plot = cols_to_plot.loc[:, mask.values[0]]
            plot_values = cols_to_plot.values.tolist()[0]
            plot_labels = cols_to_plot.columns.tolist()
            plot_anot = households_in_zone

            # title variable
            type_lab = "Tract"


    # create a pie chart
    fig2, ax = plt.subplots()
    ax.pie(plot_values, autopct='%1.1f%%')
    ax.set_title(f'{type_lab}-Level Household Vacancy Rate')
    ax.legend(labels=plot_labels, loc='center left', bbox_to_anchor=(.95, .5 ))
    ax.annotate(f'Total Households in {type_lab}: {plot_anot}' , xy=(1, 1), xytext=(ax.get_xlim()[1] * .96 , ax.get_ylim()[1] * .4), bbox=dict(facecolor='white', boxstyle='round'))

    st.pyplot(fig2)
else:
    st.write('There is not enough housing data for vacancy stats')







