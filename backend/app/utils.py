from dotenv import dotenv_values
import socket

REQ_SENSOR_NUMBER_TO_NAME = {
    6: "EC",
    7: "pH",
    8: "N",
    9: "P",
    10: "K",
}

def get_pg_envvars() -> dict[str, str]:
    config = dotenv_values("../database/docker/.env")
    config["PGHOST"] = "localhost"

    return config  # type: ignore[return-value]

def get_ip_address() -> str:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address
