from fastapi import APIRouter,HTTPException,status
from app.schemas.schemas import FocusOutput
from app.service.focus_service import FocusService

from core.logger import logger

router=APIRouter()

#Get focus endpoint
@router.get("/{focus_id}")
def get_focus(focus_id:int)->FocusOutput:
    """Return all the data related to a specific focus."""
    try:
        service = FocusService()
        result = service.get_focus_details(focus_id)
        return result
    except Exception as e:
        logger.exception(f"Error retrieving focus details for focus_id={focus_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving focus details."
        )
