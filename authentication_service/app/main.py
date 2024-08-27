from fastapi import FastAPI
from app.routers import login_route, signup_route, mfa_route
from app.database import init_db

app = FastAPI()

# Initialize the database connection
init_db(app)

# Include routers
app.include_router(login_route.router, prefix="/login", tags=["Login"])
app.include_router(signup_route.router, prefix="/signup", tags=["Signup"])
app.include_router(mfa_route.router, prefix="/mfa", tags=["MFA"])
