import streamlit as st
  
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

edu_voc = st.Page(
  'socioeconomics/education.py', title = 'Educational Attainment Report', icon=":material/school:"
)

poverty = st.Page(
  'socioeconomics/poverty.py', title = 'Poverty Report', icon=":material/money_off:"
)

#social_assist = st.Page(
#  'socioeconomics/social_assistance.py', title = 'Social Assitance Report', icon=":material/bento:"
#)

poi_ri = st.Page(
  'poi/religious_institutions.py', title = 'Religious Institutions Report', icon=":material/church:"
)


pg = st.navigation(
        {
            " ": [home_page],
            "Demographics": [population, race_ethnicity, age],
            "Socioeconomics": [income, edu_voc, poverty],
            "Religious Institutions": [poi_ri]
        }
    )

pg.run()
