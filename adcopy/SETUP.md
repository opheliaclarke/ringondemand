# Campaign Setup — Ring On Demand Plumbing

One campaign per city. Replicate these settings for all 8 (and future cities).

## Structure
- **1 campaign = 1 city = 1 domain**, 3 ad groups (Urgent / Services / Local).
- **Match types:** Exact + Phrase only at launch. No Broad. Don't duplicate a string between exact and phrase.

## Location targeting
- Target the city **+ a 5–8 mile radius** (NOT a narrow zip list — that over-restricts).
- Location option: **"Presence: people in or regularly in your targeted locations."** Not "search interest."
- Campaign-level negative locations: neighboring cities you don't service.

## Bidding (the money math)
- Head terms ("emergency plumber near me") show **"below first page bid $35–97"** on a new account. **Do not pay that.**
- **Breakeven CPC ≈ payout ÷ clicks-per-converted-call** (~$100 ÷ 6 ≈ **$16.67**). Target max CPC ≈ **$12–15** for margin.
- **Cold-start play:** to get the first calls + conversion data, temporarily bid the city's **top-5 crisis terms up to $24–30** for 1–2 weeks. As CTR builds, Quality Score rises and real CPC drops well below Google's "recommended." Then ratchet back down.
- Start **Maximize Clicks (cap $15)** or **Manual CPC**, switch to **Maximize Conversions** after ~15 calls.
- **Mobile bid +20–30%** (emergency plumbing is 70%+ mobile).

## Per-city bid-up shortlist (push these first, $24–30)
- **Torrance:** slab leak repair, emergency plumber open now, burst pipe repair, main sewer line repair, water heater replacement same day
- **Fullerton:** emergency slab leak repair, burst pipe repair emergency, sewer line backup repair, emergency water heater replacement, main water line leak repair
- **Aurora CO:** burst pipe repair emergency, frozen pipe repair, sewer line backup repair, no hot water heater repair, sump pump repair
- **Mission Viejo:** slab leak repair near me, burst pipe repair near me, emergency plumber near me, water heater leaking, sewer line backup repair
- **West Covina:** slab leak repair, emergency plumber near me, burst pipe repair, sewer line backup, water heater replacement same day
- **Pasadena:** emergency plumber near me, burst pipe repair, sewer line backup, slab leak repair, water heater leaking
- **Santa Barbara:** emergency plumber near me, burst pipe repair, slab leak repair, sewer line backup, water heater leaking
- **Garden Grove:** slab leak repair, burst pipe repair near me, main sewer line backup, emergency water heater replacement, 24 hour emergency plumber near me

## Conversion tracking
- **ONE** conversion action across all cities: "Qualified Call — Ringba." Not one per city.
- Ringba → Google Ads offline import via gclid. Per-city attribution comes from campaign structure.
- Count a call as a conversion at 60s+.

## Call assets
- Add the **Ringba number** as a Call asset (campaign level). Enable call reporting.
- Never the client's direct line. Never in the ad headline/description.

## Negatives (3 levels)
- **Shared list `Plumbing_Master_Negs`** (built once, attach to every city): jobs/careers, DIY/how-to/YouTube, retail (Home Depot/Lowe's/parts/Amazon), free/cheap, rental, reddit/wiki, games.
- **Campaign level:** neighboring cities not serviced.
- **Ad-group cross-poll (phrase negs):** route queries to the intended ad group (e.g. "drain cleaning" as phrase neg in Local → pushes it to Services).
- **DIY_Info_Negs** second shared list as a backstop.

## Per-city REMOVE (don't add these keywords)
- **All 7 SoCal cities:** sump pump, well pump, frozen pipe, pipe insulation — no basements, city water, no freeze.
- **Aurora, CO (opposite):** drop slab leak repair/detection (basements, not slab) and well pump. KEEP frozen pipe + sump pump here.
