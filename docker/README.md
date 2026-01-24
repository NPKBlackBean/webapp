# CoolBeans Docker Deployment Guide

This guide shows you how to deploy the complete CoolBeans application stack using Docker images.

## Quick Start

1. **Clone/download this repository** (or just the `docker/` folder)

2. **Run the deployment script:**
   ```bash
   cd docker
   ./deploy.sh
   ```

3. **Access your services:**
   - **Frontend**: http://localhost:3001
   - **Backend API**: http://localhost:8000
   - **Grafana**: http://localhost:3000 (admin/admin123)
   - **TimescaleDB**: localhost:5432

## Manual Deployment

If you prefer to run commands manually:

```bash
cd docker

# Pull latest images
docker pull kzmuda/coolbeans_backend:latest
docker pull kzmuda/coolbeans_frontend:latest

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## Configuration

Edit the `.env` file to customize:

- Database credentials
- Port mappings  
- Grafana admin credentials

## Accessing Grafana

1. Go to http://localhost:3000
2. Login with admin/admin123 (or your configured credentials)
3. The TimescaleDB datasource is pre-configured
4. Dashboards are automatically loaded

## Troubleshooting

**View logs:**
```bash
docker-compose logs -f [service_name]
```

**Restart a service:**
```bash
docker-compose restart [service_name]
```

**Stop everything:**
```bash
docker-compose down
```

**Reset data (warning: deletes all data):**
```bash
docker-compose down -v
```

## Service Dependencies

- TimescaleDB starts first
- Grafana connects to TimescaleDB
- FastAPI backend connects to TimescaleDB
- React frontend connects to FastAPI

The docker-compose file handles these dependencies automatically.