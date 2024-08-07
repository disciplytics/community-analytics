import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import ast

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')


# connect to snowflake
conn = st.connection("snowflake")

# get the list of CBSAs for the user
cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_DATA_GEO_NAMES ORDER BY GEO_NAME ASC', ttl=0)

# return list of CBSA in a select box
cbsa_selection = st.selectbox(
 'Select a Metro/Micropolitan Area (Type a city name or state abbreviation to search)', cbsa_list)

st.write(f'Please enjoy the community report for the {cbsa_selection}. See the views on the left.')

# get geojson for selected area
geojson_sql = "SELECT COORDS FROM CBSA_DATA WHERE GEO_NAME = " + f"'{cbsa_selection}'" + "LIMIT 1"
geojson = conn.query(geojson_sql, ttl=0)

# covert to dictionary
geojson_dict = ast.literal_eval(geojson['COORDS'][0])

# create the GeoJson layer
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_dict,
    opacity=0.3,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="20",
    get_fill_color="[137, 207, 240]",
    get_line_color=[255, 255, 255],
)

INITIAL_VIEW_STATE = pdk.ViewState(latitude=geojson_dict['coordinates'][0][0][1], longitude=geojson_dict['coordinates'][0][0][0], zoom=7, max_zoom=16, pitch=45, bearing=0)

# create the pydeck using the geojson layer
r = pdk.Deck(layers=[ geojson_layer ], map_style=None, initial_view_state=INITIAL_VIEW_STATE)

# display the pydeck
st.pydeck_chart(r)

# add CBSA filter to a session variable
st.session_state['cbsa_selection'] = cbsa_selection
