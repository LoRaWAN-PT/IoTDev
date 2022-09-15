import datetime as dt
import configparser
import numpy as np
from Graph_API import *
from Webhook_API import *

confs = configparser.ConfigParser()
confs.read("config_dev.ini")
target = confs['D4API']['target']
ten_id = confs['D4API']['ten_id']
ten_k = confs['D4API']['ten_k_rw']
url = confs['Webhook']['URL']
token = confs['Webhook']['token']

"""
#List all spaces.
sps = space_list(target, ten_id, ten_k)
print(f"spaces:\n{sps}")

#Among the spaces find one which has name "Campus_Porsgrunn".
#In that space find a point named "TEMP_000" and save its id.
pnt_id = None
for s in sps:
    print(f"space:\n{s}")
    if s['name'] == "Campus_Porsgrunn":
        pnts = point_list(target, ten_id, ten_k, space_id=s['id'])
        for p in pnts:
            print(f"point:\n{p}")
            if p['name']=="TEMP_000":
                print(f"Found TEMP_000, save its id.")
                pnt_id = p['id']

#Insert signals with random values for temperature into point "TEMP_000" using its id.
"""
"""
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
#List all signals registered for that point.
signals = signal_list(target, ten_id, ten_k, point_id=pnt_id)
for s in signals:
    print(f"s:\n{s}")
"""

data = get_requests(url, token)
print(f"data:{len(data)}")
for d in data:
    print(f"d:{d}")



