# Project Structure
```
├── AnyActions-SDK/
│   ├── README.md
│   ├── .env                # environment variables definition
│   ├── .env.example        # documentation for .env
│   ├── conf.py             # auto documentation plugin
│   ├── poetry.lock
│   ├── pyproject.toml      # poetry config
│   ├── anyactions/         # source
│   │   ├── __init__.py
│   │   ├── main.py         # main entry point
|   |   └── ...
|   ├── tests/
│   │   └── ...
```

# Setup
Initialize .env file. See `.env.example` for documentation of what's needed.

# Development
1. Assuming on a MacOS/Linux system:
```
$ export VENV_PATH=venv
```

2. **[First time run]** Create virtual environment and install Poetry:
```
$ python3 -m venv $VENV_PATH
$ $VENV_PATH/bin/pip install -U pip setuptools
$ $VENV_PATH/bin/pip install poetry
```

3. Activate development environment
```
$ source $VENV_PATH/bin/activate
```

4. Install dependencies and initialize virtual environment
```
$ poetry install
```

5. Add dependency
```
$ poetry add pendulum
```

6. Run a script
```
$ poetry run <command>
$ poetry run python3 anyactions/main.py
```

7. Exit development
```
$ deactivate
```

# Documentation
<!-- ```
$ poetry run sphinx-autodoc -o docs/source/api anyactions/
$ poetry run sphinx-build -b html docs/source/api docs/build/api
``` -->

You should now populate your master file ./docs/index.rst and create other documentation source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

For instance, `make html` will build the HTML documentation.

## Coverage
```
sphinx-build -b coverage . _build/coverage
```
<!-- ```
$ poetry run sphinx-coverage -o docs/source/api anyactions/
$ poetry run sphinx-build -b html docs/source/api docs/build/api   
``` -->