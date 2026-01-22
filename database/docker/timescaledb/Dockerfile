FROM timescale/timescaledb:latest-pg16

# Copy your initialization SQL script
COPY sensor_data.sql /docker-entrypoint-initdb.d/sensor_data.sql

EXPOSE 5432
