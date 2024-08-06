import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')


conn = st.connection("snowflake")

cbsa_list = conn.query('SELECT DISTINCT GEO_NAME FROM CBSA_DATA;', ttl=600)

st.write(cbsa_list)         
