from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from agent_structure.state import GraphState
from agent_structure.URl_finder.tools import news_data_tool, tavily_search_tool
import re

llm = ChatOllama(model="qwen2.5:0.5b", temperature=0)  # lower temp for instruction-following


def _clean_query(raw: str) -> str:
    """Strip conversational filler the small model adds."""
    # If the model wraps the query in quotes, extract it
    match = re.search(r'"([^"]+)"', raw)
    if match:
        return match.group(1)
    # Take only the last line (models often put the query at the end)
    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    return lines[-1] if lines else raw.strip()


def url_agent(state: GraphState):
    messages = [
        SystemMessage(content=(
            "You are a search query optimizer. "
            "Rewrite the user's input into a simple search query. "
            "Output ONLY the search query, nothing else. "
            "No quotes, no explanation, no preamble."
        )),
        HumanMessage(content=state["query"])
    ]

    response = llm.invoke(messages)
    optimized_query = _clean_query(response.content)
    print("ADA optimized query:", optimized_query)

    articles_result = news_data_tool.invoke({"query": optimized_query})
    print("NewsAPI status:", articles_result.get("status"))
    print("NewsAPI totalResults:", articles_result.get("totalResults"))
    print("NewsAPI message:", articles_result.get("message", "none"))
    articles = articles_result.get("articles", [])

    # Fallback: if LLM mangled the query, use the raw user query
    if not articles:
        print("ADA: LLM query returned 0 results, retrying with raw query...")
        articles_result = news_data_tool.invoke({"query": state["query"]})
        articles = articles_result.get("articles", [])
        optimized_query = state["query"]

    urls = [
        {"score": 0, "url": a["url"], "description": a.get("description", "")}
        for a in articles
        if a.get("url") and a.get("description")  # skip entries with no description
    ]
    if state["search"] == "advanced":
        results = tavily_search_tool.invoke({"query": optimized_query})
        url1 = [{"score": i.get("score"), "url": i.get("url"), "description": i.get("content")}
                for i in results["results"]
                if i.get("url") and i.get("content")]
        urls = urls + url1
    return {"collected_urls": urls, "url_prompt": optimized_query}


if __name__ == "__main__":
    messages = [
        SystemMessage(content="""You are a query optimization engine. 
    Rewrite the user's input into a clean, highly detailed search query.
    Rules:
    - Output ONLY the optimized search query.
    - Do NOT include quotes.
    - Do NOT include conversational filler like 'Sure' or 'Here is the query'."""),
        HumanMessage(content="What are the latest AI news? give me a brief concentrating more on claude")
    ]
    llm = ChatOllama(model="qwen2.5:0.5b", temperature=0)
    responce = llm.invoke(messages)
    print(responce)
