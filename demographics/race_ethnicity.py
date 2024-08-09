import streamlit as st
import pandas as pd
import numpy as np

st.title("Race Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")


# race etl
total_race_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_RACE_DATA WHERE VARIABLE_NAME <> 'Race: Population | Total, 5yr Estimate' AND CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
# get the total race
total_race_df = conn.query(total_race_sql, ttl=0)

# prep data
race_dict = {
  'Origin By Race: Population | Not Hispanic or Latino | White alone | Hispanic or Latino, 5yr Estimate': 'White', 
  'Origin By Race: Population | Hispanic or Latino | Hispanic or Latino, 5yr Estimate': 'Hispanic or Latino',
  'Origin By Race: Population | Not Hispanic or Latino | Some other race alone | Hispanic or Latino, 5yr Estimate': 'Other Race',
  'Origin By Race: Population | Not Hispanic or Latino | Native Hawaiian and Other Pacific Islander alone | Hispanic or Latino, 5yr Estimate': 'Native Hawaiian and Other Pacific Islander',
  'Origin By Race: Population | Not Hispanic or Latino | Black or African American alone | Hispanic or Latino, 5yr Estimate': 'Black or African American',
  'Origin By Race: Population | Not Hispanic or Latino | American Indian and Alaska Native alone | Hispanic or Latino, 5yr Estimate': 'American Indian and Alaska Native',
  'Origin By Race: Population | Not Hispanic or Latino | Asian alone | Hispanic or Latino, 5yr Estimate': 'Asian',
  'Origin By Race: Population | Not Hispanic or Latino | Two or more races | Hispanic or Latino, 5yr Estimate':'Two or More Races'
}
total_race_df['Race'] = total_race_df['VARIABLE_NAME'].copy()

total_race_df = total_race_df.replace({'Race': race_dict})

total_race_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(total_race_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)
total_race_df['Counts'] = total_race_df['FIVE_YEAR_ESTIMATE'].astype(int)

race_filter = st.multiselect('Filter Races Here', total_race_df['Race'].unique(),total_race_df['Race'].unique())
st.write('Race Trends')
  
st.bar_chart(
    data = total_race_df[total_race_df['Race'].isin(race_filter)],
    x = 'FIVE_YEAR_ESTIMATE_DATE',
    y = 'Counts',
    x_label = '5 Year Estimate Date',
    y_label = 'Total',
    color = 'Race',
    stack = False,
    use_container_width = True)
  
st.write(f"Race Breakdown For Year {total_race_df['FIVE_YEAR_ESTIMATE_DATE'].max()}")
  
st.bar_chart(
    data = total_race_df[(total_race_df['Race'].isin(race_filter)) & (total_race_df['FIVE_YEAR_ESTIMATE_DATE'] == total_race_df['FIVE_YEAR_ESTIMATE_DATE'].max())].sort_values(by=['Counts'], ascending = True),
    x = 'Race',
    y = 'Counts',
    y_label = 'Total',
    x_label = 'Race',
    #color = 'Race',
    #stack = False,
    horizontal=False,)

st.write(f"Race Breakdown Table For Year {total_race_df['FIVE_YEAR_ESTIMATE_DATE'].max()}")
st.dataframe(total_race_df[(total_race_df['Race'].isin(race_filter)) & (total_race_df['FIVE_YEAR_ESTIMATE_DATE'] == total_race_df['FIVE_YEAR_ESTIMATE_DATE'].max())][['Race', 'Counts']].sort_values(by=['Counts'], ascending = False).set_index(['Race']),
            use_container_width = True)
