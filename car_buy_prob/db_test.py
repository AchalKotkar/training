import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="tmt_analysis",
    user="postgres",
    password="wemotive",
    port=5432
)

cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM "Vehicle";')
print(cur.fetchone())

cur.close()
conn.close()
