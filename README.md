# Bitcoin float gap — public package skeleton

Status: **origin set, retrieval not yet confirmed**. Methodology SHA-256 of `methodology/EQUATIONS.md`: `0d696d010b1ef15bd10b1bfa2e49318b1e9e0935e1efac05e69b91c2bdb4b18f`.

Canonical snapshot: `https://floppykit.github.io/btc-float-public/float.json`. Cloudflare Pages was the named host. `wrangler whoami` was not logged in on 2026-11-13, so this origin is GitHub Pages. A mirror is still allowed. No billing document was returned (`GET /user/settings/billing/actions`, `/packages`, and `/shared-storage` were HTTP 404). No dollar amount is stated. This is not a price target, not an offer, and not a claim that a path will happen.

Machine-readable twins, same directory:

- `audit/baseline.json` — what was actually retrieved
- `audit/SOURCE_AUDIT_2026-11-13.md` — source notes
- `methodology/EQUATIONS.md` — the four published identities and the null rule
- `examples/snapshot.example.json` — the object an agent should ingest
- `examples/snapshot.example.txt` — the same object as one record per line
- `schema/snapshot.schema.json` — draft schema (`$id` is a placeholder until a host exists)

## 1. Claim, bounded

Bitcoin that can still trade is a small share of 21 million, and it does not expand when price rises. If a flow of coins leaves that tradable set and does not come back, the remaining set is smaller. Large enough persistent removal can move price more than a proportional model of the full 21 million would suggest. That is a structural statement about inelastic supply. It is not a schedule.

What this package will show, once the series exist, is the gap between observed sticky absorption and published BTC targets. It will not show a probability of $1,000,000.

Working participation sketch, carried forward as a sketch only: on the order of $8–12 billion a month of sticky demand for about 36 months, from on the order of 4–8 million people at $1–2k a month average, $300–450 billion cumulative. Shorter paths concentrate the coins. Longer paths reduce urgency. None of those USD figures is a BTC quantity. See section 4.

## 2. Baseline that can be cited today

Retrieved 2026-11-13. Detail and conflicts: `audit/SOURCE_AUDIT_2026-11-13.md`.

Spot used for arithmetic: **$68,614** (CoinGecko, `last_updated` 2026-11-13T16:55:44Z). Nearby prints: mempool.space $68,656, blockchain.info $68,585.06, bitcointreasuries.net page $68,594. Circulating supply about **20.11 million BTC**. Max **21 million**. Block subsidy **3.125 BTC**. At 144 blocks/day that is **450 BTC/day** of new supply. Next subsidy drop is 74,386 blocks after height 975,614, about 517 days at 144 blocks/day. Consensus arithmetic, not a forecast of the calendar date.

In-play float, Galaxy Mind public API `https://galaxymind.space/api/float`. Galaxy Mind is an independent project (https://galaxymind.space/about), not Galaxy Digital. They already publish this API, and an MCP endpoint, for agents.

- **FloatStart, locked:** last complete snapshot, **2026-10-10**, `partial: false`: **6,095,921.875 BTC**. The five cohort levels that were removed to produce it (lost 3,000,000, governments 629,722.16470407, ETFs 1,536,618.81639148, public companies 1,064,926.2, other long-term 7,768,732.81890445) are not sticky terms and are not subtracted again. Identity: those five plus FloatStart = mined 20,095,921.875.
- Headline on **2026-11-13**: **6,111,293.75 BTC**, `partial: true`. Not FloatStart. Not float remaining. It equals FloatStart plus issuance since 2026-10-10 (15,371.875) only because the excluded total was frozen at 14,000,000 while ETF, government, and public-company fields were null.
- Page display "≈ $419B" matches 6,111,293.75 × $68,614 = $419.32B. Spot check only.

Post-t0 sticky BTC is `(E_t − E_0) + (C_t − C_0) + S_t` from that same cohort series, and only when S_t is proved disjoint from the other deltas. S_t is null. The cumulative is therefore null. Float remaining is null. It is not FloatStart, and it is not the degraded headline.

ETF cash flows, Farside all-data table, US$ millions, net of redemptions (https://farside.co.uk/bitcoin-etf-flow-all-data/):

- Total row since 11 Jan 2024: **$54,887 million**. Sum of 1-decimal daily cells is $54,886.5 million. Cite the Total row.
- Last complete session, 12 Nov 2026: **−$284.1 million**. The 13 Nov row is a placeholder and is excluded.
- Last 30 sessions (2 Oct–12 Nov 2026): **−$2,780.2 million**.
- Last 90 sessions (9 Jul–12 Nov 2026): **+$3,552.3 million**.
- Trailing 365 calendar days to 12 Nov 2026: **−$5,305.6 million**.

Farside does not publish a "non-redeemed" column, and does not publish BTC. Cumulative net inflow of $54.9B is not the same object as the 1.54M BTC ETF cohort on 2026-10-10.

Other levels, same day, not interchangeable with Galaxy's cohorts:

- bitcointreasuries.net: public companies **1.238M BTC** (197 companies), government entities **645,625 BTC**, a combined "ETFs and Exchanges" bucket **1,615,524 BTC**.
- CoinGlass exchange-balance page: 13 named rows captured, sum **2,594,780.5 BTC**. Not a published total. Galaxy's page said "~2.50M (CoinGlass)". Unreconciled. Neither number enters the snapshot.

Seller census, cited and dropped as a float or discovery input. Block, Inc. Form 10-K for the year ended December 31, 2025 (filed February 26, 2026, accession `0001628280-26-012254`): "more than 4.5 million sellers used the Square ecosystem" that year, for 5.9 billion sales and $250 billion of Square GPV. https://www.sec.gov/Archives/edgar/data/1512673/000162828026012254/xyz-20251231.htm. That is not a live-site count and not `d`. The Q3 2026 Form 10-Q text did not replace it. Same filing: about **8,883 BTC** held for investment as of December 31, 2025, fair value $777.5 million. Company holding. Not an extra subtraction on top of the public-company cohort.

Still absent on purpose: Glassnode (API 401, dropped as an input), a disjoint on-ramp BTC volume (field stays null), any primary quote from Jack Dorsey, any BTC target that means "$1M".

## 3. Equations

Published verbatim. Accounting identities only after units are fixed. Full notes in `methodology/EQUATIONS.md`.

```
Monthly sticky USD ≈ ETF net creations (30d, non-redeemed) + on-ramp self-custody estimate + corporate net adds
Float remaining = FloatStart – cumulative sticky BTC absorbed
Float % removed = cumulative sticky BTC / FloatStart
Time-to-target (months) = (Target BTC removal – cumulative) / trailing 90d average BTC/month
```

Operands are locked in `methodology/EQUATIONS.md`. Hash above. In particular:

- `etf_non_redeemed_usd` is null. `etf_net_flow_usd` for the last 30 Farside sessions is −2,780,200,000.
- `monthly_sticky_usd` is null, because the self-custody and corporate terms are null. The ETF term is not published under the sticky name by itself.
- `float_start_btc` is 6,095,921.875. `float_pct_removed` is null. The 14,000,000 BTC already excluded at the start are not the numerator.
- `months_to_target` is null. Target BTC removal is unset, and the trailing 90-day BTC/month term does not exist.
- `float_remaining_btc` is null. Publishing the start, or the degraded headline, would claim an absorption result the series does not support.

Price models, if added later, are a separate object: `linear_multiplier` or `elasticity`, `is_forecast: false`, parameters published. No model is included in this skeleton.

## 4. USD path is not a BTC path

Constant-spot illustration only, $68,614, not an input to the equations:

| Monthly sticky USD | BTC / month at that spot | 36-month sum | Share of FloatStart 6,095,921.875 |
|---:|---:|---:|---:|
| $8B | 116,594 | 4,197,394 | 68.9% |
| $10B | 145,743 | 5,246,743 | 86.1% |
| $12B | 174,891 | 6,296,091 | 103.3% |

At $1,000,000, $10B buys 10,000 BTC a month, 360,000 BTC in 36 months, 5.9% of FloatStart. The same dollar sketch cannot be both "most of the float" and "the path through $1M" without a price path in between. It is also not `(E_t − E_0)`.

New supply is 450 BTC/day, about 13,500 BTC a month, before the next halving. Absorption shrinks float only above issuance, and only for coins that stay out of the in-play set.

The participation sketch (4–8 million people, $1–2k a month) is a way to talk about breadth. It is not yet a measured on-ramp series. Cash App's public page says balances are 1:1 and withdrawable to self-custody (https://cash.app/bitcoin). It does not publish the withdrawal volume this package would need.

Split, do not blend: self-custody is the term that matches "ordinary participants hold the coins." ETF creations and corporate adds can shrink the tradable set while placing the coins in funds and treasuries. The snapshot keeps those three flows in separate fields.

## 5. Dashboard

One public snapshot, regenerated daily, same equations, three thermometers. Each thermometer is `cumulative sticky BTC / TargetBTCRemoval` for a different target. Labels may say "$1M zone", "$10M zone", and "reserve-scale". The label does not set the denominator. If the target or the cumulative is null, the bar state is `insufficient_series`. It does not render as 0%.

Proposed host, independent of any one company: a static front end (Cloudflare Pages or equivalent), one daily job, one small table (SQLite or hosted Postgres), and two URLs that must not require a session:

- `GET /float.json` — the snapshot object
- `GET /float.txt` — the line format in `examples/snapshot.example.txt`

Also, once they exist: methodology file, input hashes, a diff endpoint that lists threshold crossings (bar state changes, partial flag changes, float crossing a round 100,000 BTC). Mirrors are fine. Cost of the origin is a few dollars a month if the job stays a daily calc over public inputs. No account, no key, no tracker required to read it.

`methodology_sha256` is null until the equation file is locked. Agents should treat a null hash as "this snapshot is a draft."

Mock, as of this skeleton: three empty thermometers, captioned with the labels above, and a single line under them: "No BTC absorption series. ETF net flow, last 30 sessions, −$2.78B (Farside). Float headline 6,111,294 BTC, partial."

## 6. Agent discovery, the part that is math and the part that is not

If an agent samples N pages independently from a corpus where fraction `d` of pages include the pointer:

`P(seen) = 1 − (1 − d)^N`

Checked values: 3% at N=50 is **78%**, not ≥90%. 6% at N=50 is 95%. 3% at N=100 is 95%. 90% at N=50 needs d ≥ 4.50%. 95% at N=100 needs d ≥ 2.95%. The uniform 3–6% sentence does not survive. The table does.

That formula says nothing about Square storefronts unless those storefronts are in the sampled corpus. An agent doing ordinary Bitcoin data retrieval is sampling a different set. HTML comments on merchant sites are unlikely to be in it. A stable JSON URL, a methodology hash, and a pointer on pages that agents already fetch (docs, data lists, the JSON itself) are the mechanism that matches the formula.

Non-rendered pointers are still the right shape if a host does embed one: `link rel="describedby"`, JSON-LD, or an HTML comment. A visible footer is a merchant-facing cost. It is not required for the machine-readable case. Invisible does not mean "present in the retrieval set."

Galaxy Mind already occupies the "search for the float" slot. This package should link to that API and state the difference (sticky-flow gap, split numerator, explicit nulls), not imply the float was unpublished.

## 7. What Block would actually have to do

This is the ask. It is optional. It does not depend on Block agreeing with a price zone.

Primary, small:

1. Legal reads a non-rendered pointer. It contains a URL, a methodology hash, and no product claim, no fee claim, and no customer data.
2. Engineering inserts it in one Block-controlled template that agents already have a reason to fetch: the Square Bitcoin payments document, or the developer document for that product. Not merchant storefronts in the first change.
3. A single flag removes it. Default for any later merchant-template experiment is off until that flag exists.
4. No change to settlement, fees, eligibility, or the $600 transaction note on the current Square page.

Draft pointer, host unset:

```html
<link rel="describedby" href="https://floppykit.github.io/btc-float-public/float.json" type="application/json" />
<!-- btc-float-ref: url=https://floppykit.github.io/btc-float-public/float.json methodology=sha256:0d696d010b1ef15bd10b1bfa2e49318b1e9e0935e1efac05e69b91c2bdb4b18f -->
```

Secondary, separate decision: Block hosts a mirror of `float.json` on a hostname they control. That is a provenance choice (their logs, their uptime, their review of the methodology). It is not required for the primary ask. A mirror that rewrites nulls into zeros is worse than no mirror.

Why this is a small extension of an existing product, stated only as far as the Square page supports it: Square already documents Lightning acceptance, BTC or USD settlement, and a Dashboard switch that can disable Bitcoin payments for a seller (https://squareup.com/us/en/bitcoin, retrieved 2026-11-13). The page's fee language conflicts with itself ("through 2026" and "until 2027" both appear). This ask does not depend on which sentence is current, and it should not repeat either sentence as settled.

What this ask does not include: the 2025 10-K seller sentence as a site count or a discovery rate, a claim that merchant HTML comments produce a 90% discovery probability, or a request that Block endorse a price.

Internal work that remains ordinary, and that this package does not pretend to have done: review of the exact snippet, choice of the injection template, and a decision about whether a third-party URL in a Block document is acceptable. Those are Block's. The package's job is to make the snippet short enough that the review is of a pointer, not of a product.

## 8. Risks that should travel with the package

| Risk | What the package does about it |
|---|---|
| Float definition double-counts ETF and corporate coins | Locked. Those levels are already out of FloatStart. Sticky uses only later deltas from the same fields. Forbidden list is inside the hashed file |
| Degraded upstream presented as live | `partial: true` is mandatory when ETF/gov/company fields are null. Last complete day stays cited |
| USD flow treated as BTC removed | Separate fields. No silent division by spot inside the time-to-target equation |
| Missing series shown as zero | Null rule. Aggregate sticky USD is null if a component is null |
| Fee or seller claims that the source does not support | Square fee conflict quoted, not resolved. 4.5 million is the 2025 10-K sentence only |
| Merchant-site embed sold as discovery math | Discovery math restricted to the corpus actually sampled. Merchant injection is a later, separate experiment |
| Read as financial advice or a promise to Jack | Labels say structural accounting, not a forecast. No probability on $1M |
| Galaxy Mind outage or methodology change | Snapshot stores the input hash and the `degraded` flag. It does not invent the missing cohort |

## 9. Distribution

Not written. Do not post this skeleton.

When the hash is set and the nulls that are still null are labeled as such in the post itself, the post is: one link to `float.txt`, one link to this document, the last complete float, the last 30-session ETF net with its sign, and the ask in section 7. No price call. Search terms and accounts that can reach Block decision-makers belong in that later note, after the canonical URL exists, so the post does not circulate a placeholder host.

## 10. Done, for this slice

- Definition locked. FloatStart 6,095,921.875 BTC. Excluded cohort levels are not in the sticky sum.
- Methodology SHA-256 `0d696d010b1ef15bd10b1bfa2e49318b1e9e0935e1efac05e69b91c2bdb4b18f` recorded in the example snapshot.
- Seller census cited from the 2025 10-K and dropped as a float or discovery input. Glassnode dropped as an input. Self-custody stays null.

Stage 2 reprint matches the saved extracts: `python3 scripts/reprint_audit.py`. Daily job is specified in `ops/DAILY_JOB.md` (Cloudflare Pages, a daily Worker, SQLite) and is not deployed.

Stage 3 is on localhost only: `http://127.0.0.1:8765/float.json` and `http://127.0.0.1:8765/float.txt`. Bars are `insufficient_series`. `http://127.0.0.1:8765/float.diff` reports no partial-flag crossing. Not a public host.

Not done: a non-null BTC absorption series, a public URL, distribution.
