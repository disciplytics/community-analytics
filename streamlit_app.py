import streamlit as st

st.title('Community Analytics')
st.subheader('An app to better understand your neighbors...')



# demographics pages
population = st.Page(
  'demographics/population.py', title = 'Population Report', icon=":material/groups:", default=True
)

race_ethnicity = st.Page(
  'demographics/race_ethnicity.py', title = 'Race and Ethnicity Report', icon=":material/diversity_1:", default=True
)

age = st.Page(
  'demographics/age.py', title = 'Age Report', icon=":material/flare:", default=True
)

# socioeconomics pages
income = st.Page(
  'socioeconomics/income.py', title = 'Income Report', icon=":material/payments:", default=True
)

poverty = st.Page(
  'socioeconomics/poverty.py', title = 'Poverty Report', icon=":material/money_off:", default=True
)


pg = st.navigation(
        {
            "Demographics": [population, race_ethnicity, age],
            "Socioeconomics": [income, poverty],
        }
    )

pg.run()
