from nanpy import Stepper
from nanpy import Ultrasonic

defaultMotorSpeed = 5


class Kit:
    def __init__(self, **kwargs):
        self.data = kwargs['data']
        self.id = self.data['_id']


class Rack:
    def __init__(self, **kwargs):
        self.pins = kwargs.get('pins')
        self.serial = kwargs.get('serial')
        self.revsteps = 3800
        self.stepper = Stepper(
            connection=self.serial,
            pin1=self.pins[0],
            pin2=self.pins[1],
            pin3=self.pins[2],
            pin4=self.pins[3],
            revsteps=self.revsteps
        )
        self.step = 0
        if 'speed' in kwargs:
            self.stepper.setSpeed(kwargs.get('speed'))
        else:
            self.stepper.setSpeed(defaultMotorSpeed)
        self.data = kwargs.get('data')
        if('kit' in self.data):
            self.kit = Kit(data=self.data['kit'])
        if('_id' in self.data):
            self.id = self.data['_id']
        if('id' in self.data):
            self.id = self.data['id']

    def step(self, step):
        self.step += step
        self.stepper.step(self.step)

    def nextStep(self):
        self.step += 1
        self.stepper.step(self.step)

    def hasKit(self, kitId):
        return kitId == self.data['kit']['_id']

    def __str__(self):
        return str(self.id)


class Dispenser:

    defaultPins = [[4, 5, 6, 7], [8, 9, 10, 11]]
    pinsIndex = 0  # to assign pins by default

    def __init__(self, **kwargs):
        self.racks = []
        self.detector = "Ultrasonic"
        self.serial = kwargs.get('serial')
        self.data = kwargs.get('data')
        if 'racks' in self.data:
            for rack in self.data['racks']:
                if(len(self.racks) < len(Dispenser.defaultPins)):
                    r = Rack(
                        data=rack,
                        pins=Dispenser.defaultPins[Dispenser.pinsIndex],
                        serial=self.serial
                    )
                    self.racks.append(r)
                Dispenser.pinsIndex += 1
        if '_id' in self.data:
            self.id = self.data['_id']
        if 'id' in self.data:
            self.id = self.data['id']
        self.dispensed = False

    def addRack(self, rack):
        self.racks.append(rack)

    def dispense(self, rack):
        while not self.dispensed:
            rack.nextStep()

    def findRack(self, rackId):
        rackFound = None
        for rack in self.racks:
            if(rackFound == None and rack.id == rackId):
                rackFound = rack
        return rackFound

    def findRackByKit(self, kitId):
        rackFound = None
        for rack in self.racks:
            if(rackFound == None and rack.hasKit(kitId)):
                rackFound = rack
        return rackFound

    def __str__(self):
        return str(self.id)
