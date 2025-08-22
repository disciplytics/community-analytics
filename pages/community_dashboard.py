import streamlit as st
from census_elt.load_census import load_acs_data

st.dataframe(load_acs_data(api_key=st.secrets["acs_key"]))
