import pandas as pd
from census import Census
from us import states

def get_racial_breakdown(state, year=2023, dataset="acs/acs5", api_key=None):
    """
    Get racial and ethnic demographic breakdown for a given State.

    Returns a DataFrame with counts and percentages.
    """

    c = Census(api_key, year=year)
        
    variables_race = (
        "NAME",
        "DP05_0037PE", # White alone, percent
        "DP05_0037M", # White alone, percent MoE
        "DP05_0037PEA",
        "DP05_0037PMA",
        
        "DP05_0038PE", #Black or African American alone, percent
        "DP05_0038M", #Black or African American alone, percent MoE
        
        "DP05_0039PE", #American Indian and Alaska Native alone, percent
        "DP05_0039M", #American Indian and Alaska Native alone, percent MoE
        
        "DP05_0047PE", #Asian alone, percent    
        "DP05_0047M", #Asian alone, percent MoE
        
        "DP05_0055PE", #Native Hawaiian and Other Pacific Islander alone, percent
        "DP05_0055M", #Native Hawaiian and Other Pacific Islander alone, percent MoE

        "DP05_0060PE", #Some other race alone, percent
        "DP05_0060M", #Some other race alone, percent MoE
        
        "DP05_0061PE", #Two or more races, percent
        "DP05_0061M", #Two or more races, percent MoE
        
        "DP05_0076PE", #Hispanic or Latino (of any race), percent
        "DP05_0076M", #Hispanic or Latino (of any race), percent MoE
        
        "DP05_0081PE",  #Not Hispanic or Latino, percent
        "DP05_0081M"  #Not Hispanic or Latino, percent MoE
    )

    #df = pd.json_normalize(c.acs5st.state(variables_race, states.OH.fips, year=year))

    df = pd.json_normalize(c.acs5dp.get(variables_race, geo={'for': 'county:*',
                       'in': 'state:{}'.format(states.OH.fips)}))

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

    #total = df["Total"].iloc[0]

    # Compute percentages
    #for col in rename_map.values():
    #    if col != "Total":
    #        df[f"{col} (%)"] = (df[col] / total * 100).round(2)

    return df
