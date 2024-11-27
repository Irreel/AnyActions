# Project Structure
```
├── my_project/
│   ├── README.md
│   ├── .env                # environment variables definition
│   ├── .env.example        # documentation for .env
│   ├── conf.py             # documentation plugin
│   ├── poetry.lock
│   ├── pyproject.toml      # poetry config
│   ├── anyactions/         # source
│   │   ├── __init__.py
│   │   ├── main.py
|   |   └── ...
|   ├── tests/
│   │   └── ...
```

# Setup
Initialize AWS credentials. Put the following in your `.env`:
```
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials
export AWS_CONFIG_FILE=~/.aws/config
```
Put in `~/.aws/credentials`:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```
Put in `~/.aws.config`:
```
[default]
region=us-east-1
```
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

6. Exit development
```
$ deactivate
```