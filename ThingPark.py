import sys, os, struct

imageUrl_temp = "https://www.adeunis.com/wp-content/uploads/2020/07/temperature-capteur-iot-lorawan-sigfox-lpwan-adeunis-temp.jpg"
imageUrl_comfort = "https://www.adeunis.com/wp-content/uploads/2018/10/TEMPERATURE-HUMIDITE3.jpg"
imageUrl_dry_contacts = "https://www.adeunis.com/wp-content/uploads/2017/08/SENSOR-Picto-DRY-CONTACT.png"

class Logger():
    def __init__(self):
        pass


class Instrument():
    def __init__(self, message):
        self.message = message['DevEUI_uplink']
        self.DevEUI = None
        self.name = None
        self.payload = None
        self.appfl2 = 16 # bin: 0b00010000, hex: 0x10
        self.appfl1 = 8 # bin: 0b00001000, hex: 0x08
        if message:
            self.payload = self.message['payload_hex']

        self.msg_type = None
        self.periodic_df = None
        self.metadata = {}
        #Mandatory metadata
        self.metadata['Signal strength'] = ''
        self.metadata['SNR'] = ''
        self.metadata['point_id'] = ''
        self.metadata['imageUrl'] = ''
        self.metadata['timestamp'] = ''
        self.sensors = []

    def fill_meta(self):
        if 'DevEUI' in self.message:
            self.metadata['DevEUI'] = self.message['DevEUI']
        if 'Time' in self.message:
            self.metadata['timestamp'] = self.message['Time']
        if 'LrrRSSI' in self.message:
            self.metadata['Signal strength'] = self.message['LrrRSSI']
        if 'LrrSNR' in self.message:
            self.metadata['SNR'] = self.message['LrrSNR']
        if 'BatteryLevel' in self.message:
            self.metadata['BatteryLevel'] = self.bat_level(int(self.message['BatteryLevel']))
        if 'BatteryTime' in self.message:
            self.metadata['BatteryTime'] = (self.message['BatteryTime'])
        if 'Frequency' in self.message:
            self.metadata['Frequency'] = (self.message['Frequency'])

    def bat_level(self, value):
        return f"{(value - 1)/(253)*100: .2f}"

    def proc_msg(self):
        if not self.message:
            return None

    def def_type(self):
        if not self.payload:
            return None

        bfh = int(self.payload[:2], 16)
        if (bfh & self.periodic_df) == self.periodic_df:
            self.msg_type = "Periodic data frame"

    def def_value(self):
        pass

    def add_sensor(self):
        pass

class Instrument_temp(Instrument):
    def __init__(self,message, *args, **kwargs):
        super().__init__(message)
        self.name = "temp"
        self.periodic_df = int("57", 16)
        self.chnls = self.def_chnls()
        self.metadata['imageUrl'] = imageUrl_temp

    def def_chnls(self):
        bfh = int(self.payload[2:4], 16)
        if (bfh & self.appfl2) == self.appfl2:
            return 2
        else:
            return 1

    def add_sensor(self):
        chn = 0
        while chn < self.chnls:
            self.sensors.append(Sensor_temp())
            self.sensors[chn].metadata['Channel'] = chn+1
            chn+=1

    def def_value(self):
        if not self.sensors:
            return None
        stp = 0
        for s in self.sensors:
            s.value = float(int(struct.unpack('>h', bytes.fromhex(self.payload[4+stp:8+stp]))[0]))/10
            stp+=4

class Instrument_comfort(Instrument):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.name = "comfort"
        self.periodic_df = int("4c",16)
        self.metadata['imageUrl'] = imageUrl_comfort

    def add_sensor(self):
        self.sensors.append(Sensor_temp())
        self.sensors.append(Sensor_rh())

    def def_value(self):
        if not self.sensors:
            return None
        stp = 0
        for isen in range(len(self.sensors)):
            if isen%2 == 0:
                self.sensors[isen].value = float(int(struct.unpack('>h', bytes.fromhex(self.payload[4+stp:8+stp]))[0])) / 10
                #self.sensors[isen].value = float(int(self.payload[4+stp:8+stp],16))/10
                stp+=4
            if isen%2 != 0:
                self.sensors[isen].value = int(self.payload[4+stp:6+stp],16)
                stp+=2

class Instrument_dry_contacts(Instrument):
    def __init__(self,message, *args, **kwargs):
        super().__init__(message)
        self.name = "dry-contacts"
        self.periodic_df = int("40", 16)
        self.chnls = 1
        self.metadata['imageUrl'] = imageUrl_dry_contacts

    def add_sensor(self):
        chn = 0
        while chn < self.chnls:
            self.sensors.append(Sensor_dry_contacts())
            self.sensors[chn].metadata['Channel'] = chn+1
            chn+=1

    """
    payload:40c000080000000000000f
    {
      "frameCounter": 6,
      "configurationDone": false,
      "lowBattery": false,
      "hardwareError": false,
      "commandOutputDone": false,
      "type": "DATA_FRAME",
      "register": {
        "eventCounterOfTor1": 8,
        "eventCounterOfTor2": 0,
        "eventCounterOfTor3": 0,
        "eventCounterOfTor4": 0,
        "currentStateTor1": true,
        "previousFrameStateTor1": true,
        "currentStateTor2": false,
        "previousFrameStateTor2": true,
        "currentStateTor3": false,
        "previousFrameStateTor3": false,
        "currentStateTor4": false,
        "previousFrameStateTor4": false
      }
    }
    """
    def def_value(self):
        if not self.sensors:
            return None
        stp = 0
        for s in self.sensors:
            s.value = int(struct.unpack('>h', bytes.fromhex(self.payload[8+stp:12+stp]))[0])
            s.metadata["eventCounter"] = int(struct.unpack('>h', bytes.fromhex(self.payload[4+stp:8+stp]))[0])
            stp+=4

class Sensor():
    def __init__(self):
        self.unit = None
        self.value = None
        self.type = None
        self.metadata = {}

class Sensor_temp(Sensor):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.unit = "CELSIUS_DEGREES"
        self.type = "Air temperature"

class Sensor_rh(Sensor):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.unit = "PERCENTS"
        self.type = "Humidity"

class Sensor_dry_contacts(Sensor):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.unit = "GENERIC"
        self.type = "Dry_contacts"
