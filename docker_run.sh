#!/bin/sh

docker build . -t intro-project
docker kill intro-project
docker rm intro-project
docker run --name intro-project -p 8000:8000 -d intro-project
