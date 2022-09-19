import requests
import json

jsn = json

units = { "Temperature": ["CELSIUS_DEGREES","FAHRENHEIT_DEGREES","KELVINS"],
          "Sound": ["DECIBELS","BEATS_PER_MINUTE"],
          "Position":["LATITUDE_DEGREES","LONGITUDE_DEGREES"],
          "Speed, acceleration":["METERS_PER_SECOND","KILOMETERS_PER_HOUR","METERS_PER_SECOND_SQUARED"],
          "Distance":["METERS","KILOMETERS","CENTIMETERS","MILLIMETERS"],
          "Time":["SECONDS"],
          "Storage, speed":["BITS","BITS_PER_SECOND"],
          "Weight":["GRAMS","KILOGRAMS"],
          "Volume":["LITERS","CUBIC_METERS"],
          "Pressure":["PASCAL"],
          "Light":["LUX"],
          "Energy":["VOLTS","MILLIVOLTS","MILLIAMPERES"],
          "Flow":["CUBIC_METERS_PER_SECOND","LITERS_PER_SECOND","CUBIC_METERS_PER_HOUR","LITERS_PER_HOURa","KILOGRAMS_PER_HOUR"],
          "Humidity":["GRAMS_PER_METERS_CUBIC"],
          "Turbidity":["NTU"],
          "Generic":["GENERIC","DEGREES","PERCENTS","UNKNOWN"]}

def manage_response(res):
    if res.status_code != 200:
        print("Send error!")
        print(res.text)
        return None
    else:
        res_json = res.json()
        if "errors" in res_json.keys():
            print("Query error!")
            print(res_json["errors"])
            return None
        else:
            #print("Success!")
            #print(f"res_json:\n{res_json}")
            return res_json

def space_create(target, ten_id, ten_k, name=None):
    if not name:
        print(f"Space must have a name")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key': ten_k}
    query = f"""mutation CREATE_SPACE{{space{{create(input:{{name:\"{name}\"}}){{
    id
    name}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    manage_response(res)

def space_list(target, ten_id, ten_k):
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = """query LIST_SPACES_WITH_POINTS {spaces {edges {node {
    id
    name
    metadata
    points {edges {node {id
    name}}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    if not res:
        return None

    res = manage_response(res)
    ret = []
    for sp in res['data']['spaces']['edges']:
        ret.append({'id':sp['node']['id'], 'name':sp['node']['name'],'metadata':sp['node']['metadata']})

    return ret

def point_create(target, ten_id, ten_k, name=None, space_id=None):
    if not name or not space_id:
        print(f"Point must have a name and a space id.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key': ten_k}
    query =f"""
    mutation
    CREATE_POINT{{ point {{ create(input:{{spaceId:\"{space_id}\"name: \"{name}\"}}){{
        id}}}}}}
    """
    json = {"query": query}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    if not res:
        return None
    else:
        return res['data']['point']['create']['id']

def point_list(target, ten_id, ten_k, space_id=None):
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = """query LIST_SPACES_WITH_POINTS {spaces {edges {node {
    id
    name
    points {edges {node {id
    name
    metadata
    }}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)

    if not res:
        return None

    if space_id:
        return process_point_id(res, space_id)
    else:
        return process_point_all(res)

def process_point_id(res, space_id):
    ret = []
    bId = False
    for sp in res['data']['spaces']['edges']:
        if sp['node']['id'] == space_id:
            bId = True
            for p in sp['node']['points']['edges']:
                ret.append({'id': p['node']['id'], 'name': p['node']['name'], 'metadata': p['node']['metadata']})
        else:
            if bId:
                break
    return ret

def process_point_all(res):
    ret = []
    for sp in res['data']['spaces']['edges']:
        # if sp['node']['id'] == space_id:
        # bId = True
        for p in sp['node']['points']['edges']:
            space = {}
            space['space_id'] = sp['node']['id']
            space['id'] = p['node']['id']
            space['name'] = p['node']['name']
            space['metadata'] = p['node']['metadata']
            ret.append(space)

    return ret

def signal_create(target, ten_id, ten_k, point_id=None, unit=None, value=None,type=None,timestamp=None, metadata=None):
    if not point_id:
        print(f"Point id not specified")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None
    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query =f"""mutation CREATE_SIGNAL{{signal{{create(input:{{
            pointId: \"{point_id}\"
            signals: [
                {{
                    unit: {unit}
                    value: \"{value}\"
                    type: \"{type}\"
                    timestamp: \"{timestamp}\"
                    metadata: {{Signal_strength:\"{metadata['Signal strength']}\",SNR:\"{metadata['SNR']}\"}}
                }}]}}) {{
                    id
                    timestamp
                    createdAt
                    pointId
                    unit
                    type
                    metadata
                    data
                    {{
                        numericValue
                        rawValue }}}}}}}}"""
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    ret = []
    if not res:
        return None
    else:
        for s in res['data']['signal']['create']:
            ret.append({'id':s['id'], "numericValue": s['data']['numericValue'], "rawValue": s['data']['rawValue']})

    return ret

def signal_list(target, ten_id, ten_k, **kwargs):
    if len(kwargs) > 1:
        print(f"Only one parameter can be used at the moment.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    res = None
    if 'point_id' in kwargs:
        res = signal_list_pnt(target, ten_id, ten_k, point_id=kwargs['point_id'])
    elif 'timestamp_start' in kwargs:
        if 'timestamp_end' in kwargs:
            res = signal_list_betw_timestamp(target, ten_id, ten_k, timestamp_start=kwargs['timestamp_start'], timestamp_end=kwargs['timestamp_end'])
        else:
            res = signal_list_after_timestamp(target, ten_id, ten_k, timestamp_start=kwargs['timestamp_start'])
    elif 'timestamp_end' in kwargs:
        res = signal_list_before_timestamp(target, ten_id, ten_k, timestamp_end=kwargs['timestamp_end'])

    return process_res_signal(res)

def process_res_signal(res):
    ret = []
    if res:
        for e in res['data']['signals']['edges']:
            ret.append(e['node'])
            """
            ret.append(
                {'id': e['node']['id'], 'timestamp': e['node']['timestamp'], 'createdAt': e['node']['createdAt'],
                 'pointId': e['node']['pointId'], 'unit': e['node']['unit'], 'type': e['node']['type'],
                 "numericValue": e['node']['data']['numericValue'], "rawValue": e['node']['data']['rawValue']})
            """
    return ret
"""
query GET_MY_POINT{
  points(where: {name:{_EQ:"my-special-point-name"}}) {
    id
    name
  }
}
"""
def signal_list_after_timestamp(target, ten_id, ten_k, timestamp_start = None):
    if not timestamp_start:
        print(f"Specify timestamp.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = f"""query GET_MY_SIGNAL{{
    signals(where: {{timestamp: {{_GT: "{timestamp_start}"}}}}){{
        edges{{
            node{{
                id
                timestamp
                createdAt
                pointId
                unit
                type
                metadata
                data{{
                    numericValue
                    rawValue
                    }}}}}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    return res

def signal_list_betw_timestamp(target, ten_id, ten_k, timestamp_start = None, timestamp_end = None):
    if not timestamp_start:
        print(f"Specify timestamp.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = f"""query GET_MY_SIGNAL{{
    signals(where: {{_AND:[
                            {{timestamp: {{_GT: "{timestamp_start}"}}
                            {{timestamp: {{_LT: "{timestamp_end}"}}
                            ]
                    }}){{
        edges{{
            node{{
                id
                timestamp
                createdAt
                pointId
                unit
                type
                metadata
                data{{
                    numericValue
                    rawValue
                    }}}}}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    return res

def signal_list_before_timestamp(target, ten_id, ten_k, timestamp_end = None):
    if not timestamp_end:
        print(f"Specify timestamp.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = f"""query GET_MY_SIGNAL{{
    signals(where: {{timestamp: {{_LT: "{timestamp_end}"}}}}){{
        edges{{
            node{{
                id
                timestamp
                createdAt
                pointId
                unit
                type
                metadata
                data{{
                    numericValue
                    rawValue
                    }}}}}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    return res

def signal_list_pnt(target, ten_id, ten_k, point_id = None):
    if not point_id:
        print(f"Specify point id.")
        return None
    if not target:
        print(f"Target not specified.")
        return None
    if not ten_id or not ten_k:
        print(f"Target not specified.")
        return None

    headers = {'x-tenant-id': ten_id, 'x-tenant-key':ten_k}
    query = f"""query GET_MY_SIGNAL{{
    signals(
        where: {{pointId: {{_EQ: "{point_id}"}}}}){{
        edges{{
            node{{
                id
                timestamp
                createdAt
                pointId
                unit
                type
                metadata
                data{{
                    numericValue
                    rawValue
                    }}}}}}}}}}
    """
    json = {"query": query, "variables": None}
    res = None
    try:
        res = requests.post(target, json=json, headers=headers)
    except Exception as e:
        print(f"Exception:{e}")

    res = manage_response(res)
    return res
