from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import UserResponse


class ResponseModel(BaseModel):
    question_id: int
    user_id: str
    user_answer: str


router = APIRouter(
    prefix="/quiz-walk/api/response",
    tags=["response"],
    responses={404: {"description": "Not found"}},
)


@router.post("/responses/")
def submit_response(response_data: ResponseModel, db: Session = Depends(get_db)):
    db_response = UserResponse(
        question_id=response_data.question_id,
        user_id=response_data.user_id,
        user_answer=response_data.user_answer,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@router.get("/responses/")
def get_all_responses(db: Session = Depends(get_db)):
    """
    Endpoint to get all user responses.
    """
    return db.query(UserResponse).all()


@router.delete("/responses/")
def remove_all_responses(db: Session = Depends(get_db)):
    """
    Endpoint to remove all user responses.
    """
    try:
        db.query(UserResponse).delete()
        db.commit()
        return {"message": "All responses removed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/responses/{response_id}")
def remove_response(response_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to remove a single response by its ID.
    """
    try:
        query = db.query(UserResponse).filter(UserResponse.id == response_id)
        db_response = query.first()
        if db_response is None:
            raise HTTPException(status_code=404, detail="Response not found")

        query.delete()
        db.commit()
        return {"message": f"Response with ID {response_id} removed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
