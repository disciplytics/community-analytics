import streamlit as st
import pandas as pd
from census_elt.load_census import get_racial_breakdown
from census import Census
from us import states

st.dataframe(
        get_racial_breakdown('OH', year=2023, dataset="acs/acs5", api_key=st.secrets["acs_key"])
      )
