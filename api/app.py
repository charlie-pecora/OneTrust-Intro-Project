import logging

from fastapi import FastAPI, Response, Request

from . import database
from .models import TagInput, TagStats
from .config import app_settings


app = FastAPI(
    title="Intro Project",
    description="Endpoints for adding tag counts and retrieving tag total count statics",
    version="0.1.0",
    openapi_tags=[
        {"name": "health"},
        {"name": "tags", "description": "Keep track of tag counts."},
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
async def add_tag_count(request: Request, tag_input: TagInput):
    await database.db.increment_tag_total_count(tag_input.name, tag_input.value)
    logging.info(
        "tag write event",
        extra={
            "logging.googleapis.com/trace": get_logging_trace(request),
            "severity": "NOTICE",
            "data": {"tagInput": tag_input.dict()},
        },
    )


def get_logging_trace(request):
    trace = request.headers.get("X-Cloud-Trace-Context", "").split("/")[0]
    return f"projects/{app_settings.google_project_id}/traces/{trace}"
