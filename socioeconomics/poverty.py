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
race_poverty_df = race_poverty_df.replace({'VARIABLE_NAME': race_rename_dict})

# clean variables
race_poverty_df['Year'] = pd.to_datetime(race_poverty_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)

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

race_poverty_df_total = pd.pivot_table(race_poverty_df_total, index = 'Year', columns = 'VARIABLE_NAME', values = 'FIVE_YEAR_ESTIMATE', aggfunc='sum')

# calc poverty rate
race_poverty_df_total['Total Poverty Rate'] = race_poverty_df_total['Total Population In Poverty, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['American Indian and Alaska Native Alone Poverty Rate'] = race_poverty_df_total['In Poverty American Indian and Alaska Native Alone, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['Asian Alone Poverty Rate'] = race_poverty_df_total['In Poverty Asian Alone, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['Black or African American Alone Poverty Rate'] = race_poverty_df_total['In Poverty Black or African American Alone, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['Hispanic or Latino Poverty Rate'] = race_poverty_df_total['In Poverty Hispanic or Latino, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['Some Other Race Alone Poverty Rate'] = race_poverty_df_total['In Poverty Some Other Race Alone, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['Two or More Races Poverty Rate'] = race_poverty_df_total['In Poverty Two or More Races, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['White Alone Poverty Rate'] = race_poverty_df_total['In Poverty White Alone, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']
race_poverty_df_total['White Alone, Not Hispanic or Latino Poverty Rate'] = race_poverty_df_total['In Poverty White Alone, Not Hispanic or Latino, 5yr Estimate'] / race_poverty_df_total['Total, 5yr Estimate']

race_poverty_df_total = race_poverty_df_total.reset_index()
      
# agg data
race_poverty_df_total = pd.melt(race_poverty_df_total, 
                                    id_vars=['Year'], 
                                    value_vars=['Total Poverty Rate', 'American Indian and Alaska Native Alone Poverty Rate',
                                                'Asian Alone Poverty Rate', 'Black or African American Alone Poverty Rate',
                                                'Hispanic or Latino Poverty Rate', 'Some Other Race Alone Poverty Rate',
                                                'Two or More Races Poverty Rate', 'White Alone Poverty Rate', 'White Alone, Not Hispanic or Latino Poverty Rate'],
                                   var_name='Race', value_name='Rate')

race_poverty_df_total['Year'] = race_poverty_df_total['Year'].astype(str)
      
st.write('Overall Poverty Rate')
df1 = race_poverty_df_total[race_poverty_df_total['Race'] == 'Total Poverty Rate']
    
chart1 = alt.Chart(df1).mark_line().encode(
                x=alt.X('Year', sort = None),
                y=alt.Y('Rate').axis(format='%'))
      
st.altair_chart(chart1, use_container_width = True)

race_tab, age_tab = st.tabs(['Poverty By Race', 'Poverty By Age'])

with race_tab:

    total_pop_tab, by_race_tab = st.tabs(['Poverty Rate By Total Population', 'Poverty Rate By Each Race Total Population'])

    with total_pop_tab:
        st.write('Poverty Rate By Race')
        df2 = race_poverty_df_total[race_poverty_df_total['Race'] != 'Total Poverty Rate']
        chart2 = alt.Chart(df2).mark_line().encode(
            x=alt.X('Year', sort = None),
            y=alt.Y('Rate').axis(format='%'),
            color='Race:N')
      
        st.altair_chart(chart2, use_container_width = True)

    with by_race_tab:

        # calc pct for race
        race_cols = [
      'Total Population In Poverty, 5yr Estimate', 'Total, 5yr Estimate',
      'In Poverty American Indian and Alaska Native Alone, 5yr Estimate',
      'In Poverty Asian Alone, 5yr Estimate', 'In Poverty Black or African American Alone, 5yr Estimate', 
      'In Poverty Hispanic or Latino, 5yr Estimate', 'In Poverty Some Other Race Alone, 5yr Estimate',
      'In Poverty Two or More Races, 5yr Estimate', 'In Poverty White Alone, 5yr Estimate', 
      'In Poverty White Alone, Not Hispanic or Latino, 5yr Estimate', 
      'American Indian and Alaska Native Alone, 5yr Estimate', 'Asian Alone, 5yr Estimate', 
      'Black or African American Alone, 5yr Estimate', 'Hispanic or Latino, 5yr Estimate', 
      'Some Other Race Alone, 5yr Estimate', 'Two or More Races, 5yr Estimate',
      'White Alone, 5yr Estimate', 'White Alone, Not Hispanic or Latino, 5yr Estimate'
                 ]
    
        race_poverty_df_race = race_poverty_df[race_poverty_df['VARIABLE_NAME'].isin(race_cols)]

        race_poverty_df_race = pd.pivot_table(race_poverty_df_race, index = 'Year', columns = 'VARIABLE_NAME', values = 'FIVE_YEAR_ESTIMATE', aggfunc='sum')

        # calc poverty rate
        race_poverty_df_race['Total Poverty Rate'] = race_poverty_df_race['Total Population In Poverty, 5yr Estimate'] / race_poverty_df_race['Total, 5yr Estimate']
        race_poverty_df_race['American Indian and Alaska Native Alone Poverty Rate'] = race_poverty_df_race['In Poverty American Indian and Alaska Native Alone, 5yr Estimate'] / race_poverty_df_race['American Indian and Alaska Native Alone, 5yr Estimate']
        race_poverty_df_race['Asian Alone Poverty Rate'] = race_poverty_df_race['In Poverty Asian Alone, 5yr Estimate'] / race_poverty_df_race['Asian Alone, 5yr Estimate']
        race_poverty_df_race['Black or African American Alone Poverty Rate'] = race_poverty_df_race['In Poverty Black or African American Alone, 5yr Estimate'] / race_poverty_df_race['Black or African American Alone, 5yr Estimate']
        race_poverty_df_race['Hispanic or Latino Poverty Rate'] = race_poverty_df_race['In Poverty Hispanic or Latino, 5yr Estimate'] / race_poverty_df_race['Hispanic or Latino, 5yr Estimate']
        race_poverty_df_race['Some Other Race Alone Poverty Rate'] = race_poverty_df_race['In Poverty Some Other Race Alone, 5yr Estimate'] / race_poverty_df_race['Some Other Race Alone, 5yr Estimate']
        race_poverty_df_race['Two or More Races Poverty Rate'] = race_poverty_df_race['In Poverty Two or More Races, 5yr Estimate'] / race_poverty_df_race['Two or More Races, 5yr Estimate']
        race_poverty_df_race['White Alone Poverty Rate'] = race_poverty_df_race['In Poverty White Alone, 5yr Estimate'] / race_poverty_df_race['White Alone, 5yr Estimate']
        race_poverty_df_race['White Alone, Not Hispanic or Latino Poverty Rate'] = race_poverty_df_race['In Poverty White Alone, Not Hispanic or Latino, 5yr Estimate'] / race_poverty_df_race['White Alone, Not Hispanic or Latino, 5yr Estimate']

        race_poverty_df_race = race_poverty_df_race.reset_index()
      
        # agg data
        race_poverty_df_race = pd.melt(race_poverty_df_race, 
                                    id_vars=['Year'], 
                                    value_vars=['Total Poverty Rate', 'American Indian and Alaska Native Alone Poverty Rate',
                                                'Asian Alone Poverty Rate', 'Black or African American Alone Poverty Rate',
                                                'Hispanic or Latino Poverty Rate', 'Some Other Race Alone Poverty Rate',
                                                'Two or More Races Poverty Rate', 'White Alone Poverty Rate', 'White Alone, Not Hispanic or Latino Poverty Rate'],
                                   var_name='Race', value_name='Rate')

        race_poverty_df_race['Year'] = race_poverty_df_race['Year'].astype(str)
      
        st.write('Poverty Rate For Each Race By Total Population of Each Race')
        race_lc2 = alt.Chart(
            race_poverty_df_race[race_poverty_df_race['Race'] != 'Total Poverty Rate']).mark_line().encode(
            x=alt.X('Year', sort = None),
            y=alt.Y('Rate').axis(format='%'),
            color='Race:N')
      
        st.altair_chart(race_lc2, use_container_width = True)

with age_tab:
    # age_poverty etl
    age_poverty_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_POVERTY_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'" + "AND VARIABLE_NAME IN ('Poverty Status In The Past 12 Months By Age: Population | Total, 5yr Estimate', 'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Under 6 years, 5yr Estimate', 'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 6 to 11 years, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 12 to 17 years, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 18 to 59 years, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 60 to 74 years, 5yr Estimate','Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 75 to 84 years, 5yr Estimate', 'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 85 years and over, 5yr Estimate');"
    age_poverty_df = conn.query(age_poverty_sql, ttl=0)

    age_rename_dict = {
        'Poverty Status In The Past 12 Months By Age: Population | Total, 5yr Estimate': 'Total, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | Under 6 years, 5yr Estimate': 'In Poverty Under 6 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 6 to 11 years, 5yr Estimate': 'In Poverty 6 to 11 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 12 to 17 years, 5yr Estimate': 'In Poverty 12 to 17 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 18 to 59 years, 5yr Estimate': 'In Poverty 18 to 59 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 60 to 74 years, 5yr Estimate': 'In Poverty 60 to 74 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 75 to 84 years, 5yr Estimate': 'In Poverty 75 to 84 years, 5yr Estimate',
        'Poverty Status In The Past 12 Months By Age: Population | Income in the past 12 months below poverty level | 85 years and over, 5yr Estimate': 'In Poverty 85 years and over, 5yr Estimate'
  }

    # rename columns
    age_poverty_df = age_poverty_df.replace({'VARIABLE_NAME': age_rename_dict})

    # clean variables
    age_poverty_df['Year'] = pd.to_datetime(age_poverty_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)

    # pivot data
    age_poverty_df = pd.pivot_table(age_poverty_df, index = 'Year', columns = 'VARIABLE_NAME', values = 'FIVE_YEAR_ESTIMATE', aggfunc='sum')

    # calc poverty rate
    age_poverty_df['Under 6 years Poverty Rate'] = age_poverty_df['In Poverty Under 6 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['6 to 11 years Poverty Rate'] = age_poverty_df['In Poverty 6 to 11 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['12 to 17 years Poverty Rate'] = age_poverty_df['In Poverty 12 to 17 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['18 to 59 years Poverty Rate'] = age_poverty_df['In Poverty 18 to 59 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['60 to 74 years Poverty Rate'] = age_poverty_df['In Poverty 60 to 74 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['75 to 84 years Poverty Rate'] = age_poverty_df['In Poverty 75 to 84 years, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']
    age_poverty_df['85 years and over Poverty Rate'] = age_poverty_df['In Poverty 85 years and over, 5yr Estimate'] / age_poverty_df['Total, 5yr Estimate']

    age_poverty_df = age_poverty_df.reset_index()
      
    # agg data
    age_poverty_df = pd.melt(age_poverty_df, 
                                    id_vars=['Year'], 
                                    value_vars=['Under 6 years Poverty Rate','6 to 11 years Poverty Rate','12 to 17 years Poverty Rate',
                                                '18 to 59 years Poverty Rate', '60 to 74 years Poverty Rate', '75 to 84 years Poverty Rate',
                                                '85 years and over Poverty Rate'],
                                   var_name='Age Range', value_name='Rate')

    age_poverty_df['Year'] = age_poverty_df['Year'].astype(str)
      
    st.write('Poverty Rate By Age Range')
    age_lc = alt.Chart(
            age_poverty_df).mark_line().encode(
            x=alt.X('Year', sort = None),
            y=alt.Y('Rate').axis(format='%'),
            color='Age Range:N')
      
    st.altair_chart(age_lc, use_container_width = True)
