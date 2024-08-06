import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')

 
conn = st.connection("default", type = 'snowflake')

cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_DATA_GEO_NAMES;', ttl=0)


conn.close()
st.write(cbsa_list)         
