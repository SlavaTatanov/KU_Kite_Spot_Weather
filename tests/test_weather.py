import unittest
import weather


class TestWind(unittest.TestCase):
    def test_init(self):
        obj = weather.Wind(12.123, 92)
        self.assertEqual(obj.speed, "12.1")
        self.assertEqual(obj.direction, "В ⇐")
        self.assertEqual(obj.gusts, None)
        obj2 = weather.Wind(2.54, 145, 3.3)
        self.assertEqual(obj2.speed, "2.5")
        self.assertEqual(obj2.direction, "ЮВ ⇖")
        self.assertEqual(obj2.gusts, 3.3)

    def test_direction_str(self):
        obj = weather.Wind(5.1, 274)
        self.assertEqual(obj.direction_str(274), "З ⇒")

    def test_str(self):
        pass


if __name__ == '__main__':
    unittest.main()
