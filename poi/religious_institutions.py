import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

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

col1, col2 = st.columns([.6,.4])
col1.dataframe(df[['Type', 'Institution']].set_index(['Type']).sort_index())

fig = px.scatter_map(df, lat="LATITUDE", lon="LONGITUDE", color="Institution")

plot_spot = st.empty()
with plot_spot:
    col2.plotly_chart(fig, use_container_width=True)


