# Install packages
import pandas as pd
import numpy as np

from archetypes.offshore_wind.offshore_wind_metrics import (
    get_number_of_turbines,
    get_annual_production,
    get_wtg_layout,
    get_substructure_layout,
    get_substation_layout,
    get_iac_layout,
    get_export_cable,
    get_trl,
)


def offshore_wind(
    wacc_real: float,
    general_user_inputs: dict,
    archetype_user_input: dict,
    choices: dict[int, dict],
    job_data: dict,
    wind_data,
):
    """Calculates the relevant design outputs for OWF archetype

    Args:
        wacc_real (float): weighted average cost of capital (adjusted for inflation)
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design
        wind_data (dict): DUMMY wind profile (speed and density)

    Returns:
        _dict_: layout, opex, capex, trl, stack_values, production
    """
    # Wind Turbine Generator
    number_of_turbines = get_number_of_turbines(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
    )

    annual_energy_production = get_annual_production(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
        wind_data=wind_data,
    )

    wtg_layout = get_wtg_layout(number_of_turbines=number_of_turbines)  # WTG layout

    # Sub-system substructure and mooring
    substructure = get_substructure_layout(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
    )
    # Substation
    substation = get_substation_layout(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
        number_of_turbines=number_of_turbines,
    )

    # IAC
    iac = get_iac_layout(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
    )

    # Export Cable
    ec = get_export_cable(
        general_user_inputs=general_user_inputs,
        archetype_user_input=archetype_user_input,
        job_data=job_data,
        choices=choices,
    )

    # Output calculation
    dummy_capex = 10
    dummy_opex = 1

    layout = wtg_layout + substructure["substructure_size"]
    # weight = substructure["substructure_weight"] + substation["substation_weight"] + iac["iac_weight"] + ec["ec_weight"]
    trl = get_trl(choices)["trl"]
    capex = dummy_capex * layout
    opex = dummy_opex * (archetype_user_input["capacity"] + substation["substation_capacity"])
    stack_replacement_cost = 0
    stack_replacement_time = 0

    return {
        "layout": layout,
        "capex": capex,
        "opex": opex,
        "trl": trl,
        "stack_replacement_cost": stack_replacement_cost,
        "stack_replacement_time": stack_replacement_time,
        "production": annual_energy_production,
    }
