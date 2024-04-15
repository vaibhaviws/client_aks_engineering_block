# Install packages
from typing import Any
import pandas as pd
import numpy as np
from enum import Enum

from economics_package.economics_metrics import (
    get_capex,
    get_opex,
    get_lcox,
    get_feedstock_availability,
    get_production,
    get_carbon_footprint,
    get_safety,
    get_trl,
    get_layout,
)
from src.utilities import Archetypes


def economics_calculator(
    general_user_inputs: dict,
    engineering_outputs: dict,
    job_data: dict,
    start_date: float,
    wacc_real: float,
    choices: dict[int, dict],
) -> dict[str, float]:

    values = {}

    for arc in job_data.archetypes:
        if arc == Archetypes.OFFSHORE_WIND:
            capex = get_capex(
                job_data=job_data,
                general_user_inputs=general_user_inputs,
                engineering_outputs=engineering_outputs,
                wacc_real=wacc_real,
            )
            values["capex"] = capex
            opex = get_opex(
                job_data=job_data,
                general_user_inputs=general_user_inputs,
                engineering_outputs=engineering_outputs,
                start_date=start_date,
            )
            values["opex"] = opex
            production = get_production(
                general_user_inputs=general_user_inputs,
                engineering_outputs=engineering_outputs,
                job_data=job_data,
                start_date=start_date,
            )
            values["production"] = get_production(
                general_user_inputs=general_user_inputs,
                engineering_outputs=engineering_outputs,
                job_data=job_data,
                start_date=start_date,
            )
            values["LCOX"] = get_lcox(capex=capex, opex=opex, production=production)
            values["feedstock_availability"] = get_feedstock_availability()
            values["schedule"] = general_user_inputs["in_phasing"][0]
            values["trl"] = get_trl(job_data=job_data, engineering_outputs=engineering_outputs)
            values["layout"] = get_layout(job_data=job_data, engineering_outputs=engineering_outputs)
            values["carbon_footprint"] = get_carbon_footprint()
            values["safety"] = get_safety()

        if arc == Archetypes.SOLAR:
            pass

    return values
