from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import question_router, team_router, response_router

app = FastAPI()

# Include routers
app.include_router(question_router.router)
app.include_router(response_router.router)
app.include_router(team_router.router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)