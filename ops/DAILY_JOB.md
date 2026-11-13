# Daily job spec

Stage 2. Not deployed. No hostname is claimed.

Host, when Stage 4 runs:

| Piece | Name | Role |
|---|---|---|
| Front end and static endpoints | Cloudflare Pages | Serves `/float.json` and `/float.txt`. No account required to read them. |
| Daily calc | Cloudflare Worker cron, once a day | Reads inputs, applies the null rules, writes one row, regenerates the two files. |
| Time series | SQLite on the Worker (or Neon/Supabase if the Worker cannot keep a file) | One row per run. Not a second float definition. |

Cost stays a few dollars a month only if that is the invoice. This spec does not deploy and does not estimate a bill beyond that.

The methodology file is already locked. The job must refuse to write a snapshot if `methodology/EQUATIONS.md` does not hash to `0d696d010b1ef15bd10b1bfa2e49318b1e9e0935e1efac05e69b91c2bdb4b18f`.

## Inputs

Read. Do not derive a second series from a different compiler.

| Input | Use | Not a use |
|---|---|---|
| `GET https://galaxymind.space/api/float` | Cohort levels, `partial`, `degraded`, mined supply, in-play cross-check | Do not subtract in-play from FloatStart |
| Farside all-data table, date and total column | `etf_net_flow_usd` for the last 30 complete sessions, US dollars | Do not convert to BTC. Do not alias to `etf_non_redeemed_usd` |
| `methodology/EQUATIONS.sha256` | Gate. Mismatch aborts the write | |
| `methodology/LOCK.json` | FloatStart and the excluded levels | Those levels are not re-read as flows |

Not inputs, even if a later fetch succeeds: bitcointreasuries.net levels, CoinGlass balances, Glassnode, Block's 8,883 BTC investment, the 4.5 million seller sentence, spot price as a divisor inside the residual.

If Farside or Galaxy does not answer, keep the previous row and set `partial: true` on the new row. Do not copy the last complete residual forward as today's remaining.

## Nulls

`definition_id` is `galaxy-mind-strict-inplay-complete-2026-10-10`.

`float_start_btc` is 6,095,921.875. It does not change because a newer headline printed.

```
etf_net_btc       = E_t - E_0    only if the new row is partial=false and etfs is non-null
corporate_net_btc = C_t - C_0    only if the new row is partial=false and publicCompanies is non-null
self_custody_btc  = null         until a configured primary proves disjointness
```

If any of those three is null, `cumulative_sticky_btc` is null. Then `float_remaining_btc`, `float_pct_removed`, and `trailing_90d_btc_per_month` are null. Do not substitute 0. Do not substitute FloatStart. Do not substitute the Galaxy headline.

`monthly_sticky_usd` is null unless ETF USD, on-ramp USD, and corporate USD are all non-null. ETF USD alone stays in `etf_net_flow_usd`.

`etf_non_redeemed_usd` is null. Farside's net is not that field.

Bars stay `insufficient_series` until `target_btc_removal` is a published number in config. No price label sets it. Unset in this spec.

Issuance, when a mined-supply pair exists, may be stored as `issuance_since_start_btc`. It is not added into remaining while sticky is null. The subsidy rate of 450 BTC/day is not a fill-in.

## Partial flag

`float.partial` is true if any of these hold:

- the Galaxy row used for a delta has `partial: true`
- `etfs` or `publicCompanies` on that row is null
- `cumulative_sticky_btc` is null
- an input fetch failed and the row is a hold-over

A partial row still publishes `etf_net_flow_usd` when the Farside table parsed. That field is an observation, not a residual. The degraded headline may be stored under a cross-check key. It is not `float_remaining_btc`.

## One row

Columns the table must keep, and no others that restate the same coins:

`run_at`, `methodology_sha256`, `definition_id`, `galaxy_as_of`, `galaxy_partial`, `float_start_btc`, `issuance_since_start_btc`, `etf_net_btc`, `corporate_net_btc`, `self_custody_btc`, `cumulative_sticky_btc`, `float_remaining_btc`, `etf_net_flow_usd`, `etf_non_redeemed_usd`, `monthly_sticky_usd`, `partial`, `input_hashes`.

`input_hashes` is the hash of the Galaxy JSON body and the hash of the Farside cells actually summed. A mirror that rewrites a null to 0 is not a valid mirror of this row.

## Check before Stage 3

`python3 scripts/reprint_audit.py` exits 0 and writes `audit/reprint-2026-11-13.json` with `cumulative_sticky_btc` null and the Farside windows equal to `audit/baseline.json`. Stage 3 may serve that object. It may not add a series the script refused.
