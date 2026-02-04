#!/bin/bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_DIR="$SCRIPT_DIR/docker"

echo "Restarting Docker Compose CoolBeans services..."

cd "$DOCKER_DIR"

docker-compose pull
docker-compose up -d
docker-compose ps