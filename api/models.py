import re
from typing import Dict

from pydantic import BaseModel, validator, Field


tag_name_pattern = "[a-z_]{3,15}"
tag_name_expression = re.compile(tag_name_pattern)


class TagInput(BaseModel):
    name: str = Field(
        ..., description="Tag name conforming to the regexp pattern '[a-z_]{3,15}'"
    )
    value: int = Field(..., description="A positive integer less than 10")

    @validator("name")
    def validate_name(cls, v):
        if not tag_name_expression.fullmatch(v):
            raise ValueError(f"Tag name must conform to {tag_name_pattern!r}")
        return v

    @validator("value")
    def validate_value(cls, v):
        if 1 <= v <= 9:
            return v
        else:
            raise ValueError("Count value must be an positive integer less than 10.")


class TagStats(BaseModel):
    __root__: Dict[str, int] = Field(
        ...,
        description="An object where each key is a tag name and each value is thea associated total count",
    )
