# host.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_structure.pipeline import graph_builder

app = FastAPI(title="Research Agent API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize once (important for performance)
graph_app = graph_builder()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "Agent API is running"}


@app.post("/run-agent")
def run_agent(request: QueryRequest):
    try:
        result = graph_app.invoke({
            "search": "advanced",
            "query": request.query,
            "collected_urls": [],
            "parsed_pages": [],
            "filtered_pages": [],
            "verified_pages": [],
            "summaries": [],
            "final_summary": "",
            "errors": [],
            "url_prompt": ""
        })

        return {
            "final_summary": result.get("final_summary"),
            "errors": result.get("errors", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))