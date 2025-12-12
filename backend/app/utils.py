import socket

def get_ip_address() -> str:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address
