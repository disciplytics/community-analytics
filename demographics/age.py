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

# Clean up Sex
def sex_cleanup(x):
  if x[:1] == 'M':
    return x.lstrip('Male |')
  elif x[:1] == 'F':
    return x.lstrip('Female |')
age_sex_df['Age Range'] = age_sex_df['Age Range'].apply(sex_cleanup)

# remove 5yr Estimate
age_sex_df['Age Range'] = age_sex_df['Age Range'].str.rstrip(', 5yr Estimate')

# get year variable
age_sex_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(age_sex_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)

# make the age table
age_sex_df_report = pd.pivot_table(
  age_sex_df, index = 'Age Range', columns = 'FIVE_YEAR_ESTIMATE_DATE', values = 'FIVE_YEAR_ESTIMATE', aggfunc = 'sum').fillna(0)

st.dataframe(age_sex_df_report, use_container_width=True)

st.dataframe(age_sex_df)
