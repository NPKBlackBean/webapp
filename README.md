## CoolBeans Web App
## Current
### Compose setup
Example .env port config:
```bash
POSTGRES_PORT=1156
GRAFANA_PORT=1155
ROS2_PORT=1154
FASTAPI_PORT=1153
REACT_PORT=1152
```
Ensure .env is placed in ./docker, look to docker-compose.yaml ${} interpolations or database, grafana docs to figure
out what is needed; alternatively, look to the CI pipeline .yaml.
```bash
docker compose up -d ./docker
```

## Legacy
### Run the app
1. Execute:
```bash
cd frontend
bun run dev --host 0.0.0.0

cd ../backend
uv run fastapi dev app/main.py # or just fastapi dev app/main.py
```
Add .env file to database/docker and set up environmental variables required by the PostgreSQL database and Grafana containers (see: database/README.md)
```bash
cd ../database/docker # for further instructions on working with db set up go to database/README.md
sudo docker compose up -d
```
2. Open the app at `http://localhost:3000` (frontend dev server) and Grafana at `http://localhost:3001` (login with GRAFANA_USER/GRAFANA_PASSWORD from .env).

### Development setup
Install the [mypy plugin](https://plugins.jetbrains.com/plugin/25888-mypy/versions/stable) 
for PyCharm to have static typing when working with the backend.

We use [uv](https://github.com/astral-sh/uv) for package management in Python. In short, use the following
command when installing packages:
```bash
# example
uv add mypy
```

After installing uv on your system, navigate to `backend`. Execute
```bash
uv init .
```

Make sure to configure the Python interpreter to be set to the one from `backend/.venv` in PyCharm. 
What this means is: go to the bottom right corner of your IDE, and select an existing uv interpreter.
It will point to your system uv install, but you have to specify our `backend/.venv` as the Python
interpreter source.

Now execute the following to install dependencies:
```bash
uv sync
```
