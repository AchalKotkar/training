import psycopg2

def run_capacity_check():
    conn = psycopg2.connect(
        host="localhost",
        database="tmt_analysis",
        user="postgres",
        password="wemotive",
        port=5432
    )
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM "Vehicle";')
    total_vehicles = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM "Vehicle"
        WHERE "currentRentalId" IS NULL
        AND TO_TIMESTAMP("permitDueDate" / 1000)::DATE < CURRENT_DATE;
     """)
    available_vehicles = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)::float / COUNT(DISTINCT DATE("createdAt"))
    FROM "TourSummary";
    """)
    avg_daily_demand = cur.fetchone()[0]

    decision = "BUY" if avg_daily_demand > available_vehicles else "HOLD"

    cur.close()
    conn.close()
    print("\navailable: ",available_vehicles,"\navg_demand: ",avg_daily_demand,"\ndecision: ",decision)

    return {
        "available": available_vehicles,
        "avg_demand": avg_daily_demand,
        "decision": decision
    }

if __name__ == "__main__":
    run_capacity_check()
