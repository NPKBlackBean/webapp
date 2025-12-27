import argparse
from pathlib import Path
import subprocess
from datetime import datetime, timezone

from dotenv import dotenv_values

POSTGRES_DOTENV_PATH: Path = Path(__file__).resolve().parent.parent / "docker" / ".env" # .env with postgres credentials
CONTAINER_NAME = "timescaledb" # Container name as used in docker-compose
LOCAL_BACKUPS_DIR = Path(__file__).resolve().parent / "backups"

def backup():
    """
    Execute a docker command which invokes a psql pg_dump command to backup the PostgreSQL database to a .sql file.
    Copy the backup over to the Docker host and delete the .sql inside the container afterwards.
    If there are 4 backups after copy, remove the oldest one, keeping the 3 newest backups.
    """

    # Load creds from .env
    env_values = {}
    if POSTGRES_DOTENV_PATH.exists():
        # dotenv_values returns a dict-like mapping of keys to values; missing file returns {}
        env_values = {k: v for k, v in dotenv_values(str(POSTGRES_DOTENV_PATH)).items() if v is not None}

    pg_user = env_values.get("POSTGRES_USER")
    pg_db = env_values.get("POSTGRES_DB")
    pg_password = env_values.get("POSTGRES_PASSWORD")

    if not pg_user or not pg_db:
        raise RuntimeError("Missing POSTGRES_USER or POSTGRES_DB (check ../docker/.env or environment)")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{pg_db}_{timestamp}.sql"
    container_dump_path = f"/tmp/{filename}"

    # Ensure local backups directory exists next to this script
    LOCAL_BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    local_path = LOCAL_BACKUPS_DIR / filename

    # Build pg_dump command to run inside the container. Use PGPASSWORD env var for authentication.
    # We run via bash -lc so we can set the env var for the pg_dump command only.
    inner_cmd = (
        f"PGPASSWORD='{pg_password}' pg_dump -U {pg_user} -d {pg_db} -F p -f {container_dump_path}"
    )

    docker_exec_cmd = ["docker", "exec", CONTAINER_NAME, "bash", "-lc", inner_cmd]

    try:
        print(f"Running pg_dump inside container '{CONTAINER_NAME}'...")
        res = subprocess.run(docker_exec_cmd, check=True, capture_output=True, text=True)
        if res.stdout:
            print("pg_dump stdout:", res.stdout)
        if res.stderr:
            print("pg_dump stderr:", res.stderr)
    except subprocess.CalledProcessError as e:
        print("pg_dump failed:\n", e.stderr or e.output or str(e))
        raise

    # Copy the dump from container to host
    docker_cp_cmd = ["docker", "cp", f"{CONTAINER_NAME}:{container_dump_path}", str(local_path)]
    try:
        print(f"Copying dump from container to host: {local_path}")
        res = subprocess.run(docker_cp_cmd, check=True, capture_output=True, text=True)
        if res.stdout:
            print("docker cp stdout:", res.stdout)
        if res.stderr:
            print("docker cp stderr:", res.stderr)
    except subprocess.CalledProcessError as e:
        print("docker cp failed:\n", e.stderr or e.output or str(e))
        # Attempt to clean up the container file even if copy failed
        try:
            subprocess.run(["docker", "exec", CONTAINER_NAME, "rm", "-f", container_dump_path], check=False)
        except Exception:
            pass
        raise

    # Remove the dump file from the container
    try:
        subprocess.run(["docker", "exec", CONTAINER_NAME, "rm", "-f", container_dump_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Warning: failed to remove dump file in container:\n", e.stderr or str(e))

    # Rotate local backups: keep only the 3 newest
    backups = sorted(LOCAL_BACKUPS_DIR.glob(f"{pg_db}_*.sql"), key=lambda p: p.stat().st_mtime, reverse=True)
    if len(backups) > 3:
        to_delete = backups[3:]
        for p in to_delete:
            try:
                print(f"Removing old backup: {p}")
                p.unlink()
            except Exception as e:
                print(f"Failed to remove old backup {p}: {e}")

    print(f"Backup complete: {local_path}")


def restore():
    raise NotImplementedError("restore() is not yet implemented by database_backup.py")

def main(args: argparse.Namespace):
    if args.backup:
        backup()
    elif args.restore:
        restore()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--backup', action='store_true')
    group.add_argument('--restore', action='store_true')

    args = parser.parse_args()

    main(args)