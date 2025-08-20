import unittest
import model

class TankTester(unittest.TestCase):

    def setUp(self):
        self.tank = model.Tank()

    def testInit(self):
        self.assertIsInstance(self.tank.capacity, int)
        self.assertEqual(self.tank.capacity, 500)
        self.assertIsInstance(self.tank.contents, int)
        self.assertEqual(self.tank.contents, 500)

    def testRemove(self):
        # Fjern et normalt beløb
        toRemove = 50
        self.tank.remove(toRemove)
        self.assertEqual(self.tank.capacity, 500)
        self.assertEqual(self.tank.contents, self.tank.capacity - toRemove)

        # Klem ved underløb (kan ikke gå under 0)
        self.tank.remove(10000)
        self.assertEqual(self.tank.capacity, 500)
        self.assertEqual(self.tank.contents, 0)

    def testRemove_negative_amount_increases_contents_current_behavior(self):
        # Dokumentér nuværende adfærd ved negative værdier (forøgelse af indhold)
        self.tank.contents = 400
        self.tank.remove(-25)
        self.assertEqual(self.tank.contents, 425)

    def testRefuel(self):
        # Refuel sætter contents til capacity
        self.tank.contents = 123
        self.tank.refuel()
        self.assertEqual(self.tank.contents, self.tank.capacity)
        self.assertEqual(self.tank.capacity, 500)
        # Gentag sikkerhed
        self.tank.remove(50)
        self.tank.refuel()
        self.assertEqual(self.tank.contents, 500)
        self.assertEqual(self.tank.capacity, 500)


class WheelTester(unittest.TestCase):

    def setUp(self):
        self.wheel = model.Wheel()

    def testInit(self):
        self.assertIsInstance(self.wheel.orientation, int)
        self.assertTrue(0 <= self.wheel.orientation <= 360, 'Wheel position out of bounds')

    def testRotate_various_cases(self):
        # Sæt deterministisk udgangspunkt
        self.wheel.orientation = 10

        # 1 fuld omgang -> samme orientering
        self.wheel.rotate(1)
        self.assertAlmostEqual(self.wheel.orientation, 10)

        # Halv omgang
        self.wheel.rotate(0.5)
        self.assertAlmostEqual(self.wheel.orientation, (10 + 180) % 360)

        # Negativ kvart omgang
        self.wheel.rotate(-0.25)
        self.assertAlmostEqual(self.wheel.orientation, (10 + 180 - 90) % 360)  # 100

        # Stor og ikke-heltals rotation (361 grader)
        self.wheel.rotate(361 / 360.0)
        self.assertAlmostEqual(self.wheel.orientation, (100 + 361) % 360)  # 101


class CarTester(unittest.TestCase):

    def setUp(self):
        self.car = model.Car()

    def testInit(self):
        self.assertIsInstance(self.car.theEngine, model.Engine)

    def testUpdateModel_delegates_to_engine(self):
        # Erstat motoren med en dummy der registrerer kaldet
        class DummyEngine:
            def __init__(self):
                self.calls = []
            def updateModel(self, dt):
                self.calls.append(dt)

        dummy = DummyEngine()
        self.car.theEngine = dummy
        self.car.updateModel(123.45)
        self.assertEqual(dummy.calls, [123.45])


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

    def testUpdateModel_zero_throttle_no_consumption_no_rotation(self):
        start_contents = float(self.engine.theTank.contents)
        # Sørg for at rotation ville kunne ske hvis der var omdrejninger
        self.engine.theGearbox.clutchEngaged = True
        for w in self.engine.theGearbox.wheels.values():
            w.orientation = 30
        self.engine.updateModel(60)
        self.assertEqual(self.engine.currentRpm, 0)
        self.assertAlmostEqual(self.engine.theTank.contents, start_contents)
        # Ingen rotation når rpm=0
        for w in self.engine.theGearbox.wheels.values():
            self.assertAlmostEqual(w.orientation, 30)

    def testUpdateModel_with_throttle_and_fuel(self):
        # rpm og forbrug
        self.engine.throttlePosition = 0.5
        self.engine.theGearbox.currentGear = 5
        self.engine.theGearbox.clutchEngaged = True
        self.engine.theGearbox.wheels['frontLeft'].orientation = 0
        self.engine.updateModel(1)
        self.assertEqual(self.engine.currentRpm, 50)
        self.assertAlmostEqual(self.engine.theTank.contents, 500 - 50 * 0.0025)  # 499.875
        # 50 rpm i 1s -> 50/60 omdr. * 3.8 gear = 3.1666.. omdr. -> 60 grader
        self.assertAlmostEqual(self.engine.theGearbox.wheels['frontLeft'].orientation, 60)

    def testUpdateModel_empty_tank_forces_zero_rpm_and_no_rotation(self):
        self.engine.theTank.contents = 0
        self.engine.throttlePosition = 0.75
        self.engine.theGearbox.currentGear = 5
        self.engine.theGearbox.clutchEngaged = True
        for w in self.engine.theGearbox.wheels.values():
            w.orientation = 0
        self.engine.updateModel(10)
        self.assertEqual(self.engine.currentRpm, 0)
        for w in self.engine.theGearbox.wheels.values():
            self.assertAlmostEqual(w.orientation, 0)
        self.assertEqual(self.engine.theTank.contents, 0)

    def testUpdateModel_multiple_calls_accumulation_and_wrap(self):
        # 100% throttle, gear 2 (ratio 1), kobling inde
        self.engine.throttlePosition = 1.0
        self.engine.theGearbox.currentGear = 2
        self.engine.theGearbox.clutchEngaged = True
        self.engine.theGearbox.wheels['frontLeft'].orientation = 0
        # 60s => 100 rpm * (60/60) = 100 omdr. -> 100*360 deg => 0 mod 360
        self.engine.updateModel(60)
        self.assertAlmostEqual(self.engine.theTank.contents, 500 - 100 * 0.0025)  # 499.75
        self.assertAlmostEqual(self.engine.theGearbox.wheels['frontLeft'].orientation, 0)


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
        self.gearbox.currentGear = 3
        self.gearbox.clutchEngaged = True
        self.gearbox.shiftUp()
        self.assertEqual(self.gearbox.currentGear, 3)

    def testShiftDown_respects_clutch(self):
        self.gearbox.currentGear = 3
        self.gearbox.clutchEngaged = True
        self.gearbox.shiftDown()
        self.assertEqual(self.gearbox.currentGear, 3)
        # Slå kobling fra og skift ned
        self.gearbox.clutchEngaged = False
        self.gearbox.shiftDown()
        self.assertEqual(self.gearbox.currentGear, 2)

    def testShiftDown_to_zero_and_no_below(self):
        self.gearbox.currentGear = 5
        for g in range(5, -1, -1):
            self.assertEqual(self.gearbox.currentGear, g)
            self.gearbox.shiftDown()
        self.gearbox.shiftDown()
        self.assertEqual(self.gearbox.currentGear, 0)

    def testRotate_requires_clutch(self):
        self.gearbox.currentGear = 1
        self.gearbox.clutchEngaged = False
        for w in self.gearbox.wheels.values():
            w.orientation = 0
        self.gearbox.rotate(1)
        # Ingen rotation uden kobling
        for w in self.gearbox.wheels.values():
            self.assertAlmostEqual(w.orientation, 0)

    def testRotate_all_wheels_and_gears(self):
        # Alle hjul roterer ens når kobling er inde
        self.gearbox.clutchEngaged = True

        # Gear 1 (0.8)
        self.gearbox.currentGear = 1
        for w in self.gearbox.wheels.values():
            w.orientation = 0
        self.gearbox.rotate(1)  # 1 * 0.8 omdr -> 288 grader
        for w in self.gearbox.wheels.values():
            self.assertAlmostEqual(w.orientation, 288)

        # Gear 3 (1.4)
        self.gearbox.currentGear = 3
        for w in self.gearbox.wheels.values():
            w.orientation = 0
        self.gearbox.rotate(1)  # 1 * 1.4 omdr -> 504 grader -> 144
        for w in self.gearbox.wheels.values():
            self.assertAlmostEqual(w.orientation, 144)


if __name__ == "__main__":
    unittest.main()
