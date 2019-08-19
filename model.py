from random import randint

class Car(object):
    def __init__(self):
        self.theEngine = Engine()

    def updateModel(self, dt):
        self.theEngine.updateModel(dt)

class Wheel(object):
    def __init__(self):
        self.orientation = randint(0, 360)

    def rotate(self, revolutions):
        self.orientation = (self.orientation + (revolutions * 360)) % 360

class Engine(object):
    def __init__(self):
        self.theGearbox = Gearbox()
        self.theTank = Tank()

        self.maxRpm = 100
        self.currentRpm = 0
        self.throttlePosition = 0
        self.consumptionConstant = 0.0025

    def updateModel(self, dt):
        if self.theTank.contents > 0:
            self.currentRpm = self.maxRpm * self.throttlePosition
            self.theTank.remove(self.currentRpm * self.consumptionConstant)
            self.theGearbox.rotate(self.currentRpm * (dt / 60))

class Gearbox(object):
    """
    frontLeft = Wheel()
    frontRight = Wheel()
    rearLeft = Wheel()
    rearRight = Wheel()"""

    def __init__(self):
        self.clutchEngaged = False
        self.gears = [0, 0.8, 1, 1.4, 2.2, 3.8]
        self.currentGear = 0
        self.wheels = {}
        for wheel in ['frontLeft', 'frontRight', 'rearLeft', 'rearRight']:
            self.wheels[wheel] = Wheel()

    def shiftUp(self):
        if not self.currentGear == len(self.gears) and not self.clutchEngaged:
            self.currentGear = self.currentGear + 1

    def shiftDown(self):
        if self.currentGear > 0 and not self.clutchEngaged:
            self.currentGear = self.currentGear - 1

    def rotate(self, revolutions):
        if self.clutchEngaged:
            for wheel in self.wheels:
                self.wheels[wheel].rotate(revolutions * self.gears[self.currentGear])

class Tank(object):
    def __init__(self):
        self.capacity = 100
        self.contents = 100

    def remove(self, amount):
        if self.contents > amount:
            self.contents = self.contents - amount
        else:
            self.contents = 0

    def refuel(self):
        self.contents = self.capacity
