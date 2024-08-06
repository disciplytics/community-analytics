import streamlit as st

home_page = st.Page(
  'home_page/home_page.py', title = 'Home', icon=":material/home:", default=True
)

# demographics pages
population = st.Page(
  'demographics/population.py', title = 'Population Report', icon=":material/groups:"
)

race_ethnicity = st.Page(
  'demographics/race_ethnicity.py', title = 'Race and Ethnicity Report', icon=":material/diversity_1:"
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
            "Home Page": [home_page],
            "Demographics": [population, race_ethnicity, age],
            "Socioeconomics": [income, poverty],
        }
    )

pg.run()
