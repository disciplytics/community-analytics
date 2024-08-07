import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

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

# get polygon for selected area
polygon_sql = "SELECT POLYGON FROM CBSA_DATA WHERE GEO_NAME = " + f"'{cbsa_selection}'" + "LIMIT 1"
polygon = conn.query(polygon_sql, ttl=0)

# find averages of polygons
center_point = np.average(polygon['POLYGON'][0][9:-2], axis=0)

st.write(center_point)

polygon_layer_snow = pdk.Layer(
        "PolygonLayer",
        polygon,
        #id="geojson",
        opacity=0.05,
        stroked=True,
        get_polygon="POLYGON",
        filled=True,
        get_line_color=[200, 200, 200],
        auto_highlight=True,
        pickable=True,
    )


r = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
        latitude=center_point[1],
        longitude=center_point[0],
        zoom=3,
        pitch=50,
    ),
    layers=[polygon_layer_snow]    
)

st.pydeck_chart(r)



