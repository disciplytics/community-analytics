import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')

 
conn = st.connection("snowflake")

cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_DATA_GEO_NAMES', ttl=0)

cbsa_selection = st.selectbox(
 'Select a Metro/Micropolitan Area (Type to Search)',cbsa_list)

st.write(cbsa_selection)
