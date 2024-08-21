import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Poverty Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")

# connect to snowflake
conn = st.connection("snowflake")

race_tab, age_tab, household_tab = st.tabs(['Poverty By Race', 'Poverty By Age', 'Poverty by Household Type'])

with race_tab:
  # race_poverty etl
  race_poverty_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_POVERTY_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'" + "AND VARIABLE_NAME IN ('Poverty Status In The Past 12 Months By Age: Population | Total | American Indian and Alaska Native Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | Asian Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | Black or African American Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | Hispanic or Latino, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | Some Other Race Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | Two or More Races, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | White Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total | White Alone, Not Hispanic or Latino, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Total, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | American Indian and Alaska Native Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Asian Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Black or African American Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Hispanic or Latino, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Some Other Race Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Two or More Races, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | White Alone, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | White Alone, Not Hispanic or Latino, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level, 5yr Estimate');"
  race_poverty_df = conn.query(race_poverty_sql, ttl=0)

  race_rename_dict = {
'Poverty Status In The Past 12 Months By Age: Population | Total | American Indian and Alaska Native Alone, 5yr Estimate' : 'American Indian and Alaska Native Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | Asian Alone, 5yr Estimate': 'Asian Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | Black or African American Alone, 5yr Estimate': 'Black or African American Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | Hispanic or Latino, 5yr Estimate': 'Hispanic or Latino, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | Some Other Race Alone, 5yr Estimate': 'Some Other Race Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | Two or More Races, 5yr Estimate': 'Two or More Races, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | White Alone, 5yr Estimate': 'White Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total | White Alone, Not Hispanic or Latino, 5yr Estimate': 'White Alone, Not Hispanic or Latino, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Total, 5yr Estimate': 'Total, 5yr Estimate',

'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | American Indian and Alaska Native Alone, 5yr Estimate': 'In Poverty American Indian and Alaska Native Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Asian Alone, 5yr Estimate': 'In Poverty Asian Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Black or African American Alone, 5yr Estimate': 'In Poverty Black or African American Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Hispanic or Latino, 5yr Estimate': 'In Poverty Hispanic or Latino, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Some Other Race Alone, 5yr Estimate': 'In Poverty Some Other Race Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Two or More Races, 5yr Estimate': 'In Poverty Two or More Races, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | White Alone, 5yr Estimate': 'In Poverty White Alone, 5yr Estimate',
'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | White Alone, Not Hispanic or Latino, 5yr Estimate': 'In Poverty White Alone, Not Hispanic or Latino, 5yr Estimate',

'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level, 5yr Estimate': 'Total Population In Poverty, 5yr Estimate'
  }

  # rename columns
  race_poverty_df = race_poverty_df.rename(columns=race_rename_dict)

  # clean variables
  race_poverty_df['Year'] = pd.to_datetime(race_poverty_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)
  
  total_pop_tab, by_race_tab = st.tabs(['Poverty Rate By Total Population', 'Poverty Rate By Race Total Population'])

  with total_pop_tab:

    # calc pct for total
    total_cols = [
      'Total Population In Poverty, 5yr Estimate', 'Total, 5yr Estimate',
      'In Poverty American Indian and Alaska Native Alone, 5yr Estimate',
      'In Poverty Asian Alone, 5yr Estimate', 'In Poverty Black or African American Alone, 5yr Estimate', 
      'In Poverty Hispanic or Latino, 5yr Estimate', 'In Poverty Some Other Race Alone, 5yr Estimate',
      'In Poverty Two or More Races, 5yr Estimate', 'In Poverty White Alone, 5yr Estimate', 
      'In Poverty White Alone, Not Hispanic or Latino, 5yr Estimate',
                 ]
    
    race_poverty_df_total = race_poverty_df[race_poverty_df['VARIABLE_NAME'].isin(total_cols)]

    race_poverty_df_total = race_poverty_df_total.pivot(index = 'Year', columns = 'VARIABLE_NAME', values = 'FIVE_YEAR_ESTIMATE')

    st.table(race_poverty_df_total)




# create table report
edu_table_df = pd.pivot_table(education_df, index = 'Educational Attainment', columns = 'FIVE_YEAR_ESTIMATE_DATE', values = 'FIVE_YEAR_ESTIMATE', aggfunc = 'sum').fillna(0)
# reindex
edu_table_df = edu_table_df.reindex([
        "Less Than High School Graduate",
        "High School Graduate or Equivalent",
        "Some College or Associate's Degree",
        "Bachelor's Degree of Higher"])

# line chart
st.subheader('Educational Attainment Trends')
lc_df = education_df[education_df['Educational Attainment'].isnull()==False]
lc_df['Year'] = lc_df['FIVE_YEAR_ESTIMATE_DATE'].astype(str)
lc_df['Population'] = lc_df['FIVE_YEAR_ESTIMATE'].copy()
st.line_chart(lc_df, x = 'Year', y = 'Population', color = 'Educational Attainment')


st.dataframe(edu_table_df, use_container_width=True)

# percent diff plot
lc_df2 = education_df[education_df['Educational Attainment'].isnull()==False]
lc_df2['Year'] = lc_df2['FIVE_YEAR_ESTIMATE_DATE'].astype(int)
lc_df2['Population'] = lc_df2['FIVE_YEAR_ESTIMATE'].copy()
lc_df_report_pct_diff = lc_df2[lc_df2['Year'] >= lc_df2['Year'].max()-1]

lc_df_report_pct_diff = lc_df_report_pct_diff.groupby(['Educational Attainment', 'Year'])['Population'].sum().reset_index()

lc_df_report_pct_diff = lc_df_report_pct_diff.sort_values(by = ['Year'], ascending = True)

lc_df_report_pct_diff['% Change In Last 2 Years'] = np.round(lc_df_report_pct_diff.sort_values('Year').groupby(['Educational Attainment']).Population.pct_change(),2)

lc_df_report_pct_diff = lc_df_report_pct_diff.dropna()

pctdiff_lc = alt.Chart(lc_df_report_pct_diff).mark_line().encode(
    x=alt.X('Educational Attainment', sort = None),
    y=alt.Y('% Change In Last 2 Years').axis(format='%')
)

st.write('Percent Change in Population Over the Last Two Years')
st.altair_chart(pctdiff_lc, use_container_width = True)
