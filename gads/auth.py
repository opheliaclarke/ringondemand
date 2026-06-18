"""One-time helper: mint an OAuth refresh token for the Google Ads API.

Run this ONCE on a machine that has a web browser (e.g. your laptop):

    pip install google-auth-oauthlib
    python auth.py

Paste the client_id / client_secret from your OAuth "Desktop app" client.
A browser window opens; log in with the Google account that owns the ads,
approve, and the script prints a refresh_token. Copy it into google-ads.yaml.

Note: set your Cloud OAuth consent screen to "In production" (not "Testing")
before doing this, otherwise the refresh token expires after 7 days.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main():
    client_id = input("OAuth client_id: ").strip()
    client_secret = input("OAuth client_secret: ").strip()
    cfg = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(cfg, scopes=SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    print("\n=== Copy this into google-ads.yaml ===")
    print("refresh_token:", creds.refresh_token)


if __name__ == "__main__":
    main()
