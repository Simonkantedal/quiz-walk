from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz_walk.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    correct_answer = Column(String)


class UserResponse(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, index=True)
    user_id = Column(String, index=True)
    user_answer = Column(String)
    score = Column(Integer, default=0)


class QuizTeam(Base):
    __tablename__ = "quiz_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, index=True)
    team_score = Column(Integer, nullable=True, default=0)
