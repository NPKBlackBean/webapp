#!/bin/bash

# Check if tag is provided
if [ -z "$1" ]; then
  echo "Usage: ./run.sh <TAG>"
  exit 1
fi

TAG=$1

# Copy .env from database/docker to external
mkdir -p ./external
cp ../database/docker/.env ./external/

# Build the docker image
docker build -t "$TAG" .