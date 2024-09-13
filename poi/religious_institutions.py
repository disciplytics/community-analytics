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

ri_df = ri_df.rename(columns={
    'CATEGORY_MAIN': 'Type',
    'CITY_STATE': 'Location',
    'POI_NAME': 'Institution'})

options = st.multiselect(
    "Select the Type(s) of Institution:",
    ri_df.Type.unique(),
    ri_df.Type.unique())


df = ri_df.query('Type==@options')

col1, col2 = st.columns([.35,.65])
col1.dataframe(df[['Institution']].set_index(['Institution']), use_container_width=True)

col2.map(data=df, latitude='LATITUDE', longitude='LONGITUDE', use_container_width=True)


