import json

def proc_resp_json(resp_tot):
    data = []
    if resp_tot:
        for irt in resp_tot:
            if 'content' in irt:
                if irt['content']:
                    data.append(json.loads(irt['content']))
    else:
        print(f"proc_resp_json: not resp_tot: {resp_tot}")
    return data

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
