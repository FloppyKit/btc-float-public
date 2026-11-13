# Source audit — 2026-11-13

Retrieval window: 2026-11-13T16:57Z to about 17:05Z. Machine-readable twin: `baseline.json`. This file records what was fetched, what conflicted, and what was not fetched. It does not update the float thesis into a forecast.

Browser session: BrowserClaw CDP at `127.0.0.1:9100`, new tab, existing tabs left alone. Public JSON APIs fetched directly. Farside and Galaxy Mind pages that sit behind a browser check were read through that tab.

## Classification

| Source | Role in the brief | This pass | Use |
|---|---|---|---|
| Farside Investors BTC table and all-data table | Primary ETF flows | Fetched | Cite, with the unit and sign caveats below |
| Galaxy Mind `/api/float` | Free-float / in-play | Fetched | Cite the last *complete* row for cohort math; cite the headline only with `partial: true` |
| Galaxy Mind about page | Identity of the publisher | Fetched | Independent one-person project. Not Galaxy Digital |
| mempool.space, CoinGecko, blockchain.info | Spot, height, mined supply | Fetched | Cross-check only |
| Square Bitcoin page | Product facts for the Block ask | Fetched | Cite product facts; do not pick a fee end-date |
| Cash App Bitcoin page | Self-custody withdrawal claim | Fetched | Qualitative only. No volumes |
| bitcointreasuries.net | Corporate / government / ETF levels | Fetched, page text | Levels only. Buckets are not Galaxy's buckets |
| CoinGlass exchange balances | Liquid exchange subset | Partial render | Named-row sum is not a published total |
| Glassnode | Liquidity cohorts | Not fetched | No number from memory |
| Strike, River | On-ramp aggregates | Not fetched | Leave null |
| Bitcoin Almanack, ByKaranteli | Farside mirrors | Not fetched | Not needed to read Farside itself |
| Block 10-K / 10-Q seller census | "4.5M+ sellers" | Not fetched (SEC HTML 403 on a direct pull; investor pages 403) | Do not repeat 4.5M |
| Jack Dorsey / Block letters | Public thesis quotes | Not fetched | Do not paraphrase as if quoted |

## Spot and supply

- CoinGecko `current_price.usd` **68,614**, `circulating_supply` **20,111,481**, `max_supply` **21,000,000**, `last_updated` **2026-11-13T16:55:44Z**. https://api.coingecko.com/api/v3/coins/bitcoin
- mempool.space prices: **USD 68,656** at unix `1794588902`. https://mempool.space/api/v1/prices
- Tip height **975,695**. https://mempool.space/api/blocks/tip/height
- blockchain.info `totalbc` **20,111,550 BTC**, `market_price_usd` **68,585.06**. https://api.blockchain.info/stats
- Subsidy identity: 3.125 BTC × 144 blocks/day = **450 BTC/day**. Next halving height 1,050,000. From Galaxy's snapshot height 975,614 that is 74,386 blocks, **516.6 days** at 144 blocks/day. Galaxy's page said "517 days" and "450 → 225". The issuance arithmetic checks. The date of the halving does not; it moves with block time.

Degraded in-play 6,111,293.75 × 68,614 = **$419.32B**. Galaxy's page said "≈ $419B". That display matches this spot. It does not make the degraded cohort split usable.

## Float

Publisher: Galaxy Mind, https://galaxymind.space/about — "an independent project built by one person, with no company and no investors." Do not attribute the series to Galaxy Digital.

API: https://galaxymind.space/api/float — no key, `degraded: true` when a cohort is missing, nulls rather than invented values (their API docs, https://galaxymind.space/docs/api). They already expose this to agents, including an MCP endpoint at `https://galaxymind.space/api/mcp/mcp`. A new dashboard is not the first machine-readable float feed. Its job is the sticky-flow gap and the thermometer parameters, with provenance.

Glossary definition of in-play (https://galaxymind.space/glossary/in-play): mined supply minus provably lost coins, government-seized holdings, spot-ETF custody, and public-company treasuries. The same page also says the cut removes the deep-dormant cohort. Both sentences are on the page. The API identity uses both: lost, governments, etfs, publicCompanies, and lthOther.

Last complete row, `partial: false`, date **2026-10-10**:

| Cohort | BTC |
|---|---:|
| mined supply | 20,095,921.875 |
| lost | 3,000,000 |
| governments | 629,722.16470407 |
| etfs | 1,536,618.81639148 |
| public companies | 1,064,926.2 |
| lth other | 7,768,732.81890445 |
| in-play | 6,095,921.875 |

Identity: mined − those five cohorts = in-play. The five cohorts sum to 14,000,000.000. yet-to-mine was 904,078.125 and is not part of mined supply.

Headline at fetch, `partial: true`, `degraded: true`, as-of **2026-11-13T00:15:13.028Z**:

- in-play **6,111,293.75**
- etfs, governments, publicCompanies: **null**
- lost **3,000,000**
- lthOther **11,000,000**
- mined **20,111,293.75**
- `dailyDelta` **+375** (in-play rose; the page text was "375 BTC returned yesterday")

11,000,000 = 7,768,732.81890445 + 1,536,618.81639148 + 629,722.16470407 + 1,064,926.2. The degraded `lthOther` is the 2026-10-10 sum of lth + ETF + government + public companies, folded into one placeholder. In-play then equals mined − 14,000,000, so the headline rose by issuance since 2026-10-10 (**15,371.875 BTC**), not because a live cohort update said float expanded by that much. Citing "LTH is 11.0M" or "ETF cohort is syncing so we ignore it" from today's UI would be wrong. The UI also splits lost into Satoshi 1.10M + lost 1.90M; the API has a single `lost: 3000000`.

Complete history in the payload: 73 non-partial rows from 2026-05-12 to 2026-10-10. Every row since 2026-10-11 in the fetched history is partial. A dashboard that graphs the headline through November without a partial flag is publishing a frozen subtraction.

## ETF flows

Pages: https://farside.co.uk/btc/ and https://farside.co.uk/bitcoin-etf-flow-all-data/

Unit: **US$ millions, net**. The all-data table runs from **11 Jan 2024** (655.3) through a **13 Nov 2026** placeholder. 729 parsed sessions before that placeholder. Published Total row: **54,887**. Sum of the 1-decimal daily totals: **54,886.5**. Cite **54,887**. Farside's own note: the table is generated automatically and they are not liable for errors.

Windows, placeholder day excluded, last complete session **12 Nov 2026 (−284.1)**:

| Window | Sessions | Net US$ millions |
|---|---:|---:|
| Last 30 sessions, 2026-10-02 to 2026-11-12 | 30 | **−2,780.2** |
| of which positive days |  | +2,100.7 |
| of which negative days |  | −4,880.9 |
| Last 90 sessions, 2026-07-09 to 2026-11-12 | 90 | **+3,552.3** |
| Trailing 365 calendar days to 2026-11-12 | 251 | **−5,305.6** |
| Since 2024-01-11, sum of daily cells | 729 | +54,886.5 (cite Total row 54,887) |

"Sustained sticky ETF demand" is not the live 30-day state. Cumulative net creations since launch remain positive. Both sentences have to appear together.

There is no "non-redeemed" series on this table. Net flow already subtracts redemptions. Gross creations are not published here. The first equation's phrase "non-redeemed" is undefined against this source. Implementation: store the net figure under its own name; set the non-redeemed field to null.

These are not BTC flows. Galaxy's 2026-10-10 ETF cohort was 1,536,618.82 BTC. At the 13 Nov spot that notional is about $105B. Cumulative net inflow of $54.9B is a different object (cash in, over a different interval, after redemptions, before mark-to-market). Do not divide one by the other and call the result an average entry price in the public snapshot.

## Other supply pages

bitcointreasuries.net page text, same day:

- Public companies: **1.238M BTC**, **197** companies, **$84.95B**, 30d **−1.2%**
- Government entities: **645,625 BTC**
- "ETFs and Exchanges": **1,615,524 BTC**
- "DeFi and Other": **375,179 BTC**
- Page BTC print: **$68,594**

A news line on the same page said "Strategy Tops 850,000 Bitcoin After Buying 1,036 BTC" (dated November 9, 2026 on the page). That is a headline, not a filing extract. 850,000 plus everyone else can sit inside 1.238M. It does not confirm the 1.238M figure. Galaxy's public-company cohort on 2026-10-10 was 1,064,926 BTC. The gap to 1.238M is 34 days and a different compiler. Unreconciled. Do not average them.

CoinGlass https://www.coinglass.com/Balance rendered 13 named exchange rows summing to **2,594,780.5 BTC** (Coinbase Pro 868,254.48 through Coinone 6,513.83). Galaxy's float page said exchange reserves "sit at ~2.50M (CoinGlass)". Those are not the same measurement. The 13-row sum is a capture, not CoinGlass's published total, and the table may continue. Leave both figures in the audit. Do not pick one for the snapshot.

Glassnode was not opened. No Glassnode number appears in `baseline.json`.

## Square / Block product page

https://squareup.com/us/en/bitcoin, retrieved 2026-11-13. Meta description: "Start accepting Bitcoin Payments with Square — seamless settlement, no processing fees, and easy access to your funds."

Verbatim conflicts, all on that page:

- "Bitcoin payments can be received as either bitcoin or USD, and both benefit from the same 0% processing fee through 2026."
- "get zero processing fees until 2027"
- "Bitcoin payments are fee-free until 2027, and a flat 1% after that."
- "0% fees through 2026, then 1% per transaction"

A forwardable note says the page conflicts. It does not choose 2026 or 2027.

Other sentences used, shortened only by the extraction window, not rewritten:

- Payments use the Lightning Network. The page says they settle in seconds.
- "Bitcoin payments may be automatically enabled for eligible sellers. You can change your settlement preferences or disable the feature anytime in your Dashboard."
- Conversions: up to 50% of daily net card sales, 1% fee on the converted amount. Worked example on the page: 10% of $1,000 → $99 of bitcoin and a $1 fee.
- "Bitcoin payments are currently supported for transactions up to $600."
- Survey lines ("12% of sales are set aside…", "29.2% of Square sellers are exploring…", "89% of interested Square sellers…") are attributed on the page to "Bitcoin Conversions Survey for Square". No sample size was in the extract. Not a census.

https://cash.app/bitcoin, same day: Lightning sends; "every bitcoin is held 1:1"; withdraw to a self-custody wallet. No volume.

Not found this pass, and therefore not in the public skeleton as facts:

- 4.5 million sellers
- hundreds of thousands of live Square sites
- a measured default-on rate

Latest Block filings exist (10-K for year ended 2025-12-31, filed 2026-02-26, accession `0001628280-26-012254`; 10-Q for quarter ended 2026-09-30, filed 2026-11-03). The HTML was not retrieved. Seller count stays open.

## Coverage math, checked

Assumption, which the brief's 3–6% line does not state: each of N page draws is independent, with replacement, from a corpus in which fraction `d` of pages carry the pointer.

`P(seen) = 1 − (1 − d)^N`

| N | d | P(seen) |
|---:|---:|---:|
| 50 | 3.0% | 78.2% |
| 50 | 4.50% | 90.0% |
| 50 | 6.0% | 95.5% |
| 100 | 2.28% | 90.0% |
| 100 | 2.95% | 95.0% |
| 100 | 3.0% | 95.2% |
| 100 | 6.0% | 99.8% |

Thresholds: N=50 needs d ≥ 4.50% for 90% and d ≥ 5.82% for 95%. N=100 needs d ≥ 2.28% for 90% and d ≥ 2.95% for 95%. The brief's "3–6% already yields ≥90–95% for N=50–100" is true at the corners (about 6% at N=50, about 3% at N=100) and false for 3% at N=50. Publish the table. Do not publish the sentence.

Second assumption, also required: the N pages are drawn from the corpus that contains the embeds. An agent retrieving Bitcoin data pages does not sample Square merchant storefronts. HTML comments are a weak fit for that corpus even if a crawler downloads the HTML. `rel=describedby` / JSON-LD on a page the agent already fetches is a stronger fit. Merchant-site injection is a different experiment (referring-host count, possible indexation, possible template risk). It is not the 90% calculation.

Galaxy Mind's public API is already inside the corpus an agent is likely to hit if it searches "bitcoin float". Embedding density on merchant sites does not raise that probability. A canonical URL listed next to that API, on Block's own Bitcoin docs, might.

## Sample calculations that are allowed

1. Farside last-30-session net = **−$2,780.2 million**. Source cells in `farside-date-total-2026-11-13.json`.
2. Galaxy 2026-10-10 identity holds to the satoshi, as tabulated above.
3. Constant-spot USD→BTC illustration is in `methodology/EQUATIONS.md`. It is not a time-to-target.
4. Time-to-target is **undefined**. Numerator (Target BTC removal) is unset. Denominator (trailing 90d BTC/month) is unset. The example snapshot therefore sets `months_to_target` to `null` and `state` to `insufficient_series`.

## What this does to the thesis, without replacing it

The structural claim (inelastic float, persistent absorption, nonlinear price response) is not measured by this audit. The audit constrains how the claim may be displayed:

- Float start, if it is Galaxy's strict in-play, is about **6.10M BTC** on the last complete day, not a fresh 6.11M census, and it already excludes ETF and corporate coins.
- ETF flow is a 30-day outflow in the latest sessions. A thermometer that needs "sustained sticky demand" as a present fact does not have it from this source today.
- The $8–12B/month, 36-month, 4–8M people sketch is a participation scenario. It is not a BTC absorption path until a price path is assumed. At the current spot, $12B/month for 36 months exceeds the degraded headline float; at $1M it does not come close. Both cannot be the same bar.
- Ordinary-participant capture and ETF/corporate absorption pull apart. The snapshot schema splits them so a later sum is a choice, not a hiding place.
