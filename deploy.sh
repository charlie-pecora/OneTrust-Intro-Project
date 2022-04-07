#!/bin/sh

gcloud run deploy --project charlie-intro-project --source . \
--env-vars-file ./prod_env.yaml --region us-west1 --port 8000 intro-project-api
