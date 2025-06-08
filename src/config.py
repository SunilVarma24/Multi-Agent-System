# src/config.py

# import locale
# import os
# import yaml

# # Ensure proper encoding
# locale.getpreferredencoding = lambda: "UTF-8"

# Load OpenAI API & Tavily Web Search keys
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
