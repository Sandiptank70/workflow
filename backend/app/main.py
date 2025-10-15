from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api import api_router

app = FastAPI(
    title="Workflow Automation Platform",
    description="A modular workflow automation platform with visual workflow builder",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Workflow Automation Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
