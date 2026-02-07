from datetime import datetime, timedelta
from experiments import EXPERIMENT_SETUPS

import math
import time
import random
import sqlite3

db = sqlite3.connect('db.sqlite3')

def initialize_db():
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS plant_readings')
    cursor.execute('''
        CREATE TABLE plant_readings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            datetime TIMESTAMP,
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
    x = time_in_days
    return (math.sin(2 * math.pi * x) + avg) + random.gauss(sigma=0.1)

def get_humidity_reading(time_in_days: float):
    """Return the humidity reading, ranging from 0 to 100%"""
    x = time_in_days % 1.0

    if x < 16 / 17: # soil naturally drying out
        return -85 * x + 100
    else: # just watered
        return 1360 * x - 1260

def get_ph_reading(time_in_days: float, avg):
    return avg + random.gauss(sigma=0.1)

def get_nutrient_reading(time_in_days: float, constant_offset: float, nutrient_type: str):
    x = time_in_days % 7.0

    fertilizer_added = False
    if x >= (6.0 + 16 / 17): # fertilize once a week, after watering event
        fertilizer_added = True

    # proportional noise
    proportion_p_to_n = 0.6
    proportion_k_to_n = 2.0

    if nutrient_type == "nitrogen":
        if fertilizer_added:
            return (505.25 * x - 3436.75) + random.gauss(sigma=0.1)
        else:
            return (75.95 * math.exp(-0.0718 * x) + 24.05) + random.gauss(sigma=0.1)
    elif nutrient_type == "phosphorus":
        if fertilizer_added:
            return (277.88 * x - 1885.16) + random.gauss(sigma=0.1 * proportion_p_to_n)
        else:
            return (45.46 * math.exp(-0.0643 * x) + 14.54) + random.gauss(sigma=0.1 * proportion_p_to_n)
    elif nutrient_type == "potassium":
        if fertilizer_added:
            return (394.89 * x - 2564.23) + random.gauss(sigma=0.1 * proportion_k_to_n)
        else:
            return (152.98 * math.exp(-0.02376 * x) + 47.02) + random.gauss(sigma=0.1 * proportion_k_to_n)
    else:
        raise ValueError(f"{nutrient_type} cannot be passed.")


def run_experiment(plant_id, params):
    cur_dt = datetime(2025, 12, 1, 9, 00, 00)
    end_dt = cur_dt + timedelta(days=60)

    # take reading every x mins
    sensor_resolution_mins = 5
    mins_passed = 0

    while cur_dt < end_dt:
        time_in_days = mins_passed / (60 * 24)
        temp_reading = get_temp_reading(time_in_days, avg=params["temp"])
        humidity_reading = get_humidity_reading(time_in_days)
        ph_reading = get_ph_reading(time_in_days, avg=params["ph"])

        nitrogen_reading = get_nutrient_reading(time_in_days, params["nitrogen"], "nitrogen")
        phosphorus_reading = get_nutrient_reading(time_in_days, params["phosphorus"], "phosphorus")
        potassium_reading = get_nutrient_reading(time_in_days, params["potassium"], "potassium")

        # debug :)
        # print(f"{cur_dt}  plant:{plant_id:<3d}  temp:{temp_reading:8.2f}  humidity:{humidity_reading:8.2f}  ph:{ph_reading:8.2f}")
        # print(f"{cur_dt}  plant:{plant_id:<3d}     N:{nitrogen_reading:8.2f}  P:       {phosphorus_reading:8.2f}  K: {potassium_reading:8.2f}")
        # print("------------------------------------------------------------------------")

        db.execute(
            'INSERT INTO plant_readings (plant_id, datetime, ph, n, p, k, temp, humidity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (plant_id, cur_dt, ph_reading, nitrogen_reading, phosphorus_reading, potassium_reading, temp_reading, humidity_reading)
        )

        cur_dt += timedelta(minutes=sensor_resolution_mins)
        mins_passed += sensor_resolution_mins

    db.commit()

def main():
    random.seed(42)
    initialize_db()

    n_setups = len(EXPERIMENT_SETUPS["temp"])

    for i in range(n_setups):
        experiment_params = {
            "temp": EXPERIMENT_SETUPS["temp"][i],
            "ph": EXPERIMENT_SETUPS["ph"][i],
            "nitrogen": EXPERIMENT_SETUPS["nitrogen"][i],
            "phosphorus": EXPERIMENT_SETUPS["potassium"][i],
            "potassium": EXPERIMENT_SETUPS["potassium"][i]
        }
        run_experiment(i + 1, experiment_params)

if __name__ == "__main__":
    main()