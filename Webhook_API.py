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
    d_out=[]
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
    for r in resp_tot:
        #print(f"r['data']:\n{r['data']}")
        #for rd in r['data']:
         #   d_out.append(rd)
        d_out.extend(r['data'])
    resp_tot = d_out
    #print(f"resp_tot:\n{resp_tot}")
    #data = proc_resp_json(resp_tot)
    #return data
    return resp_tot

def clean(token, all=None, uuids=None):
    if (not all and not uuids) or (all and uuids):
        return None

    if all:
        print(f"Clean all!")
        return rq.delete(f"https://webhook.site/token/{token}/request")
        #resp = rq.delete(f"https://webhook.site/token/{token}/request")
        #return resp

    if type(uuids) != list:
        return None
    print(f"Clean uuids only:")
    for iu in uuids:
        print(f"uuid to remove:{iu}")
        rq.delete(f"https://webhook.site/token/{token}/request/{iu}")
        #resp = rq.delete(f"https://webhook.site/token/{token}/request/{iu}")
        #print(f"resp:{resp}")
        #return resp
    print(f"clean finished")
    return
