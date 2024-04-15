# Install packages
import pandas as pd
import numpy as np


def get_general_user_inputs():
    """TODO: How do we get this information?
    User inputs from project setup
    Returns:
        country (str)           : Project country
        currency (str)          : Currency in which the project evaluation will be done?
        wacc_nominal (float)    : Nominal weighted average cost of capital
        inflation_rate (float)  : Inflation rate for the region
        fid (float)             : Financial Investment Decision date
        in_phasing (tuple)      : In-phasing period and distribution
        project_lifetime (float): Expected lifetime of the project
        archetype (str)         : Project archtype selected by user
    """

    wacc_nominal = 0.08
    inflation_rate = 0.02
    fid = 2026
    in_phasing = (3, (0.1, 0.5, 0.4))
    project_lifetime = 25
    discount_rate = 0.02

    return {
        "wacc_nominal": wacc_nominal,
        "inflation_rate": inflation_rate,
        "fid": fid,
        "in_phasing": in_phasing,
        "project_lifetime": project_lifetime,
        "discount_rate": discount_rate,
    }


def get_archetype_user_input(archetype):
    """TODO: How do we get this information?
    User inputs - archetype specific
    Here we'll have to set it up in such a way that given a desired project location (coordinates):
        - we can get the water depth and distance to shore
        - right now set up for offshore_wind
    Returns (EXPECTED: NOT USING ALL NOW):
        water_depth (float)         : The water depth at the desired location
        project_area (float)        : The desired project area
        capacity (float)            : The desire capacity of the project (in MW)
        distance_from_shore (float) : Based on the coordinates
    """
    if "OWF" in archetype:
        offshore_wind_input = {"water_depth": 60, "project_area": 100, "capacity": 100, "distance_from_shore": 100}
        return offshore_wind_input
    if "green_hydrogen" in archetype:
        green_hydrogen_input = {
            "placeholder1": 10,
            "placeholder2": 10,
        }
        return green_hydrogen_input


def get_data(archetype):
    file_name = "data/dummy_" + archetype + ".xlsx"
    xl = pd.read_excel(file_name, sheet_name=None, index_col=0)

    # empty dictionary
    dfs = {}

    for sheet_name, df in xl.items():
        dfs[sheet_name] = df

    return dfs


def get_start_date(fid_date: float, in_phasing_years: float) -> float:
    """TODO: recheck the start_date formula
    Evaluates the start date of the project
    Args:
        fid (float)             : Financial Investment Decision date
        in_phasing_years (float): In-phasing period
    Returns:
        start_date(float)       : start date of the project
    """
    start_date = fid_date + in_phasing_years + 1
    return start_date


def get_wacc_real(wacc_nominal: float, inflation_rate: float) -> float:
    """TODO: recheck the formula
    Evaluates the weighted average cost of capital adjusted for inflation
    Args:
        wacc_nominal (float)    : Nominal weighted average cost of capital
        inflation_rate (float)  : Inflation rate for the region
    Returns:
        wacc_real (float)       : Real weighted average cost of capital
    """
    wacc_real = (1 + wacc_nominal) / (1 + inflation_rate) - 1
    return wacc_real
