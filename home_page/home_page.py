import streamlit as st
import json
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
geojson_sql = "SELECT GEO_JSON FROM CBSA_DATA WHERE GEO_NAME = " + f"'{cbsa_selection}'" + "LIMIT 1"
geojson = conn.query(geojson_sql, ttl=0)


st.write(json.load(geojson))

# create the GeoJson layer
#geojson = pdk.Layer(
#    "GeoJsonLayer",
#    geojsondata,
#    opacity=0.8,
#    stroked=False,
#   filled=True,
#    extruded=True,
#    wireframe=True,
#    get_elevation="properties.valuePerSqm / 20",
#    get_fill_color="[255, 255, properties.growth * 255]",
#    get_line_color=[255, 255, 255],
#)
