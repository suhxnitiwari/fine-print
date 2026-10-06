"""The entry point the website calls. Pyodide runs this exact code in the visitor's browser."""
from __future__ import annotations

import json

from .catalog import load, pretty
from .decode import Decoded, decode, together


def stats() -> str:
    return json.dumps({"ingredients": len(load().by_key)})


def _product(d: Decoded, foundation: bool) -> dict:
    heroes = {id(h.item): h for h in d.heroes}
    culprits = {c.split(" (#")[0] for c in d.fragrance.culprits}
    items = []
    for i in d.items:
        hero = heroes.get(id(i))
        items.append({
            "pos": i.entry.position,
            "printed": i.entry.printed,
            "name": pretty(i.inci),
            "known": i.ingredient is not None,
            "how": i.match.how,
            "atMost": i.at_most,
            "below": i.below_line,
            "mayContain": i.entry.may_contain,
            "jobs": i.ingredient.jobs if i.ingredient else [],
            "hero": hero.verdict if hero else "",
            "scent": pretty(i.inci) in culprits,
        })
    show_base = foundation or d.is_makeup
    b = d.base
    above = [i for i in d.ordered if not i.below_line]
    return {
        "name": d.name,
        "count": len(d.ordered),
        "colorants": len(d.items) - len(d.ordered),
        "fragrance": {"free": d.fragrance.free, "verdict": d.fragrance.verdict, "culprits": d.fragrance.culprits},
        "line": d.line,
        "lineName": pretty(d.ordered[d.line - 1].inci) if d.line else "",
        "aboveShare": 100 - (len(d.ordered) - len(above)) if d.line else None,
        "aboveCount": len(above),
        "heroes": [{"name": h.active.name, "verdict": h.verdict, "note": h.note, "pos": h.item.entry.position}
                   for h in d.heroes],
        "base": {"kind": b.kind, "emulsion": b.emulsion, "confidence": b.confidence, "rule": b.rule,
                 "heat": b.heat_note, "evidence": b.evidence} if show_base else None,
        "items": items,
        "fuzzy": [{"printed": i.entry.printed, "name": pretty(i.inci)} for i in d.fuzzy],
        "unknown": [i.entry.printed for i in d.unknown],
    }


def decode_json(products: str) -> str:
    """products: [{"name": ..., "text": ..., "foundation": bool}, ...] -> everything the page draws."""
    asked = [p for p in json.loads(products) if p.get("text", "").strip()]
    decoded = [decode(p["text"], p.get("name") or f"Product {n + 1}") for n, p in enumerate(asked)]
    clashes = [{
        "a": c.first[0], "aIngredient": pretty(c.first[1].inci), "aFamily": c.clash.a,
        "b": c.second[0], "bIngredient": pretty(c.second[1].inci), "bFamily": c.clash.b,
        "why": c.clash.why, "instead": c.clash.instead,
    } for c in together(decoded)]
    return json.dumps({
        "products": [_product(d, p.get("foundation", False)) for d, p in zip(decoded, asked)],
        "clashes": clashes,
    })
