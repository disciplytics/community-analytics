import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initialization
if 'cbsa_selection' not in st.session_state:
    st.session_state['cbsa_selection'] = 'Abbeville, Alabama'

st.title("Age Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")


# connect to snowflake
conn = st.connection("snowflake")

# rietl
ri_sql = "SELECT DISTINCT * FROM RELIGIOUS_POI WHERE CITY_STATE = " + f"'{st.session_state['cbsa_selection']}'"
ri_df = conn.query(ri_sql, ttl=0)


options = st.multiselect(
    "Select the Type(s) of Institution:",
    ri_df.CATEGORY_MAIN.unique(),
    ri_df.CATEGORY_MAIN.unique())

st.dataframe(ri_df.query('CATEGORY_MAIN==@options'))
