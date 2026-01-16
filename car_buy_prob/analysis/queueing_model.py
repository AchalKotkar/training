import psycopg2

def run_queueing_model():
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
    servers = cur.fetchone()[0]

    if servers == 0:
        return {"rho": 1.0, "decision": "BUY"}

    cur.execute("""
    SELECT COUNT(*)::float / COUNT(DISTINCT DATE("createdAt"))
    FROM "TourSummary";
    """)
    arrival_rate = cur.fetchone()[0]

    service_rate = 1
    rho = arrival_rate / (servers * service_rate)

    if rho >= 1:
        decision = "BUY"
    elif rho > 0.8:
        decision = "CONSIDER"
    else:
        decision = "HOLD"

    cur.close()
    conn.close()

    return {
        "utilization": rho,
        "decision": decision
    }
