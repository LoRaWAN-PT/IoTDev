class Sensor():
    def __init__(self):
        self.unit = None
        self.value = None
        self.type = None
        self.DevEUI = None
        self.metadata = {}
        self.metadata['Signal strength'] = None
        self.metadata['SNR'] = None
        self.metadata['imageUrl'] = None
        self.metadata['point_id'] = None
        self.metadata['timestamp'] = None

class Sensor_temp(Sensor):
    def __init__(self):
        super().__init__()
        self.unit = "CELSIUS_DEGREES"
        self.type = "Air temperature"

class Sensor_rh(Sensor):
    def __init__(self):
        super().__init__()
        self.unit = "PERCENT"
        self.type = "Relative humidity"

class Sensor_comfort(Sensor):
    def __init__(self):
        super().__init__()