import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Educational Attainment Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")

# connect to snowflake
conn = st.connection("snowflake")

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
