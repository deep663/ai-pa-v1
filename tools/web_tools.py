import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults


def check_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

duckduckgo_tool = DuckDuckGoSearchResults()

@tool("advanced_web_search", description="Perform a web search and return summarized results.")
def advanced_web_search(query: str, max_results: int = 5) -> str:
    """
    Perform an advanced web search using DuckDuckGo.
    
    Args:
        query: The search query string.
        max_results: Number of results to return (default: 5).
    """
    if not check_connection():
        return "No internet connection."
    try:
        results = duckduckgo_tool.run(query)
        # print(results)
        if not results:
            return "No search results found."
        
        # The default tool returns text summaries (not JSON). Let's limit the output.
        lines = results.split("\n")[:max_results]
        return "\n".join(lines)
    
    except Exception as e:
        return f"Error during web search: {str(e)}"

# res = advanced_web_search(query="iphone 17 pro price in india")
# print("[Results]: ",res)