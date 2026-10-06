"""Fine Print ✦  Paste the ingredients. I'll tell you what's actually in it.

    python -m fineprint "Aqua, Niacinamide, Glycerin, ..."      decode a label
    python -m fineprint examples/serum.txt                      or a file with one in it
    python -m fineprint examples/retinol.txt examples/toner.txt can I use these together?
    python -m fineprint examples/foundation.txt --base          what base is this foundation?
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .catalog import pretty
from .decode import Decoded, decode, fmt, together

ROSE, BOLD, DIM, RESET = "\033[38;5;174m", "\033[1m", "\033[2m", "\033[0m"


def read(arg: str, n: int) -> tuple[str, str]:
    path = Path(arg)
    if len(arg) < 260 and path.is_file():
        return path.stem.replace("-", " ").replace("_", " ").title(), path.read_text(encoding="utf-8")
    return (f"Product {n}" if n else "This product"), arg


def show(d: Decoded, every: bool, base: bool) -> None:
    print(f"\n{ROSE}{BOLD}{d.name} ✦{RESET}  {DIM}{len(d.ordered)} ingredients"
          + (f", {len(d.items) - len(d.ordered)} shade colorants" if len(d.items) > len(d.ordered) else "") + RESET)

    f = d.fragrance
    print(f"\n{BOLD}Fragrance-free?{RESET}  {'' if f.free else 'No. '}{f.verdict}")
    for c in f.culprits:
        print(f"   {DIM}·{RESET} {c}")

    print(f"\n{BOLD}What's doing the work{RESET}")
    if d.line:
        above = [i for i in d.ordered if not i.below_line]
        print(f"   The 1% line falls at #{d.line} ({pretty(d.ordered[d.line - 1].inci)}). "
              f"Everything from there down is 1% or less, so {len(above)} ingredients make up at least "
              f"{100 - (len(d.ordered) - len(above)):.0f}% of the bottle.")
    else:
        print("   No preservative or thickener shows where the 1% line is, so the caps below are from order alone.")
    if not d.heroes:
        print(f"   {DIM}No well-studied actives on this list.{RESET}")
    for h in d.heroes:
        mark = {"too little": "✗", "works low": "✓", "could be enough": "✓"}[h.verdict]
        print(f"   {mark} {BOLD}{h.active.name}{RESET}: {h.note}")

    if base or d.is_makeup:
        b = d.base
        print(f"\n{BOLD}Base{RESET}  {b.kind}  {DIM}({b.emulsion}, {b.confidence} confidence){RESET}")
        print(f"   {b.rule}")
        if b.heat_note:
            print(f"   In heat: {b.heat_note}")
        for line in b.evidence[:5]:
            print(f"   {DIM}{line}{RESET}")

    if d.fuzzy or d.unknown:
        print(f"\n{BOLD}Spelling check{RESET}")
        for i in d.fuzzy:
            print(f"   \"{i.entry.printed}\" read as {pretty(i.inci)}")
        for i in d.unknown:
            print(f"   \"{i.entry.printed}\" isn't in the EU ingredient database")

    if every:
        print(f"\n{BOLD}Every ingredient{RESET}")
        for i in d.items:
            pos = f"#{i.entry.position:<2}" if i.entry.position else "+/-"
            cap = f"≤{fmt(i.at_most)}%" if i.at_most is not None else ""
            jobs = ", ".join(i.ingredient.jobs) if i.ingredient else "?"
            print(f"   {pos} {pretty(i.inci):<42} {cap:>6}  {DIM}{jobs}{RESET}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="fineprint", description="Paste the ingredients. I'll tell you what's actually in it.")
    p.add_argument("labels", nargs="+", help="an ingredient list, or a text file with one; give two or more to check a routine")
    p.add_argument("--base", action="store_true", help="say what base a foundation is (automatic for makeup)")
    p.add_argument("--all", action="store_true", help="list every ingredient, its cap and what it does")
    args = p.parse_intermixed_args(argv)   # flags can go anywhere

    many = len(args.labels) > 1
    products = [decode(text, name) for name, text in (read(a, n + 1 if many else 0) for n, a in enumerate(args.labels))]
    for d in products:
        show(d, args.all, args.base)

    if many:
        print(f"\n{ROSE}{BOLD}Can I use these together? ✦{RESET}")
        clashes = together(products)
        if not clashes:
            print("   Yes. Nothing in this routine fights.")
        for c in clashes:
            (an, ai), (bn, bi) = c.first, c.second
            print(f"   {BOLD}{an}{RESET}'s {pretty(ai.inci)} + {BOLD}{bn}{RESET}'s {pretty(bi.inci)}")
            print(f"   {c.clash.why}")
            print(f"   {ROSE}{c.clash.instead}{RESET}")
    print(f"\n{DIM}Ingredient data: EU CosIng. Amounts are rough ranges from published studies, not medical advice.{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
