from app.schemas.schemas import AnalyseOutput
from fastapi import HTTPException, status, Depends
from core.logger import logger
from app.utils.utils import verify_user
import httpx
from langchain_core.prompts import ChatPromptTemplate
from app.service.focus_service import FocusService
from app.service.token_service import TokenService
from app.utils import rag_chain
from datetime import datetime
from sqlmodel import Session


import requests

# INTERNAL_API_URL = "http://localhost:8000/api/generate-analysis"
# EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/posts/1"

class AnalysisService:
    def __init__(self):
        self.focus_service = FocusService()
        self.token_service = TokenService()

    async def generate_analysis(self,user_id: int, focus_id: int,session:Session)->AnalyseOutput:
        """Service class to generate analysis for a given user and focus."""

        if not verify_user(user_id):
            logger.error(f"User verification failed for user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
        )
        try:
            logger.debug(f"Generating analysis for user_id={user_id}, focus_id={focus_id}")
            

            # sending request with httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(EXTERNAL_API_URL)
                response.raise_for_status()
                data = response.json()
                logger.debug(f"External API response data: {data}")

            # #sending request with requests
            # response=requests.get(EXTERNAL_API_URL)
            # response.raise_for_status()
            # data=response.json()
            # logger.debug(f"External API response data: {data}") 

            #Sending request with aiohttp.ClientSession
            # async with aiohttp.ClientSession(auto_decompress=False) as session:
            #     try:
            #         async with session.get(EXTERNAL_API_URL, headers={"Accept-Encoding": "zstd"}) as resp:
            #             compressed_data = await resp.read()
            #             encoding = resp.headers.get("Content-Encoding","none")
            #             print("Content-Encoding",encoding)
            #             if encoding == "zstd":
            #                 dctx = zstd.ZstdDecompressor()
            #                 with dctx.stream_reader(compressed_data) as reader:
            #                     data = reader.read().decode("utf-8")
            #             else:
            #                 data = compressed_data.decode("utf-8")
            #             print("data :",data)
                
            #             logger.debug(f"External API response data: {data}")
            #     except Exception as e:
            #         logger.error(f"Error fetching data from external API: {e}")
            #         raise
            #     data=json.loads(data)
            

            #Retrieve reports related to a specific focus id
            focus_details=self.focus_service.get_focus_details(focus_id)
            context= focus_details.reports 
            context_text = "\n\n".join(
                [
                    f"Country: {r.country}\nDescription: {r.description}\nDate: {r.created_at}"
                    for r in context
                ]
            )

            # Define a chat prompt template 
            chat_template= ChatPromptTemplate.from_messages([
                {
                    "role": "system",
                    "content": """Using the given reports included in the context,
                                give a comprehensive analysis report""",
                },
                {
                    "role": "user",
                    "content": f"""Context:{context}""",
                },
            ])
            prompt = chat_template.format(context=context_text)
            logger.debug(f"Prompt{prompt}")
            logger.debug(f"llm :{rag_chain.llm}")

            #Generate response
            response = rag_chain.llm.invoke(prompt)
            logger.debug(f"LLM response: {response}")

            #Update the token count
            token_count = response.usage_metadata["total_tokens"]
            logger.info(f"token count:{token_count}")
            update_tokens = self.token_service.set_token_count(
                user_id,
                datetime.utcnow().month,
                token_count,
                session    
                )

            result=AnalyseOutput(
                user_id=user_id,
                focus_id=focus_id,
                analysis=f"This is a generated analysis.\n{response.content}"
            )
            logger.info(f"Analysis generated for user_id={user_id}, focus_id={focus_id} successfully")
            return result
        except httpx.HTTPError as http_err:
            logger.exception(f"HTTP error occurred while generating analysis for user_id={user_id}, focus_id={focus_id}: {http_err}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to retrieve data from external service."
            )