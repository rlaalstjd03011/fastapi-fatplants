from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

try:
    from .citation_retrieval_module_python import CitationRetrievalService
except ImportError:
    from citation_retrieval_module_python import CitationRetrievalService

import os
import requests

# Router for citation API (instead of creating a new FastAPI app)
router = APIRouter(
    tags=["citationAPI"],
    responses={404: {"description": "Citation API not found"}},
)

# http://localhost:5004/api/retrieve_literature?query=%22testtesttest%22&num_citations=3
@router.get("/api/retrieve_literature")
async def retrieve_citations_endpoint(query: str, num_citations: int = 3):
    try:
        # API key should be loaded from environment variable
        ncbi_api_key = os.getenv("NCBI_API_KEY", "your API key")

        # Service initialized inside the function
        citation_service = CitationRetrievalService(ncbi_api_key=ncbi_api_key)

        citations = await citation_service.retrieve_and_rank_citations(
            requests.query, requests.num_citations
        )
        return {"citations": citations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return f"{query}+{num_citations}"

