import sys, os
import struct
import time
import datetime as dt
import configparser
import numpy as np
from Graph_API import *
from Webhook_API import *
from process_json import *

temp_imageUrl = "https://www.adeunis.com/wp-content/uploads/2020/07/temperature-capteur-iot-lorawan-sigfox-lpwan-adeunis-temp.jpg"
comfort_imageUrl = "https://www.adeunis.com/wp-content/uploads/2018/10/TEMPERATURE-HUMIDITE3.jpg"

def register_signals(target, ten_id, ten_k, data, points_map):
    for d in data:

        if not 'DevEUI_uplink' in d['content']:
            continue

        dd = d['content']['DevEUI_uplink']
        if not dd['DevEUI'] in points_map:
            print(f"No device DevEUI:{dd['DevEUI']}")
            continue
        args = []

        if dd['DriverCfg']['mod']['mId'] == "temp":
            arguments = {}
            arguments['unit'] = "CELSIUS_DEGREES"

            arguments['value'] = f"{float(struct.unpack('>h',bytes.fromhex(dd['payload_hex'][4:8]))[0])/10}"
            arguments['type'] = "Air temperature"
            arguments['metadata'] = {}
            arguments['metadata']['Signal strength'] = f"{dd['LrrRSSI']}"
            arguments['metadata']['SNR'] = f"{dd['LrrSNR']}"
            arguments['metadata']['imageUrl'] = temp_imageUrl
            arguments['point_id'] = points_map[dd['DevEUI']]
            arguments['timestamp'] = dd['Time']
            args.append(arguments)
        elif dd['DriverCfg']['mod']['mId'] == "comfort":
            arguments = {}
            arguments['unit'] = "CELSIUS_DEGREES"
            arguments['value'] = f"{float(struct.unpack('>h',bytes.fromhex(dd['payload_hex'][4:8]))[0])/10}"
            arguments['type'] = "Air temperature"
            arguments['metadata'] = {}
            arguments['metadata']['Signal strength'] = f"{dd['LrrRSSI']}"
            arguments['metadata']['SNR'] = f"{dd['LrrSNR']}"
            arguments['metadata']['imageUrl'] = comfort_imageUrl
            arguments['point_id'] = points_map[dd['DevEUI']]
            arguments['timestamp'] = dd['Time']
            args.append(arguments)
            arguments = {}
            arguments['unit'] = "PERCENTS"
            arguments['value'] = f"{int.from_bytes(bytes.fromhex(dd['payload_hex'][8:10]), byteorder=sys.byteorder)}"
            arguments['type'] = "Humidity"
            arguments['metadata'] = {}
            arguments['metadata']['Signal strength'] = f"{dd['LrrRSSI']}"
            arguments['metadata']['SNR'] = f"{dd['LrrSNR']}"
            arguments['metadata']['imageUrl'] = comfort_imageUrl
            arguments['point_id'] = points_map[dd['DevEUI']]
            arguments['timestamp'] = dd['Time']
            args.append(arguments)
        else:
            continue

        print(f"args:{args}")
        for a in args:
            signal_create(target, ten_id, ten_k, **a)

#conf_path = "config_dev.ini"
#conf_path = "config.ini"
conf_path = "/home/pi/CodePython/IoTDev/config.ini"
confs = configparser.ConfigParser()
confs.read(conf_path)
target = confs['D4API']['target']
ten_id = confs['D4API']['ten_id']
ten_k = confs['D4API']['ten_k_rw']
url = confs['Webhook']['URL']
token = confs['Webhook']['token']

"""
#List all spaces.
sps = space_list(target, ten_id, ten_k)
print(f"spaces:\n{sps}")
"""
"""
#Among the spaces find one which has name "Campus_Porsgrunn".
#In that space find a point named "TEMP_000" and save its id.
pnt_id = None
for s in sps:
    print(f"space:\n{s}")
    if s['name'] == "Campus_Porsgrunn":
        pnts = point_list(target, ten_id, ten_k, space_id=s['id'])
        for p in pnts:
            print(f"point:\n{p}")
            if p['name']=="USN1":
                print(f"Found USN1, save its id.")
                pnt_id = p['id']
"""
"""
#Insert signals with random values for temperature into point "TEMP_000" using its id.
s_reged = None
if pnt_id :
    for i in range(4):
        s_reged = signal_create(target, ten_id, ten_k, point_id=pnt_id, unit="CELSIUS_DEGREES", value=f"{float(int(np.random.random()*35*100))/100}", type="TEMP", timestamp=dt.datetime.now(dt.timezone.utc).isoformat())
        print(f"s_reged:\n{s_reged}")
        time.sleep(5)
else:
    print(f"Could not find the point!.")
"""
"""
pnt_id = "63230e49eac7b9be6beb2983"

#List all signals registered for that point.
signals = signal_list(target, ten_id, ten_k, point_id=pnt_id)
for signal in signals:
    print(f"signal:\n{signal}")
"""

#Request data from webhook
data = get_requests(url, token)
data_graph = proc_resp_json(get_requests(url, token))
if not data_graph:
    print(f"No data!")
    sys.exit()

#print(f"data:{len(data)}")
for d in data_graph:
    print(f"d:{d}")

#Get all points from tenant
pnts = point_list(target,ten_id,ten_k)
#print(f"pnts:{pnts}")
for p in pnts:
    print(f"p:{p}")

#Map devices to points
map = map_point_device(pnts)
#Register all data from webhook in D4
print(f"map:{map}")
register_signals(target,ten_id,ten_k,data_graph,map)
"""
#Request all signals from one point 
pnt_id = "63230e49eac7b9be6beb2983"
""""""
#List all signals registered for that point.
signals = signal_list(target, ten_id, ten_k, point_id=pnt_id)
for signal in signals:
    print(f"signal:\n{signal}")
"""
#Remove the saved data from Webhook
uuids = []
for d in data:
    uuids.append(d['uuid'])
clean(token, uuids=uuids)
"""
clean(token, uuids=["ca015fa5-a494-4a74-968f-ac55b7e86e4a"])
"""
