"""Make CHANGES to Google Ads. DRY-RUN by default — prints the exact operation
and does nothing. Add --confirm to actually apply it.

Subcommands:
    add-negative   --campaign-id ID --text "free estimate" --match phrase
    set-bid        --ad-group-id ID --criterion-id ID --bid 14.00
    pause-keyword  --ad-group-id ID --criterion-id ID
    enable-keyword --ad-group-id ID --criterion-id ID
    set-budget     --budget-id ID --amount 50.00

All commands require --customer (account id, digits only).
Nothing is sent to Google unless --confirm is present.
"""
import argparse

from google.api_core import protobuf_helpers

from _client import load_client, dollars_to_micros, micros_to_dollars

MATCH = {"exact": "EXACT", "phrase": "PHRASE", "broad": "BROAD"}


def _guard(args, summary):
    print("OPERATION:", summary)
    if not args.confirm:
        print("DRY-RUN — nothing sent. Re-run with --confirm to apply.")
        return False
    return True


def add_negative(client, args):
    summary = (f"add NEGATIVE [{args.match}] \"{args.text}\" "
               f"to campaign {args.campaign_id}")
    if not _guard(args, summary):
        return
    svc = client.get_service("CampaignCriterionService")
    op = client.get_type("CampaignCriterionOperation")
    crit = op.create
    crit.campaign = client.get_service("CampaignService").campaign_path(
        args.customer, args.campaign_id)
    crit.negative = True
    crit.keyword.text = args.text
    crit.keyword.match_type = client.enums.KeywordMatchTypeEnum[MATCH[args.match]]
    resp = svc.mutate_campaign_criteria(customer_id=args.customer, operations=[op])
    print("APPLIED:", resp.results[0].resource_name)


def _update_ad_group_criterion(client, args, mutate):
    svc = client.get_service("AdGroupCriterionService")
    op = client.get_type("AdGroupCriterionOperation")
    crit = op.update
    crit.resource_name = svc.ad_group_criterion_path(
        args.customer, args.ad_group_id, args.criterion_id)
    mutate(crit)
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, crit._pb))
    resp = svc.mutate_ad_group_criteria(customer_id=args.customer, operations=[op])
    print("APPLIED:", resp.results[0].resource_name)


def set_bid(client, args):
    summary = (f"set MAX CPC ${args.bid} on keyword "
               f"{args.ad_group_id}~{args.criterion_id}")
    if not _guard(args, summary):
        return
    _update_ad_group_criterion(
        client, args, lambda c: setattr(c, "cpc_bid_micros", dollars_to_micros(args.bid)))


def set_status(client, args, status):
    summary = f"{status} keyword {args.ad_group_id}~{args.criterion_id}"
    if not _guard(args, summary):
        return
    enum = client.enums.AdGroupCriterionStatusEnum[status]
    _update_ad_group_criterion(client, args, lambda c: setattr(c, "status", enum))


def set_budget(client, args):
    summary = f"set DAILY BUDGET ${args.amount} on budget {args.budget_id}"
    if not _guard(args, summary):
        return
    svc = client.get_service("CampaignBudgetService")
    op = client.get_type("CampaignBudgetOperation")
    b = op.update
    b.resource_name = svc.campaign_budget_path(args.customer, args.budget_id)
    b.amount_micros = dollars_to_micros(args.amount)
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, b._pb))
    resp = svc.mutate_campaign_budgets(customer_id=args.customer, operations=[op])
    print("APPLIED:", resp.results[0].resource_name)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--customer", required=True)
    p.add_argument("--confirm", action="store_true", help="actually apply the change")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add-negative")
    a.add_argument("--campaign-id", required=True)
    a.add_argument("--text", required=True)
    a.add_argument("--match", choices=MATCH, default="phrase")

    b = sub.add_parser("set-bid")
    b.add_argument("--ad-group-id", required=True)
    b.add_argument("--criterion-id", required=True)
    b.add_argument("--bid", required=True)

    for name in ("pause-keyword", "enable-keyword"):
        s = sub.add_parser(name)
        s.add_argument("--ad-group-id", required=True)
        s.add_argument("--criterion-id", required=True)

    c = sub.add_parser("set-budget")
    c.add_argument("--budget-id", required=True)
    c.add_argument("--amount", required=True)

    args = p.parse_args()
    client = load_client()

    if args.cmd == "add-negative":
        add_negative(client, args)
    elif args.cmd == "set-bid":
        set_bid(client, args)
    elif args.cmd == "pause-keyword":
        set_status(client, args, "PAUSED")
    elif args.cmd == "enable-keyword":
        set_status(client, args, "ENABLED")
    elif args.cmd == "set-budget":
        set_budget(client, args)


if __name__ == "__main__":
    main()
