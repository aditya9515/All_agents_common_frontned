from langchain.messages import HumanMessage
from agent_structure.state import GraphState
from langchain_ollama import ChatOllama


llm = ChatOllama(model="qwen2.5:0.5b", temperature=0.7, max_tokens=1000)   


def summary_agent(state: GraphState):
    # Combine filtered pages into a manageable context
    context = "\n\n".join([text for text in state["filtered_pages"][:10]])

    print("ADA summary context length:", len(context))
    prompt = f"""Based on the following research documents, provide a final summary regarding: {state['query']}

    Rules:
    - Fact-check the information: If sources contradict, note the discrepancy.
    - Focus on unique insights.
    - Remove marketing fluff.

    Source Documents:
    {context}"""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    print("ADA summary response:", response.content)
    return {"final_summary": response.content}
