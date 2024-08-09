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
    elif 'Household' in x:
        return 'Household'
income_df['Category'] = income_df['VARIABLE_NAME'].apply(get_cat)

# rename metric col
income_df = income_df.rename(columns = {'FIVE_YEAR_ESTIMATE': 'Population'})

# subset dfs
hh_df = income_df[income_df['Category'] == 'Household']
fam_df = income_df[income_df['Category'] == 'Family']

# reindx df
hh_df = hh_df.set_index(['Measure'])
hh_df = hh_df.reindex([
    f'Median Household Income In The Past 12 Months, 5yr Estimate ({report_year})',
    f'Less than $10,000, 5yr Estimate ({report_year})',
    f'$10,000 to $14,999, 5yr Estimate ({report_year})',
    f'$15,000 to $19,999, 5yr Estimate ({report_year})',
    f'$20,000 to $24,999, 5yr Estimate ({report_year})',
    f'$25,000 to $29,999, 5yr Estimate ({report_year})',
    f'$30,000 to $34,999, 5yr Estimate ({report_year})',
    f'$35,000 to $39,999, 5yr Estimate ({report_year})',
    f'$40,000 to $44,999, 5yr Estimate ({report_year})',
    f'$45,000 to $49,999, 5yr Estimate ({report_year})',
    f'$50,000 to $59,999, 5yr Estimate ({report_year})',
    f'$60,000 to $74,999, 5yr Estimate ({report_year})',
    f'$75,000 to $99,999, 5yr Estimate ({report_year})',
    f'$100,000 to $124,999, 5yr Estimate ({report_year})',
    f'$125,000 to $149,999, 5yr Estimate ({report_year})',
    f'$150,000 to $199,999, 5yr Estimate ({report_year})',
    f'$200,000 or more, 5yr Estimate ({report_year})',]).reset_index()

# reindx df
fam_df = fam_df.set_index(['Measure'])
fam_df = fam_df.reindex([
    f'Median Family Income In The Past 12 Months, 5yr Estimate ({report_year})',
    f'Less than $10,000, 5yr Estimate ({report_year})',
    f'$10,000 to $14,999, 5yr Estimate ({report_year})',
    f'$15,000 to $19,999, 5yr Estimate ({report_year})',
    f'$20,000 to $24,999, 5yr Estimate ({report_year})',
    f'$25,000 to $29,999, 5yr Estimate ({report_year})',
    f'$30,000 to $34,999, 5yr Estimate ({report_year})',
    f'$35,000 to $39,999, 5yr Estimate ({report_year})',
    f'$40,000 to $44,999, 5yr Estimate ({report_year})',
    f'$45,000 to $49,999, 5yr Estimate ({report_year})',
    f'$50,000 to $59,999, 5yr Estimate ({report_year})',
    f'$60,000 to $74,999, 5yr Estimate ({report_year})',
    f'$75,000 to $99,999, 5yr Estimate ({report_year})',
    f'$100,000 to $124,999, 5yr Estimate ({report_year})',
    f'$125,000 to $149,999, 5yr Estimate ({report_year})',
    f'$150,000 to $199,999, 5yr Estimate ({report_year})',
    f'$200,000 or more, 5yr Estimate ({report_year})',]).reset_index()

# get metrics
hh_metric = hh_df[hh_df['Measure'] == f'Median Household Income In The Past 12 Months, 5yr Estimate ({report_year})']['Population']
fam_metric = fam_df[fam_df['Measure'] == f'Median Family Income In The Past 12 Months, 5yr Estimate ({report_year})']['Population']

# get range tables
hh_df = hh_df[hh_df['Measure'] != f'Median Household Income In The Past 12 Months, 5yr Estimate ({report_year})']
fam_df = fam_df[fam_df['Measure'] != f'Median Family Income In The Past 12 Months, 5yr Estimate ({report_year})']

# select needed cols
household_tab, family_tab = st.tabs(['Household Income', 'Family Income'])

with household_tab:
    col1_met, col1_table = st.columns([0.3, 0.7])
    col1_met.metric(hh_metric)
    col1_table.dataframe(hh_df)

with family_tab:
    col2_met, col2_table = st.columns([0.3, 0.7])
    col2_met.metric(fam_metric)
    col2_table.dataframe(fam_df)
