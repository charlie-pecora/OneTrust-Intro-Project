from typing import Optional

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    db_type: str = "test"
    db_collection = "test_tags"
    google_project_id: str = "charlie-intro-project"

    class Config:
        env_nested_delimiter = "__"


app_settings = AppSettings()
