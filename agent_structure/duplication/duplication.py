from langchain_ollama import OllamaEmbeddings
from agent_structure.Relevence_checker.relevence_checker import calculate_cosine_similarity
from agent_structure.state import GraphState
import numpy as np


embedding = OllamaEmbeddings(model="nomic-embed-text")


def filter_agent(state: GraphState):
    raw_pages = state["parsed_pages"]
    unique_contents = []

    for page in raw_pages:
        content = page["content"]
        # Basic check: is this too short to be useful?
        if len(content) < 300: 
            continue

        # Semantic check: compare with already accepted pages
        is_duplicate = False
        current_emb = np.array(embedding.embed_query(content[:1000])) # Embed first 1000 chars

        for existing_emb in unique_contents:
            similarity = calculate_cosine_similarity(current_emb, existing_emb['embedding'])
            if similarity > 0.92:  # Threshold for "nearly identical"
                is_duplicate = True
                break

        if not is_duplicate:
            unique_contents.append({"content": content, "embedding": current_emb})

    return {"filtered_pages": [item["content"] for item in unique_contents]}