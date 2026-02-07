#!/bin/bash
set -e

echo "Restarting CoolBeans from local images..."

NETWORK="coolbeans_net"

CONTAINERS=(
  react
  fastapi
  ros2
  grafana
  timescaledb
)

IMAGES=(
  kzmuda/coolbeans_frontend:latest
  kzmuda/coolbeans_backend:latest
  docker-ros2
  grafana/grafana:latest
  timescale/timescaledb:latest-pg16
)

### -----------------------
### Sanity checks
### -----------------------

for img in "${IMAGES[@]}"; do
  if ! docker image inspect "$img" >/dev/null 2>&1; then
    echo "❌ Missing local image: $img"
    exit 1
  fi
done

docker network inspect "$NETWORK" >/dev/null 2>&1 || \
  docker network create "$NETWORK"

### -----------------------
### Stop old containers
### -----------------------

for c in "${CONTAINERS[@]}"; do
  docker stop "$c" 2>/dev/null || true
  docker rm "$c" 2>/dev/null || true
done

### -----------------------
### Start services
### -----------------------

echo "Starting TimescaleDB..."
docker run -d \
  --name timescaledb \
  --network "$NETWORK" \
  --restart unless-stopped \
  -p 5432:5432 \
  -e POSTGRES_DB \
  -e POSTGRES_USER \
  -e POSTGRES_PASSWORD \
  timescale/timescaledb:latest-pg16

echo "Starting Grafana..."
docker run -d \
  --name grafana \
  --network "$NETWORK" \
  --restart unless-stopped \
  -p 3001:3000 \
  grafana/grafana:latest

echo "Starting ROS2..."
docker run -d \
  --name ros2 \
  --network "$NETWORK" \
  --restart unless-stopped \
  -p 1154:9090 \
  docker-ros2

echo "Starting FastAPI backend..."
docker run -d \
  --name fastapi \
  --network "$NETWORK" \
  --restart unless-stopped \
  -e POSTGRES_HOST=timescaledb \
  -e POSTGRES_DB \
  -e POSTGRES_USER \
  -e POSTGRES_PASSWORD \
  -e NODE_ENV \
  kzmuda/coolbeans_backend:latest

echo "Starting React frontend..."
docker run -d \
  --name react \
  --network "$NETWORK" \
  --restart unless-stopped \
  -p 1152:3000 \
  kzmuda/coolbeans_frontend:latest

echo
echo "CoolBeans Stack running:"
docker ps
