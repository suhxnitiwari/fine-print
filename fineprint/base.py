"""What base is this foundation? Water, silicone, oil, or none at all.

The base is the phase that touches your skin, not the biggest ingredient. Most liquid
foundations are water-in-silicone, and they still list water first (40-60% of the bottle).
So the decoder reads the top of the list plus the emulsifier, never ingredient #1 alone.

Rules come from the research in reports/Foundation bases and hot climates.md. They are checked
in order and the first match wins. Label law only orders ingredients above 1%, so position
means something only near the top: the decoder looks at the first eight.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .catalog import pretty

TOP = 8

FAMILIES = {
    "water": r"^(water|aqua|eau)$",
    "water_like": r"(leaf|flower|fruit) (juice|water)$|hydrosol",
    "cyclic_silicone": r"cyclo(tetra|penta|hexa)siloxane|cyclomethicone",
    "silicone_emulsifier": r"(peg|ppg|peg/ppg)-[\d/]+.*(dimethicone|methicone)|polydimethylsiloxyethyl dimethicone"
                           r"|tris\(trimethylsiloxy\)silylethyl dimethicone|dimethicone copolyol"
                           r"|dimethicone/peg-[\d/]+ crosspolymer",
    "silicone_film": r"trimethylsiloxysilicate|polypropylsilsesquioxane|acrylates/dimethicone copolymer",
    "pigment_coating": r"triethoxycaprylylsilane|isopropyl titanium triisostearate|hydrogenated lecithin",
    "silicone": r"dimethicone|methicone|siloxane|siloxysilicate|silsesquioxane|trimethicone",   # not "silicate": that's clay
    "volatile_hydrocarbon": r"isododecane|isohexadecane|c\d+-\d+ (iso)?alkane|hemisqualane|undecane|tridecane|polydecene",
    "oil": r"triglyceride|squalane|\boil$|butter$|jojoba|(palmitate|isononanoate|laurate|stearate|myristate)$|alkyl benzoate",
    "w_o_emulsifier": r"polyglyceryl-\d+ .*(stearate|polyhydroxystearate)|dipolyhydroxystearate|sorbitan (iso)?stearate"
                      r"|sorbitan oleate|quaternium-(18|90)|disteardimonium hectorite|stearalkonium hectorite",
    "o_w_thickener": r"xanthan gum|carbomer|acrylates/c10-30 alkyl acrylate crosspolymer|acryloyldimethyltaurate"
                     r"|sodium polyacrylate|hydroxyethylcellulose|steareth-\d+|ceteareth-\d+|polysorbate \d+"
                     r"|peg-100 stearate|potassium cetyl phosphate",
}
PATTERNS = {name: re.compile(p) for name, p in FAMILIES.items()}
# More specific families claim an ingredient before the catch-all "silicone" can.
ORDER = ["water", "water_like", "cyclic_silicone", "silicone_emulsifier", "silicone_film", "pigment_coating",
         "w_o_emulsifier", "o_w_thickener", "volatile_hydrocarbon", "silicone", "oil"]
SAY = {
    "water": "water", "water_like": "a plant water", "cyclic_silicone": "evaporating silicone",
    "silicone_emulsifier": "silicone emulsifier", "silicone_film": "silicone film former",
    "pigment_coating": "pigment coating", "silicone": "silicone", "volatile_hydrocarbon": "evaporating oil",
    "oil": "oil or ester", "w_o_emulsifier": "water-in-oil emulsifier", "o_w_thickener": "water-phase thickener",
}
SILICONES = {"cyclic_silicone", "silicone", "silicone_film"}
OILY = {"volatile_hydrocarbon", "oil"}


def family(name: str) -> str:
    name = name.lower().strip()
    for fam in ORDER:
        if PATTERNS[fam].search(name):
            return fam
    return ""


@dataclass
class Base:
    kind: str          # "silicone", "water", "oil", "silicone + oil", "waterless silicone", "waterless oil", "unknown"
    emulsion: str      # what a chemist would call it
    confidence: str    # "high", "medium", "low" or "a guess"
    rule: str          # which rule decided
    evidence: list[str]

    @property
    def heat_note(self) -> str:
        return HEAT.get(self.kind, "")


HEAT = {
    "silicone": "Holds up best in heat: skin oil doesn't dissolve a silicone film the way it dissolves an oil one.",
    "silicone + oil": "Middle of the road. The silicone helps; the oils soften once you start getting shiny.",
    "oil": "Silicone-free, but it wears like a silicone base, not a water one. Oilier skin will break it down faster in heat.",
    "waterless oil": "Skin oil dissolves into it, so it slides fastest on oily skin and in humid heat.",
    "waterless silicone": "Usually primer-like and long-wearing.",
    "water": "Light and breathable, but there's no water-resistant film, so sweat moves it.",
}


def classify(names: list[str]) -> Base:
    """`names` is the ordered list (INCI names, may-contain colorants left out)."""
    fams = [family(n) for n in names]
    top = fams[:TOP]
    where = lambda fam_set, upto=TOP: [i + 1 for i, f in enumerate(fams[:upto]) if f in fam_set]
    evidence = [f"{i + 1}. {pretty(n)}  ({SAY[f]})" for i, (n, f) in enumerate(zip(names[:TOP], top)) if f]

    has_water = any(f in ("water", "water_like") for f in fams)
    water_top3 = bool(where({"water"}, 3))
    si_top4 = where(SILICONES, 4)
    oily_top4 = where(OILY, 4)
    si_emul = "silicone_emulsifier" in fams
    wo_emul = "w_o_emulsifier" in fams
    ow = "o_w_thickener" in fams

    if not has_water:                                                          # R1
        first3 = [f for f in fams[:3] if f]
        silicone_led = sum(f in SILICONES for f in first3) > sum(f in OILY for f in first3)
        return Base("waterless silicone" if silicone_led else "waterless oil", "anhydrous", "high",
                    "No water anywhere on the list.", evidence)
    if water_top3 and si_top4 and si_emul and not oily_top4:                   # R2
        return Base("silicone", "water-in-silicone", "high",
                    f"Water near the top, a silicone at #{si_top4[0]} and a silicone emulsifier.", evidence)
    if fams and fams[0] in SILICONES:                                          # R3
        return Base("silicone", "water-in-silicone", "high", "A silicone comes before the water.", evidence)
    if water_top3 and oily_top4 and (wo_emul or si_emul) and not si_top4:      # R4
        return Base("oil", "water-in-oil", "medium",
                    f"Water near the top, oils or hydrocarbons at #{oily_top4[0]}, a water-in-oil emulsifier and no silicone up top.",
                    evidence)
    if where(SILICONES, 5) and where(OILY, 5) and si_emul:                     # R5
        return Base("silicone + oil", "water-in-silicone with oils", "medium",
                    "Silicones and oils share the top five, held together by a silicone emulsifier.", evidence)
    if fams and fams[0] == "water" and not where(SILICONES | {"volatile_hydrocarbon"}, 4) and not wo_emul:  # R6
        return Base("water", "oil-in-water", "high" if ow else "low",
                    "Water first, nothing silicone or oily up top" + (", and water-phase thickeners." if ow else "."),
                    evidence)
    if fams and fams[0] == "water" and where(SILICONES, 5) and not wo_emul and ow:  # R7
        return Base("water", "silicone-in-water", "a guess",
                    "Water first with silicones in it, thickened like a water-based gel.", evidence)
    return Base("unknown", "unknown", "low", "None of the rules fit. Here's what the decoder saw.", evidence)  # R8
