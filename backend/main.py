from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import trends, auth
from database import engine
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Google Trends Visualizer")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*"  # Allow all origins for production (secure this later if needed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Google Trends Visualizer API is running"}

app.include_router(trends.router)
app.include_router(auth.router)
