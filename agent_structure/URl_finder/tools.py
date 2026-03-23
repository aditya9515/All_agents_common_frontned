from langchain.tools import tool
from agent_structure.URl_finder.news_data import news_api_data


@tool
def news_data_tool(query: str):
    """Searches for news articles based on a query and returns their URLs."""
    data = news_api_data(query)
    return data


@tool
def tavily_search_tool(query: str):
    """Searches for news articles using the Tavily API."""
    from agent_structure.URl_finder.tavily_api import tvaily_search
    return tvaily_search(query)