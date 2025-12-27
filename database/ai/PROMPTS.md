2025-12-27

Prompt #1:

Purpose: Compose the list of arguments passed to subprocess, for the task of creating a database backup script.
Model: GPT-5 mini
Mode: agent
Attached context: database/backup/database_backup.py
Conversation: new
Prompt:

You are a Python developer with experience in Linux system administration tasks, interacting with
the operating system and executing commands using the subprocess library, managing Docker containers and
automating the backup of TimescaleDB databases. As a reminder, TimescaleDB databases are extensions of PostgreSQL
databases and use the `pg_dump` command for backup.

You are tasked with filling out a Python function responsible for running a `pg_dump` database backup, for which 
a docstring has already been provided, as well as comments detailing what the function will do at a high level.

Here is the function:

def backup():
    """
    Execute a docker command which invokes a psql pg_dump command to backup the PostgreSQL database to a .sql file.
    Copy the backup over to the Docker host and delete the backup in the container.
    If there are 4 backups after copy, remove the oldest one, keeping the 3 newest backups.
    :return:
    """

    # 1. construct the command to be used for subprocess database dump
    # ["docker", "exec", "container", "pg_dump", ...]
    # 2. command to be used for copying over the dump
    # 3. command to delete the dump in the container
    # 4. command to check whether there is a 4th dump and if yes, delete it

    pass

I will now provide you with the details of the container. Here is an excerpt straight from the docker-compose.yaml
used to launch the database:
services:
  timescaledb:
    networks:
      - shared_stack_net
    image: timescale/timescaledb:latest-pg16
    container_name: timescaledb
    ports:
      - "${POSTGRES_PORT}:5432"
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - timescale_data:/var/lib/postgresql/data
      - ../init:/docker-entrypoint-initdb.d
    restart: unless-stopped

And here is part of the TimescaleDB documentation called "Logical backup with pg_dump and pg_restore", which
targets the exact use case of creating a database backup (they dubbed it "logical"). I am enclosing it in triple quotes:
"""
Set your connection strings

These variables hold the connection information for the source database to backup from and the target database to restore to:

export SOURCE=postgres://<user>:<password>@<source host>:<source port>/<db_name>
export TARGET=postgres://<user>:<password>@<source host>:<source port>
Backup your database

pg_dump -d "$SOURCE" \
  -Fc -f <db_name>.bak
You may see some errors while pg_dump is running. See Troubleshooting self-hosted TimescaleDB to check if they can be safely ignored.
"""

Do note that we do not have a "TARGET" database, instead our target is to have the database dump be saved to disk
in the container, and then for us to copy that dumped .sql file over to the Docker host, deleting the .sql inside
of the Docker container afterwards.


Prompt #2:

Purpose: Write the systemd service responsible for running database backups.
Model: GPT-5 mini
Mode: ask
Attached context: database/backup/database_backup.py, database_backup.service
Conversation: follows Prompt #1, 2025-12-27
Prompt:

Implement database_backup.service. You can expect database_backup.py to be placed under the
/home/coolbeans/webapp/database/backup directory, and the database_backup.service to be placed under
/etc/systemd/system. This service will run on a daily timer, namely database_backup.timer which you do not have
to worry about now. It will be run as the coolbeans user.

The database_backup.py Python file will have its own venv at /home/coolbeans/webapp/database/backup/.venv, with
the requirements being installed beforehand. Thus, when you activate the Python interpreter from that venv, you
can assume it will have all the necessary dependencies.

Prompt #3:

Purpose: Write the systemd time responsible for running the systemd service.
Model: GPT-5 mini
Mode: ask
Attached context: database_backup.service
Conversation: follows Prompts #1, #2 2025-12-27
Prompt:

Create the corrresponding timer, as you have suggested. I want it to run at 19:00.