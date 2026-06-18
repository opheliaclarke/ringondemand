"""Shared client loader + helpers."""
import os
from google.ads.googleads.client import GoogleAdsClient

_HERE = os.path.dirname(os.path.abspath(__file__))
_CONFIG = os.path.join(_HERE, "google-ads.yaml")


def load_client():
    if not os.path.exists(_CONFIG):
        raise SystemExit(
            "Missing google-ads.yaml. Copy google-ads.example.yaml and fill it in."
        )
    return GoogleAdsClient.load_from_storage(_CONFIG)


def micros_to_dollars(micros):
    return round((micros or 0) / 1_000_000, 2)


def dollars_to_micros(dollars):
    return int(round(float(dollars) * 1_000_000))


def date_range_clause(days):
    """GAQL clause for the trailing <days> days, ending yesterday."""
    from datetime import date, timedelta
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    return f"segments.date BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'"
