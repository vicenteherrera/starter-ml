# jupyter_ml

Lightweight way to use Jupyter Notebooks locally.

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
