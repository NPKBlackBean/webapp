CREATE TABLE sensor_data (
  time        TIMESTAMPTZ NOT NULL,
  sensor_id   TEXT NOT NULL,
  ec          REAL,   
  ph          REAL,   
  nitrogen    REAL,   
  phosphorus  REAL,   
  potassium   REAL   
);
