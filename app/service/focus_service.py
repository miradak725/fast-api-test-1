from app.schemas.schemas import FocusOutput,FocusReport
from core.logger import logger
import requests

EXTERNAL_API_URL = "http://localhost:3000/focus"

class FocusService:
    def __init__(self):
        pass

    def get_focus_details(self,focus_id: int) -> FocusOutput:
        """Service class to get all the data related to specific focus."""
    
        #sending request to external API to get focus details
        try:
            response=requests.get(f"{EXTERNAL_API_URL}/{focus_id}")
            response.raise_for_status()
            data=response.json()
            logger.debug(f"External API response data for focus_id={focus_id}: {data}")
            # return FocusOutput(**data)
        
            return FocusOutput(
                focus_id=focus_id,
                focus_name=data["focus_name"],
                reports=[FocusReport(**report) for report in data.get("reports", [])]
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while fetching focus details from external API for focus_id={focus_id}: {e}")
            raise