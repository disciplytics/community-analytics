import streamlit as st
import pandas as pd
from census_elt.load_census import load_acs_data
import requests

from census import Census

c = Census(st.secrets["acs_key"])

def get_acs_data(state_fips, csa_code=None, msa_code=None, year=2022, survey="acs5", variables=None):
    """
    Fetch ACS data by state → CSA → MSA/μSA.

    Args:
        state_fips (str): FIPS code of the state (e.g., "06" for California)
        csa_code (str, optional): Combined Statistical Area code (partial match allowed)
        msa_code (str, optional): Metropolitan/Micropolitan Statistical Area code (partial match allowed)
        year (int): ACS year
        survey (str): ACS survey ("acs5", "acs1", etc.)
        variables (list, optional): List of ACS variables to fetch, e.g., ["B01003_001E"] (total population)

    Returns:
        pandas.DataFrame: ACS data filtered by CSA/MSA
    """
    if variables is None:
        variables = ["NAME", "B01003_001E"]  # Default: geography name & total population

    # Fetch all MSAs/μSAs in the state
    data = c.acs5.state_msa(
        fields=variables,
        state_fips=state_fips,
        year=year
    )

    df = pd.DataFrame(data)

    # Filter by CSA if provided
    if csa_code:
        df = df[df['NAME'].str.contains(csa_code, case=False, na=False)]

    # Filter by MSA/μSA if provided
    if msa_code:
        df = df[df['NAME'].str.contains(msa_code, case=False, na=False)]

    return df

# Example usage:
# Get ACS total population for all MSAs in Ohio
df_ca = get_acs_data(state_fips="39")
st.dataframe(df_ca.head())



st.dataframe(
      load_acs_data(
          year=2023, 
          dataset="acs/acs5", 
          variables=["NAME", "B01001_001E"], 
          for_geo="zip code tabulation area:44883", 
          in_geo="state:*",
          api_key=st.secrets["acs_key"]
      )
)


def get_racial_breakdown(zipcode, year=2022, dataset="acs/acs5", api_key=None):
    """
    Get racial and ethnic demographic breakdown for a given ZIP Code (ZCTA).

    Returns a DataFrame with counts and percentages.
    """
    variables_race = [
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
    ]

    df = load_acs_data(
        year=year,
        dataset=dataset,
        variables=variables_race,
        for_geo=f"zip code tabulation area:{zipcode}",
        api_key=st.secrets["acs_key"]
    )

    # Convert to numeric
    for col in df.columns:
        if col not in ["NAME", "zip code tabulation area"]:
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
      get_racial_breakdown(
            zipcode=44883
            , year=2023
            , dataset="acs/acs5"
            , api_key=st.secrets["acs_key"]
            )
      )
