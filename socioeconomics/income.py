import streamlit as st
import pandas as pd
import numpy as np

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Income Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")
st.write('Household and Family Incomes')


# connect to snowflake
conn = st.connection("snowflake")

# income etl
income_sql = "SELECT GEO_NAME, VARIABLE_NAME, DATE as Five_Year_Estimate_Date, VALUE as Five_Year_Estimate FROM CBSA_INCOME_DATA WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
income_df = conn.query(income_sql, ttl=0)

# get the report year
report_year = pd.to_datetime(income_df['FIVE_YEAR_ESTIMATE_DATE']).dt.year.astype(int).max()

# clean variables
def var_cleaner(x):
    if x[:1] == 'F':
        return x.lstrip(f'Family Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars): Population |')
    elif x[:1] == 'H':
        return x.lstrip(f'Household Income In The Past 12 Months (In {report_year} Inflation-Adjusted Dollars): Population |')
    elif 'Median Family Income' in x:
        return f'Median Family Income In The Past 12 Months, 5yr Estimate ({report_year})'
    elif 'Median Household Income' in x:
        return f'Median Household Income In The Past 12 Months, 5yr Estimate ({report_year})'
        
income_df['Measure'] = income_df['VARIABLE_NAME'].apply(var_cleaner)

# get category
def get_cat(x):
    if 'Family' in x:
        return 'Family'
    elif 'Household' in x
        return 'Household'

income_df['Category'] = income_df['VARIABLE_NAME'].apply(get_cat)




household_tab, family_tab = st.tabs(['Household Income', 'Family Income'])

st.dataframe(income_df)
