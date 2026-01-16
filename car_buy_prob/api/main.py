from fastapi import FastAPI
from analysis.capacity_check import run_capacity_check
from analysis.monte_carlo import run_monte_carlo
from analysis.queueing_model import run_queueing_model
from analysis.decision_engine import final_decision

app = FastAPI()

@app.get("/analysis/capacity")
def capacity():
    return run_capacity_check()

@app.get("/analysis/monte-carlo")
def monte_carlo():
    return run_monte_carlo()

@app.get("/analysis/queueing")
def queueing():
    return run_queueing_model()

@app.get("/analysis/decision_engine")
def final():
    return final_decision()
