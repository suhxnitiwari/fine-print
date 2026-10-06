"""Turn the ingredient list off the back of a box into clean, ordered names.

Labels are messy in predictable ways:

    Ingredients: Aqua/Water/Eau, Niacinamide, 1,2-Hexanediol, Parfum (Fragrance)*, ...
    *Organic.  May Contain [+/-]: CI 77891 (Titanium Dioxide), CI 77491.

- a comma usually ends a name, but not in chemistry ("1,2-Hexanediol", "2,4-Dichlorobenzyl Alcohol")
- one ingredient can be written three ways at once ("Aqua/Water/Eau", "Parfum (Fragrance)")
- footnote marks and their notes ("*", "**Organic", "†")
- makeup lists end with "may contain", the shade colorants, which are outside the order
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

LABEL = re.compile(r"^\s*(?:full\s+)?(?:ingredients?|ingrédients|inci|contains)\s*(?:list)?\s*:\s*", re.I)
MAY_CONTAIN = re.compile(r"(?:\[\s*\+\s*/\s*-\s*\]|\(\s*\+\s*/\s*-\s*\)|\+\s*/\s*-|\bmay\s+contain\b|\bpeut\s+contenir\b)\s*:?", re.I)
FOOTNOTE_NOTE = re.compile(r"(?:^|\s)[*†‡]+\s*[A-Za-z][^,]*$")   # "*Organic", "** from natural origin"
MARKS = re.compile(r"[*†‡®™]+")
BULLETS = re.compile(r"\s*[•·|;]\s*|\n+")


@dataclass
class Entry:
    """One ingredient as printed, plus the other names it was printed with."""
    position: int                     # 1-based place on the list; 0 for "may contain"
    printed: str                      # exactly what the label said
    names: list[str] = field(default_factory=list)   # candidate names, best guess first
    may_contain: bool = False


def split_commas(text: str) -> list[str]:
    """Split on commas, but not inside brackets and not between digits (1,2-Hexanediol)."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(depth - 1, 0)
        elif ch == "," and depth == 0:
            before, after = text[i - 1:i], text[i + 1:i + 2]
            if before.isdigit() and after.isdigit():
                continue
            parts.append(text[start:i])
            start = i + 1
    parts.append(text[start:])
    return [p.strip() for p in parts if p.strip()]


def tidy(name: str) -> str:
    name = MARKS.sub("", name)
    name = re.sub(r"\s+", " ", name).strip(" .:-")
    return name


def alternatives(printed: str) -> list[str]:
    """Every name an entry could mean. 'Parfum (Fragrance)' -> ['Parfum (Fragrance)', 'Parfum', 'Fragrance'].

    The whole thing goes first: real INCI names contain slashes and brackets too
    ('Acrylates/C10-30 Alkyl Acrylate Crosspolymer'), so splitting is only a fallback.
    """
    whole = tidy(printed)
    names = [whole]
    outside = tidy(re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", whole))
    inside = [tidy(m) for m in re.findall(r"\(([^)]*)\)|\[([^\]]*)\]", whole) for m in m if m]
    for n in [outside, *inside]:
        names.append(n)
    for n in list(names):
        if "/" in n or "\\" in n:
            names.extend(tidy(p) for p in re.split(r"\s*[/\\]\s*", n))
    seen, out = set(), []
    for n in names:
        if n and n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out


def parse(text: str) -> list[Entry]:
    """The label, in order, as Entries."""
    text = LABEL.sub("", text.strip())
    text = BULLETS.sub(", ", text)
    pieces = MAY_CONTAIN.split(text, maxsplit=1)
    ordered = pieces[0]
    extras = MAY_CONTAIN.sub("", pieces[1]) if len(pieces) > 1 else ""   # "May contain [+/-]:" has two markers

    entries: list[Entry] = []
    for raw in split_commas(ordered):
        raw = FOOTNOTE_NOTE.sub("", raw).strip().rstrip(".")      # drops "*Organic" and friends
        if not tidy(raw):
            continue
        entries.append(Entry(len(entries) + 1, raw, alternatives(raw)))
    for raw in split_commas(extras.strip(" .")):
        if tidy(raw):
            entries.append(Entry(0, raw.rstrip("."), alternatives(raw), may_contain=True))
    return entries
