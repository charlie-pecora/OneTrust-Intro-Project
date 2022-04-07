from typing import Optional
import os
from pathlib import Path
import json

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    db_type: str = "test"
    db_collection = "test_tags"
    google_project_id: str = "charlie-intro-project"

    class Config:
        env_nested_delimiter = "__"


app_settings = AppSettings()


def write_credentials_file():
    if "GOOGLE_PRIVATE_KEY_ID" in os.environ:
        with open(
            Path(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]), "w", encoding="utf8"
        ) as f:
            s = json.dumps(
                {
                    "type": "service_account",
                    "project_id": app_settings.google_project_id,
                    "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
                    "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace(
                        "\\n", "\n"
                    ),
                    "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
                    "client_id": os.environ["GOOGLE_CLIENT_ID"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.environ["GOOGLE_CLIENT_CERT_URL"],
                },
                indent=2,
            )
            f.write(s)


write_credentials_file()
