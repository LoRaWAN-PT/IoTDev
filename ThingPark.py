class Instrument():
    def __init__(self):
        self.DevEUI = None
        self.metadata = {}
        self.metadata['Signal strength'] = None
        self.metadata['SNR'] = None
        self.metadata['point_id'] = None
        self.metadata['imageUrl'] = None

class Sensor():
    def __init__(self):
        self.unit = None
        self.value = None
        self.type = None
        self.DevEUI = None
        self.metadata = {}
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

class Instrument_comfort(Sensor):
    def __init__(self):
        super().__init__()