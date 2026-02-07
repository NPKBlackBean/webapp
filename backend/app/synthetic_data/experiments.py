# unlabelled rows are noise, one could replace them with random "sensible" values (ie. dont make the pH 42)
# and they won't be taken into account in the f(x,y,z) func calculating plant height
EXPERIMENT_SETUPS: dict = {
    "temp": [
        17.0, 19.0, 21.0, 23.0, # only temp changing, 4 pts on curve
        21.0, 21.0, 21.0, 21.0,
        21.0, 21.0, 21.0, 21.0,
        21.0, 21.0, 21.0, 21.0,
        21.0, 21.0, 21.0, 21.0,
        17.0, 19.0, 21.0, 23.0, # temp and ph changing, 4 pts on curve
        17.0, 19.0, 21.0, 23.0, # temp and p changing, 4 pts on curve
        21.0, 21.0, 21.0, 21.0,
        17.0, 19.0, 21.0, 23.0, # temp, ph and p changing, 4 pts on curve
    ],
    "ph": [
        6.5, 6.5, 6.5, 6.5,
        5.7, 6.3, 7.0, 7.5, # only ph changing, 4 pts on curve
        6.5, 6.5, 6.5, 6.5,
        6.5, 6.5, 6.5, 6.5,
        6.5, 6.5, 6.5, 6.5,
        5.7, 6.3, 7.0, 7.5, # temp and ph changing, 4 pts on curve
        6.5, 6.5, 6.5, 6.5,
        5.7, 6.3, 7.0, 7.5, # ph and p changing, 4 pts on curve
        5.7, 6.3, 7.0, 7.5, # temp, ph and p changing, 4 pts on curve
    ],
    "nitrogen": [
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
    ],
    "phosphorus": [
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        -15.0, -5.0, 5.0, 15.0, # only phosphorus changing, 4 pts on curve
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        -15.0, -5.0, 5.0, 15.0, # temp and p changing, 4 pts on curve
        -15.0, -5.0, 5.0, 15.0, # ph and p changing, 4 pts on curve
        -15.0, -5.0, 5.0, 15.0 # temp, ph and p changing, 4 pts on curve
    ],
    "potassium": [
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0,
    ],
}