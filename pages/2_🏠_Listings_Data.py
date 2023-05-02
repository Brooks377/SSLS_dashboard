import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
from collections import Counter
import ast
from os import path

st.set_page_config(
    page_title="Listings Data",
    page_icon="inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

"""
# Select a Month and a Neighborhood/Tract to View Current Listings Data
"""


@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    return df
@st.cache_data
def load_gpd(path):
    df = gpd.read_file(path)
    return df


# load datasets
boston_NBH = load_csv("inputs/boston_NBH.csv")
boston_NBH_map = load_gpd("inputs/Census2020_BG_Neighborhoods/Census2020_BG_Neighborhoods.shp")
boston_tract = load_csv("inputs/boston_tract.csv")
boston_tract_map = load_gpd("inputs/Census2020_Tracts/Census2020_Tracts.shp")

# load graphic master dataset
master = load_csv('inputs/master.csv')
master_short = load_csv('inputs/master_short.csv')
master['date'] = pd.to_datetime(master['date'])

#######################################
# Sidebar
#######################################

# sidebar prep
start_date = pd.to_datetime('2023-03-19')
end_date = pd.to_datetime('2024-03-18')
dates = pd.date_range(start=start_date, end=end_date, freq='MS')
dates = [d.strftime('%B %Y') for d in dates]

with st.sidebar:
    
    "Select Month"
    month_select = st.selectbox("Month", dates)

    "Select Zone Type"
    zone_type = st.selectbox("Zone Type", ['Neighborhoods','Census-Tracts'])
    
    if zone_type == 'Neighborhoods':
        "Select Neighborhood"
        zone_select = st.selectbox("Neighborhood", ['All (Boston)'] + boston_NBH.query('BNBs != 0')['BlockGr202'].tolist())
    else:
        "Select Census Tract"
        zone_select = st.selectbox("Census Tract", ['All (Boston)'] + boston_tract.query('BNBs != 0')['NAME20'].tolist())
        
    st.button("Rerun")

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

    boston_tract_map.to_crs('epsg:4326', inplace=True)
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
# filter data based on sidebar
#####################################################

if zone_type == "Neighborhoods":
    if zone_select == "All (Boston)":
        master_filt = master
        month_selected = pd.to_datetime(month_select)
        master_filt = master_filt.loc[(master_filt['date'] >= month_selected)
                                            & (master_filt['date'] < month_selected + pd.DateOffset(months=1))]
    else:
        # select neighborhood
        master_filt = master.loc[master['census_NBH'] == zone_select].reset_index()

        # select date
        month_selected = pd.to_datetime(month_select)
        master_filt = master_filt.loc[(master_filt['date'] >= month_selected)
                                            & (master_filt['date'] < month_selected + pd.DateOffset(months=1))]
else:
    if zone_select == "All (Boston)":
        master_filt = master
        month_selected = pd.to_datetime(month_select)
        master_filt = master_filt.loc[(master_filt['date'] >= month_selected)
                                            & (master_filt['date'] < month_selected + pd.DateOffset(months=1))]
    else:
        # select tract
        master_filt = master.loc[master['census_tract'] == zone_select].reset_index()

        # select date
        month_selected = pd.to_datetime(month_select)
        master_filt = master_filt.loc[(master_filt['date'] >= month_selected)
                                            & (master_filt['date'] < month_selected + pd.DateOffset(months=1))]

############################################
# Start of listings data displays
############################################

# display total listings
if zone_type == "Neighborhoods":
    if zone_select == "All (Boston)":
        total_listings = boston_NBH['BNBs'].sum()
        zone_text = 'Boston'
    else:
        total_listings = boston_NBH.loc[zone_select, 'BNBs']
        zone_text = zone_select
else:
    if zone_select == "All (Boston)":
        total_listings = boston_tract['BNBs'].sum()
        zone_text = 'Boston'
    else:
        total_listings = boston_tract.loc[zone_select, 'BNBs']
        zone_text = f'Tract #{zone_select}'

# total listings
st.write(f'<p style="font-size: 25px;">Total Listings in {zone_text}: {int(total_listings)}</p>', unsafe_allow_html=True)

# display pricing data
high_price = master_filt['price'].max()
low_price = master_filt.loc[master_filt['price'] > 0, 'price'].min()
avg_price = master_filt['price'].mean()

data = [{'Highest Price': high_price,
         'Average Price': avg_price,
        'Lowest Price': low_price}]

prices = pd.DataFrame.from_dict(data)
prices = prices.T.rename(columns={0:f'{month_select} List Price'}).style.format('${:.2f}')

# write prices dataframe
st.write(prices)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

########################
# room-type distribution
########################

if zone_type == "Neighborhoods":
    # create room_type plot
    fig1, ax = plt.subplots()
    sns.countplot(data = master_filt, y = 'room_type', hue = 'room_type', 
                  palette = 'Oranges')

else:
    fig1, ax = plt.subplots()
    sns.countplot(data = master_filt, y = 'room_type', hue = 'room_type', 
                  palette = 'Blues')

ax.set_title('Room-Type Distribution')
ax.set_xlabel('Count\n(days * listings in selected month)')
ax.set_ylabel('Room Type')
ax.legend(title='Room Type')

sns.move_legend(ax, "center left", bbox_to_anchor=(1,.6))

# displaying plot
st.pyplot(fig1)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

###################
# Availability data
###################

# using master_filt from above
avail_list = np.where(master_filt.loc[:, 'available'] == 't', 'available', 'booked')
master_filt = master_filt.assign(Availability=avail_list)

# create annotation stat
sum = master_filt['Availability'].value_counts().sum()
vac = master_filt['Availability'].value_counts()['available']
vac_rate = (vac / sum).round(2)

# create plot
if zone_type == "Neighborhoods":
    fig2, ax = plt.subplots()
    sns.countplot(data = master_filt,
                  y = 'available',
                  hue = 'Availability',
                  palette = 'Oranges')

else:
    fig2, ax = plt.subplots()
    sns.countplot(data = master_filt,
                  y = 'available',
                  hue = 'Availability',
                  palette = 'Blues')


sns.move_legend(ax, "center left",  bbox_to_anchor=(1,.6))
ax.set_title('Availability of Listings')
ax.set_xlabel('Count\n(days * listings in selected month)')
ax.set_ylabel('Available')
ax.annotate(f'Vacancy Rate: {vac_rate}', xy=(1, 1), xytext=(ax.get_xlim()[1] * 1.015, ax.get_ylim()[1] *.4), bbox=dict(facecolor='white', boxstyle='round'))

# displaying plot
st.pyplot(fig2)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

##########################
# Short-term listings data
##########################

# using master_filt from above
rental_list = np.where(master_filt.loc[:, 'minimum_nights'] < 28, 'short-term', 'long-term')
master_filt = master_filt.assign(rental_length=rental_list)

# remove minimum nights outliers
master_filt.query('minimum_nights < 200', inplace=True)

# create annotation stat
sum = master_filt['rental_length'].value_counts().sum()
try:
    short = master_filt['rental_length'].value_counts()['short-term']
except KeyError:
    short = 0
short_term_percent = (short / sum).round(2)

# pre-define bins
bins = [i for i in range(1, master_filt['minimum_nights'].max() + 1)]

if zone_type == "Neighborhoods":
    # Create plot
    fig3, ax = plt.subplots()
    sns.histplot(data=master_filt, x='minimum_nights', hue='rental_length', palette='Oranges', ax=ax, bins=bins, multiple="stack")

else:
    # Create plot
    fig3, ax = plt.subplots()
    sns.histplot(data=master_filt, x='minimum_nights', hue='rental_length', palette='Blues', ax=ax, bins=bins, multiple="stack")
    

# Add vertical line
ax.axvline(x=28, color='red', lw=1)
ax.text(28 , ax.get_ylim()[1] * .85, "STR Threshold", rotation=90, va='center', ha='right', color='red')

# plot stuff
ax.set_title('Short-Term Rentals')
ax.set_xlabel('Minimum Nights')
ax.set_ylabel('Count\n(days * listings in selected month)')
ax.annotate(f'Short-Term Listings: {short_term_percent * 100}%', xy=(1, 1), xytext=(ax.get_xlim()[1] * 1.015, ax.get_ylim()[1] *.7), bbox=dict(facecolor='white', boxstyle='round'))

# displaying plot
st.pyplot(fig3)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

######################
# Word Clouds
######################

# filter data based on sidebar inputs
if zone_type == "Neighborhoods":
    if zone_select == "All (Boston)":
        listings_filt = master_short
    else:
        # select neighborhood
        listings_filt = master_short.loc[master_short['census_NBH'] == zone_select].reset_index()
else:
    if zone_select == "All (Boston)":
        listings_filt = master_short
    else:
        # select neighborhood
        listings_filt = master_short.loc[master_short['census_tract'] == zone_select].reset_index()

# split into high/low prices
listings_filt_low = listings_filt.loc[listings_filt['price'] < listings_filt['price'].mean()]
listings_filt_high = listings_filt.loc[listings_filt['price'] >= listings_filt['price'].mean()]

amenities_low = listings_filt_low['amenities'].apply(lambda x: ast.literal_eval(x))
amenities_high = listings_filt_high['amenities'].apply(lambda x: ast.literal_eval(x))

word_counts_low = Counter()
for amenity_list in amenities_low:
    for amenity in amenity_list:
        word_counts_low[amenity] += 1

# sort the word frequency dictionary by value in descending order
sorted_word_freq = {k: v for k, v in sorted(word_counts_low.items(), key=lambda item: item[1], reverse=True)}

word_freq_low = {}
# print out the top 5-90 most common words
for word, freq in list(sorted_word_freq.items())[5:90]:
    word_freq_low[word] = freq

# same as above but with high price listings
word_counts_high = Counter()
for amenity_list in amenities_high:
    for amenity in amenity_list:
        word_counts_high[amenity] += 1

# sort the word frequency dictionary by value in descending order
sorted_word_freq = {k: v for k, v in sorted(word_counts_high.items(), key=lambda item: item[1], reverse=True)}

word_freq_high = {}
# print out the top 5-90 most common words
for word, freq in list(sorted_word_freq.items())[5:90]:
    word_freq_high[word] = freq


# word cloud creation function
def create_word_cloud(word_freq, mask_path):
    mask = np.array(Image.open(path.join(mask_path)))
    wc = WordCloud(background_color="white", width=1600, height=800, mask=mask)
    wordcloud = wc.generate_from_frequencies(word_freq)
    image = wordcloud.to_image()
    del wc
    return image


# create and display word clouds
wordcloud_high = create_word_cloud(word_freq_high, "inputs/mass_outline.png")
wordcloud_low = create_word_cloud(word_freq_low, "inputs/mass_outline.png")

"""
**Common Amenities of High Price Listings**
"""
st.image(wordcloud_high)

# lame horizontal line
st.markdown('<hr style="border-top: 2px solid #bbb;">', unsafe_allow_html=True)

"""
**Common Amenities of Low Price Listings**
"""
st.image(wordcloud_low)


# garbage collect manually to help stop memory overload
for name in dir():
    if not name.startswith('_'):
        del globals()[name]

import gc
gc.collect()