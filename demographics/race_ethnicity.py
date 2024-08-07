import streamlit as st
import pandas as pd
import numpy as np

st.title("Race and Ethnicity Report:")
st.subheader(f"{st.session_state['cbsa_selection']}")
