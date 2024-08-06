import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')

conn = st.connnection("snowflake")

cbsa_list = conn.query('SELECT DISTINCT GEO_NAME FROM CBSA_DATA LIMIT 1000;', ttl=600)

st.write(cbsa_list)         
