from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.router import router as v1_router

app = FastAPI(title="Bug Bounty Tool API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")
