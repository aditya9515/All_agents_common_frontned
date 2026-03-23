from tavily import TavilyClient
import json


def tvaily_search(query: str):
    tavily_client = TavilyClient(api_key="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")
    response = tavily_client.search(query, search_depth="advanced")
    return response


if __name__ == "__main__":
    query = "What are the latest advancements in AI research?"
    results = tvaily_search(query)
    print(results)
    with open("agent_structure/URl_finder/tavily_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
