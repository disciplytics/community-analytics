import streamlit as st
import pandas as pd
import numpy as np

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Income Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")

# income etl
income_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_INCOME_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
income_df = conn.query(income_sql, ttl=0)

# get the report year
report_year = pd.to_datetime(income_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int)

# clean variables
def var_cleaner(x):
    if x[:1] == 'F':
        return x.lstrip(f'Family Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars): Population |')
    elif x[:1] == 'H':
        return x.lstrip(f'Household Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars): Population |')
    elif x == f'Median Family Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars): Population | Median family income in the past 12 months (in {report_year} inflation-adjusted dollars), 5yr Estimate ({report_year})':
        return 'Median Family Income In The Past 12 Months'
    elif x == f'Median Household Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars) By Household Size: Population | Total, 5yr Estimate ({report_year})':
        return 'Median Household Income In The Past 12 Months'
        
income_df['Measure'] = income_df['VARIABLE_NAME'].apply(var_cleaner)

st.dataframe(income_df)
