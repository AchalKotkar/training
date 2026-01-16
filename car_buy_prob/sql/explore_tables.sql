SELECT COUNT(*) FROM "Vehicle";
SELECT COUNT(*) FROM "Driver";

SELECT COUNT(*) 
FROM "Vehicle"
WHERE "currentRentalId" IS NULL;

SELECT
    COUNT(*) FILTER (WHERE "currentRentalId" IS NULL) AS available,
    COUNT(*) FILTER (WHERE "currentRentalId" IS NOT NULL) AS in_use
FROM "Vehicle";

SELECT
    DATE("createdAt") AS date,
    SUM("bookingCount") AS total_demand
FROM "DemandAggregate"
GROUP BY DATE("createdAt")
ORDER BY date;


