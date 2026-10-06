"""Download every ingredient in the EU's CosIng database into fineprint/data/cosing.json.

    python tools/fetch_cosing.py

CosIng's website is a front end for the EU search API. That API stops at 10,000 results
for any one query, and there are more than 33,000 ingredients. Its range filters don't work
on the ID field (IDs are stored as text), but exact matches do, so the download asks for the
IDs in explicit batches of 5,000 ("any of 30000, 30001, ... 34999"), pages through each batch,
and checks the total against the API's own count.
"""
from __future__ import annotations

import json
import time
import urllib.request
import uuid
from pathlib import Path

API = "https://webgate.ec.europa.eu/es/search-api/rest/search"
KEY = "285a77fd-1257-4271-8507-f0c6b2961203"   # the public key CosIng's own site uses
PAGE = 100
CAP = 10_000
BATCH = 5_000      # a terms filter much longer than this comes back empty
LAST_ID = 200_000
OUT = Path(__file__).resolve().parent.parent / "fineprint" / "data" / "cosing.json"


def search(query: dict, page: int = 1, size: int = PAGE) -> dict:
    """One page of results. The API wants the query as a multipart form field."""
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"query\"\r\n"
            f"Content-Type: application/json\r\n\r\n{json.dumps(query)}\r\n--{boundary}--\r\n").encode()
    url = f"{API}?apiKey={KEY}&text=*&pageSize={size}&pageNumber={page}"
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def ingredients(extra: list | None = None) -> dict:
    return {"bool": {"must": [{"terms": {"itemType": ["ingredient"]}}] + (extra or [])}}


def batch(lo: int, hi: int) -> dict:
    return ingredients([{"terms": {"substanceId": [str(i) for i in range(lo, hi)]}}])


def first(meta: dict, key: str) -> str:
    values = meta.get(key) or []
    return values[0].strip() if values and values[0] and values[0].strip() != "-" else ""


def record(meta: dict) -> dict:
    """Keep only what the decoder uses."""
    return {
        "inci": first(meta, "inciName"),
        "functions": sorted({f.strip().lower() for f in meta.get("functionName") or [] if f.strip()}),
        "active": first(meta, "status") == "Active",
    }


def compact(rows: list[dict]) -> dict:
    """Small enough for a phone: 82 function names stored once, each row points at them by number.

    A row is [INCI name, [function numbers]], plus a trailing 0 if CosIng marks it no longer active.
    """
    functions = sorted({f for r in rows for f in r["functions"]})
    number = {f: i for i, f in enumerate(functions)}
    return {"functions": functions,
            "rows": [[r["inci"], [number[f] for f in r["functions"]]] + ([] if r["active"] else [0]) for r in rows]}


def collect(query: dict, total: int, found: dict) -> None:
    for page in range(1, (total - 1) // PAGE + 2):
        for hit in search(query, page)["results"]:
            meta = hit["metadata"]
            sid = first(meta, "substanceId")
            if sid and first(meta, "inciName"):
                found[sid] = record(meta)


def main() -> None:
    expected = search(ingredients(), size=1)["totalResults"]
    print(f"CosIng says it has {expected:,} ingredients.")
    found: dict[str, dict] = {}
    for lo in range(0, LAST_ID, BATCH):
        query = batch(lo, lo + BATCH)
        total = search(query, size=1)["totalResults"]
        if total >= CAP:
            raise SystemExit(f"IDs {lo}-{lo + BATCH} hold {total:,} ingredients; make BATCH smaller.")
        collect(query, total, found)
        print(f"  IDs {lo:>6}-{lo + BATCH - 1:<6} {total:>5} ingredients  ({len(found):,} so far)")
    rows = sorted(found.values(), key=lambda r: r["inci"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(compact(rows), ensure_ascii=False, separators=(",", ":")))
    print(f"Saved {len(rows):,} of {expected:,} to {OUT.name} ({OUT.stat().st_size / 1e6:.1f} MB).")
    if len(rows) < expected * 0.99:
        raise SystemExit("Missing more than 1% of CosIng. Raise LAST_ID.")


if __name__ == "__main__":
    main()
