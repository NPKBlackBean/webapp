from abc import ABC, abstractmethod
import os
import psycopg2

from domain import SensorReading
from utils import get_pg_envvars

class DatabaseInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def save_reading(self, plant_id: int, reading: SensorReading):
        pass

    @abstractmethod
    def close(self):
        pass

class PostgresDatabase(DatabaseInterface):
    def __init__(self):
        self.conn = None
        config = get_pg_envvars()
        self.params = {
            "host": config["PGHOST"],
            "port": config["POSTGRES_PORT"],
            "dbname": config["POSTGRES_DB"],
            "user": config["POSTGRES_USER"],
            "password": config["POSTGRES_PASSWORD"],
        }
        sslmode = config.get("PGSSLMODE", "")
        if sslmode:
            self.params["sslmode"] = sslmode

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.params)
            cur = self.conn.cursor()
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
                self.conn.commit()
            except psycopg2.Error as e:
                self.conn.rollback()
                print(e)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sensor_data (
                    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    plant_id TEXT NOT NULL,
                    ec DOUBLE PRECISION,
                    ph DOUBLE PRECISION,
                    nitrogen DOUBLE PRECISION,
                    phosphorus DOUBLE PRECISION,
                    potassium DOUBLE PRECISION
                );
                """
            )
            self.conn.commit()
            try:
                cur.execute("SELECT create_hypertable('sensor_data','time', if_not_exists => TRUE);")
                self.conn.commit()
            except psycopg2.Error as e:
                self.conn.rollback()
                print(e)
            print(f"[DB] Connected to Postgres: {self.params.get('host')}:{self.params.get('port')}")
        except psycopg2.Error as e:
            print(f"[DB] Error connecting to Postgres: {e}")

    def save_reading(self, plant_id: int, reading: SensorReading):
        """Plant ID is 1-indexed"""
        if not self.conn:
            self.connect()
        try:
            cur = self.conn.cursor()
            query = f"INSERT INTO sensor_data VALUES (NOW(), %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (plant_id, reading.EC, reading.pH, reading.N, reading.P, reading.K))
            self.conn.commit()
            print(f"[DB] Saved: {plant_id} -> {SensorReading}") # uses __format__, not __repr__ or __str__
        except psycopg2.Error as e:
            self.conn.rollback()
            print("Error, rolled back with conn.rollback()")
            raise RuntimeError(e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("[DB] Connection closed.")
