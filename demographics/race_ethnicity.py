import streamlit as st
import pandas as pd
import numpy as np

st.title("Race and Ethnicity Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")

# race etl
total_race_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE VARIABLE_NAME <> 'Race: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total race
total_race_df = conn.query(total_race_sql, ttl=0)

# prep data
total_race_df['Measure'] = total_race_df['VARIABLE_NAME'].str.lstrip('Race: Population | ')
total_race_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(total_race_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)
total_race_df['Counts'] = total_race_df['FIVE_YEAR_ESTIMATE'].astype(int)

st.write('Race Trends')
race_filter = st.multiselect('Filter Races Here', total_race_df['Measure'].unique(),total_race_df['Measure'].unique())
st.bar_chart(
  data = total_race_df[total_race_df['Measure'].isin(race_filter)],
  x = 'FIVE_YEAR_ESTIMATE_DATE',
  y = 'Counts',
  x_label = '5 Year Estimate Date',
  y_label = 'Total',
  color = 'Measure',
  stack = False,
  use_container_width = True)
