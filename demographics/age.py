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

# rename year ranges
general_mapping_dict = {
  'Und': 'Under 5 Yrs Old',
  '5 to 9': '5 to 17 Yrs Old',
  '10 to 14': '5 to 17 Yrs Old',
  '15 to 17': '5 to 17 Yrs Old',
  '18 and 19': '18 to 24 Yrs Old',
  '20': '18 to 24 Yrs Old',
  '21': '18 to 24 Yrs Old',
  '22 to 24': '18 to 24 Yrs Old',
  '25 to 29': '25 to 34 Yrs Old',
  '30 to 34': '25 to 34 Yrs Old',
  '35 to 39': '35 to 54 Yrs Old',
  '40 to 44': '35 to 54 Yrs Old',
  '45 to 49': '35 to 54 Yrs Old',
  '50 to 54': '35 to 54 Yrs Old',
  '55 to 59': '55 to 64 Yrs Old',
  '60 and 61': '55 to 64 Yrs Old',
  '62 to 64':  '55 to 64 Yrs Old',
  '65 and 66': '65 Yrs and Older',
  '67 to 69': '65 Yrs and Older',
  '70 to 74': '65 Yrs and Older',
  '75 to 79': '65 Yrs and Older',
  '80 to 84': '65 Yrs and Older',
  '85 years and ov': '65 Yrs and Older',
}

# phase of life dict
phase_of_life_dict = {
  'Under 5 Yrs Old': 'Before Formal Schooling',
  '5 to 17 Yrs Old': 'Required Formal Schooling',
  '18 to 24 Yrs Old': 'College/Career Starts',
  '25 to 34 Yrs Old': 'Singles & Young Families',
  '35 to 54 Yrs Old': 'Families & Empty Nesters',
  '55 to 64 Yrs Old': 'Enrichment Years Singles/Couples',
  '65 Yrs and Older': 'Retirement Opportunities'
}
  
  
# replace ages with readable values
general_age_sex_df = age_sex_df.replace({'Age Range': general_mapping_dict})

# create phase of life field
general_age_sex_df['Phase of Life'] = general_age_sex_df['Age Range'].copy()
general_age_sex_df = general_age_sex_df.replace({'Phase of Life': phase_of_life_dict})

# make the general age table
general_age_sex_df_report = pd.pivot_table(
  general_age_sex_df, 
  index = ['Phase of Life', 'Age Range'], 
  columns = 'FIVE_YEAR_ESTIMATE_DATE', 
  values = 'FIVE_YEAR_ESTIMATE', 
  aggfunc = 'sum').fillna(0)

# reorder indicies
general_age_sex_df_report = general_age_sex_df_report.reindex([
  'Before Formal Schooling', 'Required Formal Schooling', 'College/Career Starts',
  'Singles & Young Families', 'Familes & Empty Nesters', 'Enrichment Years Singles/Couples',
  'Retirement Opportunities'], level = 0)


st.dataframe(general_age_sex_df_report, use_container_width=True)

# percent diff plot
st.write(general_age_sex_df_report.columns)





