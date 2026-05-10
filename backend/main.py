import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import wellness, oportunidades
from app.models.database import create_tables

app = FastAPI()

# CORS configuration for pratarealestate.com.br and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pratarealestate.com.br",
        "http://localhost:3000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(wellness)
app.include_router(oportunidades)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)