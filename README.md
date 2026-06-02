# Ring On Demand — Plumbing Pay-Per-Call

Team working repo for the plumbing pay-per-call campaigns (8 cities). **Each city = 1 campaign = 1 domain = 3 ad groups (Urgent / Services / Local).**

🔗 **Live pages:** https://opheliaclarke.github.io/ringondemand/

## What's here

### `adcopy/` — the campaign playbook (implement these in Google Ads)
| File | What it covers |
|------|----------------|
| [README](adcopy/README.md) | Campaign overview, the 8 cities, non-negotiable rules |
| [SETUP](adcopy/SETUP.md) | Geo targeting, conversion tracking, negatives, per-city setup |
| [BIDS](adcopy/BIDS.md) | Max-CPC plan: basic bid + per-city high-intent call-drivers |
| [cities/](adcopy/cities) | Per-city keyword → ad-group mapping + RSA copy (8 files) |

### `site/` — the landing pages
- `site/index.html` — per-city keyword-research dashboard
- `site/west-covina.html`, `site/west-covina-ads.html` — West Covina landing + ads
- `site/littleton/` — Littleton site + assets

## The 3 ad groups (every city)
1. **Urgent** — emergency / 24-7 / same-day / burst-pipe. Highest payout, run 24/7.
2. **Services** — specific high-ticket jobs (slab leak, repipe, sewer, water heater).
3. **Local** — generic hire terms (plumber near me, licensed, residential).

## Non-negotiable rules
- **No city names in keywords** (geo-targeting handles location); city names OK in ad text.
- **No phone numbers in ad text** — Ringba number goes only in the Call asset.
- RSA + Call assets only. One DKI `{KeyWord}` headline per ad. Mind char limits (H≤30, D≤90).
