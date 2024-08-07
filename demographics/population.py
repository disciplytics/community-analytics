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

# family breakdown etl
bd_fam_sql = "SELECT  GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_HHFAM_DATA WHERE VARIABLE_NAME IN ('Households By Type: Population | Married-couple household, 5yr Estimate', 'Households By Type: Population | Married-couple household | With no children of the householder under 18 years, 5yr Estimate', 'Households By Type: Population | Married-couple household | With children of the householder under 18 years, 5yr Estimate', 'Households By Type: Population | Cohabiting couple household, 5yr Estimate', 'Households By Type: Population | Cohabiting couple household | With no children of the householder under 18 years, 5yr Estimate', 'Households By Type: Population | Cohabiting couple household | With children of the householder under 18 years, 5yr Estimate', 'Households By Type: Population | Male householder, no spouse or partner present, 5yr Estimate', 'Households By Type: Population | Female householder, no spouse or partner present, 5yr Estimate') AND GEO_NAME = " + f"'{st.session_state['cbsa_selection']}'";
# get the breakdown family
bd_fam_df = conn.query(bd_fam_sql, ttl=0)



# create UI
overview_tab, fam_tab = st.tabs(['Overview', 'Family Breakdown View'])

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
  overview_df_pop['Measure'] = 'Total Population'

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
  overview_df_hh['Measure'] = 'Total Households'
  
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
  overview_df_fam['Measure'] = 'Total Families'

  ## append tables
  overview_df = pd.concat([overview_df_pop, overview_df_hh, overview_df_fam])

  ## Get Year
  overview_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(overview_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)
  # change calcs to rows
  overview_df_pivot = pd.melt(overview_df, id_vars = ['Measure', 'FIVE_YEAR_ESTIMATE_DATE'], value_vars = ['Count', 'Percent Change'])
  overview_df_pivot = overview_df_pivot.pivot(
    values = 'value', 
    index = ['Measure', 'variable'], 
    columns = 'FIVE_YEAR_ESTIMATE_DATE')

  # reorder df
  overview_df_pivot = overview_df_pivot.sort_index(level = 0, ascending=False)

  # plot 
  st.bar_chart(
    data = overview_df,
    x = 'FIVE_YEAR_ESTIMATE_DATE',
    y = 'Count',
    x_label = '5 Year Estimate Date',
    y_label = 'Total',
    color = 'Measure',
    stack = True)
  # table
  st.dataframe(overview_df_pivot)

with fam_tab:

  st.write(bd_fam_df['VARIABLE_NAME'].unique())

