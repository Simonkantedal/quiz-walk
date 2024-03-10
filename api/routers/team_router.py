from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from api import models
from api.database import get_db


router = APIRouter(
    prefix="/quiz-walk/api/team",
    tags=["team"],
    responses={404: {"description": "Not found"}},
)


@router.post("/questions/")
def create_team(team_name: str, db: Session = Depends(get_db)):
    db_team = models.QuizTeam(team_name=team_name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/questions/")
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = db.query(models.QuizTeam).offset(skip).limit(limit).all()
    return teams


@router.get("/questions/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(models.QuizTeam).filter(models.QuizTeam.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team
