from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from citation_retrieval_module_python import CitationRetrievalService # Assuming your service is in this file
import os

app = FastAPI()

class CitationRequest(BaseModel):
    query: str
    num_citations: int = 3

# Initialize the CitationRetrievalService
# It's good practice to get the API key from environment variables in a real app

ncbi_api_key = "your API key"

citation_service = CitationRetrievalService(ncbi_api_key=ncbi_api_key)

# Define POST endpoint
@app.post("/retrieve-citations")
async def retrieve_citations_endpoint(request: CitationRequest):
    try:
        citations = await citation_service.retrieve_and_rank_citations(
            request.query, request.num_citations
        )
        return {"citations": citations}
    except Exception as e:
        # Raise HTTP 500 if any error occurs
        raise HTTPException(status_code=500, detail=str(e))

# Run instructions:
# For development, run using uvicorn:
# uvicorn citation_api:app --reload --host 0.0.0.0 --port 5001
