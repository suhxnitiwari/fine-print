# Foundation Base Chemistry and INCI-Based Base Classification Rules

Scope: liquid foundation base types (water-based / O/W, W/O, water-in-silicone, silicone-in-water, anhydrous), the job of each key ingredient class, the EU D4/D5/D6 restrictions, and rules a Python program could use to classify a foundation's base from its ordered INCI list. Researched October 2026. "Formulator lore" (practitioner rules of thumb that no primary or peer-reviewed source documents) is marked as such.

## Q1. What emulsion types are used in foundations, and which dominates modern long-wear foundations? Why water-in-silicone?

### Takeaway
Liquid foundations are mostly emulsions: O/W, W/O, or W/O where the oil phase is mainly silicone (W/Si). Anhydrous products (sticks, pancake, waterless serum or oil foundations) make up a smaller share. Formulator sources agree that the "vast majority" of modern liquid foundations are water-in-oil/silicone. The reasons are that a continuous silicone/oil phase sits against the skin (better spread and feel, and it hides the dry feel of the pigment) and that silicones form flexible, long-lasting films and allow an "oil-free" claim.

### Cited Findings
- Foundation categories in current use: loose and pressed powders, anhydrous "pancake" formulas (powder + emollient + wax), and emulsions (O/W or W/O). — [UL Prospector, "PCC: Contemporary Foundation Formulations"](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)
- "The vast majority of current marketed forms are water in oil/silicone-based formulations." The reason given: they "apply more evenly and feel better on skin because the continuous oil phase of the emulsion is in contact with skin, which reduces the dry feel of the pigments." The source credits the shift to better W/O polymeric emulsifiers, emollients and pigment coating technology over the last 20 years. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)
- Typical W/O/W-Si foundation composition: water 40–60%, humectants 1–10%, emulsifiers 2–5%, emollients/silicones 10–20%, coverage pigment (TiO2, occasionally ZnO) 3–15%, shade pigments (iron oxides) 1–5%, effect pigments 0–3%, other powders 0–5%, stabilizers 0.5–2%, preservatives 1–3%, dispersing agents 0.5–1%, chelators 0.05–0.1%. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)
- Silicone-free ("green") W/O foundation ranges: water 50–70%, emollients/waxes 10–20%, coverage pigments 5–20%, iron oxides 1–7%, emulsifier 2–5%. W/O is preferred for these too because pigments disperse better in the oil phase, with less agglomeration and less drying than in O/W. — [UL Prospector, "PCC: How to Formulate Green Liquid Foundations"](https://ulprospector.ul.com/knowledge/9591/pcc-how-to-formulate-green-liquid-foundations/)
- Lab Muffin (Michelle Wong, PhD chemist) states that "water-in-silicone foundations are now more than 90% of liquid foundations in the market." Over the past ~20 years silicone emulsions replaced the earlier O/W and W/O types. Reasons she gives: silicones are very slippery as the outer phase, so foundation spreads evenly without caking or skill; they form flexible films that last long on skin (long-wear); they don't feel greasy; and they let brands say "oil-free" because silicones aren't technically oils. — [Lab Muffin, "Fixing foundation clumping"](https://labmuffin.com/fixing-foundation-clumping-with-video/). *The ">90%" figure is a chemist-blogger estimate with no market data behind it. Treat it as lore-grade.*
- Dow's W/Si emulsifiers are marketed to make W/Si and water-in-silicone-and-oil emulsions with textures from lotion to cream, "leaving a light, non-greasy after feel." Their small particle size gives stability at elevated temperature and through freeze-thaw cycles. — [Univar/Dow, DOWSIL FZ-2233](https://www.univarsolutions.com/dowsil-fz-2233-16040847); [Univar/Dow, DOWSIL ES-5300](https://www.univarsolutions.com/dowsil-es-5300-formulation-aid-16040013) *(supplier marketing)*
- W/O and W/Si foundations resist water because, after spreading, the water evaporates and leaves an oil or silicone film on the skin. — [US patent 5,985,297 / RE39218, "Anhydrous and water-resistant cosmetic compositions"](https://patents.google.com/patent/US5985297)
- Patent definitions of "anhydrous" usually mean <5% water by mass (down to <0.01%). Anhydrous bases avoid water-related limits, such as including moisture-sensitive materials. — [USPTO patent 12,673,013 "Cosmetic composition"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12673013); [US 6,103,250](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6103250)
- Mismatched outer phases (e.g. a water-based product layered under a silicone-based foundation) can repel each other and cause "patchy clumping." — [Lab Muffin](https://labmuffin.com/fixing-foundation-clumping-with-video/)

### Inferences
- In a W/Si or W/O foundation, water is usually 40–70% of the formula even though silicone/oil is the *continuous* phase. So **water is normally ingredient #1 on the label of a "silicone-based" foundation.** The first ingredient alone cannot separate O/W from W/Si.
- Silicone-in-water (Si/W) foundations exist in principle: silicone droplets in a continuous water phase, the silicone analogue of O/W. Chemically and for label purposes they behave like O/W, with water and hydrophilic thickeners in the continuous phase. I found no source on their market share.
- The commercial "base" labels ("water-based", "silicone-based", "oil-based") describe the **continuous (outer) phase**, not the largest ingredient. This matters for primer/foundation compatibility, which is also about the outer phase.

### Gaps
- No independent market-share data (e.g. Mintel or Euromonitor) for W/Si vs O/W vs anhydrous liquid foundations. The only quantitative claim is Lab Muffin's ">90%".
- I found no primary source specific to silicone-in-water foundations.

## Q2. Roles of volatile silicones/hydrocarbons, non-volatile silicones, silicone emulsifiers, film formers, and coated pigments

### Takeaway
A long-wear W/Si foundation is built in layers. A volatile carrier (D5/D6 historically, now isododecane, hemisqualane, C13-15 alkane, or low-viscosity dimethicone) gives slip and then evaporates. Non-volatile silicones and elastomers (dimethicone, dimethicone crosspolymer) stay behind for feel and blur. Silicone polyether emulsifiers hold the water droplets inside the silicone phase. Resins (trimethylsiloxysilicate) and acrylates form a durable, transfer-resistant film. Hydrophobically coated TiO2 and iron oxides (often triethoxycaprylylsilane-treated) disperse in the oil/silicone phase and stabilize the emulsion.

### Cited Findings
**Silicone emulsifiers (W/Si):**
- W/O-W/Si emulsifiers named for foundations: Lauryl PEG-9 Polydimethylsiloxyethyl Dimethicone, PEG-10 Dimethicone, PEG/PPG-18/18 Dimethicone, Cetyl PEG/PPG-10/1 Dimethicone. Non-silicone W/O emulsifiers: PEG-30 Dipolyhydroxystearate, Polyglyceryl-4 Isostearate. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)
- Silicone-free W/O emulsifiers: Tri(polyglyceryl-3/lauryl) hydrogenated trilinoleate, polyglyceryl-2 dipolyhydroxystearate, polyglyceryl-4 diisostearate/polyhydroxystearate/sebacate. W/O stabilizers: silica, silica silylate, quaternium-18 bentonite, quaternium-90 sepiolite/montmorillonite. Silicone-free emollients: squalane, jojoba, caprylic/capric triglyceride, isoamyl laurate. — [UL Prospector, green foundations](https://ulprospector.ul.com/knowledge/9591/pcc-how-to-formulate-green-liquid-foundations/)
- Patent literature lists W/Si emulsifiers including dimethicone PEG-10/15 crosspolymer, dimethicone copolyol (old name for PEG-x dimethicone), cetyl dimethicone copolyol, PEG-15 lauryl dimethicone crosspolymer, PEG-10 dimethicone, PEG-10 dimethicone crosspolymer. Typical levels range from 0.001–10%, with preferred ranges of 0.01–5% and "below 1%." — [USPTO patent 8,501,162](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8501162)
- An example W/Si SPF foundation main phase in a patent: cyclopentasiloxane, ethylhexyl methoxycinnamate, ethylhexyl stearate, cyclohexasiloxane, dimethicone, dimethicone copolyol, cetyl PEG/PPG-10/1 dimethicone, hexyl laurate, polyglyceryl-4 isostearate, phenoxyethanol. This shows silicone and oil emulsifiers being combined ("water-in-silicone-and-oil"). — [USPTO patent 8,501,162](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8501162)
- Anhydrous products can also contain emulsifying silicone elastomers and silicone polyethers such as PEG/PPG-18/18 dimethicone and Lauryl PEG-10 Tris(Trimethylsiloxy)silylethyl Dimethicone. **A silicone emulsifier is therefore not proof that water is present.** — [US 6,103,250 "Anhydrous cosmetic compositions containing emulsifying siloxane elastomer"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6103250)

**Volatile carriers:**
- Hemisqualane, isododecane, C13-15 alkane and polydecene are the volatile/light replacements for D5. Isododecane "flashes off more quickly than D5" and gives a very dry finish. Hemisqualane is the closest one-to-one match for slip and dry-down. Example blends: 60% hemisqualane + 40% isododecane for light emulsions; 50/30/20 hemisqualane/C13-15 alkane/polydecene for primers or BB creams. — [Grand Ingredients, "D5 Replacement: Volatile Profiles Without Siloxanes"](https://grandingredients.com/d5-replacement-siloxane-free/) *(supplier marketing)*
- Aprinnova (hemisqualane/squalane maker) published data on replacing D5. — [Cosmetics & Toiletries news](https://www.cosmeticsandtoiletries.com/home/news/21860401/aprinnova-15304-aprinnova-rolls-out-data-resources-to-replace-d5-in-aps) *(supplier news; full text not reviewed)*

**Film formers:**
- Trimethylsiloxysilicate (MQ silicone resin) forms a durable, flexible film for long-wear, transfer resistance, and water/oil resistance with a non-greasy feel. Uses include foundations and makeup that need rub-off resistance. — [MakingCosmetics silicone resin fact sheet](https://makingcosmetics.com/on/demandware.static/-/Sites-makingcosmetics-master/default/dwa8b13674/fact-sheets/fact-sheet-silicone-resin.pdf); [Elkem PURESIL TMS IDD 50 (trimethylsiloxysilicate pre-dissolved in isododecane)](https://knowde.com/stores/elkem-silicones/products/puresil-tms-idd-50)
- Shin-Etsu and Siltech both market newer silicone film-former technologies for long-wear foundations. — [MedEsthetics on Shin-Etsu](https://www.medestheticsmag.com/home/news/22886546/shin-etsu-silicones-of-america-shinetsu-silicones-of-americas-unveils-silicone-film-former-tech-for-long-wear-comfort); [Cosmetics & Toiletries on Siltech](https://www.cosmeticsandtoiletries.com/cosmetic-ingredients/colorant/news/22968872/siltech-siltech-shakes-up-color-cosmetics-with-launch-of-highperformance-film-former-and-dualeffect-elastomers)

**Coated pigments:**
- TiO2 (anatase or rutile) provides coverage and iron oxides provide shade. Pigments go in the external phase of the emulsion and may need hydrophobic surface treatment in W/O foundations. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)
- Triethoxycaprylylsilane (TC)-treated pigments carry a very hydrophobic alkyl-silane coating. It eases dispersion in oils and silicones (best in non-polar or low-polarity oils), lowers oil absorption, improves wear, and "improve[s] the stability of W/Si and W/O emulsions." Available as TC-treated TiO2, red/yellow/black iron oxide and ultramarines, for BB creams, foundations and pressed powders. — [Gelest technical library, TC-treated pigments](https://technical.gelest.com/brochures/cosmetic-pigments/triethoxycaprylylsilane-tc-treated/)
- Surface-treated pigments were once mostly limited to anhydrous products (lipsticks, powders, mascaras) and heavy oil-based emulsions. They are now also used in O/W emulsions. — [UL Prospector search summary of contemporary foundations article](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)

### Inferences
- On the label, coating agents (triethoxycaprylylsilane, dimethicone, methicone, hydrogenated lecithin, isopropyl titanium triisostearate, aluminum hydroxide, etc.) usually appear as separate ingredients, often well down the list. **A low-position silicone such as triethoxycaprylylsilane or methicone signals pigment treatment, not a silicone base.** A classifier should ignore these when deciding the base. (Inference based on Gelest naming the INCI as "Triethoxycaprylylsilane". Exact label positions are not documented in my sources.)
- Ingredients that come as supplier pre-blends (e.g. trimethylsiloxysilicate in isododecane, or elastomers swollen in dimethicone or D5) add their carrier to the label. This is why isododecane or dimethicone can rank high even when the "active" polymer is minor.

### Gaps
- I found no primary source on trisiloxane or low-viscosity dimethicone (0.65–2 cSt) as volatile D5 replacements in foundations. My background knowledge says Dow and others sell these as D5 alternatives, but I did not verify it in this session.
- I found no source specifying acrylates copolymer or the acrylates/dimethicone copolymer film formers in foundations. Their role as film formers is general knowledge but uncited here.
- I found no typical-percentage data for volatile silicone, film former or emulsifier separately within a foundation, beyond the 10–20% "emollients/silicones" bucket and the patent emulsifier ranges.

## Q3. How to tell the base from the label, including edge cases

### Takeaway
Read the base from the **top ~5 ingredients plus the emulsifier type**, not from ingredient #1. If water is first and a silicone polyether emulsifier is present, with silicones or volatile alkanes in positions 2–4, the product is W/Si. If water is first and there are hydrophilic thickeners and O/W emulsifiers, with silicones only low on the list, it is water-based (O/W). If silicones or hydrocarbons/esters are first and there is no water anywhere, it is anhydrous. Label law limits how precise this can be: only ingredients above 1% must appear in descending order.

### Cited Findings
- **Label ordering law (US):** Ingredients appear in descending order of predominance. As an alternative, ingredients >1% (non-color) go in descending order, then ingredients ≤1% in any order, then color additives in any order. — [21 CFR 701.3 (govinfo)](https://www.govinfo.gov/content/pkg/CFR-1996-title21-vol7/html/CFR-1996-title21-vol7-sec701-3.htm)
- **Label ordering law (EU):** Regulation 1223/2009 Art. 19 requires INCI names in descending order of weight at the time of addition. Ingredients below 1% may appear in any order after those above 1%. Colorants (other than hair dyes) may appear in any order after other ingredients, using CI numbers (e.g. CI 77891 = TiO2, CI 77491/77492/77499 = iron oxides). — [ChemLinked EU ingredient regulations summary](https://cosmetic.chemlinked.com/cosmepedia/eu-cosmetic-ingredient-regulations); [Ceway, cosmetic product label](https://news.ceway.eu/?p=693)
- **Chemist rule of thumb:** "If the ingredients list has silicones in the top 4 ingredients, it's almost guaranteed that it's a water-in-silicone emulsion." Look for names ending in "-cone" or "-siloxane" (cyclopentasiloxane, dimethicone, phenyl trimethicone). Lab Muffin adds that for *non-foundation* products the ingredient list is unreliable for working out emulsion type. — [Lab Muffin](https://labmuffin.com/fixing-foundation-clumping-with-video/)
- Consumer/brand guidance: water-based foundations have water/aqua first and normally contain no silicones, or only small amounts low on the list. Silicone-based ones have "-cone"/"-siloxane" names (dimethicone, cyclopentasiloxane, trimethylsiloxysilicate) in the top three. Water listed first "doesn't necessarily mean that the foundation is water based." — [Women's Weekly AU](https://www.womensweekly.com.au/beauty/makeup/water-based-foundation-silicone-based-foundation/); [L'Oréal Paris USA](https://www.lorealparisusa.com/beauty-magazine/makeup/face-makeup/water-based-foundation) *(consumer and brand sources, lower authority; they agree with Lab Muffin)*
- W/Si foundations contain 40–60% water. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)

### Inferences (edge cases)
- **Water first in W/Si:** expected, since water is 40–60%. Decide by what follows: silicone emulsifiers plus silicones or volatile alkanes in positions 2–5.
- **Silicone-free W/O ("oil-based" emulsion):** water first, then isododecane, C13-15 alkane, hemisqualane/squalane or esters, with polyglyceryl/PEG-30 dipolyhydroxystearate emulsifiers and quaternium-18/90 clays. These are W/O, not O/W, but a naive "no silicones = water-based" rule would label them water-based.
- **Isododecane as a silicone substitute:** functionally it plays the volatile-carrier role of D5 (it evaporates and leaves pigments/film). For wear and primer compatibility it behaves more like a silicone-phase product than an O/W one. A classifier should output something like "W/O (hydrocarbon)" rather than "water-based".
- **Post-2024 EU reformulations:** cyclopentasiloxane and cyclohexasiloxane will drift off EU labels. The likely replacements are dimethicone (low-viscosity), isododecane, hemisqualane, C13-15 alkane, undecane/tridecane, or trisiloxane. Rules keyed only on "cyclo*siloxane" will miss newer W/Si formulas. Key on any silicone name *plus* emulsifier type instead.
- **Pre-blends:** a high-ranking "dimethicone" may be the carrier for an elastomer (dimethicone crosspolymer). It still indicates a silicone continuous phase.
- **Low-position silicones** (triethoxycaprylylsilane, methicone, dimethicone below ~position 10) are often pigment coatings or minor feel modifiers. They don't make a product silicone-based.
- **Anhydrous with silicone emulsifier:** some waterless formulas contain PEG/PPG dimethicones or emulsifying elastomers, per US 6,103,250. No water/aqua anywhere means anhydrous, whatever emulsifier is present.
- **Glycerin, butylene glycol or propanediol high on the list** with no water: possibly a polyol-in-silicone "anhydrous emulsion". This is rare. Flag it as anhydrous (polyol-in-Si) for review.
- **"Oil-free" claims** often mean silicone- or hydrocarbon-based, not water-based (Lab Muffin notes silicones let brands claim oil-free).

### Gaps
- No peer-reviewed validation of the "top 4 silicones" heuristic. It is chemist lore, though from a credible chemist.
- Below position ~5–8 (wherever ingredients drop under 1%), order carries no concentration information. No source gives a typical label position for the 1% cutoff. Phenoxyethanol (capped at 1% in the EU) is often used informally as a marker; that is lore and uncited here.

## Q4. EU restrictions on D4, D5, D6 and how formulators replaced them

### Takeaway
D4 is banned outright from EU cosmetics (Annex II, 2019). D4 and D5 were capped at 0.1% in wash-off cosmetics from 31 Jan 2020 (Reg. 2018/35). Regulation (EU) 2024/1328 extended a 0.1% cap on D4/D5/D6 to leave-on cosmetics, effective **6 June 2027**, and covers D6 in wash-off products too. That means leave-on foundations sold in the EU must drop D5/D6 by mid-2027. Replacements are hydrocarbons (isododecane, hemisqualane, C13-15 alkane, polydecene), often blended, plus non-cyclic silicones.

### Cited Findings
- **Regulation (EU) 2018/35** (10 Jan 2018) amended REACH Annex XVII to cap D4 and D5 at 0.1% by weight in wash-off cosmetics from **31 Jan 2020**, due to environmental risk from wastewater discharge. D4 is PBT and vPvB; D5 is vPvB. The 0.1% limit "effectively ensures that all intentional use … will cease." — [Cosmetics & Toiletries, "EU Effectively Bans D4 and D5 in Wash-Off Products"](https://www.cosmeticsandtoiletries.com/regulations/regional/news/21841038/eu-effectively-bans-d4-and-d5-in-wash-off-products); [Regulation 2018/35 text (CELEX 32018R0035)](https://www.moew.government.bg/static/media/ups/articles/attachments/CELEX_32018R0035_EN_TXT96586c7bc89e26003f05da3255f44445.pdf)
- **D4 in Annex II (prohibited):** Regulation (EU) 2019/831 of 22 May 2019 added octamethylcyclotetrasiloxane (D4) to Annex II of Cosmetics Regulation 1223/2009 as entry 1388 (CMR reclassification). It cannot be intentionally added to leave-on or rinse-off products; only technically unavoidable traces are allowed. — [Ceway, "D4 and D5 effectively banned"](https://news.ceway.eu/d4-d5-effectively-banned/); [Obelis](https://www.obelis.net/blog/silicones-on-the-spot-again)
- **Regulation (EU) 2024/1328** was published 16–17 May 2024 (sources differ by a day: OJ publication vs. adoption) and entered into force **6 June 2024**. It amends REACH Annex XVII entry 70 to cap D4, D5 and D6 at 0.1% w/w in cosmetics and other consumer/professional products. Cosmetics timeline: D5 in rinse-off already ≤0.1% since 31 Jan 2020; D5 in leave-on ≤0.1% from **6 June 2027**; D6 in rinse-off and leave-on ≤0.1% from **6 June 2027**. — [CosLaw.eu](https://coslaw.eu/reach-update-the-european-union-further-restricts-the-use-of-silicones-d5-and-d6-in-cosmetic-products/); [Biorius](https://biorius.com/cosmetic-news/d4-d5-d6-restrictions/)
- **Conflict:** one Biorius-derived summary says D6 in wash-off applies from **6 June 2026**, while CosLaw says **6 June 2027** for both rinse-off and leave-on D6. — [Biorius](https://biorius.com/cosmetic-news/d4-d5-d6-restrictions/) vs. [CosLaw.eu](https://coslaw.eu/reach-update-the-european-union-further-restricts-the-use-of-silicones-d5-and-d6-in-cosmetic-products/). *Check against the EUR-Lex text of 2024/1328 before relying on it. For leave-on foundations the date is 6 June 2027 in both sources.*
- Rationale: ECHA's Risk Assessment Committee found cosmetics to be the main source of D4/D5/D6 release to water and air. — [CosLaw.eu](https://coslaw.eu/reach-update-the-european-union-further-restricts-the-use-of-silicones-d5-and-d6-in-cosmetic-products/)
- Most EU rinse-off and leave-on formulas have already either removed D5 or kept it below 0.1%. — [Grand Ingredients](https://grandingredients.com/d5-replacement-siloxane-free/) *(supplier claim; unverified)*
- Replacements: hemisqualane, isododecane, C13-15 alkane, polydecene, usually blended because no single material matches D5's volatility. — [Grand Ingredients](https://grandingredients.com/d5-replacement-siloxane-free/). Silicone-free W/O systems use squalane, jojoba, caprylic/capric triglyceride, isoamyl laurate and polyglyceryl emulsifiers. — [UL Prospector](https://ulprospector.ul.com/knowledge/9591/pcc-how-to-formulate-green-liquid-foundations/)

### Inferences
- Cyclic siloxanes also occur as residual impurities in silicone polymers (dimethicone, silicone polyethers). The 0.1% cap is partly about these traces. That suggests EU W/Si foundations remain viable using linear dimethicone grades low in cyclics, so "D5-free" does not mean "silicone-free".
- As of October 2026, EU labels during the transition (until June 2027) may still list cyclopentasiloxane. Non-EU markets (US, many Asian markets) were not restricted in the sources I reviewed, so global SKUs may differ by region.
- "Cyclomethicone" is an older INCI umbrella for the D4–D6 mixture and may still appear on older or non-EU labels. A classifier should treat it as a volatile cyclic silicone. (Naming background, uncited.)

### Gaps
- I could not fetch the EUR-Lex 2024/1328 text or the CTPA page (403), so the D6 rinse-off date conflict is unresolved.
- I found no source on non-EU restrictions (Canada, UK REACH, China) as of 2026.

## Q5. Concrete classification rules for a Python program (with caveats)

### Takeaway
Use a small ordered rule set over normalized INCI tokens. Look at the position of the first water token, silicone tokens, volatile hydrocarbon tokens, emulsifier family, and the top-N composition. Treat the order beyond roughly the first 5–8 ingredients as uninformative (the 1% rule), and ignore colorants (CI numbers / "may contain" block).

### Cited Findings (anchors for the rules)
- Order is meaningful only for ingredients >1%. Ingredients ≤1% and colorants can be in any order. — [21 CFR 701.3](https://www.govinfo.gov/content/pkg/CFR-1996-title21-vol7/html/CFR-1996-title21-vol7-sec701-3.htm); [ChemLinked EU summary](https://cosmetic.chemlinked.com/cosmepedia/eu-cosmetic-ingredient-regulations)
- "Silicones in the top 4" ⇒ almost certainly W/Si (for foundations). — [Lab Muffin](https://labmuffin.com/fixing-foundation-clumping-with-video/)
- W/Si emulsifier names, non-silicone W/O emulsifiers and W/O clay stabilizers: as listed in Q2. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/); [UL Prospector green](https://ulprospector.ul.com/knowledge/9591/pcc-how-to-formulate-green-liquid-foundations/)
- Water ≈ 40–70% in W/O and W/Si foundations. — [UL Prospector](https://ulprospector.ul.com/knowledge/7389/pcc-contemporary-foundation-formulations/)

### Inferences: the proposed rule set
(These rules are my synthesis. Thresholds are heuristic lore built from the cited anchors, not validated values.)

**Pre-processing**
1. Lowercase, strip, split on commas. Drop everything after "may contain", "+/-" or "[+/-". Drop tokens matching `^ci \d{5}` and named colorants (titanium dioxide, iron oxides, mica, ultramarines) *for phase decisions*, but keep them for pigment info. Normalize "aqua/water/eau" to `water`.
2. Use only the top N = 8 tokens (configurable) for position logic. Past that, ingredients are probably ≤1% and unordered.

**Token families (regex)**
- WATER: `^(water|aqua|eau)\b` and compounds like "aqua/water/eau".
- VOLATILE_CYCLIC_SI: `cyclo(penta|hexa|tetra)siloxane|cyclomethicone`
- OTHER_SILICONE: `(dimethicone|methicone|siloxane|silicate|silsesquioxane|trimethicone)` minus the emulsifier patterns below. Also `trisiloxane`, `caprylyl methicone`.
- SI_EMULSIFIER: `(peg|ppg|peg/ppg)-[\d/]+.*(dimethicone|methicone)|lauryl peg-\d+ polydimethylsiloxyethyl dimethicone|lauryl peg-\d+ tris\(trimethylsiloxy\)silylethyl dimethicone|cetyl peg/ppg-\d+/\d+ dimethicone|dimethicone/peg-\d+/\d+ crosspolymer|peg-\d+ dimethicone crosspolymer|dimethicone copolyol`
- SI_FILM: `trimethylsiloxysilicate|polypropylsilsesquioxane|acrylates/dimethicone copolymer` (+ `acrylates copolymer` as non-Si film former)
- PIGMENT_COATING (ignore for base): `triethoxycaprylylsilane|isopropyl titanium triisostearate|hydrogenated lecithin` and anything below position ~10 among `methicone|dimethicone`.
- VOLATILE_HC: `isododecane|isohexadecane|c\d+-\d+ (iso)?alkane|hemisqualane|undecane|tridecane|polydecene`
- OIL_ESTER: tokens ending `-ate` with fatty chains (e.g. `ethylhexyl palmitate`, `isononyl isononanoate`, `caprylic/capric triglyceride`), `squalane`, `oil`, `butter`, `jojoba`
- WO_NON_SI_EMULSIFIER: `polyglyceryl-\d+ (di)?(iso)?stearate|dipolyhydroxystearate|polyhydroxystearate|peg-30 dipolyhydroxystearate|sorbitan (iso)?stearate|sorbitan oleate|quaternium-(18|90) (bentonite|hectorite|sepiolite)|disteardimonium hectorite|stearalkonium hectorite`
- OW_SIGNALS: `xanthan gum|carbomer|acrylates/c10-30 alkyl acrylate crosspolymer|ammonium acryloyldimethyltaurate|sodium polyacrylate|hydroxyethylcellulose|steareth-\d+|ceteareth-\d+|polysorbate \d+|glyceryl stearate|peg-100 stearate|potassium cetyl phosphate|triethanolamine` *(uncited; standard O/W thickeners and emulsifiers from general cosmetic-chemistry knowledge)*

**Decision rules (first match wins)**
- R1 ANHYDROUS: no WATER token anywhere. Subtype by the top-3 majority: silicone → "anhydrous silicone"; VOLATILE_HC/OIL_ESTER → "anhydrous oil/hydrocarbon". *Caveat:* some waterless formulas still contain silicone emulsifiers ([US 6,103,250](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6103250)). Absence of water decides it. Also check for "aloe barbadensis leaf juice", hydrosols or "rose flower water" as water substitutes.
- R2 W/Si: WATER in top 3 AND (≥1 VOLATILE_CYCLIC_SI or OTHER_SILICONE in positions 1–4) AND (SI_EMULSIFIER present anywhere). High confidence. *Caveat:* Lab Muffin's top-4 rule alone gives "almost guaranteed" W/Si. The emulsifier check adds specificity.
- R3 SILICONE-FIRST: position 1 is a silicone or VOLATILE_CYCLIC_SI, and water is present lower → W/Si (water can rank below a silicone if water <~40%). If water is absent → R1.
- R4 W/O (hydrocarbon/oil, silicone-free or silicone-light): WATER in top 3 AND VOLATILE_HC or OIL_ESTER in positions 2–4 AND (WO_NON_SI_EMULSIFIER or SI_EMULSIFIER present) AND no silicone in the top 4. Output "W/O – oil/hydrocarbon". *Caveat:* this is the post-D5 EU pattern. Isododecane-led W/O wears and layers more like W/Si than O/W.
- R5 Mixed W/(Si+O): R2 and R4 both partly true (silicone AND hydrocarbon/ester in the top 5 with a silicone emulsifier) → "W/Si-oil hybrid". Common in patents (e.g. [US 8,501,162](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8501162)).
- R6 O/W (water-based): WATER is #1 AND no silicone or volatile hydrocarbon in the top 4 AND no SI_EMULSIFIER/WO_NON_SI_EMULSIFIER AND ≥1 OW_SIGNALS present. High confidence. Water #1 with no silicone/HC in the top 4 but none of the O/W signals → "probably water-based, low confidence".
- R7 Si/W (silicone-in-water): WATER #1, silicones at positions 2–5, NO W/O-type emulsifier, AND O/W hydrophilic thickeners present (e.g. carbomer, acryloyldimethyltaurate). Output "Si/W (water-continuous)". *Caveat:* no source covers this type, so treat it as speculative. On the label it can look like a "silicone-rich O/W" product.
- R8 Fallback: "unknown"; return the evidence (positions found) for human review.

**Confidence modifiers and caveats**
- Count silicone tokens below position ~8 (dimethicone, methicone, triethoxycaprylylsilane) as minor. They are often coatings or feel modifiers and shouldn't flip an O/W call.
- Pre-blend carriers (e.g. "isododecane" right before "trimethylsiloxysilicate", or "dimethicone" next to "dimethicone crosspolymer") inflate positions. Still evidence of the continuous phase.
- Glycerin/butylene glycol at position 2 is common in every water-containing type and is not diagnostic.
- Region: EU labels after June 2027 should lack cyclopentasiloxane/cyclohexasiloxane (≤0.1%). Don't use "absence of D5" as evidence of a silicone-free base.
- Translation and formatting: lists may use "aqua (water)", slashes, "&", or bracketed nano markers "[nano]". Normalize them.
- Label accuracy: retailer-scraped INCI lists are sometimes outdated or for another region. Note the source and date per record.

### Gaps
- None of these thresholds (top-3 water, top-4 silicone, N = 8 ordered window) has been validated against a labeled dataset. They should be checked against hand-labeled foundations (e.g. 50–100 products with known base) before use.
- OW_SIGNALS and some emulsifier patterns come from general cosmetic-chemistry knowledge, not sources fetched in this session.
