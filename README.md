# Fine Print ✦

*Paste the ingredients. Find out what's actually in it.*

## Ownership

© 2026 Suhani Tiwari. **All rights reserved.** This is my original work. The code is public so you can see how I build, not so you can reuse it: copying, reusing or republishing any part of it, including for a portfolio or a class assignment, is not permitted without my written permission. See [LICENSE](LICENSE).

## What it is

A skincare and makeup ingredient decoder. It runs as a website (the Python runs right in your browser) and on the command line. You paste the ingredient list off the back of a product, or a few of them for your whole routine, and it answers the questions the front of the box won't:

- **Is it actually fragrance-free?** Not just "is *parfum* on the list," but also essential oils and the fragrance allergens EU law makes brands name.
- **What's really doing the work?** Where the 1% line falls, and whether the hero ingredient on the front is in there at an amount that does anything.
- **Can I use these together?** Retinol with glycolic acid, vitamin C with benzoyl peroxide, and so on, across the products in your routine.
- **What base is this foundation?** Silicone, water or oil, and how it'll hold up in heat.

```
$ python -m fineprint examples/hero-dusting-cream.txt

Hero Dusting Cream ✦  16 ingredients

Fragrance-free?  No. No 'parfum' on the label, but it's scented with essential oils.
   · Lavandula Angustifolia Oil (#13)
   · Citrus Aurantium Dulcis Peel Oil (#14)
   · Limonene (#15)
   · Linalool (#16)

What's doing the work
   The 1% line falls at #8 (Phenoxyethanol). Everything from there down is 1% or less, so 7 ingredients make up at least 91% of the bottle.
   ✗ niacinamide: At #10 it's at most 1%, and studies use 2-10%. It's on the label more than it's in the bottle.
   ✗ vitamin C (L-ascorbic acid): At #11 it's at most 1%, and studies use 8-20%. It's on the label more than it's in the bottle.
   ✗ tranexamic acid: At #12 it's at most 1%, and studies use 2-5%. It's on the label more than it's in the bottle.
```

## How it's built

Plain Python on the standard library. The website runs that same Python in the browser through **Pyodide** (WebAssembly), so the command line and the site share one engine, and nothing you paste leaves your device.

1. **Data** (`tools/fetch_cosing.py`): all 33,639 ingredients in the EU's CosIng database, downloaded from the API behind CosIng's own website. That API stops at 10,000 results per query, and its range filters don't work on the ID field, so the script asks for IDs in explicit batches of 5,000, pages through each batch, and checks the total against the API's own count.
2. **Parsing** (`parse.py`): labels are messy in predictable ways. A comma ends a name, except in chemistry (`1,2-Hexanediol`) and inside brackets. One ingredient can be printed three ways at once (`Aqua/Water/Eau`, `Parfum (Fragrance)`). Footnotes (`*Organic`) get dropped, and the "may contain [+/-]" shade colorants are kept apart because they sit outside the order.
3. **Matching** (`catalog.py`): everyday names first (`Water`, `Vitamin C`), then exact INCI names after normalizing, then fuzzy matching for typos. A **trigram index** narrows 33,000 names to 40 candidates, and **Damerau-Levenshtein edit distance** picks the closest, so `Glycrein` reads as Glycerin. Anything further than about one typo per eight letters stays unknown rather than being guessed.
4. **The 1% line** (`decode.py`): ingredients above 1% are listed from most to least, so the one at position *n* can't be more than 100/*n* percent. The first preservative or thickener that's almost never used above 1% (phenoxyethanol, xanthan gum, EDTA) draws the line, and everything from there down is capped at 1%. Each hero ingredient's cap is compared with the range studies use.
5. **Rules as data** (`knowledge.py`): the fragrance allergens, the under-1% markers, the actives and their working ranges, and the ingredient clashes each live in one table, not in if-statements. A clash only counts when the active is there at a working level, so lactic acid adjusting the pH doesn't count as an exfoliant.
6. **Foundation base** (`base.py`): ingredients are sorted into families (evaporating silicones, silicone emulsifiers, film formers, pigment coatings, water-in-oil emulsifiers, water-phase thickeners), and eight rules are checked in order, first match wins. Water is listed first in most silicone foundations, so it reads the top eight and the emulsifier, never ingredient #1 alone. The rules come from my research in [reports/](reports/).
7. **The website** (`index.html`, `web/app.js`, `fineprint/web.py`): paste one label or a whole routine. Each label is drawn with its 1% line, a bar for the most each ingredient can be, and tags on the heroes and the scent. The database ships as 1.5 MB of compact JSON (82 function names stored once, rows point at them by number), and a service worker keeps Pyodide on the phone after the first visit.
8. **Check** (`tests/`): 38 pytest cases covering the parser's edge cases, the matching, every fragrance verdict, the 1% caps, the clash rules and each foundation base.

## Tech stack

Python (standard library), Pyodide / WebAssembly, vanilla JavaScript, service worker, the EU CosIng API, pytest, GitHub Pages.

## Run it locally

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m fineprint "Aqua, Niacinamide, Glycerin, Phenoxyethanol"
.venv/bin/python -m fineprint examples/retinol-night-cream.txt examples/glow-toner.txt
.venv/bin/python -m fineprint examples/long-wear-foundation.txt --all
.venv/bin/python -m pytest -q
.venv/bin/python tools/fetch_cosing.py          # download CosIng again
python3 -m http.server 8000                      # the website, at http://localhost:8000
```

| Option | What it does |
|---|---|
| one label | decode it: fragrance, the 1% line, the hero check |
| two or more | also check the routine for clashes |
| `--base` | say what base it is (automatic when the list has pigments) |
| `--all` | every ingredient, its cap and what CosIng says it does |

Ingredient data from the European Commission's CosIng database. The working ranges are rough, from published studies, and this is not medical advice.

Built by [Suhani Tiwari](https://suhanitiwari.com).
