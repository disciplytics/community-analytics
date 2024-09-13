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

ri_df['LATITUDE'] = pd.to_numeric(ri_df['LATITUDE'])
ri_df['LONGITUDE'] = pd.to_numeric(ri_df['LONGITUDE'])

ri_df = ri_df.rename(columns={
    'CATEGORY_MAIN': 'Type',
    'CITY_STATE': 'Location',
    'POI_NAME': 'Institution'
})

options = st.multiselect(
    "Select the Type(s) of Institution:",
    ri_df.Type.unique(),
    ri_df.Type.unique())


df = ri_df.query('Type==@options')

col1, col2 = st.columns([.6,.4])
col1.dataframe(df[['Type', 'Institution']].set_index(['Type']).sort_index())

def display_map(location_data:pd.DataFrame):

    fig = px.scatter_mapbox(location_data, lat="LATITUDE", lon="LONGITUDE", zoom=12, 
                            hover_name='Institution', hover_data=['Type', 'Institution'])

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
col2.plotly_chart(display_map(df))


