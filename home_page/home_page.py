import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')


# connect to snowflake
conn = st.connection("snowflake")

# get the list of CBSAs for the user
cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_DATA_GEO_NAMES ORDER BY GEO_NAME ASC', ttl=0)

# return list of CBSA in a select box
cbsa_selection = st.selectbox(
 'Select a Metro/Micropolitan Area (Type a city name or state abbreviation to search)',cbsa_list)

st.write(f'Please enjoy the community report for the {cbsa_selection}. See the views on the left.')

# get geojson for selected area
geojson = conn.query(f"SELECT GEO_JSON FROM COMMUNITY_ANALYTICS.PUBLIC.CBSA_DATA WHERE GEO_NAME = {cbsa_selection} LIMIT 1;", ttl=0)

st.write(geojson)
