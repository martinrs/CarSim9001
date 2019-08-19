import unittest
import model

class TankTester(unittest.TestCase):

    def setUp(self):
        self.tank = model.Tank()

    def testInit(self):
        self.assertIsInstance(self.tank.capacity, int)
        self.assertEqual(self.tank.capacity, 100)
        self.assertIsInstance(self.tank.contents, int)
        self.assertEqual(self.tank.contents, 100)

    def testRemove(self):
        toRemove = 50
        self.tank.remove(toRemove)
        self.assertEqual(self.tank.capacity, 100)
        self.assertEqual(self.tank.contents, self.tank.capacity - toRemove)

        self.tank.remove(toRemove)
        self.tank.remove(toRemove)
        self.assertEqual(self.tank.capacity, 100)
        self.assertEqual(self.tank.contents, 0)

    def testRefuel(self):
        self.tank.refuel()
        self.assertEqual(self.tank.capacity, 100)
        self.tank.remove(50)
        self.tank.refuel()
        self.assertEqual(self.tank.capacity, 100)

if __name__ == "__main__":
    unittest.main()
