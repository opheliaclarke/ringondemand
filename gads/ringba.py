"""Pull Ringba call logs and tally plumbing calls per day.
Account: Ring on demand. Creds in ringba_creds.json (gitignored).
Usage: python3 ringba.py <start YYYY-MM-DD> <end YYYY-MM-DD>
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "ringba_creds.json")))
BASE = f"https://api.ringba.com/v2/{C['account_id']}"


def calllogs(start, end, size=500):
    body = json.dumps({
        "reportStart": f"{start}T00:00:00Z", "reportEnd": f"{end}T23:59:59Z",
        "offset": 0, "size": size,
        "valueColumns": [{"column": c} for c in (
            "callDt", "campaignName", "inboundPhoneNumber", "callLengthInSeconds",
            "connectedCallLengthInSeconds", "hasConnected", "hasConverted", "payoutAmount")],
    }).encode()
    req = urllib.request.Request(f"{BASE}/calllogs", data=body, headers={
        "Authorization": f"Token {C['token']}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["report"]["records"]


def day(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).astimezone(
        ).strftime("%Y-%m-%d")


if __name__ == "__main__":
    start, end = sys.argv[1], sys.argv[2]
    recs = [r for r in calllogs(start, end) if "plumb" in r.get("campaignName", "").lower()]
    days = {}
    for r in recs:
        d = days.setdefault(day(r["callDt"]), {"calls": 0, "conn": 0, "conv": 0, "payout": 0.0, "qual60": 0})
        d["calls"] += 1
        if r.get("hasConnected"): d["conn"] += 1
        if r.get("hasConverted"): d["conv"] += 1
        if int(r.get("connectedCallLengthInSeconds", 0) or 0) >= 60: d["qual60"] += 1
        d["payout"] += float(r.get("payoutAmount", 0) or 0)
    print(f"{'date':<12}{'calls':>6}{'connected':>11}{'conv':>6}{'qual60s':>9}{'payout':>9}")
    for d in sorted(days):
        x = days[d]
        print(f"{d:<12}{x['calls']:>6}{x['conn']:>11}{x['conv']:>6}{x['qual60']:>9}{x['payout']:>9.2f}")
    print(f"TOTAL plumbing calls in range: {len(recs)}")
