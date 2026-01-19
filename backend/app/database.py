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
        self.config = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", ""),
            "database": os.getenv("POSTGRES_DB", "testdb"),
        }

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
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
                    plant_id INTEGER NOT NULL,
                    ec REAL,
                    ph REAL,
                    nitrogen REAL,
                    phosphorus REAL,
                    potassium REAL
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
            print(f"[DB] Connected to Postgres: {self.config.get('host')}:{self.config.get('port')}")
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
