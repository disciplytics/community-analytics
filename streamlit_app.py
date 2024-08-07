import streamlit as st

# connect to snowflake
conn = st.connection("snowflake")

# get the list of CBSAs for the user
cbsa_default = conn.query('SELECT GEO_NAME FROM CBSA_DATA_GEO_NAMES ORDER BY GEO_NAME ASC LIMIT 1', ttl=0)

# add CBSA filter to a session variable
st.session_state['cbsa_selection'] = cbsa_default

home_page = st.Page(
  'home_page/home_page.py', title = 'Home', icon=":material/home:", default=True
)

# demographics pages
population = st.Page(
  'demographics/population.py', title = 'Population Report', icon=":material/groups:"
)

race_ethnicity = st.Page(
  'demographics/race_ethnicity.py', title = 'Race Report', icon=":material/diversity_1:"
)

age = st.Page(
  'demographics/age.py', title = 'Age Report', icon=":material/flare:"
)

# socioeconomics pages
income = st.Page(
  'socioeconomics/income.py', title = 'Income Report', icon=":material/payments:"
)

poverty = st.Page(
  'socioeconomics/poverty.py', title = 'Poverty Report', icon=":material/money_off:"
)


pg = st.navigation(
        {
            " ": [home_page],
            "Demographics": [population, race_ethnicity, age],
            "Socioeconomics": [income, poverty],
        }
    )

pg.run()
