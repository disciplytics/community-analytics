import streamlit as st
from census_elt.load_census import load_acs_data

st.dataframe(
      load_acs_data(
          year=2023, 
          dataset="acs/acs5", 
          variables=["NAME", "B01001_001E"], 
          for_geo="zip code tabulation area:*", 
          in_geo="state:39",
          api_key=st.secrets["acs_key"]
      )
