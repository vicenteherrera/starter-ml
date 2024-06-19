# jupyter_ml

Lightweight way to use Jupyter Notebooks locally.

## Prerequisites

Check the global [README.md](../README.md) file regarding PyEnv and Poetry.

Jupyter requires that you install SQLite, you can do that on Debian with `sudo apt-get install libsqlite3-dev`.

## How to use

To launch Jupyter use:
```bash
# Launch Jupyter
make
```

That will switch with pyenv to a specific Python version, automatically creating a virtual environment and installing dependencies. It will have several machine learning related libraries cached and pre-installed, so you don't have to install them each time with your notebook.

If you want to add or update libraries, use:
```bash
# Add a new dependency
poetry add keras

# Update dependencies
poetry update
```

## Trobleshooting

### ModuleNotFoundError: No module named 'pysqlite2'

If you get this error, probably while running Jupyter, you need to install Sqlite before installing the specific Python version with PyEnv:

```bash
sudo apt-get install libsqlite3-dev
```

If you already had Python installed, you can reinstall it after you update this package, and rebuild the virtual environment with the new binary using:

```bash
make refresh
```
