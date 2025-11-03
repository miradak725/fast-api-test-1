from fastapi import HTTPException, status,APIRouter,Depends
from core.logger import logger
from app.service.analysis_service import AnalysisService
from app.schemas.schemas import AnalyseInput,AnalyseOutput
from sqlmodel import Session
from app.db.db import get_session



import requests
import json
import httpx
import aiohttp
import zstandard as zstd

router = APIRouter()

# @app.get("/call-external")
# async def call_external_api():
#     async with httpx.AsyncClient() as client:
#         response = await client.get("https://api.github.com")
#         return response.json()


# analysis endpoint
@router.post("/create", tags=["Analysis"],response_model=AnalyseOutput, status_code=status.HTTP_201_CREATED)
async def create_analysis(user_id: int, focus_id: int,session:Session = Depends(get_session))->AnalyseOutput:

    try:
        analysis_service = AnalysisService()
        result = await analysis_service.generate_analysis(user_id=user_id, focus_id=focus_id,session=session)
        return result
    except Exception as e:
        logger.exception(f"Error generating analysis for user_id={user_id}, focus_id={focus_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the analysis."
        )

