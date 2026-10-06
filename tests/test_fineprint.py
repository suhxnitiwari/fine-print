from pathlib import Path

import pytest

from fineprint.base import classify, family
from fineprint.catalog import edit_distance, key, load
from fineprint.decode import decode, together
from fineprint.parse import alternatives, parse, split_commas

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def example(name):
    return decode((EXAMPLES / f"{name}.txt").read_text(), name)


# Parsing the label

def test_chemistry_commas_stay_inside_names():
    assert split_commas("Aqua, 1,2-Hexanediol, 2,4-Dichlorobenzyl Alcohol") == [
        "Aqua", "1,2-Hexanediol", "2,4-Dichlorobenzyl Alcohol"]


def test_commas_inside_brackets_stay_together():
    assert split_commas("Water, Iron Oxides (CI 77491, CI 77492)") == ["Water", "Iron Oxides (CI 77491, CI 77492)"]


def test_one_ingredient_written_three_ways():
    assert alternatives("Aqua/Water/Eau")[:4] == ["Aqua/Water/Eau", "Aqua", "Water", "Eau"]
    assert alternatives("Parfum (Fragrance)*") == ["Parfum (Fragrance)", "Parfum", "Fragrance"]


def test_label_word_footnotes_and_may_contain():
    entries = parse("Ingredients: Aqua, Glycerin*, Parfum. *Organic. May Contain [+/-]: CI 77891, CI 77491.")
    assert [e.printed for e in entries if not e.may_contain] == ["Aqua", "Glycerin*", "Parfum"]
    assert [e.printed for e in entries if e.may_contain] == ["CI 77891", "CI 77491"]
    assert all(e.position == 0 for e in entries if e.may_contain)


def test_bullets_and_new_lines_are_separators():
    assert [e.printed for e in parse("Water • Glycerin\nNiacinamide")] == ["Water", "Glycerin", "Niacinamide"]


# Finding each ingredient in CosIng

def test_catalog_is_the_whole_eu_database():
    assert len(load().by_key) > 30_000


def test_key_normalizes_spacing_and_dashes():
    assert key(" sodium   hyaluronate. ") == "SODIUM HYALURONATE"
    assert key("PEG - 10 Dimethicone") == "PEG-10 DIMETHICONE"


@pytest.mark.parametrize("printed, inci, how", [
    ("Niacinamide", "NIACINAMIDE", "exact"),
    ("Aqua/Water/Eau", "AQUA", "exact"),
    ("Water", "AQUA", "everyday"),
    ("Vitamin C", "ASCORBIC ACID", "everyday"),
    ("Glycrein", "GLYCERIN", "fuzzy"),
    ("Niacinamid", "NIACINAMIDE", "fuzzy"),
])
def test_matching(printed, inci, how):
    m = load().match(alternatives(printed))
    assert (m.ingredient.inci, m.how) == (inci, how)


def test_nonsense_stays_unknown():
    assert load().match(["Unicorn Tears"]).ingredient is None


def test_swapped_letters_are_one_typo():
    assert edit_distance("GLYCERIN", "GLYCREIN") == 1
    assert edit_distance("GLYCERIN", "GLYCERIN") == 0


def test_essential_oils_vs_carrier_oils():
    c = load()
    assert c.get("LAVANDULA ANGUSTIFOLIA OIL").essential_oil
    assert c.get("CITRUS LIMON PEEL OIL").essential_oil
    for carrier in ("RICINUS COMMUNIS SEED OIL", "COCOS NUCIFERA OIL", "SIMMONDSIA CHINENSIS SEED OIL"):
        assert not c.get(carrier).essential_oil


# Fragrance-free?

def test_parfum_means_not_fragrance_free():
    f = example("glow-toner").fragrance
    assert not f.free and "Parfum (#11)" in f.culprits


def test_essential_oils_are_fragrance_too():
    assert not example("hero-dusting-cream").fragrance.free


def test_allergens_alone_give_it_away():
    assert not decode("Aqua, Glycerin, Phenoxyethanol, Linalool, Limonene").fragrance.free


def test_benzyl_alcohol_alone_is_a_preservative():
    assert decode("Aqua, Glycerin, Benzyl Alcohol, Dehydroacetic Acid").fragrance.free


def test_clean_list_is_fragrance_free():
    assert example("niacinamide-serum").fragrance.free


# What's doing the work

def test_one_percent_line_is_the_first_preservative_or_thickener():
    assert example("niacinamide-serum").line == 7      # Xanthan Gum
    assert example("glow-toner").line == 9             # Phenoxyethanol


def test_position_caps_how_much_there_can_be():
    d = decode("Aqua, Glycerin, Niacinamide, Phenoxyethanol, Panthenol")
    caps = [i.at_most for i in d.ordered]
    assert caps[:3] == [100, 50, pytest.approx(100 / 3)]
    assert caps[3:] == [1, 1]


def test_heroes_below_the_line_are_label_dusting():
    verdicts = {h.active.name: h.verdict for h in example("hero-dusting-cream").heroes}
    assert verdicts["niacinamide"] == "too little"
    assert verdicts["tranexamic acid"] == "too little"


def test_low_dose_actives_are_fine_below_the_line():
    heroes = decode("Aqua, Glycerin, Phenoxyethanol, Retinol").heroes
    assert heroes[0].verdict == "works low"


def test_niacinamide_at_two_could_be_enough():
    assert example("niacinamide-serum").heroes[0].verdict == "could be enough"


# Can I use these together?

def test_retinol_and_glycolic_clash():
    clashes = together([example("retinol-night-cream"), example("glow-toner")])
    assert [(c.clash.a, c.clash.b) for c in clashes] == [("retinoid", "AHA")]


def test_lactic_acid_as_a_ph_tweak_is_not_an_exfoliant():
    retinol = example("retinol-night-cream")
    tweak = decode("Aqua, Glycerin, Squalane, Phenoxyethanol, Lactic Acid", "pH")
    assert together([retinol, tweak]) == []


def test_no_clash_inside_one_routine_of_gentle_things():
    assert together([example("niacinamide-serum"), example("skin-tint")]) == []


# What base is this foundation?

def test_families():
    assert family("Cyclopentasiloxane") == "cyclic_silicone"
    assert family("PEG-10 Dimethicone") == "silicone_emulsifier"
    assert family("Triethoxycaprylylsilane") == "pigment_coating"
    assert family("Magnesium Aluminum Silicate") == ""       # a clay, not a silicone
    assert family("Sodium Benzoate") == ""                   # a preservative, not an ester


def test_water_first_can_still_be_silicone_based():
    b = classify(["AQUA", "CYCLOPENTASILOXANE", "DIMETHICONE", "BUTYLENE GLYCOL", "PEG-10 DIMETHICONE"])
    assert (b.kind, b.emulsion, b.confidence) == ("silicone", "water-in-silicone", "high")


def test_silicone_first():
    assert classify(["DIMETHICONE", "AQUA", "GLYCERIN"]).kind == "silicone"


def test_silicone_and_oil_hybrid():
    assert example("long-wear-foundation").base.kind == "silicone + oil"


def test_silicone_free_water_in_oil():
    b = classify(["AQUA", "ISODODECANE", "CAPRYLIC/CAPRIC TRIGLYCERIDE", "GLYCERIN", "POLYGLYCERYL-4 ISOSTEARATE"])
    assert (b.kind, b.emulsion) == ("oil", "water-in-oil")


def test_water_based_skin_tint():
    b = example("skin-tint").base
    assert (b.kind, b.confidence) == ("water", "high")


def test_waterless_balm():
    assert example("balm-foundation").base.kind == "waterless oil"


def test_makeup_is_spotted_by_its_pigments():
    assert example("skin-tint").is_makeup
    assert not example("niacinamide-serum").is_makeup


def test_jobs_are_what_it_does_in_skincare():
    c = load()
    assert c.get("GLYCERIN").jobs[0] == "humectant"
    assert c.get("PHENOXYETHANOL").jobs[0] == "preservative"
    assert c.get("LAVANDULA ANGUSTIFOLIA OIL").jobs[0] == "scent"
