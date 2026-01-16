from analysis.capacity_check import run_capacity_check
from analysis.monte_carlo import run_monte_carlo
from analysis.queueing_model import run_queueing_model

def final_decision():
    cap = run_capacity_check()
    mc = run_monte_carlo()
    qm = run_queueing_model()
   
    decisions = [
        mc["decision"],
        qm["decision"],
        cap["decision"]
    ]

    print("\n========= ALGORITHM RESULTS =========")
    print("Capacity Check  :", cap)
    print("Monte Carlo      :", mc)
    print("Queueing Model   :", qm)


    print("\n========= FINAL BUSINESS DECISION =========")

    if decisions.count("BUY") >= 2:
        r="FINAL DECISION: BUY NEW VEHICLES"

    elif "CONSIDER" in decisions:
        r="FINAL DECISION: MONITOR & WAIT"

    else:
        r="FINAL DECISION: DO NOT BUY"
    
    return r

if __name__ == "__main__":
    final_decision()
