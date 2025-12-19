CREATE TABLE IF NOT EXISTS sensor_data (
  time        TIMESTAMPTZ NOT NULL,
  plant_id    TEXT NOT NULL,
  ec          REAL,   
  ph          REAL,   
  nitrogen    REAL,   
  phosphorus  REAL,   
  potassium   REAL   
);

-- Sample data for testing (EC/ph stay in green; N/P/K vary to hit all bands)
INSERT INTO sensor_data (time, plant_id, ec, ph, nitrogen, phosphorus, potassium)
VALUES
  (NOW(),                     'plant_01', 920.0,  6.8, 12.0,  6.0, 11.0), -- green EC/pH, mid NPK
  (NOW() - INTERVAL '10 min', 'plant_02', 840.0,  6.7, 28.0, 12.0, 29.0), -- green EC/pH, high N/K (green)
  (NOW() - INTERVAL '20 min', 'plant_03', 880.0,  6.6, 22.0,  4.0, 18.0), -- green EC/pH, yellow P, yellow K
  (NOW() - INTERVAL '30 min', 'plant_01', 860.0,  6.9, 15.0,  9.0, 21.0), -- green EC/pH, yellow K
  (NOW() - INTERVAL '40 min', 'plant_02', 900.0,  7.0,  8.0,  3.0,  9.0), -- green EC/pH, orange N/P/K
  (NOW() - INTERVAL '50 min', 'plant_03', 830.0,  6.5,  5.0,  2.5,  5.5), -- green EC/pH, red N/P/K
  (NOW() - INTERVAL '1 hour', 'plant_01', 950.0,  6.8, 32.0, 14.0, 32.0), -- green EC/pH, high green NPK
  (NOW() - INTERVAL '90 min', 'plant_02', 870.0,  6.7, 18.0, 11.0, 24.0), -- green EC/pH, yellow/green mix
  (NOW() - INTERVAL '2 hours','plant_03', 820.0,  6.6, 10.0,  5.0, 10.0), -- green EC/pH, orange N/K, orange P
  (NOW() - INTERVAL '3 hours','plant_01', 910.0,  6.8, 24.0,  7.0, 15.0), -- green EC/pH, yellow P
  (NOW() - INTERVAL '4 hours','plant_02', 940.0,  6.9,  6.0,  1.5,  6.0), -- green EC/pH, red P
  (NOW() - INTERVAL '5 hours','plant_03', 880.0,  6.7, 14.0,  8.0, 14.0); -- green EC/pH, yellow N/K

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM timescaledb_information.hypertables
    WHERE hypertable_name = 'sensor_data'
  ) THEN
    PERFORM create_hypertable(
      'sensor_data',
      'time',
      'plant_id',
      number_partitions => 4
    );
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS sensor_data_time_idx
  ON sensor_data (plant_id, time DESC);
