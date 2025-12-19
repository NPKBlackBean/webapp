# TimescaleDB set up for CoolBeans

This set up contains PostgreSQL database with Timescale, run in a Docker container. Follow the instructions below to run the container yourself; 

_Some commands may have slightly different syntax for Windows operating system._

## Purpose

This TimescaleDB instance stores time-series data for the plant sensor readings.

This setup is intended for:
- Local development
- Staging environments

Production runs might be managed with Timescale Cloud.

## Architecture

- TimescaleDB runs as a Docker container
- Grafana runs as a Docker container with provisioned dashboards
- Data is persisted in Docker volumes (`timescale_data`, `grafana_data`)
- Initialization scripts run once on first startup from `init/sensor_data.sql`
- Application services connect via port 5432 (PostgreSQL) and 3000 (Grafana)

## Configuration

Configuration is done via environment variables.

Required variables:
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- GRAFANA_USER
- GRAFANA_PASSWORD
- GRAFANA_PORT

These are defined in `.env` in database/docker directory (not committed).


## Getting started

### Prerequisites
- Docker installed
- PostgreSQL installed

### Run the container from docker-compose.yml

To run the container with TimescaleDB setup use:
```bash
sudo docker compose up -d
```

To check logs:
```bash
sudo docker compose logs -f
```

### Use PostgreSQL in the container
Verify PosgreSQL and TimescaleDB is there:
```sql
psql -h localhost -p 5432 -U admin -d metrics -- database name
-- temporary password for admin user is in the docker-compose.yml
\dx -- prints the list of installed extensions, as TimescaleDB is a PostreSQL extension
```

Should print something that looks like:
```md
                        List of installed extensions
    Name     | Version |   Schema   |                                      Description                                      
-------------+---------+------------+---------------------------------------------------------------------------------------
 plpgsql     | 1.0     | pg_catalog | PL/pgSQL procedural language
 timescaledb | 2.24.0  | public     | Enables scalable inserts and complex queries for time-series data (Community Edition)
```

If there is indeed a row mentioning TimescaleDB, then we are all set!

### Access Grafana Dashboards
Open `http://localhost:3000` in your browser, login info being what you put in the `.env` file:

| Field      | Value               |
|------------|---------------------|
| **login**  | `${GRAFANA_USER}`   |
| **password** | `${GRAFANA_PASSWORD}` |

Available dashboards:
- **All - Soil Sensor Data**: Main dashboard showing all plants with stat panels, timeseries charts (EC, pH, N, P, K), and Recent Alerts table. Color-coded thresholds (red/orange/yellow/green).
- **Plant Comparison - Soil Sensor Data**: Cross-plant analytics with side-by-side values, deviation-from-target, health ranking, multi-plant comparison charts (plant_01: purple, plant_02: blue, plant_03: pink), and Recent Alerts.
- **plant_01 / plant_02 / plant_03**: Individual plant dashboards with same layout as main dashboard, filtered per plant.

```java
/* TODO: 
- backup strategy/scripts
    docker exec timescaledb pg_dump -U admin metrics_db > backup.sql
    restoring: psql -h localhost -U admin metrics_db < backup.sql
*/
```

To stop the container use:
```bash
docker compose stop
```

## Data persistence
The tables and sensor data should persist even when the container is stopped, unless you use:
```bash
docker compose down -v
```

## Common Commands
```bash
# Start database and Grafana:
sudo docker compose up -d

# Stop database and Grafana:
sudo docker compose stop

# Restart Grafana (to reload dashboards):
sudo docker compose restart grafana

# View logs:
sudo docker compose logs -f

# Connect via psql:
psql -h localhost -U admin -d metrics_db

# Exit the psql:
quit
```

## Executing commands in the compose
Use docker exec
```bash
# Example
docker exec -it timescaledb psql -U admin -d metrics
```

Then you can execute SQL statements, like
```sql
\dt -- See list of tables
\q -- Quit
```

## TimescaleDB Conventions

- All hypertables must include a `time TIMESTAMPTZ NOT NULL` column
- Chunk interval defaults to 1 day
- Compression after 7 days
- Retention after 30 days

## Troubleshooting

### Database won’t start
- Check if port 5432 is already in use
- Run `sudo docker compose logs timescaledb`

### Tables missing
- Ensure volume was not removed
- Do NOT run `sudo docker compose down -v`

### Slow queries
- Check if hypertable exists
- Ensure time column is indexed
