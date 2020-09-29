from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

from kivy.uix.slider import Slider

from model import Car

class CarSimApp(App):

    def build(self):
        self.theView = CarView()
        Clock.schedule_interval(self.theView.tick, 1.0/60.0)
        return self.theView

class CarView(GridLayout):
    theCar = Car()
    frontLeft = NumericProperty(0)
    frontRight = NumericProperty(0)
    rearLeft = NumericProperty(0)
    rearRight = NumericProperty(0)
    currentGear = NumericProperty(0)
    throttlePosition = NumericProperty(0)
    fuelMeter = NumericProperty(0)
    currentEngineRpm = StringProperty('000')
    currentWheelRpm = StringProperty('000')

    def tick(self, dt):
        self.updateModel(dt)
        self.updateView()

    def updateModel(self, dt):
        self.theCar.updateModel(dt)

    def updateView(self):
        self.frontLeft = self.theCar.theEngine.theGearbox.wheels['frontLeft'].orientation
        self.frontRight = self.theCar.theEngine.theGearbox.wheels['frontRight'].orientation
        self.rearLeft = self.theCar.theEngine.theGearbox.wheels['rearLeft'].orientation
        self.rearRight = self.theCar.theEngine.theGearbox.wheels['rearRight'].orientation
        self.currentGear = self.theCar.theEngine.theGearbox.currentGear
        self.throttlePosition = self.theCar.theEngine.throttlePosition
        self.fuelMeter = self.theCar.theEngine.theTank.contents
        self.currentEngineRpm = str(round(self.theCar.theEngine.currentRpm)).zfill(3)
        self.currentWheelRpm = str(round(self.theCar.theEngine.currentRpm * self.theCar.theEngine.theGearbox.gears[self.theCar.theEngine.theGearbox.currentGear])).zfill(3)

if __name__ in ('__main__', '__android__'):
    CarSimApp().run()
