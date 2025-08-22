import streamlit as st
import pandas as pd
from census_elt.load_census import load_acs_data
import requests

# --- State FIPS lookup table ---
STATE_FIPS = {
    "AL": "01", "Alabama": "01",
    "AK": "02", "Alaska": "02",
    "AZ": "04", "Arizona": "04",
    "AR": "05", "Arkansas": "05",
    "CA": "06", "California": "06",
    "CO": "08", "Colorado": "08",
    "CT": "09", "Connecticut": "09",
    "DE": "10", "Delaware": "10",
    "DC": "11", "District of Columbia": "11",
    "FL": "12", "Florida": "12",
    "GA": "13", "Georgia": "13",
    "HI": "15", "Hawaii": "15",
    "ID": "16", "Idaho": "16",
    "IL": "17", "Illinois": "17",
    "IN": "18", "Indiana": "18",
    "IA": "19", "Iowa": "19",
    "KS": "20", "Kansas": "20",
    "KY": "21", "Kentucky": "21",
    "LA": "22", "Louisiana": "22",
    "ME": "23", "Maine": "23",
    "MD": "24", "Maryland": "24",
    "MA": "25", "Massachusetts": "25",
    "MI": "26", "Michigan": "26",
    "MN": "27", "Minnesota": "27",
    "MS": "28", "Mississippi": "28",
    "MO": "29", "Missouri": "29",
    "MT": "30", "Montana": "30",
    "NE": "31", "Nebraska": "31",
    "NV": "32", "Nevada": "32",
    "NH": "33", "New Hampshire": "33",
    "NJ": "34", "New Jersey": "34",
    "NM": "35", "New Mexico": "35",
    "NY": "36", "New York": "36",
    "NC": "37", "North Carolina": "37",
    "ND": "38", "North Dakota": "38",
    "OH": "39", "Ohio": "39",
    "OK": "40", "Oklahoma": "40",
    "OR": "41", "Oregon": "41",
    "PA": "42", "Pennsylvania": "42",
    "RI": "44", "Rhode Island": "44",
    "SC": "45", "South Carolina": "45",
    "SD": "46", "South Dakota": "46",
    "TN": "47", "Tennessee": "47",
    "TX": "48", "Texas": "48",
    "UT": "49", "Utah": "49",
    "VT": "50", "Vermont": "50",
    "VA": "51", "Virginia": "51",
    "WA": "53", "Washington": "53",
    "WV": "54", "West Virginia": "54",
    "WI": "55", "Wisconsin": "55",
    "WY": "56", "Wyoming": "56",
    "PR": "72", "Puerto Rico": "72",
}


def load_hud_crosswalk(url="https://www.huduser.gov/portal/datasets/usps/ZIP_COUNTY_122024.csv"):
    """Load HUD ZIP-to-County crosswalk file, including weights."""
    df = pd.read_csv(url, dtype=str)
    df["RES_RATIO"] = pd.to_numeric(df["RES_RATIO"], errors="coerce")
    return df[["ZIP", "STATE", "COUNTY", "RES_RATIO"]].drop_duplicates()

def get_county_lookup(year=2023):
    """Get county FIPS -> name mapping from Census API."""
    url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME&for=county:*"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["STATEFP"] = df["state"]
    df["COUNTYFP"] = df["county"]
    df["FIPS"] = df["STATEFP"].str.zfill(2) + df["COUNTYFP"].str.zfill(3)
    return df.set_index("FIPS")["NAME"].to_dict()

def get_racial_breakdown_by_state(state, year=2023, dataset="acs/acs5", api_key=None,
                                  crosswalk_url="https://www.huduser.gov/portal/datasets/usps/ZIP_COUNTY_122024.csv",
                                  long_format=False, include_county=True):
    """Get racial breakdown per ZIP, split proportionally across counties using HUD RES_RATIO."""
    # Normalize state input
    if state in STATE_FIPS:
        state_fips = STATE_FIPS[state]
    elif state.zfill(2) in STATE_FIPS.values():
        state_fips = state.zfill(2)
    else:
        raise ValueError(f"Invalid state input: {state}")

    # HUD crosswalk
    crosswalk = load_hud_crosswalk(crosswalk_url)
    crosswalk = crosswalk[crosswalk["STATE"] == state_fips]

    variables_race = [
        "NAME",
        "B02001_001E", "B02001_002E", "B02001_003E", "B02001_004E",
        "B02001_005E", "B02001_006E", "B02001_007E", "B02001_008E",
        "B03003_003E",
    ]

    # ACS data for all ZCTAs
    base_url = f"https://api.census.gov/data/{year}/{dataset}"
    params = {"get": ",".join(variables_race), "for": "zip code tabulation area:*"}
    if api_key:
        params["key"] = api_key
    r = requests.get(base_url, params=params)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert numeric
    for col in df.columns:
        if col not in ["NAME", "zip code tabulation area"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rename columns
    rename_map = {
        "B02001_001E": "Total", "B02001_002E": "White", "B02001_003E": "Black",
        "B02001_004E": "American Indian/Alaska Native", "B02001_005E": "Asian",
        "B02001_006E": "Native Hawaiian/Pacific Islander", "B02001_007E": "Some Other Race",
        "B02001_008E": "Two or More Races", "B03003_003E": "Hispanic/Latino",
    }
    df = df.rename(columns=rename_map)

    # Merge ACS ZIP data with crosswalk to assign counties
    df = df.merge(crosswalk, left_on="zip code tabulation area", right_on="ZIP", how="left")
    
    # Apply RES_RATIO to split counts across counties
    for col in rename_map.values():
        df[col] = df[col] * df["RES_RATIO"]

    # Compute percentages per ZIP+County
    df["Total (%)"] = 100
    for col in rename_map.values():
        if col != "Total":
            df[f"{col} (%)"] = (df[col] / df["Total"] * 100).round(2)

    # Map county names
    county_lookup = get_county_lookup(year)
    df["County Name"] = (df["STATE"].str.zfill(2) + df["COUNTY"].str.zfill(3)).map(county_lookup)

    # Select / reorder columns
    cols = ["zip code tabulation area", "NAME", "STATE", "COUNTY", "County Name", "Total"] + \
           [c for c in rename_map.values()] + [f"{c} (%)" for c in rename_map.values() if c != "Total"]
    df = df[cols]

    if long_format:
        id_vars = ["zip code tabulation area", "NAME", "STATE", "COUNTY", "County Name", "Total"]
        value_vars = [c for c in df.columns if c not in id_vars]
        long_df = df.melt(id_vars=id_vars, value_vars=value_vars,
                          var_name="Race/Category", value_name="Value")
        long_df["Metric"] = long_df["Race/Category"].apply(lambda x: "%" if "(%)" in x else "Count")
        long_df["Race/Category"] = long_df["Race/Category"].str.replace(" (%)", "", regex=False)
        long_df = long_df.pivot_table(
            index=["zip code tabulation area", "NAME", "STATE", "COUNTY", "County Name", "Race/Category", "Total"],
            columns="Metric", values="Value"
        ).reset_index()
        return long_df

    return df.reset_index(drop=True)


# Wide format, counties weighted
df_wide = get_racial_breakdown_by_state("OH", api_key=st.secrets["acs_key"], long_format=False)
st.dataframe(df_wide.head())

# Long format, ready for plotting
df_long = get_racial_breakdown_by_state("OH", api_key=st.secrets["acs_key"], long_format=True)
st.dataframe(df_long.head(20))


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
