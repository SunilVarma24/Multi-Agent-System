# src/tools.py

from tavily import AsyncTavilyClient
from langchain_core.tools import tool

# Step 1: Get absolute path to the project root
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

# Step 2: Construct .env path explicitly
env_path = project_root / ".env"

# Step 3: Load it explicitly
load_dotenv(dotenv_path=env_path)

# Initialize async Tavily client
async_tavily_client = AsyncTavilyClient()

@tool
async def tv_search(query: str) -> str:
    """Search the web using Tavily with async support"""
    try:
        response = await async_tavily_client.search(
            query=query, 
            max_results=3,
            search_depth="advanced"
        )
        
        # Format the results similar to TavilySearchResults format
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0)
            })
        
        return str(results)
    except Exception as e:
        return f"Search error: {str(e)}"

@tool
async def kaggle_dataset_search(query: str) -> str:
    """Search for relevant datasets on Kaggle"""
    try:
        search_query = f"site:kaggle.com datasets {query}"
        response = await async_tavily_client.search(
            query=search_query,
            max_results=3,
            search_depth="advanced"
        )
        
        # Format results
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0)
            })
        
        return str(results)
    except Exception as e:
        return f"Kaggle search error: {str(e)}"

@tool
async def huggingface_search(query: str) -> str:
    """Search for relevant datasets on HuggingFace"""
    try:
        search_query = f"site:huggingface.co {query}"
        response = await async_tavily_client.search(
            query=search_query,
            max_results=3,
            search_depth="advanced"
        )
        
        # Format results
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0)
            })
        
        return str(results)
    except Exception as e:
        return f"HuggingFace search error: {str(e)}"

@tool
async def github_search(query: str) -> str:
    """Search for relevant repositories on GitHub"""
    try:
        search_query = f"site:github.com {query}"
        response = await async_tavily_client.search(
            query=search_query,
            max_results=3,
            search_depth="advanced"
        )
        
        # Format results
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0)
            })
        
        return str(results)
    except Exception as e:
        return f"GitHub search error: {str(e)}"

