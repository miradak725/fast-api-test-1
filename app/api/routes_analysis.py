from fastapi import HTTPException, status,APIRouter
from app.utils.utils import verify_user
from app.schemas.schemas import analyseModel
from core.logger import logger

router = APIRouter()


@router.post("/create", tags=["Analysis"],response_model=analyseModel)
async def create_analysis(user_id: int, focus_id: int)-> analyseModel:

    if not verify_user(user_id):
        logger.error(f"User verification failed for user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    try:
        logger.debug(f"Generating analysis for user_id={user_id}, focus_id={focus_id}")
        result=analyseModel(
            user_id=user_id,
            focus_id=focus_id,
            analysis="This is a generated analysis."
        )
        logger.info(f"Analysis generated for user_id={user_id}, focus_id={focus_id} successfully")
        return result
    except Exception as e:
        logger.exception(f"Error generating analysis for user_id={user_id}, focus_id={focus_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the analysis."
        )

