"""
FastAPI application for the VisualResearcher backend.
"""
from fastapi import FastAPI

app = FastAPI(title="VisualResearcher API")

@app.get("/")
def read_root():
    return {"message": "AutoResearch Lab Backend API coming soon"}

# TODO: Claude Code to implement specific endpoints for the experiment runner and timeline UI
