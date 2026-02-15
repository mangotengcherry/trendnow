from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import trends

app = FastAPI(title="Google Trends Visualizer")

origins = [
    "http://localhost:5173", # Vite default port
    "http://localhost:3000",
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
