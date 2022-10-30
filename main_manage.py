import configparser
from Graph_API import *
from Webhook_API import *
from ThingPark import *
from process_json import *

def value_QC_range(min, max, value):
    if (value <= max) and (value >= min):
        return "G"
    else:
        return "B"

def create_instr(data_in, map):
    instr = None
    if not ('DevEUI_uplink' in data_in):
        print(f"line: {sys._getframe().f_lineno}: create_instr: NO DevEUI_uplink")
        return None

    dd = data_in['DevEUI_uplink']

    if not ('DevEUI' in dd):
        print(f"line: {sys._getframe().f_lineno}: create_instr: NO DevEUI")
        return None

    if not (dd['DevEUI'] in map):
        print(f"line: {sys._getframe().f_lineno}: create_instr: DevEUI NOT in map")
        return None

    if not ('DriverCfg' in dd):
        print(f"line: {sys._getframe().f_lineno}: create_instr: NO DriverCfg")
        return None

    if not ('mod' in dd['DriverCfg']):
        print(f"line: {sys._getframe().f_lineno}: create_instr: NO mod")
        return None

    if not ('mId' in dd['DriverCfg']['mod']):
        print(f"line: {sys._getframe().f_lineno}: create_instr: NO mId")
        return None

    if dd['DriverCfg']['mod']['mId'] == "temp":
        instr = Instrument_temp(data_in)
    elif dd['DriverCfg']['mod']['mId'] == "comfort":
        instr = Instrument_comfort(data_in)

    if not instr:
        print(f"line: {sys._getframe().f_lineno}: create_instr: NOT instr")
        return None

    instr.def_type()
    if instr.msg_type != "Periodic data frame":
        print(f"line: {sys._getframe().f_lineno}: create_instr: NOT Periodic data frame")
        return None

    instr.fill_meta()
    instr.metadata['point_id'] = map[instr.metadata['DevEUI']]
    instr.add_sensor()
    instr.def_value()

    return instr

def form_signal_from_instruments(instrs):
    args = []

    for instr in instrs:
        for isen in instr.sensors:
            arguments = {}
            arguments['point_id'] = instr.metadata['point_id']
            arguments['timestamp'] = instr.metadata['timestamp']
            arguments['metadata'] = {}
            arguments['metadata']['Signal strength'] = instr.metadata['Signal strength']
            arguments['metadata']['SNR'] = instr.metadata['SNR']
            arguments['metadata']['imageUrl'] = instr.metadata['imageUrl']
            if 'BatteryLevel' in instr.metadata:
                arguments['metadata']['BatteryLevel'] = instr.metadata['BatteryLevel']

            if 'Channel' in isen.metadata:
                arguments['metadata']['Channel'] = isen.metadata['Channel']

            arguments['unit'] = isen.unit
            arguments['value'] = isen.value
            arguments['type'] = isen.type

            if isen.type == "Air temperature":
                arguments['metadata']['value_QC'] = value_QC_range(-50, 50, arguments['value'])

            if isen.type == "Humidity":
                arguments['metadata']['value_QC'] = value_QC_range(0, 100, arguments['value'])

            args.append(arguments)

    return args

def proc_all_data(data_in,map):
    instrs = []
    cnt = 0
    for d in data_in:
        if cnt>10:
            break
        iinstr = create_instr(d, map)
        if iinstr:
            instrs.append(iinstr)
        cnt+=1

    sgn_data = form_signal_from_instruments(instrs)
    if sgn_data:
        print(f"sgn_data:\n{sgn_data}")
    else:
        print(f"NO sgn_data")

    for sd in sgn_data:
        signal_create(target, ten_id, ten_k, **sd)

#conf_path = "config_dev.ini"
conf_path = "config.ini"
#conf_path = "/home/pi/CodePython/IoTDev/config.ini"
confs = configparser.ConfigParser()
confs.read(conf_path)
target = confs['D4API']['target']
ten_id = confs['D4API']['ten_id']
ten_k = confs['D4API']['ten_k_rw']
url = confs['Webhook']['URL']
token = confs['Webhook']['token']

#Request data from webhook
data = get_requests(url, token)
data_proc = proc_resp_json(data)
if not data_proc:
    print(f"No data!")
    sys.exit()

#Get all points from tenant
pnts = point_list(target,ten_id,ten_k)

#Map devices to points, create a dictionary
map = map_point_device(pnts)
#Register all data from webhook in D4
print(f"map:{map}")

proc_all_data(data_proc, map)

#Remove the saved data from Webhook
uuids = []
for d in data:
    uuids.append(d['uuid'])
clean(token, uuids=uuids)
