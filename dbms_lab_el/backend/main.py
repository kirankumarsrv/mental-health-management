from fastapi import FastAPI
from .database import engine, Base
from . import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PTSD Simulation API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import therapist, person, scenario, simulation, reaction, report, auth
from .routers import analytics
from .routers.questionnaire import router as questionnaire_router, assessment_router
from .routers import therapist_dashboard

app.include_router(therapist.router)
app.include_router(therapist_dashboard.router)
app.include_router(person.router)
app.include_router(scenario.router)
app.include_router(simulation.router)
app.include_router(reaction.router)
app.include_router(report.router)
app.include_router(auth.router)
app.include_router(questionnaire_router)
app.include_router(assessment_router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PTSD Agent-Based Simulation System API"}
