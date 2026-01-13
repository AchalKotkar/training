import unittest
from maths import add, divide


class TestMaths(unittest.TestCase):
    """
    This is a TEST CASE
    """

    # ---------- Test Fixture ----------
    def setUp(self):
        # runs BEFORE each test
        print("\nSetting up test")
        self.a = 10
        self.b = 5

    def tearDown(self):
        # runs AFTER each test
        print("Cleaning up test")

    # ---------- Test Methods ----------
    def test_add(self):
        result = add(self.a, self.b)
        self.assertEqual(result, 15)

    def test_divide(self):
        result = divide(self.a, self.b)
        self.assertEqual(result, 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(self.a, 0)


if __name__ == "__main__":
    unittest.main()
