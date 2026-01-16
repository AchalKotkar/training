import psycopg2
import random

def run_monte_carlo():
    conn = psycopg2.connect(
        host="localhost",
        database="tmt_analysis",
        user="postgres",
        password="wemotive",
        port=5432
    )
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM "Vehicle"
    WHERE "currentRentalId" IS NULL;
    """)
    available_vehicles = cur.fetchone()[0]

    cur.execute("""
    SELECT DATE("createdAt"), COUNT(*)
    FROM "TourSummary"
    GROUP BY DATE("createdAt");
    """)
    daily_demand = [row[1] for row in cur.fetchall()]

    if not daily_demand:
        return {"avg_lost": 0, "decision": "INSUFFICIENT_DATA"}

    SIMULATIONS = 1000
    lost_bookings = []

    for _ in range(SIMULATIONS):
        demand = random.choice(daily_demand)
        lost = max(0, demand - available_vehicles)
        lost_bookings.append(lost)

    avg_lost = sum(lost_bookings) / SIMULATIONS

    decision = "BUY" if avg_lost > 0 else "HOLD"

    cur.close()
    conn.close()

    print("\navg_lost: ",avg_lost,"\ndecision: ",decision)

    return {
        "avg_lost": avg_lost,
        "decision": decision
    }

if __name__ == "__main__":
    run_monte_carlo()
