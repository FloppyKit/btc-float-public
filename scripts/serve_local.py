#!/usr/bin/env python3
"""Build and serve the Stage 3 snapshot on localhost.

GET /float.json and GET /float.txt are the snapshot. GET /float.diff is the
partial-flag note. Binds 127.0.0.1 only. Does not fetch, does not deploy,
and does not fill a null sticky term.

  python3 scripts/serve_local.py --build-only
  python3 scripts/serve_local.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVE = ROOT / "serve"
DB = SERVE / "series.sqlite"
HOST = "127.0.0.1"
PORT = 8765

BARS = (
    ("zone_1m_2026usd", "$1M zone (2026 dollars) — label only until a BTC target is published"),
    ("zone_10m_2026usd", "$10M zone (2026 dollars) — label only until a BTC target is published"),
    ("zone_reserve_scale", "Reserve-scale marker — label only until a BTC target is published"),
)


def now_z() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_url() -> str:
    path = ROOT / "ops" / "CANONICAL_URL"
    if not path.exists():
        return "UNSET"
    return path.read_text().strip().rstrip("/")


def load(path: Path):
    return json.loads(path.read_text())


def usd_from_millions(value: float) -> int:
    return int(round(value * 1_000_000))


def build() -> dict:
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "reprint_audit.py")])
    reprint = load(ROOT / "audit" / "reprint-2026-11-13.json")
    if reprint.get("errors"):
        raise SystemExit(f"reprint has errors: {reprint['errors']}")
    lock = load(ROOT / "methodology" / "LOCK.json")
    if reprint["methodology_sha256"] != lock["methodology_sha256"]:
        raise SystemExit("reprint hash != LOCK.json")
    if reprint["galaxy"]["cumulative_sticky_btc"] is not None:
        raise SystemExit("reprint filled cumulative_sticky_btc")
    if reprint["farside"]["converted_to_btc"] is not None:
        raise SystemExit("reprint converted Farside USD to BTC")

    targets = {"zone_1m_2026usd": None, "zone_10m_2026usd": None, "zone_reserve_scale": None}
    target_path = SERVE / "targets.json"
    if target_path.exists():
        raw = load(target_path)
        for key in targets:
            if key in raw:
                targets[key] = raw[key]

    cumulative = reprint["galaxy"]["cumulative_sticky_btc"]
    bars = []
    for bar_id, label in BARS:
        target = targets[bar_id]
        # A published target is not enough. The BTC series is still null.
        state = "insufficient_series"
        if target is not None and cumulative is None:
            state = "insufficient_series"
        bars.append({
            "id": bar_id,
            "label": label,
            "target_btc_removal": target,
            "months_to_target": None,
            "state": state,
        })

    snapshot = {
        "schema_version": "btc-float-snapshot/v0",
        "generated_at": now_z(),
        "methodology_sha256": reprint["methodology_sha256"],
        "float": {
            "definition_id": reprint["definition_id"],
            "as_of": reprint["galaxy"]["float_start_as_of"],
            "partial": True,
            "float_start_btc": reprint["galaxy"]["float_start_btc"],
            "float_remaining_btc": None,
            "cumulative_sticky_btc": None,
            "float_pct_removed": None,
        },
        "flow": {
            "window": "last_30_sessions",
            "etf_net_flow_usd": usd_from_millions(reprint["farside"]["last_30_sessions_usd_millions"]),
            "etf_non_redeemed_usd": None,
            "self_custody_btc": None,
            "etf_net_btc": None,
            "corporate_net_btc": None,
            "monthly_sticky_usd": None,
            "trailing_90d_btc_per_month": None,
        },
        "bars": bars,
        "model": None,
        "provenance": [
            {
                "id": "farside_all_data",
                "url": "https://farside.co.uk/bitcoin-etf-flow-all-data/",
                "retrieved_at": "2026-11-13",
            },
            {
                "id": "galaxy_mind_float_api",
                "url": "https://galaxymind.space/api/float",
                "retrieved_at": "2026-11-13T17:01:05.958Z",
            },
            {
                "id": "reprint",
                "url": "audit/reprint-2026-11-13.json",
                "retrieved_at": reprint["methodology_sha256"],
            },
        ],
    }
    if snapshot["flow"]["etf_net_flow_usd"] != -2_780_200_000:
        raise SystemExit(f"unexpected etf usd {snapshot['flow']['etf_net_flow_usd']}")
    if snapshot["float"]["float_start_btc"] != 6095921.875:
        raise SystemExit("float start drifted")
    return snapshot


def to_txt(snapshot: dict) -> str:
    f = snapshot["float"]
    flow = snapshot["flow"]
    lines = [
        snapshot["schema_version"],
        f"generated_at: {snapshot['generated_at']}",
        f"methodology_sha256: {snapshot['methodology_sha256']}",
        f"float_definition: {f['definition_id']}",
        f"float_partial: {str(f['partial']).lower()}",
        f"float_start_btc: {f['float_start_btc']}",
        f"float_start_as_of: {f['as_of']}",
        "float_remaining_btc: null",
        "cumulative_sticky_btc: null",
        "float_pct_removed: null",
        f"etf_net_flow_usd_last_30_sessions: {flow['etf_net_flow_usd']}",
        "etf_non_redeemed_usd: null",
        "self_custody_btc: null",
        "etf_net_btc: null",
        "corporate_net_btc: null",
        "monthly_sticky_usd: null",
        "trailing_90d_btc_per_month: null",
    ]
    for bar in snapshot["bars"]:
        lines.append(f"bar.{bar['id']}: {bar['state']}")
    lines.append(f"canonical_url: {canonical_url()}")
    lines.append("already_excluded_not_in_sticky: lost,governments,etfs,publicCompanies,lthOther")
    return "\n".join(lines) + "\n"


def record(snapshot: dict) -> str:
    SERVE.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
          id INTEGER PRIMARY KEY,
          run_at TEXT NOT NULL,
          partial INTEGER NOT NULL,
          methodology_sha256 TEXT NOT NULL,
          float_start_btc REAL NOT NULL,
          cumulative_sticky_btc REAL,
          etf_net_flow_usd REAL,
          float_remaining_btc REAL
        )
        """
    )
    prior = conn.execute(
        "SELECT run_at, partial FROM runs ORDER BY id DESC LIMIT 1"
    ).fetchone()
    partial = 1 if snapshot["float"]["partial"] else 0
    conn.execute(
        """
        INSERT INTO runs (
          run_at, partial, methodology_sha256, float_start_btc,
          cumulative_sticky_btc, etf_net_flow_usd, float_remaining_btc
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            snapshot["generated_at"],
            partial,
            snapshot["methodology_sha256"],
            snapshot["float"]["float_start_btc"],
            snapshot["float"]["cumulative_sticky_btc"],
            snapshot["flow"]["etf_net_flow_usd"],
            snapshot["float"]["float_remaining_btc"],
        ),
    )
    conn.commit()
    rows = conn.execute("SELECT run_at, partial FROM runs ORDER BY id").fetchall()
    conn.close()

    crossings = []
    previous = None
    for run_at, flag in rows:
        if previous is None:
            previous = flag
            continue
        if flag != previous:
            crossings.append((run_at, previous, flag))
            previous = flag
    lines = [
        "btc-float-diff/v0",
        f"changes: {len(crossings)}",
        f"current_partial: {str(bool(partial)).lower()}",
        f"prior_partial: {('null' if prior is None else str(bool(prior[1])).lower())}",
        f"crossing: {str(bool(crossings) and (prior is not None and prior[1] != partial)).lower()}",
    ]
    if not crossings:
        lines.append("note: no partial-flag crossing. partial=true is the stored state, not a change from false.")
    else:
        for i, (run_at, was, now) in enumerate(crossings, start=1):
            lines.append(f"change.{i}: {run_at} partial {str(bool(was)).lower()} -> {str(bool(now)).lower()}")
    return "\n".join(lines) + "\n"


def write_outputs(snapshot: dict, diff: str) -> None:
    SERVE.mkdir(exist_ok=True)
    (SERVE / "float.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    (SERVE / "float.txt").write_text(to_txt(snapshot))
    (SERVE / "float.diff").write_text(diff)
    if not (SERVE / "targets.json").exists():
        (SERVE / "targets.json").write_text(json.dumps({
            "zone_1m_2026usd": None,
            "zone_10m_2026usd": None,
            "zone_reserve_scale": None,
        }, indent=2) + "\n")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        files = {
            "/float.json": ("application/json; charset=utf-8", SERVE / "float.json"),
            "/float.txt": ("text/plain; charset=utf-8", SERVE / "float.txt"),
            "/float.diff": ("text/plain; charset=utf-8", SERVE / "float.diff"),
        }
        item = files.get(path)
        if item is None:
            body = b"not found\n"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        ctype, file_path = item
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    snapshot = build()
    diff = record(snapshot)
    write_outputs(snapshot, diff)
    print(f"wrote {SERVE / 'float.json'}")
    print(f"partial={str(snapshot['float']['partial']).lower()} sticky=null bars=insufficient_series")
    print(diff, end="")
    if args.build_only:
        return 0
    server = ThreadingHTTPServer((HOST, args.port), Handler)
    print(f"serving http://{HOST}:{args.port}/float.json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
