import json

def proc_resp_json(resp_tot):
    data = []
    for irt in resp_tot:
        if 'content' in irt:
            if irt['content']:
                data_item = {}
                data_item['uuid'] = irt['uuid']
                data_item['content'] = json.loads(irt['content'])
                data.append(data_item)
    return data

"""
        data_0JSON = json.loads(data[idata]['content'])
        #print(f"data_0JSON:\n{data_0JSON}")

        if 'DevEUI_uplink' in data_0JSON:
            data_item['uuid'] = data[idata]['uuid']
            # data_item = json.loads(idata['content'])
            # print(f"idata['content']:\n{idata['content']}")
            #data_0JSON = json.loads(idata['content'])

            data_item['time'] = data_0JSON['DevEUI_uplink']['Time']
            data_item['DevEUI'] = data_0JSON['DevEUI_uplink']['DevEUI']
            data_item['payload'] = data_0JSON['DevEUI_uplink']['payload_hex']
            data_item['time'] = data_0JSON['DevEUI_uplink']['Time']
            if 'DriverCfg' in data_0JSON['DevEUI_uplink']:
                data_item['measurement'] = data_0JSON['DevEUI_uplink']['DriverCfg']['mod']['mId']
            #data[idata] = data_item
            #print(f"data[{idata}]:\n{data[idata]}")
            #print(f"data_item:\n{data_item}")
            data_out.append(data_item)
        
    return data_out
    #return data
"""
def map_point_device(points = None):
    if not points:
        print(f"No points have been provided!")
        return None

    map = {}
    for pnt in points:
        if 'metadata' in pnt:
            if 'DevEUI' in pnt['metadata']:
                map[pnt['metadata']['DevEUI']] = pnt['id']

    return map
