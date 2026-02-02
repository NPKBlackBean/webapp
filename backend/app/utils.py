from dotenv import dotenv_values
import os
import socket

REQ_SENSOR_NUMBER_TO_NAME = {
    6: "EC",
    7: "pH",
    8: "N",
    9: "P",
    10: "K",
}

def get_pg_envvars() -> dict[str, str]:
    
    # Check environment variables first (prioritize CI/CD and explicit settings)
    config = {
        "POSTGRES_DB": os.getenv("POSTGRES_DB", ""),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", ""),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT", ""),
        "PGHOST": os.getenv("PGHOST", "localhost"),
        "PGSSLMODE": os.getenv("PGSSLMODE", ""),
    }
    
    # Only fall back to .env file if environment variables are not set (local development)
    if not any(config.values()):
        try:
            env_config = dotenv_values("/backend/external/.env")
            for key in config.keys():
                if not config[key] and key in env_config:
                    config[key] = env_config[key]
            # Always set localhost for local development
            if not config["PGHOST"]:
                config["PGHOST"] = "localhost"
        except Exception:
            # If .env file not found and no env vars, use defaults
            pass

    return config  # type: ignore[return-value]

def get_ros2_envvars() -> dict[str, str]:
    config = {
        "ROS2_HOSTNAME": os.getenv("ROS2_HOSTNAME", ""),
        "ROS2_PORT": os.getenv("ROS2_PORT", ""),
    }

    # Only fall back to .env file if environment variables are not set (local development)
    if not any(config.values()):
        try:
            env_config = dotenv_values("/backend/external/.env")
            for key in config.keys():
                if not config[key] and key in env_config:
                    config[key] = env_config[key]
        except Exception:
            # If .env file not found and no env vars, use defaults
            pass

    return config

def get_ip_address() -> str:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address
