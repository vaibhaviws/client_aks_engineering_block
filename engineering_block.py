# Install packages
import pandas as pd
import numpy as np

# from economics_package.economics_calculator import get_metrics
from metrics import get_archetype_user_input, get_data

# Archetype packages
from archetypes.offshore_wind.offshore_wind import offshore_wind
from archetypes.green_hydrogen.green_hydrogen import green_hydrogen
from archetypes.pipelines.pipelines import pipelines
from archetypes.carbon_capture.carbon_capture import carbon_capture
from archetypes.ammonia.ammonia import ammonia
from archetypes.solar.solar import solar


def engineering_block(general_user_inputs: dict, job_data: dict, choices: dict[int, dict], wacc_real: float):
    """This block calls the relevant engineering blocks and gets the engineering output for economics calculator

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design
        wacc_real (float): weighted average cost of capital (adjusted for inflation)

    Returns:
        _dict_: Engineering output per archetype in a dictionary
    """
    archetypes = job_data.archetypes
    engineering_outputs = {}

    # DUMMY STRUCTURE engineering calc
    for arc in archetypes:
        archetype_user_input = get_archetype_user_input(arc)
        if arc == "OWF":
            wind_data = get_data("wind")
            engineering_outputs[f"{arc}"] = offshore_wind(
                wacc_real=wacc_real,
                general_user_inputs=general_user_inputs,
                archetype_user_input=archetype_user_input,
                choices=choices,
                job_data=job_data,
                wind_data=wind_data,
            )

        elif arc == "green_hydrogen":
            pass

    return engineering_outputs
