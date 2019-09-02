from random import randint

class Car(object):
    pass

class Wheel(object):

    def __init__(self):
        self.orientation = randint(0, 360)

    def rotate(self, revolutions):
        self.orientation = (self.orientation + (revolutions * 360)) % 360

class Engine(object):
    pass

class Gearbox(object):

    def __init__(self):
        self.wheels = {'frontLeft': Wheel(), 'frontRight': Wheel(), 'rearLeft': Wheel(), 'rearRight': Wheel()}
        self.gears = [0, 0.8, 1, 1.4, 2.2, 3.8]
        self.clutchEngaged = False
        self.currentGear = 0

    # Vi glemte koblingen!
    def shiftUp(self):
        if self.currentGear < len(self.gears)-1:
            self.currentGear = self.currentGear + 1

class Tank(object):

    def __init__(self):
        self.capacity = 100
        self.contents = 100

    def refuel(self):
        self.contents = self.capacity

    def remove(self, amount):
        self.contents = self.contents - amount
        if self.contents < 0:
            self.contents = 0
