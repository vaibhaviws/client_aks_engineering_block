# Install packages
import pandas as pd
import numpy as np


def get_capex(general_user_inputs, engineering_outputs, wacc_real, job_data):
    """Get capex for all the archetypes

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        job_data (dict): Contains all archetype and vendor data
        engineering_outputs (dict) : Contains all archetype engineering output
        wacc_real (float): weighted average cost of capital (adjusted for inflation)

    Returns:
        _float_: capex for all archetypes (net present value)
    """

    year = 2024
    lead_time = general_user_inputs["fid"] - year
    capex = 0

    for arc in job_data.archetypes:
        arc_engineering_outputs = engineering_outputs[arc]
        arc_capex = arc_engineering_outputs["capex"]
        for i in range(general_user_inputs["in_phasing"][0]):
            capex = capex + arc_capex * general_user_inputs["in_phasing"][1][i] / ((1 + wacc_real) ** (lead_time + i))

    return capex


def get_opex(general_user_inputs, engineering_outputs, job_data, start_date):
    """Get opex for all the archetypes

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        job_data (dict): Contains all archetype and vendor data
        engineering_outputs (dict) : Contains all archetype engineering output
        start_date (_type_): production start date

    Returns:
        _float_: opex for all archetypes (net present value)
    """

    year = 2024
    lead_time = start_date - year
    opex = 0

    for arc in job_data.archetypes:

        arc_engineering_outputs = engineering_outputs[arc]
        arc_opex = arc_engineering_outputs["opex"]
        # arc_stack_replacement_cost = arc_engineering_outputs["stack_replacement_cost"]
        # arc_stack_replacement_time = arc_engineering_outputs["stack_replacement_time"]

        for i in range(general_user_inputs["project_lifetime"]):
            opex = opex + arc_opex / ((1 + general_user_inputs["discount_rate"]) ** (lead_time + i))

            # if (arc_stack_replacement_cost == True) and ((i + 1) % arc_stack_replacement_time == 0):
            #     opex = opex + arc_stack_replacement_cost

    return opex


def get_production(general_user_inputs, engineering_outputs, job_data, start_date):
    """Get production for the project lifetime

    Args:
        general_user_inputs (dict): DUMMY general user inputs
        job_data (dict): Contains all archetype and vendor data
        engineering_outputs (dict) : Contains all archetype engineering output
        start_date (_type_): production start date

    Returns:
        _float_: production in monetary terms for all archetypes aggregated
    """
    year = 2024
    lead_time = start_date - year
    production = 0

    for arc in job_data.archetypes:
        arc_engineering_outputs = engineering_outputs[arc]
        arc_production = arc_engineering_outputs["production"]

        for i in range(general_user_inputs["project_lifetime"]):
            production = production + arc_production / (1 + general_user_inputs["discount_rate"] ** (lead_time + i))

    return production


def get_trl(job_data, engineering_outputs):
    """Gets the overall technological readiness level for all archtypes. Its is ASSUMED that a product is how we go about it

    Args:
        job_data (dict): Contains all archetype and vendor data
        engineering_outputs (dict) : Contains all archetype engineering output

    Returns:
        _float_: trl for all archtypes
    """
    trl = 1
    for arc in job_data.archetypes:
        arc_engineering_outputs = engineering_outputs[arc]
        arc_trl = arc_engineering_outputs["trl"]
        trl = trl * arc_trl
    return trl


def get_layout(job_data, engineering_outputs):
    """Gets the overall layout for all archetypes

    Args:
        job_data (dict): Contains all archetype and vendor data
        engineering_outputs (dict) : Contains all archetype engineering output

    Returns:
        _float_: total archetypes
    """
    layout = 0
    for arc in job_data.archetypes:
        arc_engineering_outputs = engineering_outputs[arc]
        arc_layout = arc_engineering_outputs["layout"]
        layout = layout + arc_layout
    return layout


def get_lcox(capex, opex, production):
    """Gets the overall LCOX for the set of srchetypes - question is whether we want to keep LCOH/lcoe separate?

    Args:
        capex (_float_): NPV capex of all archetypes
        opex (_float_): NPV opex of all archetypes
        production (_float_): NPV production(monetary) of all archetypes

    Returns:
        _float_: levelised cost of x
    """

    lcox = (capex + opex) / production
    return lcox


def get_feedstock_availability():
    pass


def get_safety():
    pass


def get_carbon_footprint():
    pass
