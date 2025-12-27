### Manual testing
```bash
# from project root
python -m venv database/backup/.venv
source database/backup/.venv/bin/activate
pip install -r database/backup/requirements.txt

python database/backup/database_backup.py --backup
# verify
ls -lah database/backup/backups/
```

### Install and enable
```bash
# Copy units to systemd directory
sudo cp database/backup/database_backup.service /etc/systemd/system/database_backup.service
sudo cp database/backup/database_backup.timer   /etc/systemd/system/database_backup.timer

# Reload systemd to pick up new units
sudo systemctl daemon-reload

# Enable and start the timer (will run daily at 19:00)
sudo systemctl enable --now database_backup.timer
```

Verify:
```bash
# Check timer status and next run
sudo systemctl status database_backup.timer

# Check last/active service runs
sudo systemctl status database_backup.service
```