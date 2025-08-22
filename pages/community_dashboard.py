import streamlit as st
import pandas as pd
from census_elt.load_census import load_acs_data
import requests

from census import Census
from us import states

racial_vars = (
        "NAME",
        "B02001_001E",  # Total
        "B02001_002E",  # White
        "B02001_003E",  # Black
        "B02001_004E",  # American Indian/Alaska Native
        "B02001_005E",  # Asian
        "B02001_006E",  # Native Hawaiian/Pacific Islander
        "B02001_007E",  # Some other race
        "B02001_008E",  # Two or more races
        "B03003_003E",  # Hispanic/Latino
)


st.write(pd.json_normalize(c.acs5.state(racial_vars, states.OH.fips, year=2023)))


def get_racial_breakdown(state, year=2023, dataset="acs/acs5", api_key=None):
    """
    Get racial and ethnic demographic breakdown for a given State.

    Returns a DataFrame with counts and percentages.
    """

    c = Census(api_key)
        
    variables_race = (
        "NAME",
        "B02001_001E",  # Total
        "B02001_002E",  # White
        "B02001_003E",  # Black
        "B02001_004E",  # American Indian/Alaska Native
        "B02001_005E",  # Asian
        "B02001_006E",  # Native Hawaiian/Pacific Islander
        "B02001_007E",  # Some other race
        "B02001_008E",  # Two or more races
        "B03003_003E",  # Hispanic/Latino
    )

    df = pd.json_normalize(c.acs5.state(variables_race, f'states.{state}.fips', year=year))

    # Convert to numeric
    for col in df.columns:
        if col not in ["NAME"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rename columns to human-readable labels
    rename_map = {
        "B02001_001E": "Total",
        "B02001_002E": "White",
        "B02001_003E": "Black",
        "B02001_004E": "American Indian/Alaska Native",
        "B02001_005E": "Asian",
        "B02001_006E": "Native Hawaiian/Pacific Islander",
        "B02001_007E": "Some Other Race",
        "B02001_008E": "Two or More Races",
        "B03003_003E": "Hispanic/Latino",
    }
    df = df.rename(columns=rename_map)

    total = df["Total"].iloc[0]

    # Compute percentages
    for col in rename_map.values():
        if col != "Total":
            df[f"{col} (%)"] = (df[col] / total * 100).round(2)

    return df

st.dataframe(
        get_racial_breakdown('OH, year=2023, dataset="acs/acs5", api_key=st.secrets["acs_key"])
      )
