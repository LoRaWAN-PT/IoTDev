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
    d_out=[]
    resp_tot = []
    try:
        resp_json = resp.json()
    except Exception as e:
        print(f"ERROR! {e}")
        return None

    resp_tot.append(resp_json)
    page = 1
    while 1:
        if resp_json['total'] > resp_json['to']:
            page+=1
            resp = rq.get(f"{path}&page={page}")
            resp_json = resp.json()
            resp_tot.append(resp_json)
        else:
            break
    for r in resp_tot:
        d_out.extend(r['data'])
    resp_tot = d_out
    return resp_tot

def clean(token, all=None, uuids=None):
    if (not all and not uuids) or (all and uuids):
        return None

    if all:
        print(f"Clean all!")
        return rq.delete(f"https://webhook.site/token/{token}/request")

    if type(uuids) != list:
        return None
    print(f"Clean uuids only:")
    for iu in uuids:
        print(f"uuid to remove:{iu}")
        rq.delete(f"https://webhook.site/token/{token}/request/{iu}")
    print(f"clean finished")
    return
