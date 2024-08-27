from fastapi import FastAPI
from app.routers import game_session_routes
from app.database import init_db

app = FastAPI()

# Initialize the database connection
init_db(app)

# Include routers
app.include_router(game_session_routes.router, prefix="/game", tags=["Game Session"])
