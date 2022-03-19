import re

from fastapi import FastAPI
from pydantic import BaseModel, validator

from . import database
from .logger import logger


app = FastAPI()


@app.on_event("startup")
def startup_event():
    database.db.create_collection("tags")


@app.get("/")
async def index():
    return {"msg": "ok"}


@app.get("/tags")
async def get_tag_stats():
    tag_data = database.db.get_all_documents_in_collection("tags")
    return {document.id: document.document.get("total_count") for document in tag_data}


tag_name_pattern = "[a-z_]{3,15}"
tag_name_expression = re.compile(tag_name_pattern)

class TagInput(BaseModel):
    name: str
    value: int

    @validator('name')
    def validate_name(cls, v):
        if not tag_name_expression.fullmatch(v):
            raise ValueError(f"Tag name must conform to {tag_name_pattern!r}")
        return v
    
    @validator('value')
    def validate_value(cls, v):
        if 1 <= v <= 9:
            return v
        else: raise ValueError("Count value must be an positive integer less than 10.")


@app.put("/tags", status_code=204)
async def add_tag_count(tag_input: TagInput):
    database.db.increment_tag_total_count(tag_input.name, tag_input.value)