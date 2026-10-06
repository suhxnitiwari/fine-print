"""Read one product, or a whole routine, and answer the three questions.

1. Is it actually fragrance-free?
2. What's really doing the work? (the 1% line, and how much of each hero there can be)
3. Can I use these together?
Plus, for foundations: what base is it?

How much of an ingredient can there be? Ingredients above 1% are listed from most to least,
so the ingredient at position n can't be more than 100/n percent: the n-1 before it are at
least as big, and together they can't pass 100. Below the 1% line, the cap is 1%.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import knowledge as K
from .base import Base, classify
from .catalog import Catalog, Ingredient, Match, load, pretty
from .parse import Entry, parse

PIGMENTS = ("CI 77891", "CI 77491", "CI 77492", "CI 77499")


@dataclass
class Item:
    entry: Entry
    match: Match
    at_most: float | None = None      # % ceiling from the list order; None for "may contain"
    below_line: bool = False

    @property
    def ingredient(self) -> Ingredient | None:
        return self.match.ingredient

    @property
    def inci(self) -> str:
        return self.ingredient.inci if self.ingredient else self.entry.printed


@dataclass
class Hero:
    active: K.Active
    item: Item
    verdict: str        # "could be enough", "too little", "works low"
    note: str


@dataclass
class Fragrance:
    free: bool
    verdict: str
    culprits: list[str] = field(default_factory=list)


@dataclass
class Decoded:
    name: str
    items: list[Item]
    line: int | None                  # position of the 1% line, if the list shows one
    fragrance: Fragrance
    heroes: list[Hero]
    base: Base
    is_makeup: bool

    @property
    def ordered(self) -> list[Item]:
        return [i for i in self.items if not i.entry.may_contain]

    @property
    def unknown(self) -> list[Item]:
        return [i for i in self.items if i.ingredient is None]

    @property
    def fuzzy(self) -> list[Item]:
        return [i for i in self.items if i.match.how == "fuzzy"]

    def families(self) -> dict[str, Item]:
        """The active families present at a level that matters (lactic acid as a pH tweak doesn't count)."""
        found = {}
        for item in self.ordered:
            for fam, members in K.FAMILIES.items():
                if item.inci in members and fam not in found:
                    active = K.ACTIVES.get(item.inci)
                    if active and item.at_most is not None and item.at_most < active.works_from:
                        continue
                    found[fam] = item
        return found


def one_percent_line(items: list[Item]) -> int | None:
    for item in items:
        if item.inci in K.UNDER_ONE_PERCENT:
            return item.entry.position
    return None


def fragrance_check(items: list[Item]) -> Fragrance:
    added = [i for i in items if i.inci in K.FRAGRANCE]
    oils = [i for i in items if i.ingredient and i.ingredient.essential_oil]
    allergens = [i for i in items if i.inci in K.ALLERGENS]
    real_allergens = [i for i in allergens if i.inci not in K.ALLERGEN_BUT_PRESERVATIVE]
    names = lambda xs: [f"{pretty(i.inci)} (#{i.entry.position})" for i in xs]

    if added:
        why = "It has added fragrance"
        if real_allergens:
            why += f", and the label names {len(real_allergens)} of the allergens hiding in it"
        return Fragrance(False, why + ".", names(added + real_allergens))
    if oils:
        return Fragrance(False, "No 'parfum' on the label, but it's scented with essential oils.", names(oils + real_allergens))
    if real_allergens:
        return Fragrance(False, "No 'parfum' on the label, but these are fragrance allergens: the parts a scent is made of.",
                         names(real_allergens))
    if allergens:
        return Fragrance(True, "Yes, most likely. Benzyl alcohol is on the EU allergen list, but here it's almost "
                               "certainly the preservative.", names(allergens))
    return Fragrance(True, "Yes. Nothing on this list is there to make it smell.")


def hero_check(items: list[Item]) -> list[Hero]:
    heroes, seen = [], set()
    for item in items:
        active = K.ACTIVES.get(item.inci)
        if not active or active.name in seen or item.at_most is None:
            continue
        seen.add(active.name)
        cap = item.at_most
        if cap < active.works_from:
            verdict = "too little"
            note = (f"At #{item.entry.position} it's at most {fmt(cap)}%, and studies use {active.usual}. "
                    "It's on the label more than it's in the bottle.")
        elif active.works_from < 1 and item.below_line:
            verdict = "works low"
            note = f"Below the 1% line, which is fine: {active.note or f'it works at {active.usual}.'}"
        else:
            verdict = "could be enough"
            note = f"At #{item.entry.position} it can be up to {fmt(cap)}%. Studies use {active.usual}."
        if active.note and verdict != "works low":
            note += f" {active.note}"
        heroes.append(Hero(active, item, verdict, note))
    return heroes


def fmt(pct: float) -> str:
    return f"{pct:.0f}" if pct >= 10 else f"{pct:.1f}".rstrip("0").rstrip(".")


def decode(text: str, name: str = "This product", catalog: Catalog | None = None) -> Decoded:
    catalog = catalog or load()
    items = [Item(e, catalog.match(e.names)) for e in parse(text)]
    ordered = [i for i in items if not i.entry.may_contain]
    line = one_percent_line(ordered)
    for item in ordered:
        pos = item.entry.position
        item.below_line = line is not None and pos >= line
        item.at_most = min(100 / pos, 1.0) if item.below_line else 100 / pos
    pigments = [i for i in items if i.inci in PIGMENTS]
    return Decoded(
        name=name,
        items=items,
        line=line,
        fragrance=fragrance_check(items),
        heroes=hero_check(ordered),
        base=classify([i.inci for i in ordered if not i.inci.startswith("CI ")]),
        is_makeup=bool(pigments),
    )


@dataclass
class Conflict:
    clash: K.Clash
    first: tuple[str, Item]
    second: tuple[str, Item]


def together(products: list[Decoded]) -> list[Conflict]:
    """Clashes between different products. Inside one product, the chemist already made it work."""
    found = []
    for i, a in enumerate(products):
        for b in products[i + 1:]:
            fa, fb = a.families(), b.families()
            for clash in K.CLASHES:
                for x, y in ((clash.a, clash.b), (clash.b, clash.a)):
                    if x in fa and y in fb:
                        found.append(Conflict(clash, (a.name, fa[x]), (b.name, fb[y])))
                        break
    return found
