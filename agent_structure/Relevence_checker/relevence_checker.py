from langchain_ollama import OllamaEmbeddings
from agent_structure.state import GraphState
import numpy as np


embedding = OllamaEmbeddings(model="nomic-embed-text")


def relevence_agent(state: GraphState):
    filter_quesry = embedding.embed_query(state["url_prompt"])
    urls = []
    for i in state["collected_urls"]:
        query = embedding.embed_query(i["description"])
        relevence_score = calculate_cosine_similarity(filter_quesry, query)
        urls.append({"score": relevence_score, "url": i["url"], "description": i["description"]})
    urls = sorted(urls, key=lambda x: x["score"], reverse=True)
    # print("ADA relevence urls is")
    # print(urls[:2])
    with open("agent_structure/Relevence_checker/relevnce.txt", "w", encoding="utf-8", errors="ignore") as f:
        for url in urls:
            f.write(f"Score: {url['score']}, URL: {url['url']}, Description: {url['description']}\n")
    return {"collected_urls": urls}


def calculate_cosine_similarity(vec1, vec2):
    # Convert the standard Python lists to NumPy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    # Calculate the dot product and the norms (magnitude)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    # Return the cosine similarity
    return dot_product / (norm_v1 * norm_v2)
