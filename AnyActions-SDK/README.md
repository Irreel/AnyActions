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

4. **[First time run]** Install dependencies
```
$ poetry install
```

5. Add dependency
```
$ poetry add pendulum
```

6. Exit development
```
$ deactivate
```