# Install packages
import pandas as pd


def get_number_of_turbines(
    general_user_inputs: dict, archetype_user_input: dict, job_data: dict, choices: dict[int, dict]
):
    """Calculates the number of turbines required based on the chosen turbine and required capacity

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design

    Returns:
        _float_: number of turbines
    """
    block_data = choices["44d5d149-ae06-4749-b308-a90c801a11ec"]
    for key, value in block_data.items():
        wtg_choice = key
        wtg_data = value

    number_of_turbines = archetype_user_input["capacity"] / wtg_data["ratedpower"]

    return number_of_turbines


def get_annual_production(
    general_user_inputs: dict, archetype_user_input: dict, job_data: dict, choices: dict[int, dict], wind_data: dict
):
    """Calculates the annual production of energy based on the turbines and wind profile

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design
        wind_data (dict): DUMMY wind profile (speed and density)

    Returns:
        _float_: energy produced per year
    """
    block_data = choices["44d5d149-ae06-4749-b308-a90c801a11ec"]
    for key, value in block_data.items():
        wtg_choice = key
        wtg_data = value

    wind_data = wind_data["sheet1"]
    concept_wind = wind_data[wind_data["country"] == job_data.country]
    hours_per_year = 365 * 22
    normalise = 100000
    annual_energy_production = (
        wtg_data["ratedpower"]
        * concept_wind["wind"][0]
        * concept_wind["airDensity"][0]
        * hours_per_year
        / normalise
        # * wtg_data["sweptArea"]
    )
    # production profile for the entire project lifetime.
    return annual_energy_production


def get_wtg_layout(number_of_turbines: float) -> float:
    """Calculate the footprint of the wind turbine unit

    Args:
        number_of_turbines (float): number of turbines

    Returns:
        float: area of the unit
    """
    dummy_area = 10  # m^sq
    wtg_layout = number_of_turbines * dummy_area
    return wtg_layout


def get_substructure_layout(
    general_user_inputs: dict, archetype_user_input: dict, job_data: dict, choices: dict[int, dict]
):
    """Calculates the footprint of the substruture, size and weight

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design

    Returns:
        _dict_: type, configuration, size and weight of the substructure
    """

    if archetype_user_input["water_depth"] > 60:
        substructure_type = "Floating"
        substructure_config = "Mooring"
        block_data = choices["4e89c80a-8dd8-4810-b285-755f345dafb3"]

        for key, value in block_data.items():
            mooring_key = key
            mooring_data = value

        substructure_size = mooring_data["weightpercsasize"]
        substructure_weight = mooring_data["weightpermeter"] * substructure_size

    else:
        substructure_type = "Bottom-fixed"
        substructure_config = "Substructure"
        block_data = choices["64c5eec0-9f91-43a4-a5d3-d8d9d4abb549"]

        for key, value in block_data.items():
            substructure_key = key
            substructure_data = value

        # substructure_length = concept_substructure['mooringSizeCSA']
        substructure_size = 10  # DUMMY
        substructure_weight = substructure_data["weightpermw"] * archetype_user_input["capacity"]

    return {
        "substructure_type": substructure_type,
        "substructure_config": substructure_config,
        "substructure_size": substructure_size,
        "substructure_weight": substructure_weight,
    }


def get_substation_layout(
    general_user_inputs: dict,
    archetype_user_input: dict,
    job_data: dict,
    choices: dict[int, dict],
    number_of_turbines: float,
):
    """Calculates the substation layout, capacity, number and weight

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design
        number_of_turbines (float): number of turbines

    Returns:
        _dict_: returns substation capacity, number of substations and the weight
    """

    block_data = choices["8f5dd5e6-9a73-4eac-843f-f0f856f1e79e"]
    for key, value in block_data.items():
        substation_key = key
        substation_data = value

    substation_capacity = substation_data["capacity"]
    number_of_substations = substation_capacity / number_of_turbines
    substation_weight = (
        number_of_substations
        * (substation_data["weighttopsidepermw"] + substation_data["weighthullpermw"])
        * substation_capacity
    )

    return {
        "substation_capacity": substation_capacity,
        "number_of_substations": number_of_substations,
        "substation_weight": substation_weight,
    }


def get_iac_layout(general_user_inputs: dict, archetype_user_input: dict, job_data: dict, choices: dict[int, dict]):
    """Get IAC layout - gets the number of IAC and weight

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design

    Returns:
        _dict_: number of the units and weight
    """

    block_data = choices["d94945e9-3d9f-4e04-b08c-bc9f73b2e543"]
    for key, value in block_data.items():
        iac_key = key
        iac_data = value

    number_of_iac = archetype_user_input["capacity"] / iac_data["ratedpower"]
    iac_weight = number_of_iac * iac_data["weightperkm"]

    return {"number_of_iac": number_of_iac, "iac_weight": iac_weight}


def get_export_cable(general_user_inputs: dict, archetype_user_input: dict, job_data: dict, choices: dict[int, dict]):
    """Get export cable layout - gets the number of export cable and weight

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        archetype_user_input (dict): DUMMY OWF specific user input
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design

    Returns:
        _dict_: number of the units and weight
    """
    block_data = choices["bf837696-47ee-45dd-ac14-cbf001dd76cf"]
    for key, value in block_data.items():
        ec_key = key
        ec_data = value

    number_of_ec = archetype_user_input["capacity"] / ec_data["ratedpower"]
    ec_weight = number_of_ec * ec_data["weightperkm"]

    return {"number_of_ec": number_of_ec, "ec_weight": ec_weight}


def get_trl(choices: dict[int, dict]):
    """Gets the TRL for the system. The trl has been assumed to be a sum of the individual TRL.
    This is probably wrong

    Args:
        choices (dict[int, dict]): Chosen project design

    Returns:
        _dict_: technology readiness level
    """

    trl = 0

    for key, value in choices.items():
        block_id = key
        block_data = value
        if "trlmaturity" in block_data:
            trl = trl + block_data["trlmaturity"]

    return {"trl": trl}
