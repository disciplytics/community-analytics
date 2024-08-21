import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Education and Vocation Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")

# connect to snowflake
conn = st.connection("snowflake")

# education etl
education_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_EDUCATION_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
education_df = conn.query(education_sql, ttl=0)

st.dataframe(education_df)
