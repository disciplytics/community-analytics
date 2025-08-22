import requests
import pandas as pd

def load_acs_data(year=2023, dataset="acs/acs5", variables=["NAME", "B01001_001E"], 
                  for_geo="county:*", in_geo="state:39", api_key=None):
    """
    Load ACS data from the U.S. Census Bureau API.

    Parameters:
    - year (int): Year of ACS dataset (default: 2023).
    - dataset (str): ACS dataset, e.g., "acs/acs5" or "acs/acs1".
    - variables (list): List of variable codes (default: total population).
    - for_geo (str): Geography to pull data for (default: all counties).
    - in_geo (str): Higher-level geography filter (default: state:39 for Ohio).
    - api_key (str): Your Census API key (get one free at https://api.census.gov/data/key_signup.html).

    Returns:
    - pd.DataFrame: ACS data
    """
    base_url = f"https://api.census.gov/data/{year}/{dataset}"
    params = {
        "get": ",".join(variables),
        "for": for_geo,
        "in": in_geo
    }
    if api_key:
        params["key"] = api_key

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df
