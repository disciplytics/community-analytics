import streamlit as st
import pandas as pd
import numpy as np

st.title("Age Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")

# age and sex etl
age_sex_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_AGESEX_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
age_sex_df = conn.query(age_sex_sql, ttl=0)

# get age aggregate column
age_sex_df['Age Range'] = age_sex_df['VARIABLE_NAME'].str.lstrip('Sex By Age: Population |')
st.dataframe(age_sex_df)
