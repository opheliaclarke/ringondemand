"""Read Google Ads data via GAQL. Prints CSV to stdout (redirect to a file).

Examples:
    python pull.py --customer 1234567890 search-terms --days 7
    python pull.py --customer 1234567890 keywords --days 14
    python pull.py --customer 1234567890 campaigns --days 30
    python pull.py --customer 1234567890 calls --days 30
    python pull.py --customer 1234567890 gaql "SELECT campaign.name FROM campaign"

--customer is the account you operate on (digits only, no dashes).
"""
import argparse
import csv
import sys

from _client import load_client, micros_to_dollars, date_range_clause

PRESETS = {
    "search-terms": lambda d: f"""
        SELECT campaign.name, ad_group.name, search_term_view.search_term,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions
        FROM search_term_view
        WHERE {date_range_clause(d)}
        ORDER BY metrics.cost_micros DESC""",
    "keywords": lambda d: f"""
        SELECT campaign.name, ad_group.name, ad_group_criterion.criterion_id,
               ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
               ad_group_criterion.effective_cpc_bid_micros,
               metrics.clicks, metrics.cost_micros, metrics.average_cpc,
               metrics.conversions
        FROM keyword_view
        WHERE {date_range_clause(d)}
        ORDER BY metrics.cost_micros DESC""",
    "campaigns": lambda d: f"""
        SELECT campaign.name, campaign.status, metrics.impressions, metrics.clicks,
               metrics.cost_micros, metrics.average_cpc, metrics.conversions,
               metrics.cost_per_conversion
        FROM campaign
        WHERE {date_range_clause(d)}
        ORDER BY metrics.cost_micros DESC""",
    "calls": lambda d: f"""
        SELECT campaign.name, segments.conversion_action_name,
               metrics.conversions, metrics.all_conversions, metrics.cost_micros
        FROM campaign
        WHERE {date_range_clause(d)} AND metrics.conversions > 0
        ORDER BY metrics.conversions DESC""",
}

# Fields we render as dollars instead of raw micros.
MICRO_FIELDS = {
    "metrics.cost_micros", "metrics.average_cpc", "metrics.cost_per_conversion",
    "ad_group_criterion.effective_cpc_bid_micros",
}


def flatten(row, fields):
    out = {}
    for f in fields:
        obj = row
        for part in f.split("."):
            obj = getattr(obj, part)
        if f in MICRO_FIELDS:
            obj = micros_to_dollars(obj)
        out[f] = obj
    return out


def field_list(query):
    head = query.upper().split("FROM")[0].replace("SELECT", "")
    return [f.strip() for f in head.split(",") if f.strip()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--customer", required=True, help="account id, digits only")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("report", help="one of: " + ", ".join(PRESETS) + ", or 'gaql'")
    p.add_argument("query", nargs="?", help="raw GAQL when report=gaql")
    args = p.parse_args()

    if args.report == "gaql":
        if not args.query:
            raise SystemExit("gaql requires a query string")
        query = args.query
    elif args.report in PRESETS:
        query = PRESETS[args.report](args.days)
    else:
        raise SystemExit(f"unknown report '{args.report}'")

    client = load_client()
    service = client.get_service("GoogleAdsService")
    fields = field_list(query)
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for batch in service.search_stream(customer_id=args.customer, query=query):
        for row in batch.results:
            writer.writerow(flatten(row, fields))


if __name__ == "__main__":
    main()
