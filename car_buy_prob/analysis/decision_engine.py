from monte_carlo import run_monte_carlo
from queueing_model import run_queueing_model
from capacity_check import run_capacity_check

def final_decision():
    mc = run_monte_carlo()
    qm = run_queueing_model()
    cap = run_capacity_check()

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
        print("FINAL DECISION: BUY NEW VEHICLES")

    elif "CONSIDER" in decisions:
        print("FINAL DECISION: MONITOR & WAIT")

    else:
        print("FINAL DECISION: DO NOT BUY")

if __name__ == "__main__":
    final_decision()
