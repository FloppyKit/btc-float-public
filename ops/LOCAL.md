# Local snapshot

Stage 3. Not a public host. Binds `127.0.0.1` only.

```
python3 scripts/serve_local.py
```

| URL | Body |
|---|---|
| `http://127.0.0.1:8765/float.json` | Snapshot. Schema `btc-float-snapshot/v0`. |
| `http://127.0.0.1:8765/float.txt` | Same fields, one `key: value` per line. |
| `http://127.0.0.1:8765/float.diff` | Partial-flag crossings. A first row with `partial=true` is not a crossing. |

The process rebuilds from `scripts/reprint_audit.py` before it listens. If that reprint does not match, it does not serve. `serve/targets.json` may set a bar denominator later. A number there does not flip a bar to `ok` while `cumulative_sticky_btc` is null.

Rebuild without listening: `python3 scripts/serve_local.py --build-only`.
