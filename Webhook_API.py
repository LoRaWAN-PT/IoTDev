import requests as rq
import json

def get_requests(url, token=None, all=True):
    if not token:
        return None

    path = f"{url}/token/{token}"
    if all:
        return get_all_requests(path)

def get_all_requests(url):
    if not url:
        return None

    #path = f"{url}/requests"
    path = f"{url}/requests?per_page=100"
    #path = f"{url}/request/latest"
    resp = rq.get(path)
    #print(f"resp:\n{resp},resp.text:\n{resp.text}")
    """
    resp_json = resp.json()
    print(f"resp_json:\n{resp_json}")
    print(f"resp_json['total']:\n{resp_json['total']}")
    print(f"resp_json['to']:\n{resp_json['to']}")
    """
    resp_tot = []
    try:
        resp_json = resp.json()
    except Exception as e:
        print(f"ERROR! {e}")
        return None

    #print(f"resp_json:\n{resp_json}")
    resp_tot.append(resp_json)
    page = 1
    while 1:
        #print(f"resp_json['total']:{resp_json['total']},resp_json['to']:{resp_json['to']}")
        if resp_json['total'] > resp_json['to']:
            #print(f"resp_json['total']:{resp_json['total']}>resp_json['to']:{resp_json['to']}")
            page+=1
            #path = f"{path}?per_page=100&page={page}"
            #path_req = f"{path}&page={page}"
            #print(f"path:\n{path}")
            #print(f"path_req:\n{path_req}")

            resp = rq.get(f"{path}&page={page}")
            #print(f"resp:\n{resp}")
            resp_json = resp.json()
            #print(f"resp_json:\n{resp_json}")
            resp_tot.append(resp_json)
        else:
            break

    #print(f"resp_tot:\n{resp_tot}")
    data = proc_resp_json(resp_tot)
    return data

def proc_resp_json(resp_tot):
    data = []
    data_out = []
    for irt in resp_tot:
        for idata in irt['data']:
            data_item = {}
            data_item['uuid'] = idata['uuid']
            if 'content' in idata:
                data_item['content'] = idata['content']
            data.append(data_item)

    for idata in range(len(data)):
        data_item = {}
        if not data[idata]['content'] or len(data[idata]['content']) == 0:
            #print(f"idata:\n{idata}")
            continue

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

def clean(token, all=None, uuids=None):
    if (not all and not uuids) or (all and uuids):
        return None

    if all:
        return rq.delete(f"https://webhook.site/token{token}/request")
        #resp = rq.delete(f"https://webhook.site/token{token}/request")
        #return resp

    if type(uuids) != list:
        return None

    for iu in uuids:
        rq.delete(f"https://webhook.site/token{token}/request/{iu}")
        #resp = rq.delete(f"https://webhook.site/token{token}/request/{iu}")
        #return resp
    return
