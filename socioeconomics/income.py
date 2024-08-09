import streamlit as st

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

# clean variables
def var_cleaner(x):
    if x[:1] == 'F':
        return x.lstrip('Family Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |').rstrip(', 5yr Estimate (2022)')
    elif x[:1] == 'H':
        return x.lstrip('Household Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |').rstrip(', 5yr Estimate (2022)')
    elif x == 'Median Family Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population | Median family income in the past 12 months (in 2022 inflation-adjusted dollars), 5yr Estimate (2022)':
        return 'Median Family Income In The Past 12 Months'
    elif x == 'Median Household Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars) By Household Size: Population | Total, 5yr Estimate (2022)':
        return 'Median Household Income In The Past 12 Months'
        
income_df['Measure'] = income_df['VARIABLE_NAME'].apply(var_cleaner)

st.dataframe(income_df)
