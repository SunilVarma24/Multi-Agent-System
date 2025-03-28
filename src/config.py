# src/config.py

import locale
import os
import yaml

# Ensure proper encoding
locale.getpreferredencoding = lambda: "UTF-8"

# Load OpenAI API key
with open("openai_key.yaml", 'r') as file:
    api_creds = yaml.safe_load(file)
os.environ["OPENAI_API_KEY"] = api_creds['openai_key']

# Load Tavily API key
with open("tavily_key.yaml", 'r') as file:
    api_creds = yaml.safe_load(file)
os.environ["TAVILY_API_KEY"] = api_creds['tavily_key']
