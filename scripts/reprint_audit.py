#!/usr/bin/env python3
"""Reprint the Stage 0 audit windows from the saved extracts.

Reads only:
  audit/farside-date-total-2026-11-13.json
  audit/galaxy-float-excerpt-2026-11-13.json
  audit/baseline.json
  methodology/EQUATIONS.md
  methodology/EQUATIONS.sha256
  methodology/LOCK.json

Does not fetch, does not convert USD to BTC, and does not fill a null
sticky term with zero. Exit 0 only when the recomputation matches the
audit baseline and the methodology hash.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
METH = ROOT / "methodology"

PLACEHOLDER = dt.date(2026, 11, 13)
LAST_COMPLETE_SESSION = dt.date(2026, 11, 12)


def load(path: Path):
    return json.loads(path.read_text())


def parse_num(cell: str):
    s = cell.replace(",", "").replace("(", "-").replace(")", "").strip()
    if s in ("", "-", "–", "—"):
        return None
    return float(s)


def parse_farside(doc):
    sessions = []
    total_row = None
    for date_cell, total_cell in doc["rows"]:
        if date_cell == "Total":
            total_row = parse_num(total_cell)
            continue
        try:
            day = dt.datetime.strptime(date_cell, "%d %b %Y").date()
        except ValueError:
            continue
        value = parse_num(total_cell)
        if value is None:
            continue
        sessions.append((day, value))
    sessions.sort()
    return sessions, total_row


def complete_sessions(sessions):
    """Drop the 13 Nov 2026 placeholder (dashes rendered as 0.0)."""
    out = []
    for day, value in sessions:
        if day == PLACEHOLDER and value == 0.0:
            continue
        if day > LAST_COMPLETE_SESSION:
            continue
        out.append((day, value))
    return out


def sum_rounded(rows):
    return round(sum(v for _, v in rows), 1)


def window_sessions(sessions, n):
    return sessions[-n:]


def calendar_window(sessions, end, days):
    start = end - dt.timedelta(days=days - 1)
    return [(d, v) for d, v in sessions if start <= d <= end]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def galaxy_checks(excerpt, lock):
    complete = excerpt["last_complete"]
    current = excerpt["current"]
    c = complete["cohorts"]
    excluded = (
        c["lost"]
        + c["governments"]
        + c["etfs"]
        + c["publicCompanies"]
        + c["lthOther"]
    )
    identity_ok = abs((excluded + complete["inPlay"]) - complete["minedSupply"]) < 1e-6
    folded = (
        c["lthOther"] + c["etfs"] + c["governments"] + c["publicCompanies"]
    )
    issuance = current["minedSupply"] - complete["minedSupply"]
    headline_is_start_plus_issuance = abs(
        (complete["inPlay"] + issuance) - current["inPlay"]
    ) < 1e-6
    # Sticky cannot be computed. A partial row is not a zero delta.
    etf_delta = None if current["cohorts"]["etfs"] is None else "refused"
    co_delta = None if current["cohorts"]["publicCompanies"] is None else "refused"
    return {
        "float_start_btc": complete["inPlay"],
        "float_start_as_of": complete["asOf"],
        "partial_complete_row": complete["partial"],
        "excluded_sum_btc": excluded,
        "identity_ok": identity_ok,
        "folded_lth_other_equals": folded,
        "current_lth_other": current["cohorts"]["lthOther"],
        "folded_placeholder_matches": abs(folded - current["cohorts"]["lthOther"]) < 1e-6,
        "issuance_since_start_btc": issuance,
        "degraded_headline_btc": current["inPlay"],
        "degraded_partial": current["partial"],
        "headline_equals_start_plus_issuance": headline_is_start_plus_issuance,
        "etf_net_btc": etf_delta,
        "corporate_net_btc": co_delta,
        "self_custody_btc": None,
        "cumulative_sticky_btc": None,
        "float_remaining_btc": None,
        "float_pct_removed": None,
        "matches_lock_start": complete["inPlay"] == lock["float_start_btc"],
    }


def main():
    errors = []
    hash_line = (METH / "EQUATIONS.sha256").read_text().split()[0]
    digest = sha256_file(METH / "EQUATIONS.md")
    if digest != hash_line:
        errors.append(f"methodology hash mismatch: {digest} != {hash_line}")

    baseline = load(AUDIT / "baseline.json")
    lock = load(METH / "LOCK.json")
    if baseline.get("methodology_sha256") != digest:
        errors.append("baseline methodology_sha256 does not match file bytes")
    if lock.get("methodology_sha256") != digest:
        errors.append("LOCK.json methodology_sha256 does not match file bytes")

    sessions, total_row = parse_farside(load(AUDIT / "farside-date-total-2026-11-13.json"))
    complete = complete_sessions(sessions)
    last30 = window_sessions(complete, 30)
    last90 = window_sessions(complete, 90)
    trail365 = calendar_window(complete, LAST_COMPLETE_SESSION, 365)
    pos = round(sum(v for _, v in last30 if v > 0), 1)
    neg = round(sum(v for _, v in last30 if v < 0), 1)

    farside = {
        "table_total_row_usd_millions": total_row,
        "sum_of_displayed_daily_totals_usd_millions": sum_rounded(complete),
        "first_session": complete[0][0].isoformat(),
        "last_complete_session": complete[-1][0].isoformat(),
        "last_complete_day_usd_millions": complete[-1][1],
        "last_30_sessions_from": last30[0][0].isoformat(),
        "last_30_sessions_to": last30[-1][0].isoformat(),
        "last_30_sessions_usd_millions": sum_rounded(last30),
        "last_30_sessions_positive_usd_millions": pos,
        "last_30_sessions_negative_usd_millions": neg,
        "last_90_sessions_from": last90[0][0].isoformat(),
        "last_90_sessions_to": last90[-1][0].isoformat(),
        "last_90_sessions_usd_millions": sum_rounded(last90),
        "trailing_365_from": trail365[0][0].isoformat(),
        "trailing_365_to": trail365[-1][0].isoformat(),
        "trailing_365_sessions": len(trail365),
        "trailing_365_calendar_days_usd_millions": sum_rounded(trail365),
        "sessions_parsed": len(complete),
        "unit": "USD millions, net. Not BTC.",
        "etf_non_redeemed_usd": None,
        "converted_to_btc": None,
    }

    expected = baseline["etf_flows_farside"]
    checks = {
        "table_total_row_usd_millions": expected["table_total_row_usd_millions"],
        "sum_of_displayed_daily_totals_usd_millions": expected["sum_of_displayed_daily_totals_usd_millions"],
        "first_session": expected["first_session"],
        "last_complete_session": expected["last_complete_session"],
        "last_complete_day_usd_millions": expected["last_complete_day_usd_millions"],
        "last_30_sessions_usd_millions": expected["last_30_sessions_2026_10_02_to_2026_11_12_usd_millions"],
        "last_30_sessions_positive_usd_millions": expected["last_30_sessions_positive_usd_millions"],
        "last_30_sessions_negative_usd_millions": expected["last_30_sessions_negative_usd_millions"],
        "last_90_sessions_usd_millions": expected["last_90_sessions_2026_07_09_to_2026_11_12_usd_millions"],
        "trailing_365_calendar_days_usd_millions": expected["trailing_365_calendar_days_to_2026_11_12_usd_millions"],
        "sessions_parsed": expected["sessions_parsed"],
    }
    for key, want in checks.items():
        got = farside[key]
        if got != want:
            errors.append(f"farside {key}: got {got} want {want}")
    if farside["last_30_sessions_from"] != "2026-10-02":
        errors.append(f"last 30 starts {farside['last_30_sessions_from']}, want 2026-10-02")
    if farside["last_90_sessions_from"] != "2026-07-09":
        errors.append(f"last 90 starts {farside['last_90_sessions_from']}, want 2026-07-09")

    galaxy = galaxy_checks(load(AUDIT / "galaxy-float-excerpt-2026-11-13.json"), lock)
    gexp = baseline["float"]
    if galaxy["float_start_btc"] != gexp["last_complete_2026_10_10"]["in_play_btc"]:
        errors.append("float start does not match baseline")
    if galaxy["degraded_headline_btc"] != gexp["degraded_headline_2026_11_13"]["in_play_btc"]:
        errors.append("degraded headline does not match baseline")
    if not galaxy["identity_ok"]:
        errors.append("excluded cohorts + float start != mined supply")
    if not galaxy["folded_placeholder_matches"]:
        errors.append("degraded lthOther is not the folded t0 sum")
    if not galaxy["headline_equals_start_plus_issuance"]:
        errors.append("degraded headline is not start + issuance")
    if not galaxy["matches_lock_start"]:
        errors.append("excerpt float start != LOCK.json")
    if galaxy["cumulative_sticky_btc"] is not None or galaxy["float_remaining_btc"] is not None:
        errors.append("sticky or remaining was filled")
    if galaxy["etf_net_btc"] is not None or galaxy["corporate_net_btc"] is not None:
        errors.append("cohort delta filled from a partial row")
    if farside["converted_to_btc"] is not None:
        errors.append("Farside USD was converted to BTC")

    report = {
        "schema": "btc-float-reprint/v0",
        "generated_from": "saved extracts only",
        "methodology_sha256": digest,
        "definition_id": lock["definition_id"],
        "residual_path": "equation",
        "farside": farside,
        "galaxy": galaxy,
        "not_invented": [
            "etf_net_btc",
            "corporate_net_btc",
            "self_custody_btc",
            "cumulative_sticky_btc",
            "float_remaining_btc",
            "monthly_sticky_usd",
            "trailing_90d_btc_per_month",
            "target_btc_removal",
        ],
        "errors": errors,
    }
    out = AUDIT / "reprint-2026-11-13.json"
    out.write_text(json.dumps(report, indent=2) + "\n")

    print(f"methodology_sha256 {digest}")
    print(f"farside total row {farside['table_total_row_usd_millions']} sum {farside['sum_of_displayed_daily_totals_usd_millions']}")
    print(f"farside last 30 {farside['last_30_sessions_from']}..{farside['last_30_sessions_to']} {farside['last_30_sessions_usd_millions']}")
    print(f"farside last 90 {farside['last_90_sessions_from']}..{farside['last_90_sessions_to']} {farside['last_90_sessions_usd_millions']}")
    print(f"farside 365d {farside['trailing_365_from']}..{farside['trailing_365_to']} n={farside['trailing_365_sessions']} {farside['trailing_365_calendar_days_usd_millions']}")
    print(f"float_start {galaxy['float_start_btc']} excluded {galaxy['excluded_sum_btc']} identity {galaxy['identity_ok']}")
    print(f"issuance_since_start {galaxy['issuance_since_start_btc']} headline {galaxy['degraded_headline_btc']} partial {galaxy['degraded_partial']}")
    print("cumulative_sticky_btc null")
    print("float_remaining_btc null")
    print(f"wrote {out}")
    if errors:
        print("FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("MATCH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
