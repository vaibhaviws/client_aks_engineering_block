from datetime import datetime
from io import StringIO
from enum import Enum
import pickle
from pathlib import Path
from typing import Any, Union
from munch import Munch, munchify
from pprint import pprint
from src.data_io.job_data import JobData


def unpack_tuple(tup: tuple) -> tuple:
    """Unpacks a tuple of the form (number, (a, b, c)) into two separate values.
    Args:
        tup (tuple): Tuple of the form (number, (a, b, c))
    Returns:
        tuple: Two separate values - the number and the tuple (a, b, c)
    """
    number, inner_tuple = tup
    return number, inner_tuple


def get_choices(file_path: str) -> dict:

    with open(file_path, "rb") as f:
        choices = pickle.load(f)

    arc_choices = {}
    # Process choice data
    for key, option_data in choices.items():

        name = option_data.name
        properties = option_data.properties
        block_uuid = option_data.block_uuid

        properties_dict = {prop_name: prop_value.value for prop_name, prop_value in properties.items()}
        option_dict = {name: properties_dict}
        if block_uuid not in arc_choices:
            arc_choices[block_uuid] = {}
            arc_choices[block_uuid].update(option_dict)

    return arc_choices


def load_job_data_from_file(input_file: Union[str, Path]) -> Munch:
    """Load job data from file path and return the job data

    Args:
        input_file (str | Path): input file path

    Returns:
        Munch: job data
    """
    input_file = Path(input_file)

    with input_file.open() as f:
        file_data = Munch.fromJSON(f.read())

    job_data = JobData(**file_data)

    return job_data


class Archetypes(str, Enum):
    OFFSHORE_WIND = "OWF"
    SOLAR = "solar"
    GREEN_HYDROGEN = "green_hydrogen"
    AMMONIA = "ammonia"
    CARBON_CAPTURE = "carbon_capture"
    PIPELINES = "pipelines"
    BLUE_HYDROGEN = "blue_hydrogen"
    CARBON_LIQUEFACTION = "carbon_liquefaction"
