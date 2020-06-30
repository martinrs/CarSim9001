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

class WheelTester(unittest.TestCase):

    def setUp(self):
        self.wheel = model.Wheel()

    def testInit(self):
        self.assertIsInstance(self.wheel.orientation, int)
        for i in range(10):
            self.assertTrue(self.wheel.orientation >= 0 and self.wheel.orientation <= 360, 'Wheel position out of bounds')

    def testRotate(self):
        beforeRot = self.wheel.orientation
        self.wheel.rotate(1)
        self.assertEqual(beforeRot, self.wheel.orientation)
        beforeRot = self.wheel.orientation
        self.wheel.rotate(0.5)
        self.assertEqual((beforeRot + (0.5 * 360)) % 360, self.wheel.orientation)
        beforeRot = self.wheel.orientation
        self.wheel.rotate(2.5)
        self.assertEqual((beforeRot + (2.5 * 360)) % 360, self.wheel.orientation)

class CarTester(unittest.TestCase):

    def setUp(self):
        self.car = model.Car()

    def testInit(self):
        self.assertIsInstance(self.car.theEngine, model.Engine)

class EngineTester(unittest.TestCase):

    def setUp(self):
        self.engine = model.Engine()

    def testInit(self):
        self.assertIsInstance(self.engine.theGearbox, model.Gearbox)
        self.assertIsInstance(self.engine.theTank, model.Tank)
        self.assertEqual(self.engine.maxRpm, 100)
        self.assertEqual(self.engine.currentRpm, 0)
        self.assertEqual(self.engine.throttlePosition, 0)
        self.assertEqual(self.engine.consumptionConstant, 0.0025)

    def testUpdateModel(self):
        # Test nul throttle
        self.engine.updateModel(60)
        self.assertEqual(self.engine.currentRpm, 0)
        # Test rpm og forbrug med throttle
        self.engine.throttlePosition = 0.5
        self.engine.updateModel(60)
        self.assertEqual(self.engine.currentRpm, 50)
        self.assertEqual(self.engine.theTank.contents, 99.875)
        # Test korrekt rotation af gearbox
        self.engine.theGearbox.wheels['frontLeft'].orientation = 0
        self.engine.theGearbox.currentGear = 5
        self.engine.theGearbox.clutchEngaged = True
        self.engine.updateModel(1)
        self.assertEqual(self.engine.theGearbox.wheels['frontLeft'].orientation, 60)
        # Gentag tests med tom tank
        self.engine.theTank.contents = 0
        # Test rpm med throttle
        self.engine.throttlePosition = 0.5
        self.engine.updateModel(60)
        self.assertEqual(self.engine.currentRpm, 0)
        # Test korrekt rotation af gearbox
        self.engine.theGearbox.wheels['frontLeft'].orientation = 0
        self.engine.theGearbox.currentGear = 5
        self.engine.theGearbox.clutchEngaged = True
        self.engine.updateModel(1)
        self.assertEqual(self.engine.theGearbox.wheels['frontLeft'].orientation, 0)

class GearboxTester(unittest.TestCase):

    def setUp(self):
        self.gearbox = model.Gearbox()

    def testInit(self):
        self.assertIsInstance(self.gearbox.clutchEngaged, bool)
        self.assertIn(0, self.gearbox.gears)
        self.assertIn(0.8, self.gearbox.gears)
        self.assertIn(1, self.gearbox.gears)
        self.assertIn(1.4, self.gearbox.gears)
        self.assertIn(2.2, self.gearbox.gears)
        self.assertIn(3.8, self.gearbox.gears)
        self.assertEqual(self.gearbox.currentGear, 0)
        self.assertListEqual(['frontLeft', 'frontRight', 'rearLeft', 'rearRight'], list(self.gearbox.wheels.keys()))
        for e in self.gearbox.wheels.values():
            self.assertIsInstance(e, model.Wheel)

    def testShiftUp(self):
        self.assertEqual(self.gearbox.currentGear, 0)
        for g in range(1, 6):
            self.gearbox.shiftUp()
            self.assertEqual(self.gearbox.currentGear, g)
        self.gearbox.shiftUp()
        self.assertEqual(self.gearbox.currentGear, 5)

    def testShiftDown(self):
        self.gearbox.currentGear = 5
        for g in range(5, -1, -1):
            self.assertEqual(self.gearbox.currentGear, g)
            self.gearbox.shiftDown()
        self.gearbox.shiftDown()
        self.assertEqual(self.gearbox.currentGear, 0)

    def testRotate(self):
        self.gearbox.rotate(1)
        beforeRot = self.gearbox.wheels['frontLeft'].orientation
        self.assertEqual(self.gearbox.wheels['frontLeft'].orientation, beforeRot)
        self.gearbox.shiftUp()
        self.gearbox.wheels['frontLeft'].orientation = 0
        self.gearbox.rotate(1)
        self.assertEqual(self.gearbox.wheels['frontLeft'].orientation, 0)
        self.gearbox.wheels['frontLeft'].orientation = 0
        self.gearbox.clutchEngaged = True
        self.gearbox.rotate(1)
        self.assertEqual(self.gearbox.wheels['frontLeft'].orientation, 360 * 0.8)

if __name__ == "__main__":
    unittest.main()
