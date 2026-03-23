from agent_structure.Relevence_checker.relevence_checker import relevence_agent
from agent_structure.URl_finder.filter_agent import url_agent
from agent_structure.state import GraphState
from langgraph.graph import StateGraph, END
from agent_structure.URl_scrapper_parcer.url_scrapper_parcer import scrapper_parcer
from agent_structure.duplication.duplication import filter_agent
from agent_structure.summarizer.summarizer import summary_agent


def check_urls(state: GraphState):
    """Stop early if no URLs were collected."""
    if not state.get("collected_urls"):
        print("ADA: No URLs found, ending pipeline.")
        return "end"
    return "continue"


def check_pages(state: GraphState):
    """Stop early if scraping yielded nothing."""
    if not state.get("filtered_pages"):
        print("ADA: No content after filtering, ending pipeline.")
        return "end"
    return "continue"


def graph_builder():
    graph = StateGraph(GraphState)

    graph.add_node("url_agent", url_agent)
    graph.add_node("relevence_agent", relevence_agent)
    graph.add_node("scraper_parcer", scrapper_parcer)
    graph.add_node("duplication_agent", filter_agent)
    graph.add_node("summary_agent", summary_agent)

    graph.set_entry_point("url_agent")
    graph.add_conditional_edges(
        "url_agent",
        check_urls,
        {"continue": "relevence_agent", "end": END}
    )
    graph.add_edge("relevence_agent", "scraper_parcer")
    graph.add_edge("scraper_parcer", "duplication_agent")
    graph.add_conditional_edges(
        "duplication_agent",
        check_pages,
        {"continue": "summary_agent", "end": END}
    )
    graph.add_edge("summary_agent", END)

    return graph.compile()


if __name__ == "__main__":
    a = input("Enter your query: ")
    app = graph.compile()
    result = app.invoke({
        "search": "advanced",
        "query": a,
        "collected_urls": [],
        "parsed_pages": [],
        "filtered_pages": [],
        "verified_pages": [],
        "summaries": [],
        "final_summary": "",
        "errors": [],
        "url_prompt": ""
    })
    print("\n=== FINAL SUMMARY ===")
    print(result.get("final_summary", "No summary generated."))
