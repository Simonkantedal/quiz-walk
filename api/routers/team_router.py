from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from api import models
from api.database import get_db


router = APIRouter(
    prefix="/quiz-walk/api/team",
    tags=["team"],
    responses={404: {"description": "Not found"}},
)


@router.post("/teams/")
def create_team(team_name: str, db: Session = Depends(get_db)):
    db_team = models.QuizTeam(team_name=team_name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/teams/")
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = db.query(models.QuizTeam).offset(skip).limit(limit).all()
    return teams


@router.get("/teams/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(models.QuizTeam).filter(models.QuizTeam.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.delete("/teams/")
def remove_all_teams(db: Session = Depends(get_db)):
    """
    Endpoint to remove all teams.
    """
    try:
        db.query(models.QuizTeam).delete()
        db.commit()
        return {"message": "All teams removed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/teams/{team_id}")
def remove_team(team_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to remove a single team by its ID.
    """
    try:
        query = db.query(models.QuizTeam).filter(models.QuizTeam.id == team_id)
        db_team = query.first()
        if db_team is None:
            raise HTTPException(status_code=404, detail="Team not found")

        query.delete()
        db.commit()
        return {"message": f"Team with ID {team_id} removed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))