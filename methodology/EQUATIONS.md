# Equations

Status: **locked 2026-11-13**. This file is the methodology text. Its SHA-256 is stored outside this file, in `EQUATIONS.sha256`. Do not insert the hash here.

The four identities below are published verbatim. They are accounting identities only after the operands in the locked section are used. They are not a price model.

```
Monthly sticky USD ≈ ETF net creations (30d, non-redeemed) + on-ramp self-custody estimate + corporate net adds
Float remaining = FloatStart – cumulative sticky BTC absorbed
Float % removed = cumulative sticky BTC / FloatStart
Time-to-target (months) = (Target BTC removal – cumulative) / trailing 90d average BTC/month
```

## Locked definition

`definition_id`: `galaxy-mind-strict-inplay-complete-2026-10-10`

`residual_path`: `equation`

One residual. The equation path is the one the bars use. A later Galaxy Mind in-play print is a cross-check. It is not a second residual, and it is not then reduced by the sticky sum.

### FloatStart

FloatStart = **6,095,921.875 BTC**

| Field | Value |
|---|---|
| Source | `https://galaxymind.space/api/float` |
| Row | last `partial: false` row |
| date | 2026-10-10 |
| as_of | 2026-10-10T00:15:12.448Z |
| block_height | 970695 |
| mined_supply_btc | 20,095,921.875 |

This number is the residual after the cohort levels below have already been removed. Those levels are the complement of FloatStart. They are not sticky terms. They are not subtracted again from FloatStart, from float remaining, or from any bar.

| Cohort already excluded at t0 | BTC | Role |
|---|---:|---|
| lost | 3,000,000 | Not sticky. Not subtracted again. |
| governments | 629,722.16470407 | Not sticky. Not subtracted again. |
| etfs | 1,536,618.81639148 | Level already out. Only a later delta can enter sticky. |
| publicCompanies | 1,064,926.2 | Level already out. Only a later delta can enter sticky. |
| lthOther | 7,768,732.81890445 | Not a self-custody measure. Not subtracted again. |

Identity, which must hold before any snapshot is published:

```
lost + governments + etfs + publicCompanies + lthOther + FloatStart = mined_supply
3,000,000 + 629,722.16470407 + 1,536,618.81639148 + 1,064,926.2 + 7,768,732.81890445 + 6,095,921.875 = 20,095,921.875
```

The five excluded levels sum to 14,000,000 exactly.

Do not use the 2026-11-13 headline 6,111,293.75 as FloatStart. That row is `partial: true`. Its ETF, government, and public-company fields are null. Its 11,000,000 `lthOther` equals the t0 sum of lthOther + etfs + governments + publicCompanies. It is a folded placeholder, not a new exclusion to subtract.

### Cumulative sticky BTC absorbed

Post-t0 only. One measurement per coin. Levels at t0 do not appear in this sum.

```
cumulative_sticky_btc(t) = (E_t - E_0) + (C_t - C_0) + S_t
```

| Term | Meaning | When it is null |
|---|---|---|
| E_t - E_0 | Change in the Galaxy Mind `etfs` field after t0 | Later row missing, `partial: true`, or `etfs` null |
| C_t - C_0 | Change in the Galaxy Mind `publicCompanies` field after t0 | Later row missing, `partial: true`, or `publicCompanies` null |
| S_t | Self-custody that left the in-play set and is not inside (E_t - E_0), (C_t - C_0), (G_t - G_0), or (H_t - H_0) | No primary series proves that disjointness |

E_t and C_t must come from the same fields that defined E_0 and C_0. A decrease is negative. Do not floor a delta at zero. Redemptions and treasury sales reduce the cumulative.

If any of the three terms is null, `cumulative_sticky_btc` is null. Do not treat a missing term as zero.

S_t is null on this lock. No on-ramp report retrieved for this stage supplied a dated BTC volume that is disjoint from the cohort deltas. Exchange-balance change is not S_t. Cash App custodial balances are not S_t. A survey is not S_t.

### Float remaining

The verbatim line is applied only to the incremental cumulative above. It is not applied to the excluded levels.

Issuance is not absorption. Coins mined after t0 were not in FloatStart and must not be treated as removed. The published evaluation form is:

```
float_remaining_btc = FloatStart - cumulative_sticky_btc + issuance_since_start_btc
```

`issuance_since_start_btc = minedSupply_t - minedSupply_t0`, from the same snapshot pair. It is not filled with 450 BTC/day. The subsidy identity (3.125 × 144 = 450 BTC/day) is a check, not an input.

When `cumulative_sticky_btc` is null, `float_remaining_btc` is null. Do not publish FloatStart as remaining. That would claim zero absorption. Do not publish 6,111,293.75 as remaining either. That print equals FloatStart + 15,371.875, and 15,371.875 is mined supply since t0, because the excluded total was held at 14,000,000 while cohorts were null. It is not evidence that sticky absorption was zero.

### Float percent removed

```
float_pct_removed = cumulative_sticky_btc / FloatStart
```

Numerator is the post-t0 sticky sum only. The 14,000,000 BTC already excluded at t0 are not in the numerator. On t0 the percent is 0 if the cumulative is 0. It is null while the cumulative is null. It is not `(21,000,000 - FloatStart) / 21,000,000`.

### Time-to-target

`Target BTC removal` is a published parameter per bar. A price label does not set it. While it is unset, bar state is `insufficient_series`.

The denominator is the trailing 90-day average of the same post-t0 sticky BTC definition, in BTC/month. It is not Farside USD divided by spot. While that average is null, `months_to_target` is null.

### Monthly sticky USD

Separate observation. Not an input to float remaining.

```
monthly_sticky_usd = etf_net_flow_usd + on_ramp_self_custody_usd + corporate_net_adds_usd
```

only when every term on the right is non-null. Otherwise null.

`etf_non_redeemed_usd` stays null. Farside publishes net flow (creations minus redemptions), in US dollars, not a non-redeemed series and not BTC. Publish that net under `etf_net_flow_usd`. Do not alias it to the non-redeemed field. Do not convert it to BTC and add it to `(E_t - E_0)`.

## Forbidden second subtractions

A coin removed at t0, or counted in one post-t0 delta, is not removed again under another name.

| Do not subtract | Why it would double-count |
|---|---|
| E_0 or C_0 | Already out of FloatStart |
| Lost 3,000,000 | Already out of FloatStart |
| Governments 629,722.16470407 | Already out of FloatStart. Not a sticky term. A later ΔG is a reconciliation item, not a second sticky term |
| lthOther 7,768,732.81890445 | Already out of FloatStart. Not S_t |
| Galaxy in-play after also applying the equation | One residual path. Cross-check only |
| 2026-11-13 headline 6,111,293.75 | Degraded print. Not a second float, not a subtraction from FloatStart |
| Farside USD converted to BTC, if `(E_t - E_0)` is the ETF term | Same coins, second feed |
| bitcointreasuries.net public-company level (1.238M on 2026-11-13) | Different compiler, and the t0 level is already out. Not C_t |
| CoinGlass exchange balances | Not S_t. Outflows include coins that become ETF or corporate holdings |
| Glassnode illiquid or LTH supply | No public series (API 401 without a key on 2026-11-13). Even a later chart is a cross-check of H_0 only, never an added exclusion |
| Block, Inc. bitcoin investment of about 8,883 BTC as of 2025-12-31 | Filing fact, not a float term. If those coins sit inside C_0 they are already out. Do not add 8,883 on top of `publicCompanies` |

## Inputs that are not float terms

Seller census, cited and then dropped as a float or discovery input.

Block, Inc., Form 10-K for the year ended December 31, 2025, filed February 26, 2026, accession `0001628280-26-012254`: "In the year ended December 31, 2025, more than 4.5 million sellers used the Square ecosystem to make 5.9 billion individual sales transactions totaling $250 billion of Square GPV."

https://www.sec.gov/Archives/edgar/data/1512673/000162828026012254/xyz-20251231.htm

That sentence is a 2025 ecosystem count. It is not a count of live sites, not a 2026 census, and not `d` in the discovery formula. The Q3 2026 Form 10-Q text retrieved the same day did not contain a replacement seller-count sentence. Do not promote 4.5 million into either. Reintroducing it as a site count or a coverage input requires a new filing sentence and a new hash.

Same 10-K: "As of December 31, 2025, we held approximately 8,883 bitcoins for long-term investment purposes ("bitcoin investment") with a fair value of $777.5 million." Company holding. Not an additional subtraction. See the forbidden list.

Glassnode: dropped as an input. No public numeric series was retrieved.

On-ramp self-custody: not dropped as a field. Locked at null. No dated primary volume with the disjointness proof was archived in this stage.

## Unit gap (not an input)

USD sticky flow and BTC removal are different quantities. Constant-spot arithmetic at CoinGecko $68,614 (2026-11-13T16:55:44Z) is illustration only. It is not the time-to-target denominator, and it is not `(E_t - E_0)`.

| Monthly USD | BTC / month at that spot | 36-month BTC | Share of FloatStart 6,095,921.875 |
|---:|---:|---:|---:|
| $8B | 116,594.3 | 4,197,394 | 68.9% |
| $10B | 145,742.9 | 5,246,743 | 86.1% |
| $12B | 174,891.4 | 6,296,091 | 103.3% |

At $1,000,000, $10B buys 10,000 BTC / month, 360,000 BTC in 36 months, 5.9% of FloatStart. The dollar sketch is not a bar denominator.

## Price models

Optional and separate. If present:

```
model.kind = "linear_multiplier" | "elasticity"
model.parameters = { ... published numbers ... }
model.is_forecast = false
```

Absent that object, float percent removed is not a price.

## Null rule

Unknown is `null`. It is not `0`, not an interpolation, and not the last complete value copied forward without `partial: true`.
