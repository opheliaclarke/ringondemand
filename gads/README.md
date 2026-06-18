# RingOnDemand — Google Ads bridge

A read + write bridge to your Google Ads account using the official Google Ads API.

- **Reads** are free (`pull.py`).
- **Writes** are dry-run by default (`mutate.py`); nothing is sent unless you pass `--confirm`.

## One-time setup

### A. Developer token (long pole — request this first, ~1–2 business days)
1. Sign into your **Manager (MCC)** account at ads.google.com.
2. Wrench icon **Tools** → **Setup** → **API Center** (only visible in a Manager account).
3. Accept the API Terms — you'll see a developer token. It starts at **Test** access.
4. Click **Apply for Basic Access** and fill the compliance form
   ("internal tool to manage and report on our own campaigns").
   Test access only works on test accounts — you need **Basic** to touch the live account.

### B. OAuth credentials (do in parallel, ~15 min)
1. console.cloud.google.com → create/select a project.
2. **APIs & Services → Library** → enable **Google Ads API**.
3. **OAuth consent screen** → External → add your Google email as a test user →
   then **Publish to Production** (otherwise the refresh token expires after 7 days).
   Scope needed: `https://www.googleapis.com/auth/adwords`.
4. **Credentials → Create credentials → OAuth client ID → Desktop app.**
   Note the `client_id` and `client_secret`.

### C. Refresh token
On a machine with a browser:
```
pip install -r requirements.txt
python auth.py        # paste client_id/secret, log in once, copy the printed refresh_token
```

### D. Config
```
cp google-ads.example.yaml google-ads.yaml
```
Fill in: `developer_token`, `client_id`, `client_secret`, `refresh_token`,
and `login_customer_id` (your MCC id, digits only). google-ads.yaml is gitignored.

## Usage

Reads (`--customer` = the account id you operate on, digits only):
```
python pull.py --customer 1234567890 search-terms --days 7   > out/terms.csv
python pull.py --customer 1234567890 keywords --days 14
python pull.py --customer 1234567890 campaigns --days 30
python pull.py --customer 1234567890 calls --days 30
python pull.py --customer 1234567890 gaql "SELECT campaign.name FROM campaign"
```

Writes — dry-run prints the operation; `--confirm` applies it:
```
python mutate.py --customer 1234567890 add-negative --campaign-id 111 --text "free estimate" --match phrase
python mutate.py --customer 1234567890 --confirm add-negative --campaign-id 111 --text "free estimate" --match phrase
python mutate.py --customer 1234567890 set-bid --ad-group-id 222 --criterion-id 333 --bid 14.00
python mutate.py --customer 1234567890 pause-keyword --ad-group-id 222 --criterion-id 333
python mutate.py --customer 1234567890 set-budget --budget-id 444 --amount 50.00
```

`criterion-id` / `ad-group-id` come from the `keywords` report. `budget-id` from a
`gaql` query on `campaign_budget`.
