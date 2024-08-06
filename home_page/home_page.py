import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')

 
conn = st.connection("snowflake", type = "snowflake")

cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_DATA LIMIT 4;', ttl=0)


conn.close()
st.write(cbsa_list)         
