# OneTrust-Intro-Project
Intro Project developing Python API to track tags

## Setup
For python dependency setup, create a virtual environment and run the following:

```
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

In order to create a deployment to Cloud Run, the following environment variables should 
be populated based on google cloud credentials:
```yaml
DB_TYPE: cloud
DB_COLLECTION: 
GOOGLE_APPLICATION_CREDENTIALS: 
GOOGLE_PRIVATE_KEY_ID: 
GOOGLE_PRIVATE_KEY: 
GOOGLE_CLIENT_ID: 
GOOGLE_CLIENT_EMAIL: 
GOOGLE_CLIENT_CERT_URL:
```
Note that the Google APIs for Firebase Firestore, Cloud Run, and Cloud Build all need to be enabled.

## Testing
With dev environment set up, run tests locally with 
```pytest tests```, or
```pytest tests -m "not database"```
to skip tests that require Firestore access.

## Formatting
All code is formatted with `black .`

## Deployment
This app is deployed using Docker in Google Cloud Run. The `deploy.sh` bash script contains the command used to build and run the application. Note that this requires installation and configuration of the gcloud cli with authentication to the proper project. It additionally requires population of a file `prod_env.yaml` with key-value pairs of each required environment variable for deployment (see Setup above)

## Design Considerations

