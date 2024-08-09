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
        x_clean = x.lstrip('Family Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |')
    elif x[:1] == 'H':
        x_clean = x.lstrip('Household Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |')
    elif x[:23] == 'Median Household Income':
        x_clean = x.lstrip('Median Household Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |')
    elif x[:21] == 'Median Family Income':
        x_clean = x.lstrip('Median Family Income In The Past 12 Months (In 2022 Inflation-Adjusted Dollars): Population |')
    return x_clean#.rstrip('5yr Estimate (2022)')
        
income_df['Measure'] = income_df['VARIABLE_NAME'].apply(var_cleaner)

st.dataframe(income_df)
