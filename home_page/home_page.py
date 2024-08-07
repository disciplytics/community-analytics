import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geojson import Polygon

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

#st.write(np.array(polygon['POLYGON'][0][9:-2]))

# This array will contain your polygons for each district
polygons = []

# Iterate through the response records
for record in polygon["POLYGON"]:
    # This array will contain coordinates to draw a polygon
    coordinates = []
    
    # Iterate through the coordinates of the record
    for coord in record["fields"]["geo_shape"]["coordinates"][0]:
        lon = coord[0] # Longitude
        lat = coord[1] # Latitude
        
        # /!\ Order of lon & lat might be wrong here
        coordinates.append((lon, lat))

    # Append a new Polygon object to the polygons array
    # (Note that there are outer brackets, I'm not sure if you can
    # store all polygons in a single Polygon object)
    polygons.append(Polygon([coordinates]))

st.write(polygons)



