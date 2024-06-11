# simple_openai

Call [OpenAI GPT-4](https://openai.com/) endpoint with a simple prompt, and get an answer.

This is the simplest example, it doesn't require Poetry or PyEnv, just try it you your own version of Python (it was tested with 3.11.7).

Copy `env-sample.txt` to `env.txt` and put your OpenAI API key there.

```bash
# Create virtual environment
python -m venv .env

# Activate virtual environment (Bash)
source .env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run application
python ./app.py

# When finished, exit the virtual environment
deactivate
```

