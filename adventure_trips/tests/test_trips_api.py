import unittest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_session
from models import AdventureTrip

# -----------------------------
# TEST DATABASE SETUP
# -----------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///test_trips.db"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

TestSessionLocal = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


# -----------------------------
# TEST CASE
# -----------------------------
class TestAdventureTripsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Runs ONCE before all tests
        """
        import asyncio

        async def init_db():
            async with engine_test.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)

        asyncio.run(init_db())
        cls.client = TestClient(app)

    def setUp(self):
        """
        Runs BEFORE each test
        """
        self.trip_data = {
            "name": "Himalayan Trek",
            "destination": "Manali",
            "duration_days": 7,
            "cost": 15000.0,
            "max_people": 10
        }

    # -----------------------------
    # POST /trips
    # -----------------------------
    def test_create_trip(self):
        response = self.client.post("/trips", json=self.trip_data)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.trip_data["name"])
        self.assertIn("id", data)

    # -----------------------------
    # GET /trips
    # -----------------------------
    def test_get_trips(self):
        response = self.client.get("/trips")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # -----------------------------
    # GET /trips/{id}
    # -----------------------------
    def test_get_single_trip(self):
        post_response = self.client.post("/trips", json=self.trip_data)
        trip_id = post_response.json()["id"]

        get_response = self.client.get(f"/trips/{trip_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["id"], trip_id)

    # -----------------------------
    # PATCH /trips/{id}
    # -----------------------------
    def test_update_trip(self):
        post_response = self.client.post("/trips", json=self.trip_data)
        trip_id = post_response.json()["id"]

        update_data = {"cost": 18000.0}
        patch_response = self.client.patch(
            f"/trips/{trip_id}",
            json=update_data
        )

        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["cost"], 18000.0)

    # -----------------------------
    # DELETE /trips/{id}
    # -----------------------------
    def test_delete_trip(self):
        post_response = self.client.post("/trips", json=self.trip_data)
        trip_id = post_response.json()["id"]

        delete_response = self.client.delete(f"/trips/{trip_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            delete_response.json()["message"],
            "Trip deleted successfully"
        )
    
    # Negative test case:
    def test_get_trip_not_found(self):
        response = self.client.get("/trips/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Trip not found")



if __name__ == "__main__":
    unittest.main()
