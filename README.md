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
This app is deployed using Docker in Google Cloud Run. The `deploy.sh` bash script contains the 
command used to build and run the application. Note that this requires installation and configuration
 of the gcloud cli with authentication to the proper project. It additionally requires population of 
 a file `prod_env.yaml` with key-value pairs of each required environment variable for deployment 
 (see Setup above)

The deployed API is accessible at the following endpoints:
 - GET Health: https://intro-project-api-7o34w67asq-uw.a.run.app/health
 - GET Tags: https://intro-project-api-7o34w67asq-uw.a.run.app/tags
 - PUT Tags: https://intro-project-api-7o34w67asq-uw.a.run.app/tags
 - Docs: https://intro-project-api-7o34w67asq-uw.a.run.app/docs

## Database Design
### Overview
The document database is set up to use a single collection. The collection contains 1 document for 
each tag name and uses the tag name as the document ID. Each document then simply has a key 
`total_count` and the corresponding integer value. 

### Considerations
1. Using the tag name as a document ID was a simple choice to simplify and improve performance of 
database lookups by tag name.
1. I decided to simply store the `total_count` value in the database, as there was no requirement to 
keep track of the individual count values provided to the API. If this was a requirement, I would 
have included both a `total_count` stored as an integer as well as a list of all values (perhaps with 
timestamps) provided to the API.
1. I used the firestore `Increment` transformation to add to a tag's total_count value in the 
API. This ensures that if concurrent requests try to increment the value of the same tag, there is no 
chance that one will overwrite the other.
1. The write performance of this API is really just limited by the write capacity of Firestore, which 
is 10k writes per second. The API itself can be horizontally scaled until the database becomes the 
bottleneck.
1. Read performance is a bit murkier. Each read query will scan the entire contents of the Firestore 
collection and return all of the results to users. Both pagination (for instance, only return 100 tag 
counts per request) and caching could improve the read performance of the API. If there were latency 
issues with read queries, then analysis would be necessary to determine the bottleneck.

## Logging
Stackdriver structured logs were implemented. This includes a log each time the 
write endpoint is used to increment a tag count. The log-based metric was then created to extract the 
tag name and value from each request. While these metrics can be aggregated, I found the google 
metrics explorer tool unintuitive (I could not figure out how to do a simple sum of extracted values 
aggregated by the tag label) and did not complete the visualization piece of the logging metric. 
In order to visualize this data, I would probably use a python or javascript visualization library 
to query the metric data and create a dashboard.
