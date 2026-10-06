"""What the decoder knows that CosIng doesn't say. Rules live here as data, not as if-statements.

The amounts are rough ranges from published studies and dermatology references, written down
so the decoder can compare them with what a label allows. They are not medical advice.
"""
from __future__ import annotations

from dataclasses import dataclass

# Words that mean "a fragrance blend is in here".
FRAGRANCE = {"PARFUM", "AROMA", "FRAGRANCE"}

# The 26 fragrance allergens EU law makes brands name on the label
# (over 0.001% in leave-on products, 0.01% in rinse-off).
ALLERGENS = {
    "AMYL CINNAMAL", "AMYLCINNAMYL ALCOHOL", "ANISE ALCOHOL", "BENZYL ALCOHOL", "BENZYL BENZOATE",
    "BENZYL CINNAMATE", "BENZYL SALICYLATE", "BUTYLPHENYL METHYLPROPIONAL", "CINNAMAL",
    "CINNAMYL ALCOHOL", "CITRAL", "CITRONELLOL", "COUMARIN", "EUGENOL", "FARNESOL", "GERANIOL",
    "HEXYL CINNAMAL", "HYDROXYCITRONELLAL", "HYDROXYISOHEXYL 3-CYCLOHEXENE CARBOXALDEHYDE",
    "ISOEUGENOL", "LIMONENE", "LINALOOL", "METHYL 2-OCTYNOATE", "ALPHA-ISOMETHYL IONONE",
    "EVERNIA PRUNASTRI EXTRACT", "EVERNIA FURFURACEA EXTRACT",
}
# On the allergen list, but usually there as a preservative.
ALLERGEN_BUT_PRESERVATIVE = {"BENZYL ALCOHOL"}

# Ingredients that are almost never used above 1% in skincare. The first one on a list
# draws the "1% line": everything from there down is at most 1%.
UNDER_ONE_PERCENT = {
    "PHENOXYETHANOL", "ETHYLHEXYLGLYCERIN", "CHLORPHENESIN", "SODIUM BENZOATE", "POTASSIUM SORBATE",
    "METHYLPARABEN", "PROPYLPARABEN", "ETHYLPARABEN", "BUTYLPARABEN", "BENZOIC ACID", "SORBIC ACID",
    "DEHYDROACETIC ACID", "SODIUM DEHYDROACETATE", "METHYLISOTHIAZOLINONE", "CAPRYLHYDROXAMIC ACID",
    "DISODIUM EDTA", "TETRASODIUM EDTA", "TRISODIUM ETHYLENEDIAMINE DISUCCINATE", "SODIUM PHYTATE",
    "XANTHAN GUM", "CARBOMER", "PARFUM", "AROMA",
}


@dataclass(frozen=True)
class Active:
    name: str          # what people call it
    works_from: float  # the low end of the % range studies use
    usual: str         # the range, for the explanation
    note: str = ""


ACTIVES = {
    "NIACINAMIDE": Active("niacinamide", 2, "2-10%"),
    "ASCORBIC ACID": Active("vitamin C (L-ascorbic acid)", 8, "8-20%"),
    "RETINOL": Active("retinol", 0.01, "0.01-1%", "Retinol works well under 1%, so sitting low on the list is normal."),
    "RETINAL": Active("retinal", 0.03, "0.03-0.1%", "Retinal works at tiny amounts."),
    "SALICYLIC ACID": Active("salicylic acid (BHA)", 0.5, "0.5-2%"),
    "GLYCOLIC ACID": Active("glycolic acid (AHA)", 5, "5-10%"),
    "LACTIC ACID": Active("lactic acid (AHA)", 5, "5-12%", "Low on a list, lactic acid is usually just adjusting the pH."),
    "MANDELIC ACID": Active("mandelic acid (AHA)", 5, "5-10%"),
    "AZELAIC ACID": Active("azelaic acid", 10, "10-20%"),
    "TRANEXAMIC ACID": Active("tranexamic acid", 2, "2-5%"),
    "ALPHA-ARBUTIN": Active("alpha arbutin", 1, "1-2%"),
    "BENZOYL PEROXIDE": Active("benzoyl peroxide", 2.5, "2.5-10%"),
    "UREA": Active("urea", 2, "2-10%"),
    "PANTHENOL": Active("panthenol (vitamin B5)", 1, "1-5%"),
    "SODIUM HYALURONATE": Active("hyaluronic acid", 0.1, "0.1-2%", "Hyaluronic acid works at small amounts."),
    "HYALURONIC ACID": Active("hyaluronic acid", 0.1, "0.1-2%", "Hyaluronic acid works at small amounts."),
}

# What well-known ingredients are doing, in my words. CosIng lists every legal use
# (xanthan gum as a "cleanser"), so for the common ones this wins.
ROLES = {
    "AQUA": ["solvent"], "GLYCERIN": ["humectant"], "BUTYLENE GLYCOL": ["humectant", "solvent"],
    "PROPANEDIOL": ["humectant", "solvent"], "PENTYLENE GLYCOL": ["humectant", "preservative booster"],
    "CETEARYL ALCOHOL": ["thickener", "emollient"], "CETYL ALCOHOL": ["thickener", "emollient"],
    "XANTHAN GUM": ["thickener"], "CARBOMER": ["thickener"], "DISODIUM EDTA": ["chelator"],
    "SODIUM HYDROXIDE": ["pH adjuster"], "CITRIC ACID": ["pH adjuster"], "TRIETHANOLAMINE": ["pH adjuster"],
    "ETHYLHEXYLGLYCERIN": ["preservative booster"], "TOCOPHEROL": ["antioxidant"],
    "NIACINAMIDE": ["active", "brightening"], "ASCORBIC ACID": ["active", "antioxidant"],
    "TRANEXAMIC ACID": ["active", "brightening"], "ALPHA-ARBUTIN": ["active", "brightening"],
    "AZELAIC ACID": ["active", "brightening"], "RETINOL": ["active", "retinoid"], "RETINAL": ["active", "retinoid"],
    "GLYCOLIC ACID": ["active", "exfoliant"], "LACTIC ACID": ["exfoliant", "pH adjuster"],
    "MANDELIC ACID": ["active", "exfoliant"], "SALICYLIC ACID": ["active", "exfoliant"],
    "BENZOYL PEROXIDE": ["active", "acne"], "UREA": ["humectant", "exfoliant"], "PANTHENOL": ["humectant", "soothing"],
    "SODIUM HYALURONATE": ["humectant"], "HYALURONIC ACID": ["humectant"], "CERAMIDE NP": ["barrier lipid"],
    "SQUALANE": ["emollient"], "DIMETHICONE": ["silicone", "slip"], "CYCLOPENTASILOXANE": ["evaporating silicone"],
    "ISODODECANE": ["evaporating oil"], "TRIMETHYLSILOXYSILICATE": ["film former"],
    "PEG-10 DIMETHICONE": ["emulsifier"], "TRIETHOXYCAPRYLYLSILANE": ["pigment coating"],
}

# Families for the "can I use these together?" rules.
FAMILIES = {
    "retinoid": {"RETINOL", "RETINAL", "RETINYL PALMITATE", "RETINYL RETINOATE", "HYDROXYPINACOLONE RETINOATE"},
    "AHA": {"GLYCOLIC ACID", "LACTIC ACID", "MANDELIC ACID"},
    "BHA": {"SALICYLIC ACID"},
    "vitamin C": {"ASCORBIC ACID"},
    "benzoyl peroxide": {"BENZOYL PEROXIDE"},
    "copper peptide": {"COPPER TRIPEPTIDE-1"},
}


@dataclass(frozen=True)
class Clash:
    a: str
    b: str
    why: str
    instead: str


CLASHES = [
    Clash("retinoid", "AHA", "Both speed up how fast skin turns over. Together they're the classic recipe for red, peeling skin.",
          "Use them on different nights."),
    Clash("retinoid", "BHA", "Both are exfoliating in their own way, and stacked they irritate.",
          "Use them on different nights."),
    Clash("retinoid", "benzoyl peroxide", "Benzoyl peroxide is an oxidizer and can break retinoids down before they work.",
          "Benzoyl peroxide in the morning, the retinoid at night."),
    Clash("vitamin C", "benzoyl peroxide", "Benzoyl peroxide oxidizes vitamin C, which is what vitamin C is trying not to do.",
          "Use them at different times of day."),
    Clash("copper peptide", "vitamin C", "Vitamin C's low pH can break up the copper peptide.",
          "Copper peptides at night, vitamin C in the morning."),
    Clash("copper peptide", "AHA", "Acids can break up the copper peptide.", "Use them on different nights."),
    Clash("AHA", "BHA", "Two exfoliating acids at once is a lot for most skin.",
          "Fine in one well-made product; think twice about layering two separate ones."),
]
