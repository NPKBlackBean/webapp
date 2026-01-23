from datetime import datetime, timedelta
import numpy as np
import math
import time
import random
import sqlite3

db = sqlite3.connect('db.sqlite3')

def initialize_db():
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant_readings(
            plant_id INTEGER PRIMARY KEY,
            datetime TIMESTAMP,
            ec REAL,
            ph REAL,
            n REAL,
            p REAL,
            k REAL,
            temp REAL,
            humidity REAL
        )
    ''')
    db.commit()

def get_temp_reading(time_in_days: float, avg: float):
    """Return the temperature reading in degrees C"""
    return (math.sin(2 * math.pi * time_in_days) + avg) #+ random.gauss(sigma=0.2)

def run_experiment(plant_id, params):
    cur_dt = datetime(2025, 12, 1, 9, 00, 00)
    end_dt = cur_dt + timedelta(days=60)

    # take reading every x mins
    sensor_resolution_mins = 5
    mins_passed = 0
    while cur_dt < end_dt:
        temp_reading = get_temp_reading(time_in_days=mins_passed / (60 * 24), avg=26.0)
        print(cur_dt, temp_reading)
        time.sleep(0.1)

        cur_dt += timedelta(minutes=sensor_resolution_mins)
        mins_passed += sensor_resolution_mins

def main():
    random.seed(42)
    initialize_db()

    experiment_params = [""]
    for idx, params in enumerate(experiment_params):
        run_experiment(idx + 1, params)

if __name__ == "__main__":
    main()