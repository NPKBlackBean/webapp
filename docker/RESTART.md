# Docker Compose Service Restart

This directory includes tools to easily restart the CoolBeans Docker Compose services (e.g. in case of switching off the device hosting services, etc.)

## Quick Start

### Option 1: Bash Script (Direct)
```bash
cd /path/to/webapp
./restart-services.sh
```

### Option 2: Systemd Service (Automatic)
Use this on the Raspberry Pi for easy service management.

## Setup (One-time)

### 1. Copy the systemd service file to the system:
```bash
sudo cp docker/compose-restart.service /etc/systemd/system/
```

### 2. Reload systemd configuration:
```bash
sudo systemctl daemon-reload
```

### 3. Enable the service to start automatically on boot (optional):
```bash
sudo systemctl enable compose-restart.service
```

## Usage

### Start/Restart all services:
```bash
sudo systemctl start compose-restart.service
```

### Check service status:
```bash
sudo systemctl status compose-restart.service
```

### View service logs:
```bash
sudo journalctl -u compose-restart.service -n 20
```

### View full service logs with follow:
```bash
sudo journalctl -u compose-restart.service -f
```

## What It Does

The `compose-restart.service` systemd unit:
- Restarts all Docker Compose services defined in docker-compose.yaml
- Executes in one shot and completes (Type=oneshot)
- Depends on Docker daemon running
- Can be called manually anytime or scheduled with systemd timers

## Troubleshooting

If the service fails:

1. Check if Docker is running:
   ```bash
   sudo systemctl status docker
   ```

2. Check service logs:
   ```bash
   sudo journalctl -u compose-restart.service -n 50
   ```

3. Verify the docker-compose file is valid:
   ```bash
   cd /home/coolbeans/webapp/docker
   docker-compose config
   ```

4. Test running compose manually:
   ```bash
   cd /home/coolbeans/webapp/docker
   sudo docker-compose up -d
   ```