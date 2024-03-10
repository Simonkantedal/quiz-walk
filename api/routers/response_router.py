from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import UserResponse


router = APIRouter(
    prefix="/quiz-walk/api/response",
    tags=["response"],
    responses={404: {"description": "Not found"}},
)


@router.post("/responses/")
def submit_response(
    question_id: int, user_id: str, user_answer: str, db: Session = Depends(get_db)
):
    db_response = UserResponse(
        question_id=question_id, user_id=user_id, user_answer=user_answer
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response
