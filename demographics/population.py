import streamlit as st
import pandas as pd
import numpy as np

st.title("Population Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")
st.write('Population, households, and families')


# connect to snowflake
conn = st.connection("snowflake")

# total pop etl
total_pop_sql = "SELECT GEO_NAME, VARIABLE_NAME as Race, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE VARIABLE_NAME = 'Race: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total population
total_pop_df = conn.query(total_pop_sql, ttl=0)

# total HH etl
total_hh_sql = "SELECT  GEO_NAME, VARIABLE_NAME as HOUSEHOLDS, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_HHFAM_DATA WHERE VARIABLE_NAME = 'Household Type By Household Size: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total number of households
total_hh_df = conn.query(total_hh_sql, ttl=0)

# total familes etl
total_fam_sql = "SELECT GEO_NAME, VARIABLE_NAME as FAMILIES, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_HHFAM_DATA WHERE VARIABLE_NAME = 'Household Type By Household Size: Population | Family households, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total number of familes
total_fam_df = conn.query(total_fam_sql, ttl=0)

st.subheader('Population Trends')
st.line_chart(
  data = total_pop_df, 
  x = 'FIVE_YEAR_ESTIMATE_DATE', 
  y = 'FIVE_YEAR_ESTIMATE',
  x_label = '5 Year Estimate Date',
  y_label = 'Population Count')

st.subheader('Household Trends')
st.line_chart(
  data = total_hh_df, 
  x = 'FIVE_YEAR_ESTIMATE_DATE', 
  y = 'FIVE_YEAR_ESTIMATE',
  x_label = '5 Year Estimate Date',
  y_label = 'Household Count')

st.subheader('Family Trends')
st.line_chart(
  data = total_fam_df, 
  x = 'FIVE_YEAR_ESTIMATE_DATE', 
  y = 'FIVE_YEAR_ESTIMATE',
  x_label = '5 Year Estimate Date',
  y_label = 'Family Count')
