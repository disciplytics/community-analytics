import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Education and Vocation Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")

# connect to snowflake
conn = st.connection("snowflake")

edu_tab, voc_tab = st.tabs(['Educational Attainment', 'Vocations'])


with edu_tab:
    st.write('Educational Attainment For The Population 25 to 64 Years Old')
    # education etl
    education_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_EDUCATION_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
    education_df = conn.query(education_sql, ttl=0)

    def clean_edu(x):
        if x == "Educational Attainment By Employment Status For The Population 25 To 64 Years: Population | Some college or associate's degree, 5yr Estimate":
            return "Some College or Associate's Degree"
        elif x == "Educational Attainment By Employment Status For The Population 25 To 64 Years: Population | Less than high school graduate, 5yr Estimate":
            return "Less Than High School Graduate"
        elif x == "Educational Attainment By Employment Status For The Population 25 To 64 Years: Population | High school graduate (includes equivalency), 5yr Estimate":
            return "High School Graduate or Equivalent"
        elif x == "Educational Attainment By Employment Status For The Population 25 To 64 Years: Population | Bachelor's degree or higher, 5yr Estimate":
            return "Bachelor's Degree of Higher"

    # clean variables
    education_df['Educational Attainment'] = education_df['VARIABLE_NAME'].apply(clean_edu)
    education_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(education_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)
    # create table report
    edu_table_df = pd.pivot_table(education_df, index = 'Educational Attainment', columns = 'FIVE_YEAR_ESTIMATE_DATE', values = 'FIVE_YEAR_ESTIMATE', aggfunc = 'sum').fillna(0)
    # reindex
    edu_table_df = edu_table_df.reindex([
        "Less Than High School Graduate",
        "High School Graduate or Equivalent",
        "Some College or Associate's Degree",
        "Bachelor's Degree of Higher"])

    # line chart
    lc_df = education_df[education_df['Educational Attainment'].isnull()==False]
    lc_df['Year'] = lc_df['FIVE_YEAR_ESTIMATE_DATE'].astype(str)
    lc_df['Population'] = lc_df['FIVE_YEAR_ESTIMATE'].copy()
    st.line_chart(lc_df, x = 'Year', y = 'Population', color = 'Educational Attainment')

    # table view
    edu_table_df = education_df.sort_values(by=['FIVE_YEAR_ESTIMATE_DATE'])
    edu_table_df['PCT_CHANGE'] = edu_table_df['FIVE_YEAR_ESTIMATE'].pct_change()
    # drop nan from pct change
    edu_table_df = edu_table_df.dropna()
    # format the pct change and count
    edu_table_df['Percent Change'] = np.round(edu_table_df['PCT_CHANGE']*100,2).astype(str)+"%"
    edu_table_df['Count'] = edu_table_df['FIVE_YEAR_ESTIMATE'].astype(int)
    # rename VARIABLE_NAME
    edu_table_df['Measure'] = 'Total Population'

    ## Get Year
    edu_table_df['FIVE_YEAR_ESTIMATE_DATE'] = pd.to_datetime(edu_table_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)

    # change calcs to rows
    edu_table_df = pd.melt(edu_table_df, id_vars = ['Measure', 'FIVE_YEAR_ESTIMATE_DATE'], value_vars = ['Count', 'Percent Change'])
    edu_table_df = edu_table_df.pivot(
    values = 'value', 
    index = ['Measure', 'variable'], 
    columns = 'FIVE_YEAR_ESTIMATE_DATE')

    # reorder df
    edu_table_df = edu_table_df.sort_index(level = 0, ascending=False)
    st.dataframe(edu_table_df)
