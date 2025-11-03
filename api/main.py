from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Internal imports
from utils.scheduler import run_scheduler
from db.db import init_db  # initializes database connection (optional)
from .routes.institutions import router as institutions_router
from .routes.programmes import router as programmes_router

# Load environment variables
load_dotenv()

# --------------------------------------------------
# FastAPI Initialization
# --------------------------------------------------
app = FastAPI(
    title="Institution & Programme API",
    description="API serving universities, TVET colleges, and their programmes",
    version="1.0.0"
)

# --------------------------------------------------
# Middleware
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routes
# --------------------------------------------------
app.include_router(institutions_router, prefix="/institutions", tags=["Institutions"])
app.include_router(programmes_router, prefix="/programmes", tags=["Programmes"])

# --------------------------------------------------
# Root endpoint
# --------------------------------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Institution & Programme API",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# --------------------------------------------------
# Startup and shutdown events
# --------------------------------------------------
@app.on_event("startup")
def startup_event():
    """
    Runs once when the API starts up.
    Initializes database, then launches scraper scheduler in background.
    """
    print("🚀 Starting up Institution & Programme API...")
    
    # Initialize DB
    try:
        init_db()
        print("✅ Database connection established.")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")

    # Start the scraper scheduler
    try:
        run_scheduler(interval="daily", time_str="02:00")
        print("⏳ Scheduler started (runs daily at 02:00).")
    except Exception as e:
        print(f"⚠️ Failed to start scheduler: {e}")


@app.on_event("shutdown")
def shutdown_event():
    print("🛑 API shutting down...")


# --------------------------------------------------
# Entry point (for manual testing)
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
