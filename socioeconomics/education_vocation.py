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
        
    st.line_chart(education_df, x = 'FIVE_YEAR_ESTIMATE_DATE', y = 'FIVE_YEAR_ESTIMATE', color = 'Educational Attainment')
    
    st.dataframe(edu_table_df)
