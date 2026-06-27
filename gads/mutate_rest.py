"""Minimal REST mutate for Google Ads v21 using creds.json.
Usage: python3 mutate_rest.py <customer_id> <endpoint> <json-ops-file> [--apply]
Default is validate-only (nothing changes). --apply actually commits.
endpoint e.g. conversionActions:mutate | campaigns:mutate
"""
import json, os, sys, urllib.request, urllib.error
from rest import access_token, C

def mutate(cid, endpoint, body, apply=False):
    body = dict(body)
    body["validateOnly"] = not apply
    url = f"https://googleads.googleapis.com/v21/customers/{cid}/{endpoint}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
        "Authorization": f"Bearer {access_token()}",
        "developer-token": C["developer_token"],
        "login-customer-id": C["login_customer_id"],
        "Content-Type": "application/json",
    })
    try:
        return json.load(urllib.request.urlopen(req)), None
    except urllib.error.HTTPError as e:
        return None, e.read().decode()

if __name__ == "__main__":
    cid, endpoint, f = sys.argv[1], sys.argv[2], sys.argv[3]
    apply = "--apply" in sys.argv
    body = json.load(open(f))
    res, err = mutate(cid, endpoint, body, apply)
    if err:
        print("ERROR:", err[:3000]); sys.exit(1)
    print(("APPLIED" if apply else "VALIDATED-OK"), json.dumps(res, indent=2)[:2000])
