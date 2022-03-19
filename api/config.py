from typing import Optional

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    database_config: Optional[str] = None

    class Config:
        env_nested_delimiter = "__"


app_settings = AppSettings()
