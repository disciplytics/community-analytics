import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')


conn = st.connection('snowflake')

cbsa_list = conn.query('SELECT DISTINCT GEO_NAME as "Metro/Micro Area" FROM CBSA_DATA')

st.write(cbsa_list)         
