import streamlit as st
import pandas as pd
import numpy as np

st.title('Population Report')


# connect to snowflake
conn = st.connection("snowflake")

'''SELECT 
    GEO_NAME,
    VARIABLE_NAME as Race,
    DATE as Five_Year_Estimate_Date,
    VALUE as Five_Year_Estimate
FROM COMMUNITY_ANALYTICS.PUBLIC.CBSA_RACE_DATA'''

# get the total population
cbsa_list = conn.query('SELECT GEO_NAME FROM CBSA_RACE_DATA', ttl=0)
