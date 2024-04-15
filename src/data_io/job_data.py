from itertools import groupby
from typing import Any

from munch import munchify
from pydantic import BaseModel, ConfigDict, Field


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(extra='ignore')


class PropertyData(CustomBaseModel):
    name: str
    value: Any
    si_unit: str | None


class ConversionData(CustomBaseModel):
    from_value: float
    from_unit: str
    to_value: float
    to_unit: str


class ConversionCategoryData(CustomBaseModel):
    conversions: list[ConversionData]


class DriverData(CustomBaseModel):
    objective: bool
    metric: bool
    properties: dict[str, PropertyData] = Field(..., description="key=property name")


class ParameterCategoryData(CustomBaseModel):
    parameters: dict[str, PropertyData] = Field(..., description="key=parameter name")


class ParameterArchetypeData(CustomBaseModel):
    categories: dict[str, ParameterCategoryData] = Field(..., description="key=category name")


class OptionData(CustomBaseModel):
    id: int
    name: str
    choice_id: int
    block_uuid: str
    properties: dict[str, PropertyData] = Field(..., description="key=property name")
    tags: dict[str, list[str]] = Field(..., description="key=tag category")


class ChoiceData(CustomBaseModel):
    id: int
    name: str
    block_uuid: str
    options: dict[int, OptionData] = Field(..., description="key=option id")


class ConnectionData(CustomBaseModel):
    connection_type: str
    block_uuid: str


class PriorPropertyData(CustomBaseModel):
    block_uuid: str
    prior_id: int
    sequence: int
    property: str
    weight: float


class PriorData(CustomBaseModel):
    id: int
    block_uuid: str
    aggregation: str
    driver_id: int
    driver_name: str
    properties: list[PriorPropertyData]


class BlockData(CustomBaseModel):
    uuid: str
    name: str
    choices: dict[int, ChoiceData] = Field(..., description="key=choice id")
    parameters: dict[str, PropertyData] = Field(..., description="key=parameter name")
    input_connections: list[ConnectionData]
    output_connections: list[ConnectionData]
    priors: dict[str, PriorData] = Field(..., description="key=driver name")


class OptionConstraintData(CustomBaseModel):
    type: str
    options: list[int] = Field(..., description="comment=list of option ids")


class JobData(CustomBaseModel):
    engine_job_id: int
    engine_type: str
    algorithm: str
    currency: str
    country: str
    region: str
    project_id: int
    project_name: str
    archetypes: list[str]
    conversions: dict[str, ConversionCategoryData] = Field(..., description="key=conversion category")
    drivers: dict[str, DriverData] = Field(..., description="key=driver name")
    parameters: dict[str, ParameterArchetypeData] = Field(..., description="key=archetype name")
    blocks: dict[str, BlockData] = Field(..., description="key=block uuid")
    option_constraints: list[OptionConstraintData]

    def __init__(self, **data):
        data["country"] = data["project"]["country"]
        data["region"] = data["project"]["region"]
        data["project_id"] = data["project"]["pk"]
        data["project_name"] = data["project"]["name"]
        data["archetypes"] = data["project"]["archetypes"]
        data["conversions"] = self._transform_conversions(data["project"]["conversions"])
        data["drivers"] = self._transform_drivers(data["project"]["drivers"])
        data["parameters"] = self._transform_parameters(data["project"]["parameters"])
        data["currency"] = data["parameters"]["default"]["categories"]["Financials"]["parameters"] \
            .pop("default_financials_project_currency")["value"]
        data["blocks"] = self._transform_blocks(data["project"])
        data["option_constraints"] = self._transform_option_constraints(data["project"]["option_constraints"])

        super().__init__(**data)

    @classmethod
    def get_schema(cls) -> dict:
        def process_schema(schema):
            if "$ref" in schema:
                ref = schema["$ref"].split("/")[-1]
                return process_schema(json_schema["$defs"][ref])

            if "required" in schema:
                result = {}
                for name in schema.required:
                    child_schema = schema.properties[name]
                    child_description = child_schema.get("description", "")
                    if "comment=" in child_description:
                        comment = f" ({child_description.lstrip('comment=')})"
                    else:
                        comment = ""
                    result[f"{name}{comment}"] = process_schema(child_schema)
                return result

            else:
                if "anyOf" in schema:
                    schema.type = "|".join([x.type for x in schema.anyOf])
                elif "type" not in schema:
                    schema.type = "any"

                match schema.type:
                    case "object":
                        key = schema.description.lstrip("key=")
                        return {f"<{key}>": process_schema(schema.additionalProperties)}
                    case "array":
                        return [process_schema(schema["items"]), "..."]
                    case _:
                        return f"[{schema.type}]".strip()

        json_schema = munchify(cls.model_json_schema())

        return process_schema(json_schema)

    def _transform_conversions(self, conversion_data: list) -> dict[str, Any]:
        conversion_data.sort(key=lambda x: x["category"])
        return {
            category: {"conversions": list(group)}
            for category, group in groupby(conversion_data, key=lambda x: x["category"])
        }

    def _transform_drivers(self, driver_data: list) -> dict[str, Any]:
        drivers = {x["name"]: x for x in driver_data}
        for driver in drivers.values():
            driver["properties"] = {x["name"]: x for x in driver["properties"]}
        return drivers

    def _transform_parameters(self, parameter_data: list) -> dict[str, Any]:
        parameter_data.sort(key=lambda x: (x["archetype"] or "default", x["category"]))
        parameters = {
            archetype: {
                "categories": {
                    category: {
                        "parameters": {
                            parameter["name"]: parameter
                            for parameter in group
                        }
                    }
                    for category, group in groupby(archetype_group, key=lambda x: x["category"])
                }
            }
            for archetype, archetype_group in groupby(parameter_data, key=lambda x: x["archetype"] or "default")
        }
        return parameters

    def _transform_blocks(self, project_data: dict[str, Any]) -> dict[str, Any]:
        block_data = project_data["blocks"]
        connection_data = project_data["connections"]
        driver_names = {x["id"]: x["name"] for x in project_data["drivers"]}

        by_from_block_uuid = lambda x: x["from_block_uuid"]
        output_connections = {
            from_block_uuid: [
                {
                    "connection_type": x["connection_type"],
                    "block_uuid": x["to_block_uuid"]
                }
                for x in group
            ]
            for from_block_uuid, group in groupby(
                sorted(connection_data, key=by_from_block_uuid), key=by_from_block_uuid
            )
        }
        by_to_block_uuid = lambda x: x["to_block_uuid"]
        input_connections = {
            to_block_uuid: [
                {
                    "connection_type": x["connection_type"],
                    "block_uuid": x["from_block_uuid"]
                }
                for x in group
            ]
            for to_block_uuid, group in groupby(
                sorted(connection_data, key=by_to_block_uuid), key=by_to_block_uuid
            )
        }

        by_group = lambda x: x["group"]
        blocks = {
            block["uuid"]: {
                **block,
                "choices": {
                    choice["id"]: {
                        **choice,
                        "block_uuid": block["uuid"],
                        "options": {
                            option["id"]: {
                                **option,
                                "choice_id": choice["id"],
                                "block_uuid": block["uuid"],
                                "properties": {
                                    property["name"]: property
                                    for property in option["properties"]
                                },
                                "tags": {
                                    category: [x["name"] for x in group]
                                    for category, group in groupby(
                                        sorted(option["tags"], key=by_group), key=by_group
                                    )
                                }
                            }
                            for option in choice["options"]
                        }
                    }
                    for choice in block["choices"]
                },
                "parameters": {
                    parameter["name"]: parameter
                    for parameter in block["parameters"]
                },
                "input_connections": output_connections.get(block["uuid"], []),
                "output_connections": input_connections.get(block["uuid"], []),
                "priors": {
                    driver_names[prior["driver"]]: {
                        **prior,
                        "block_uuid": block["uuid"],
                        "driver_id": prior["driver"],
                        "driver_name": driver_names[prior["driver"]],
                        "properties": sorted([
                            {
                                **property,
                                "block_uuid": block["uuid"],
                                "prior_id": prior["id"],
                            }
                            for property in prior["properties"]
                        ], key=lambda x: x["sequence"])
                    }
                    for prior in block["priors"]
                }
            }
            for block in block_data
        }
        return blocks

    def _transform_option_constraints(self, option_constraint_data: list) -> list:
        option_constraints = [
            {
                "type": option_constraint["type"],
                "options": [x["option"] for x in option_constraint["options"]]
            }
            for option_constraint in option_constraint_data
        ]
        return option_constraints