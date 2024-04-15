# Import packages
from typing import Any
import pandas as pd
import numpy as np
from enum import Enum
from src.data_io.job_data import JobData

# Import functions and utilities
from engineering_block import engineering_block
from economics_package.economics_calculator import economics_calculator
from metrics import get_general_user_inputs, get_start_date, get_wacc_real
from src.utilities import get_choices, load_job_data_from_file, Archetypes

# OBTAIN DATA - TEST
option_file = "src/example_concept.pickle"
dummy_choices = get_choices(option_file)

job_data_file = "src/local_project_9_default_2_input.json"
dummy_job_data = load_job_data_from_file(job_data_file)


def get_metrics(choices: dict[int, dict], job_data: dict):
    """Engine interface to call for relevant economic metrics

    Args:
        job_data (dict): Contains all archetype and vendor data
        choices (dict[int, dict]): Chosen project design

    Returns:
        _dict_: returns a dictionary of metrics and values - aggregated for all archetypes
    """
    general_user_inputs = get_general_user_inputs()

    # PRE-EVALUATION metrics
    start_date = get_start_date(general_user_inputs["fid"], general_user_inputs["in_phasing"][0])
    wacc_real = get_wacc_real(general_user_inputs["wacc_nominal"], general_user_inputs["inflation_rate"])

    engineering_outputs = engineering_block(
        general_user_inputs=general_user_inputs, job_data=job_data, choices=choices, wacc_real=wacc_real
    )

    economics_outputs = economics_calculator(
        general_user_inputs=general_user_inputs,
        engineering_outputs=engineering_outputs,
        job_data=job_data,
        start_date=start_date,
        wacc_real=wacc_real,
        choices=choices,
    )

    return economics_outputs


# out = get_metrics(choices=dummy_choices, job_data=dummy_job_data)
# print(out)
