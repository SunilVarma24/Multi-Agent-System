# src/tools.py

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

# Initialize Tavily search tool
tv_search = TavilySearchResults(max_results=5, search_depth='advanced', max_tokens=10000)

@tool
def kaggle_dataset_search(query: str) -> str:
    """Search for relevant datasets on Kaggle"""
    # Using Tavily to search Kaggle specifically
    return tv_search.invoke(f"site:kaggle.com datasets {query}")

@tool
def huggingface_search(query: str) -> str:
    """Search for relevant datasets on HuggingFace"""
    # Using Tavily to search HuggingFace specifically
    return tv_search.invoke(f"site:huggingface.co {query}")

@tool
def github_search(query: str) -> str:
    """Search for relevant repositories on GitHub"""
    # Using Tavily to search GitHub specifically
    return tv_search.invoke(f"site:github.com {query}")
