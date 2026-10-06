"""The EU's dictionary of cosmetic ingredients (CosIng), and how a printed name finds its entry.

Matching runs in three passes, cheapest first:
1. the everyday names labels use that aren't EU INCI ("Water", "Vitamin C", "Fragrance"),
   and exact names after normalizing case, spacing and punctuation
3. fuzzy, for typos and OCR mistakes: a trigram index narrows 33,000 names to a few
   dozen candidates, then edit distance (Damerau-Levenshtein) picks the closest
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"

# Names you see on labels that aren't the EU INCI name, or that labels love to translate.
EVERYDAY = {
    "water": "AQUA", "eau": "AQUA", "agua": "AQUA", "purified water": "AQUA", "deionized water": "AQUA",
    "fragrance": "PARFUM", "perfume": "PARFUM", "flavor": "AROMA", "flavour": "AROMA",
    "vitamin c": "ASCORBIC ACID", "l-ascorbic acid": "ASCORBIC ACID",
    "vitamin e": "TOCOPHEROL", "vitamin b3": "NIACINAMIDE", "vitamin b5": "PANTHENOL",
    "vitamin a": "RETINOL", "pro-vitamin b5": "PANTHENOL", "d-panthenol": "PANTHENOL",
    "hyaluronic acid": "HYALURONIC ACID", "aloe vera": "ALOE BARBADENSIS LEAF JUICE",
    "shea butter": "BUTYROSPERMUM PARKII BUTTER", "vitamin e acetate": "TOCOPHERYL ACETATE",
    "titanium dioxide": "CI 77891", "iron oxides": "CI 77491", "mica": "MICA",
}


# CosIng's function names, in the words a label reader would use. Anything not here
# (hair conditioning, oral care, denaturant...) is about other products, so it's left out.
JOBS = {
    "uv filter": "sunscreen", "uv absorber": "sunscreen", "colorant": "color", "preservative": "preservative",
    "exfoliating": "exfoliant", "bleaching": "brightening", "anti-sebum": "oil control",
    "surfactant - emulsifying": "emulsifier", "emulsion stabilising": "emulsifier",
    "surfactant - cleansing": "cleanser", "cleansing": "cleanser", "skin conditioning - humectant": "humectant",
    "humectant": "humectant", "skin conditioning - emollient": "emollient", "skin conditioning - occlusive": "occlusive",
    "film forming": "film former", "viscosity controlling": "thickener", "chelating": "chelator",
    "buffering": "pH adjuster", "ph adjusters": "pH adjuster", "antioxidant": "antioxidant", "soothing": "soothing",
    "antimicrobial": "antimicrobial", "absorbent": "absorbs oil", "opacifying": "opacifier", "solvent": "solvent",
    "skin protecting": "skin protectant", "smoothing": "smoothing", "moisturising": "moisturizer",
    "skin conditioning": "skin conditioning", "skin conditioning - miscellaneous": "skin conditioning",
    "bulking": "filler", "slip modifier": "slip", "masking": "covers smells",
}
JOB_ORDER = ["sunscreen", "color", "preservative", "exfoliant", "brightening", "oil control", "humectant", "emollient", "occlusive",
             "film former", "thickener", "emulsifier", "cleanser", "chelator", "pH adjuster", "antioxidant",
             "soothing", "antimicrobial", "absorbs oil", "smoothing", "moisturizer", "skin protectant", "slip", "opacifier",
             "solvent", "filler", "covers smells", "skin conditioning"]

# Carrier oils whose INCI name doesn't say which part of the plant they come from.
CARRIER = re.compile(r"(COCOS NUCIFERA|ELAEIS GUINEENSIS|GLYCINE SOJA|ZEA MAYS|SESAMUM INDICUM|PERSEA GRATISSIMA|"
                     r"OLEA EUROPAEA|ARGANIA SPINOSA|SIMMONDSIA CHINENSIS|PRUNUS AMYGDALUS DULCIS) OIL$")


def key(name: str) -> str:
    """'Sodium  Hyaluronate.' / 'sodium-hyaluronate' -> 'SODIUM HYALURONATE'."""
    name = name.upper().replace("–", "-").replace("—", "-")
    name = re.sub(r"[^A-Z0-9/\-,.()+' ]", " ", name)
    name = re.sub(r"\s*-\s*", "-", name)
    return re.sub(r"\s+", " ", name).strip(" .")


KEEP_UPPER = {"PEG", "PPG", "CI", "EDTA", "PCA", "NP", "AP", "EOP", "BHT", "BHA", "TEA", "DEA", "MEA", "HCL", "PVP", "DNA", "SPF"}


def pretty(inci: str) -> str:
    """'PEG-10 DIMETHICONE' -> 'PEG-10 Dimethicone', 'CI 77891' stays 'CI 77891'."""
    def word(m):
        w = m.group(0)
        return w if w in KEEP_UPPER or any(c.isdigit() for c in w) else w.capitalize()
    return re.sub(r"[A-Z0-9]+", word, inci)


def loose(name: str) -> str:
    """Even looser, for fuzzy matching: letters and digits only."""
    return re.sub(r"[^A-Z0-9]", "", key(name))


def trigrams(text: str) -> set[str]:
    text = f"  {text} "
    return {text[i:i + 3] for i in range(len(text) - 2)}


def edit_distance(a: str, b: str) -> int:
    """Damerau-Levenshtein (optimal string alignment): swaps count as one typo, like 'Glycrein'."""
    prev2, prev = None, list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = a[i - 1] != b[j - 1]
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                cur[j] = min(cur[j], prev2[j - 2] + 1)
        prev2, prev = prev, cur
    return prev[len(b)]


@dataclass(frozen=True)
class Ingredient:
    inci: str
    functions: tuple[str, ...] = ()

    @property
    def jobs(self) -> list[str]:
        """What it's most likely doing in skincare, in plain words, best first (at most two)."""
        from .knowledge import ALLERGENS, ROLES
        if self.inci in ROLES:
            return ROLES[self.inci]
        if self.inci in ALLERGENS:
            return ["scent", "fragrance allergen"]
        ranked = sorted((JOBS[f] for f in self.functions if f in JOBS), key=lambda j: JOB_ORDER.index(j))
        if self.essential_oil or self.scent_only:
            ranked.insert(0, "scent")
        return list(dict.fromkeys(ranked))[:2]

    @property
    def scent_only(self) -> bool:
        return bool(self.functions) and set(self.functions) <= {"fragrance", "perfuming", "masking"}

    @property
    def essential_oil(self) -> bool:
        """A plant oil that's there for its smell (lavender, orange peel), not a carrier oil (jojoba).

        CosIng tags glycerin and vitamin C as "fragrance" too, so the tag alone means little.
        An oil tagged for scent and not for softening skin is the tell. Oils pressed from seeds,
        kernels, nuts or fruit flesh are carrier oils even when CosIng tags them for scent.
        """
        if re.search(r"\b(SEED|KERNEL|NUT|GERM|BRAN|FRUIT|PULP|BUTTER)\b", self.inci) or CARRIER.match(self.inci):
            return False
        scent = {"fragrance", "perfuming"} & set(self.functions)
        softens = any("emollient" in f or "occlusive" in f for f in self.functions)
        return self.inci.endswith(" OIL") and bool(scent) and not softens


@dataclass(frozen=True)
class Match:
    ingredient: Ingredient | None
    how: str                 # "exact", "everyday", "fuzzy" or "unknown"
    name_used: str = ""
    distance: int = 0


class Catalog:
    def __init__(self, data: dict):
        self.by_key: dict[str, Ingredient] = {}
        self.by_loose: dict[str, Ingredient] = {}
        functions = data["functions"]
        for row in sorted(data["rows"], key=len):            # current names (no trailing 0) win ties
            ing = Ingredient(row[0], tuple(functions[i] for i in row[1]))
            self.by_key.setdefault(key(ing.inci), ing)
            self.by_loose.setdefault(loose(ing.inci), ing)
        self._grams: dict[str, list[str]] | None = None

    @property
    def grams(self) -> dict[str, list[str]]:
        """The trigram index, built the first time a typo needs it (it's the slow part in a browser)."""
        if self._grams is None:
            self._grams = defaultdict(list)
            for name in self.by_loose:
                for g in trigrams(name):
                    self._grams[g].append(name)
        return self._grams

    def get(self, inci: str) -> Ingredient | None:
        return self.by_key.get(key(inci))

    def exact(self, name: str) -> Ingredient | None:
        return self.by_key.get(key(name)) or self.by_loose.get(loose(name))

    def fuzzy(self, name: str) -> tuple[Ingredient, int] | None:
        target = loose(name)
        if len(target) < 5:
            return None                                   # too short to guess safely
        votes = Counter(n for g in trigrams(target) for n in self.grams.get(g, ()))
        best = None
        for cand, _ in votes.most_common(40):
            d = edit_distance(target, cand)
            if best is None or d < best[1]:
                best = (cand, d)
        if best and best[1] <= max(1, len(target) // 8):  # about one typo per eight letters
            return self.by_loose[best[0]], best[1]
        return None

    def match(self, names: list[str]) -> Match:
        for name in names:
            alias = EVERYDAY.get(name.lower().strip())   # first, so "Water" and "Aqua" are one ingredient
            if alias and self.get(alias):
                return Match(self.get(alias), "everyday" if key(alias) != key(name) else "exact", name)
            ing = self.exact(name)
            if ing:
                return Match(ing, "exact", name)
        for name in names:
            hit = self.fuzzy(name)
            if hit:
                return Match(hit[0], "fuzzy", name, hit[1])
        return Match(None, "unknown", names[0] if names else "")


@lru_cache(maxsize=1)
def load() -> Catalog:
    return Catalog(json.loads((DATA / "cosing.json").read_text(encoding="utf-8")))
