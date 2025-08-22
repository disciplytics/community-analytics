import streamlit as st
from census_elt.load_census import load_acs_data

st.dataframe(
      load_acs_data(
          year=2023, 
          dataset="acs/acs5", 
          variables=["NAME", "B01001_001E"], 
          for_geo="zip code tabulation area:44883", 
          in_geo="state:39",
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
        for_geo=f"ZCTA:{zipcode}",
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
