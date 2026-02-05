#!/bin/bash
# Stops the CoolBeans Docker containers safely

containers=("grafana" "ros2" "timescaledb" "react" "fastapi")

for c in "${containers[@]}"; do
    if docker ps -q -f name="^${c}$" | grep -q .; then
        echo "Stopping container: $c"
        docker stop "$c"
    else
        echo "Container $c is not running"
    fi
done

echo "All specified containers have been stopped."
