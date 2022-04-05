import re

from fastapi import FastAPI, Response

from . import database
from .models import TagInput, TagStats
from .logger import logger


app = FastAPI(
    title="Intro Project",
    description="Endpoints for adding tag counts and retrieving tag total count statics",
    version="0.1.0",
    openapi_tags=[
        {"name": "health"},
        {"name": "tags", "description": "Endpionts for keeping track of tag counts."},
    ],
)


@app.get("/health", tags=["health"])
async def health():
    return {"msg": "ok"}


@app.get("/tags", tags=["tags"], response_model=TagStats)
async def get_tag_stats():
    tag_stats = {}
    async for tag in database.db.get_all_tags():
        tag_stats[tag.name] = tag.total_count
    return tag_stats


@app.put("/tags", tags=["tags"], status_code=204, response_class=Response)
async def add_tag_count(tag_input: TagInput):
    await database.db.increment_tag_total_count(tag_input.name, tag_input.value)
