"""Direct REST puller for the Google Ads API (v21) using creds.json.
Usage: python3 rest.py <customer_id> "<GAQL query>"
Prints raw JSON results (concatenated across stream batches).
"""
import json, os, sys, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "creds.json")))


def access_token():
    data = urllib.parse.urlencode({
        "client_id": C["client_id"], "client_secret": C["client_secret"],
        "refresh_token": C["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    return json.load(urllib.request.urlopen(req))["access_token"]


def search(customer_id, query, token=None):
    token = token or access_token()
    url = f"https://googleads.googleapis.com/v21/customers/{customer_id}/googleAds:searchStream"
    req = urllib.request.Request(url, data=json.dumps({"query": query}).encode(), headers={
        "Authorization": f"Bearer {token}", "developer-token": C["developer_token"],
        "login-customer-id": C["login_customer_id"], "Content-Type": "application/json",
    })
    try:
        batches = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:2000]); sys.exit(1)
    rows = []
    for b in batches:
        rows.extend(b.get("results", []))
    return rows


if __name__ == "__main__":
    rows = search(sys.argv[1], sys.argv[2])
    print(json.dumps(rows, indent=2))
