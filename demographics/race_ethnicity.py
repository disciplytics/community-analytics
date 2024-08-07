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

st.dataframe(total_race_df)
