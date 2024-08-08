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

# rename year ranges
mapping_dict = {
  'Und': 'Under 5 Yrs Old',
  '5 to 9': '5 to 9 Yrs Old',
  '10 to 14': '10 to 14 Yrs Old',
  '15 to 17': '15 to 17 Yrs Old',
  '18 and 19': '18 to 19 Yrs Old',
  '20': '20 Yrs Old',
  '21': '21 Yrs Old',
  '22 to 24': '22 to 24 Yrs Old',
  '25 to 29': '25 to 29 Yrs Old',
  '30 to 34': '30 to 34 Yrs Old',
  '35 to 39': '35 to 39 Yrs Old',
  '40 to 44': '40 to 44 Yrs Old',
  '45 to 49': '45 to 49 Yrs Old',
  '50 to 54': '50 to 54 Yrs Old',
  '55 to 59': '55 to 59 Yrs Old',
  '60 and 61': '60 to 61 Yrs Old',
  '62 to 64': '62 to 64 Yrs Old',
  '65 to 66': '65 to 66 Yrs Old',
  '67 to 69': '67 to 69 Yrs Old',
  '70 to 74': '70 to 74 Yrs Old',
  
}
st.dataframe(age_sex_df_report, use_container_width=True)

st.write(age_sex_df['Age Range'].unique())
