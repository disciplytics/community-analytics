import streamlit as st
import pandas as pd
import numpy as np

st.title(f"Population Report: {st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")

# total pop etl
total_pop_sql = "SELECT GEO_NAME, VARIABLE_NAME as Race, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE VARIABLE_NAME = 'Race: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
#total_pop_sql = "SELECT GEO_NAME, VARIABLE_NAME as Legend, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"

# get the total population
total_pop_df = conn.query(total_pop_sql, ttl=0)

st.subheader('Population Trends')
st.line_chart(
  data = total_pop_df, 
  x = 'FIVE_YEAR_ESTIMATE_DATE', 
  y = 'FIVE_YEAR_ESTIMATE',
  x_label = '5 Year Estimate Date',
  y_label = 'Population Count')
