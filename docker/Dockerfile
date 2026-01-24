FROM grafana/grafana:latest

# Copy provisioning files
COPY database/docker/grafana/provisioning /etc/grafana/provisioning
# Copy dashboards
COPY database/docker/grafana/dashboards /var/lib/grafana/dashboards

# Expose Grafana port
EXPOSE 3000

# Use default entrypoint
