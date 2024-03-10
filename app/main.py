from fastapi import FastAPI

from api.routers import question_router, team_router, response_router

app = FastAPI()

# Include routers
app.include_router(question_router.router)
app.include_router(response_router.router)
app.include_router(team_router.router)
