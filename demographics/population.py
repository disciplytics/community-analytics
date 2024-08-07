import streamlit as st
import pandas as pd
import numpy as np

st.title("Population Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")
st.write('Population, households, and families')


# connect to snowflake
conn = st.connection("snowflake")

# total pop etl
total_pop_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE VARIABLE_NAME = 'Race: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total population
total_pop_df = conn.query(total_pop_sql, ttl=0)

# total HH etl
total_hh_sql = "SELECT  GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_HHFAM_DATA WHERE VARIABLE_NAME = 'Household Type By Household Size: Population | Total, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total number of households
total_hh_df = conn.query(total_hh_sql, ttl=0)

# total familes etl
total_fam_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_HHFAM_DATA WHERE VARIABLE_NAME = 'Household Type By Household Size: Population | Family households, 5yr Estimate' AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'"
# get the total number of familes
total_fam_df = conn.query(total_fam_sql, ttl=0)

overview_tab, trend_tab, pct_change_tab = st.tabs(['Overview', 'Trend View', 'Percent Change View'])

with overview_tab:

  ## POPULATION
  # calc pct change
  overview_df_pop = total_pop_df.sort_values(by=['FIVE_YEAR_ESTIMATE_DATE'])
  overview_df_pop['PCT_CHANGE'] = overview_df_pop['FIVE_YEAR_ESTIMATE'].pct_change()
  # drop nan from pct change
  overview_df_pop = overview_df_pop.dropna()
  # format the pct change and count
  overview_df_pop['Percent Change'] = np.round(overview_df_pop['PCT_CHANGE']*100,2).astype(str)+"%"
  overview_df_pop['Count'] = overview_df_pop['FIVE_YEAR_ESTIMATE'].astype(int)
  # rename VARIABLE_NAME
  overview_df_pop['VARIABLE_NAME'] = 'Total Population'

  ## HOUSEHOLDS
  # calc pct change
  overview_df_hh = total_hh_df.sort_values(by=['FIVE_YEAR_ESTIMATE_DATE'])
  overview_df_hh['PCT_CHANGE'] = overview_df_hh['FIVE_YEAR_ESTIMATE'].pct_change()
  # drop nan from pct change
  overview_df_hh = overview_df_hh.dropna()
  # format the pct change and count
  overview_df_hh['Percent Change'] = np.round(overview_df_hh['PCT_CHANGE']*100,2).astype(str)+"%"
  overview_df_hh['Count'] = overview_df_hh['FIVE_YEAR_ESTIMATE'].astype(int)
  # rename VARIABLE_NAME
  overview_df_hh['VARIABLE_NAME'] = 'Total Households'
  
  ## FAMILIES
  # calc pct change
  overview_df_fam = total_fam_df.sort_values(by=['FIVE_YEAR_ESTIMATE_DATE'])
  overview_df_fam['PCT_CHANGE'] = overview_df_fam['FIVE_YEAR_ESTIMATE'].pct_change()
  # drop nan from pct change
  overview_df_fam = overview_df_fam.dropna()
  # format the pct change and count
  overview_df_fam['Percent Change'] = np.round(overview_df_fam['PCT_CHANGE']*100,2).astype(str)+"%"
  overview_df_fam['Count'] = overview_df_fam['FIVE_YEAR_ESTIMATE'].astype(int)
  # rename VARIABLE_NAME
  overview_df_fam['VARIABLE_NAME'] = 'Total Families'

  ## append tables
  overview_df = pd.concat([overview_df_pop, overview_df_hh, overview_df_fam])

  ## Get Year
  overview_df['FIVE_YEAR_ESTIMATE_DATE'] = overview_df['FIVE_YEAR_ESTIMATE_DATE'].dt.year.astype(int)
  # change calcs to rows
  overview_df = pd.melt(overview_df, id_vars = ['VARIABLE_NAME', 'FIVE_YEAR_ESTIMATE_DATE'], value_vars = ['Count', 'Percent Change'])
  overview_df = overview_df.pivot(
    values = 'value', 
    index = ['VARIABLE_NAME', 'variable'], 
    columns = 'FIVE_YEAR_ESTIMATE_DATE')

  # reorder df
  overview_df = overview_df.sort_index(level = 0, ascending=False)
  
  st.table(overview_df)

with trend_tab:
  st.subheader('PopulationTrends')
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

with pct_change_tab:
  st.write('hi')
