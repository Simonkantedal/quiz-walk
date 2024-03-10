from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from api import models
from api.database import get_db

router = APIRouter(
    prefix="/quiz-walk/api/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)


@router.post("/questions/")
def create_question(
    question_text: str, correct_answer: str, db: Session = Depends(get_db)
):
    db_question = models.Question(
        question_text=question_text, correct_answer=correct_answer
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/questions/")
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions


@router.get("/questions/{question_id}")
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = (
        db.query(models.Question).filter(models.Question.id == question_id).first()
    )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.delete("/questions/")
def remove_all_questions(db: Session = Depends(get_db)):
    """
    Endpoint to remove all questions.
    """
    try:
        # Delete all questions
        db.query(models.Question).delete()
        db.commit()  # Commit changes
        return {"message": "All questions removed successfully"}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/questions/{question_id}")
def remove_question(question_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to remove a single question by its ID.
    """
    try:
        # Find the question by ID
        query = db.query(models.Question).filter(models.Question.id == question_id)
        db_question = query.first()

        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Remove the question
        query.delete()
        db.commit()  # Commit changes
        return {"message": f"Question with ID {question_id} removed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))
