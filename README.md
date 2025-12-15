## CoolBeans Web App
### Run the app
1. Execute:
```bash
cd frontend
bun run dev

cd ../backend
uv run fastapi dev app/main.py

cd ../database/docker -- for further instructions on working with db set up go to database/README.md
sudo docker compose up -d
```
2. Open `http://localhost:3000` in your browser.

### Development setup
Install the [mypy plugin](https://plugins.jetbrains.com/plugin/25888-mypy/versions/stable) 
for PyCharm to have static typing when working with the backend.

We use [uv](https://github.com/astral-sh/uv) for package management in Python. In short, use the following
command when installing packages:
```bash
# example
uv pip install mypy
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
