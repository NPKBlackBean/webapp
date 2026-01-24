#!/bin/bash

# Script to pull and run the complete CoolBeans application stack
set -e

echo "🚀 CoolBeans Application Deployment Script"
echo "=========================================="

# Change to the docker directory
cd "$(dirname "$0")"

echo "📦 Pulling latest Docker images..."
docker pull kzmuda/coolbeans_backend:latest
docker pull kzmuda/coolbeans_frontend:latest
docker pull timescale/timescaledb:latest-pg16
docker pull grafana/grafana:latest

echo "🛑 Stopping existing containers..."
docker-compose down

echo "🗂️  Removing old volumes (optional - comment out to keep data)"
# docker volume rm docker_timescale_data docker_grafana_data 2>/dev/null || true

echo "🚀 Starting all services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your services:"
echo "  • Frontend: http://localhost:${REACT_PORT:-3001}"
echo "  • Backend API: http://localhost:${FASTAPI_PORT:-8000}"
echo "  • Grafana: http://localhost:${GRAFANA_PORT:-3000}"
echo "    - Username: ${GRAFANA_USER:-admin}"
echo "    - Password: ${GRAFANA_PASSWORD:-admin123}"
echo "  • TimescaleDB: localhost:${POSTGRES_PORT:-5432}"
echo ""
echo "📋 To view logs:"
echo "  docker-compose logs -f [service_name]"
echo ""
echo "🛑 To stop all services:"
echo "  docker-compose down"