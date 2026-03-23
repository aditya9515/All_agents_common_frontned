from typing import List
from typing_extensions import TypedDict


class GraphState(TypedDict):

    search: str

    query: str

    collected_urls: List[str]

    url_prompt: str

    parsed_pages: List[dict]

    filtered_pages: List[str]

    verified_pages: List[dict]

    summaries: List[str]

    final_summary: str

    errors: List[str]


if __name__ == "__main__":
    GraphState
