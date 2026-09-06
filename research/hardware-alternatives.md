# Cooling Mod Research — MSI Crosshair 15 B12UGSZ (i9-12900H / RTX 3070 Ti 115W)

Compiled 2026-09-06. Symptom under investigation: CPU package idles ~96°C with a 29°C
core spread — strongly suggestive of pumped/dried paste or uneven heatsink clamping
pressure on this particular unit, independent of any external cooling pad question.

Note on source quality: the laptop-cooling-pad review space is dominated by SEO/affiliate
content ("techreviewz.blog", "kryozon.com", "digitalnpq.org", "findingdulcinea.com",
"guidespot.com", "electronics.alibaba.com buying guides", AliExpress "wiki" articles).
These are treated as low-confidence/vendor-adjacent even when they cite numbers, because
methodology is rarely disclosed and language is templated across many "best of" pages
(evidence of AI-generated content farms). Independent measured reviews (Notebookcheck,
Jarrod'sTech, Igor'sLab, TechPowerUp) and forum teardown/community threads (Overclock.net,
Tom's Hardware/Guide, LaptopMedia) are weighted higher. GamersNexus and LTT Labs do not
appear to have published measured cooling-pad/vacuum-cooler content — could not verify
either way beyond absence in search results.

---

## 1. Sealed high-static-pressure cooling pads & vacuum coolers

**Claim: Sealed, gasket/foam-sealed single-large-blower pads (IETS GT500/GT600, Llano
V-series, KLIM Ultimate) can produce meaningful drops (roughly 10-20°C) on CPU/GPU under
sustained load, but only when the foam creates an actual air-tight seal against the
laptop's intake; a fan blowing at an unsealed plastic bottom does little.**
Confidence: Medium. This mechanism claim is consistent across independent sources but the
specific 10-20°C figures mostly trace back to vendor-adjacent blogs, not blind lab tests.
- IETS GT600: vendor/reseller and YouTube-style reviews claim 15-20°C CPU/GPU drops using
  a 140mm (5.5") "turbo fan" with magnetic sealed foam; no dBA figures found in any source —
  multiple reviewers note it is loud at max fan speed. [Amazon listing](https://www.amazon.com/IETS-Equipped-Turbo-Fan%EF%BC%885-5inch-Diameter%EF%BC%89-14-1-19-3/dp/B0CDC3KBC1), [shantoreview.com](https://shantoreview.com/iets-gt600-rgb-laptop-cooling-pad-review/), [tensorscience.com](https://www.tensorscience.com/cooling/my-thoughts-on-using-the-iets-gt600-turbo-fan-laptop-cooling-pad-with-usb-hub)
- IETS GT500: similarly claimed 10-20°C under load per a 2026 "review" blog — low
  confidence, no raw data shown. [techreviewz.blog](https://techreviewz.blog/iets-gt500-review/)
- IETS GT700: **not found** as a real, currently-listed product in any search — likely does
  not exist yet or is not distributed under that name. Do not assume it exists.
- Llano V12: manufacturer specs claim "44°C in 90 seconds" (marketing, not credible as
  stated); independent-style reviews report more modest ~10°C real-world drops and staying
  under 75°C with no throttling. Fan rated ≤70dB(A) per spec sheet (untested independently).
  [craftingworlds.com](https://craftingworlds.com/llano-v12-ultra-laptop-cooling-pad-review-a-laptop-cooler-that-actually-works/), [Amazon](https://www.amazon.com/llano-V12-Gaming-Laptop-Cooling/dp/B0C69BVWGB)
- KLIM Ultimate: 200mm fan (750 RPM spec); a review-farm source reports 5-9°C surface /
  3-6°C junction-temp drops (more modest than the IETS/Llano claims) — plausibly closer to
  the true unsealed-pad result. KLIM's own claim is a wide 5-20°C range "depending on
  factors," i.e. hedged marketing language. [medium.com](https://medium.com/@muteeb.com/klim-ultimate-rgb-laptop-cooling-pad-with-led-rim-review-17c98b4b00f7), [Amazon](https://www.amazon.com/KLIM-Gaming-Compatible-17-inch-Laptops/dp/B07NNQXTQT)
- Tryone: **no independent or vendor review found at all.** Could not verify performance
  claims for this brand; treat as unverified.
- Baseline calibration from an actual measured, disclosed-methodology test: **Notebookcheck**
  tested a generic top-selling Amazon pad (Havit HV-F2056, not a sealed high-pressure design)
  on an MSI GP65 with i7-10750H/RTX2070: CPU −12°C (92→80°C), GPU −6°C (76→70°C), but fan
  noise rose 53.9→59.2 dBA. This is the only source in this research with a disclosed
  control/test methodology and real dB(A) numbers. High confidence for this specific
  pad/laptop pairing; used here as a sanity-check baseline against which the vendor-blog
  15-20°C claims for "high static pressure" designs look inflated but directionally
  plausible. [Notebookcheck](https://www.notebookcheck.net/How-well-does-a-laptop-cooling-pad-work-We-Amazon-d-one-ourselves-to-find-out.464231.0.html) (2020, older but methodology still valid)
- **Jarrod'sTech** (YouTube, referenced via secondary summaries — could not independently
  re-verify the raw video data) reportedly tested multiple laptops against several cooling
  pads, a vacuum cooler, and a plain stand: pads gave ~4-10°C GPU/CPU improvements on
  average across laptops, a plain stand alone gave a similar improvement to some pads (i.e.
  elevating/improving underside airflow matters as much as active fans in some cases), and
  vacuum coolers gave the best results of the group tested. Confidence: Medium (secondary
  source, not the primary video transcript).

**Claim: Side-exhaust "vacuum" coolers (clip onto the laptop's own side/rear exhaust vent
and actively suck air out) outperform passive under-blowing pads, roughly 8-15°C CPU on
thermally-constrained gaming laptops — IF the laptop has a compatible exhaust vent
geometry and the vacuum device's pull direction matches (doesn't fight) the laptop's own
fan exhaust direction.**
Confidence: Medium-High (mechanism), Medium (magnitude). Multiple independent-ish sources
converge on the mechanism and rough magnitude, and the caveat about airflow-direction
conflict is repeated in a genuine forum thread, not a vendor page.
- IETS GT202UB (temp-display vacuum cooler, 2600-5000 RPM turbo blower): a review source
  claims 15°C CPU reduction vs. traditional pads; forum discussion at Tom's Guide raises the
  legitimate risk that if the laptop's own internal fan exhausts in the same location, a
  vacuum cooler can work against it rather than with it. [Amazon](https://www.amazon.com/IETS-temperature-intelligent-measurement-2600-5000RPM/dp/B0991V82S3), [forums.tomsguide.com](https://forums.tomsguide.com/threads/notebook-exhaust-vacuum-fan-any-thoughts.364354/latest)
- A generalized comparison (review-farm style, treat as directional only) states plain pads
  = 2-5°C CPU, vacuum coolers = 8-12°C CPU on thermally constrained gaming laptops. This
  matches the Jarrod'sTech secondary summary's relative ranking (vacuum > pad > nothing).
  Confidence in the exact numbers: Low; confidence in the *ranking* (vacuum > pad): Medium.

**Bottom line for question 1:** sealed high-pressure pads plausibly deliver on the order of
10-15°C average junction-temp improvement under sustained load when properly sealed against
intake vents, vacuum coolers can do somewhat better (~10-15°C, occasionally cited higher)
if the exhaust geometry matches, but almost all of the specific per-brand numbers trace to
marketing-adjacent content rather than blind third-party lab tests. None of this addresses
the reported 96°C **idle** temperature and 29°C core spread on the Crosshair 15 — cooling
pads/vacuum coolers only meaningfully move load temperatures, not the idle mounting-pressure
problem described.

---

## 2. Thermal interface materials for direct-die laptop use

**Honeywell PTM7950 — phase-change pad, solid at room temp, becomes putty-like ~45°C,
self-levels into microscopic die-lid gaps. Widely regarded in enthusiast circles as the
best "reapply once, forget it" option for laptop dies because it doesn't pump out under
repeated thermal cycling the way grease does.**
Confidence: High (mechanism and reputation), Medium (specific temperature-drop numbers,
which vary a lot by laptop/die and starting condition of the old paste).
- Specs cited: ~8.5 W/m·K thermal conductivity, ~0.04 °C·cm²/W thermal resistance at
  optimal compression, phase-change point ~45°C. [Apex Tech product page](https://apextech101.com/product/ptm-7950/) (vendor — cross-checked against forum/community consensus)
- Laptop anecdotes: users reported CPU/GPU going from 80-90°C to mid-70s°C after switching
  a handheld/laptop from stock paste to PTM7950; another reported CPU rarely above 65°C
  after application. [Overclock.net PTM7950 thread](https://www.overclock.net/threads/ptm7950-or-liquid-metal-on-direct-die.1811663/) (long-running community thread, page 7 referenced — treat individual anecdotes as anecdotal, not controlled)
- Important caveat found in the same material: **thickness mismatch of only ±0.05mm can
  raise junction temp 3-5°C** on thin laptop dies — i.e. this is a precision-sensitive
  material, cutting/sizing matters.

**Claim: "PTM7958" is real and is the same material as PTM7950 under a different SKU, not a
distinct improved formulation.**
Confidence: Medium-High.
- Multiple retailers (MODDIY, Framework's own store) sell PTM7958 as pad and as **paste**
  (1kg paste SKU exists — this is notable, a paste/liquid form of the same phase-change
  chemistry rather than only a pre-cut pad). One summary states 7958 is "a customer-specific
  part number assigned to a large consumer of Honeywell's PCM," functionally equivalent to
  standard PTM7950. [Framework store](https://frame.work/products/ptm7958-thermal-pad?v=FRAMCZ0001), [MODDIY paste listing](https://www.moddiy.com/products/6702/Honeywell-PTM7958-SP-Super-Highly-Thermally-Conductive-PCM-Paste-1KG.html)
- Could not find an authoritative Honeywell datasheet distinguishing 7950 vs 7958 by
  performance; treat "same chemistry, different SKU/packaging (Framework OEM contract
  number)" as the working explanation, not confirmed by a primary Honeywell source.

**Thermal Grizzly KryoSheet (graphene pad, ~0.2mm):**
Confidence: High on the electrical-conductivity finding (important safety correction),
Medium on comparative performance numbers.
- **KryoSheet IS electrically conductive, not a "safe non-conductive alternative."** This
  directly contradicts a common assumption. Thermal Grizzly's own KryoSheet does NOT ship as
  an inert dielectric graphene sheet — reviewers and product pages note it must be trimmed
  precisely to the die/heatspreader to avoid any protrusion that could bridge nearby SMDs,
  and Thermal Grizzly sells separate Kapton insulating sheets specifically to guard against
  this. Treat it like liquid metal from a "can short things out" standpoint, even though it
  is not liquid and cannot migrate/spread the way galinstan can. [igorslab.de KryoSheet review](https://www.igorslab.de/en/thermal-grizzly-cryosheet-in-lab-and-field-test-durable-all-purpose-weapon-with-minor-limitations/6/), [Amazon product listings note handling cautions](https://www.amazon.com/Thermal-Grizzly-KryoSheet-38/dp/B0C61Q2YKX), [Tom's Hardware forum thread](https://forums.tomshardware.com/threads/thermal-grizzly-kryosheet-graphene-cooling-pad.3808893/)
- Performance vs. PTM7950: mixed/dissenting evidence. One forum-summarized comparison says
  liquid metal ≈ PTM7950 + 1°C (LM slightly better), KryoSheet trails PTM7950 by 2-3°C.
  Another cited longevity test claims after 14 weeks PTM7950 averaged 79°C vs. KryoSheet
  88°C, with KryoSheet showing progressive void formation/separation over time while
  PTM7950 stayed uniformly bonded — i.e. KryoSheet may look fine on day 1 but degrade with
  thermal cycling on a laptop that flexes more than a desktop GPU shroud. Confidence:
  Medium (single forum-sourced longevity claim, not independently reproduced).
  [Overclock.net PTM7950 vs LM vs KryoSheet thread](https://www.overclock.net/threads/ptm7950-vs-liquid-metal-vs-kryosheet.1808499/)
- One laptop user (single data point) reported ~12°C average drop switching from Kryonaut
  paste to KryoSheet — consistent with KryoSheet being a large upgrade over degraded
  standard paste, even if it underperforms PTM7950/liquid metal head-to-head.
- Sizes: sold in several fixed sheet sizes (24×12mm, 33×33mm, 38×38mm) at $20-25 — must be
  cut/fit to the specific die, unlike a paste. [Thermal Grizzly product page](https://www.thermal-grizzly.com/en/kryosheet/s-tg-ks-24-12)

**Thermalright Heilos:**
Confidence: Medium. Only one substantive independent test found (Igor'sLab, Aug 2024
5-way phase-change pad roundup). Full numeric results sit behind a paginated article; the
introductory framing already signals the conclusion: Igor's Lab describes Heilos as a
"medium quality" OEM pad at 0.2mm with real limits versus PTM7950, and separately raises
the possibility it is a rebrand of an existing OEM PCM product rather than an original
Thermalright formulation (noting the packaging even misspells "Heilos"/"Helios").
Overclock.net community discussion independently claims Heilos's spec sheet is "100%
identical" to Honeywell's, with debate over whether it's a legitimate licensed rebrand or
a clone. Net: treat Heilos as a plausible **budget alternative that is not a clear win over
genuine PTM7950**, not proven equivalent. [Igor'sLab roundup](https://www.igorslab.de/en/5-phasenwechsel-pads-im-test-honeywell-ptm7950-ptm7950sp-vs-pcm5000-pcm8500-und-thermalright-heilos/), [Overclock.net Heilos thread](https://www.overclock.net/threads/thermalright-heilos-thermal-pads.1807207/)

**Thermal Grizzly Conductonaut vs. Conductonaut Extreme:**
Confidence: Medium (specs), Low (laptop-specific measured data — none found).
- Conductonaut Extreme uses a different gallium-based alloy claimed ~18% higher thermal
  conductivity than standard Conductonaut, wider rated operating range (−50 to 200°C vs.
  −10 to 140°C), and ships with an application spatula. [e-catalog.com spec comparison](https://e-catalog.com/cmp/142454/conductonaut-extreme-1g-vs-conductonaut-1g/)
- Could not find a laptop-specific (as opposed to desktop CPU/GPU delid) measured
  comparison between the two variants — this is a real gap. General enthusiast consensus
  (LTT forum thread, unverified numerically) treats Extreme as a modest incremental
  improvement, not transformative, over standard Conductonaut. [LinusTechTips forum thread](https://linustechtips.com/topic/1586126-thermal-grizzly-ptm-vs-conductonaut-extreme-liquid-metal/)

**Thick pastes (SYY-157, TF8, Kryonaut Extreme) and thermal putty (Upsiren U6 Pro/UX Pro,
K5 Pro):**
Confidence: Medium. Could not find independent lab data for SYY-157 or TF8 specifically
(searches did not surface dedicated reviews within budget of this research pass — flag as
unverified). Thermal putty for VRAM/VRM is better documented:
- Upsiren U6 Pro: ~12.8 W/m·K, electrically non-conductive, marketed specifically for
  GDDR6/VRAM and VRM hot spots, designed to be spread ~1-2mm to level height differences
  between chips of different heights on the same board (a real problem on VRM arrays).
  Manufactured in Greece with EU-co-funded R&D claims (vendor claim, unverified
  independently). A community member's direct comparison states "UX Pro" (its stablemate)
  edges it by 1-2°C in some tests but U6 Pro is easier to apply — i.e. the two products
  trade off ease-of-use vs. small performance gains, both are considered legitimate/good by
  the same enthusiast community that debunked misleading claims from a specific reseller
  ("Computer Systems GR") in a separate thread. [Overclock.net putty-vs-pads thread](https://www.overclock.net/threads/thermal-putty-vs-thermal-pads-comparison-chart.1810430/), [Overclock.net "misleading information" thread](https://www.overclock.net/threads/beware-of-misleading-information-from-computer-systems-gr-regarding-thermal-putty.1809275/), [vendor product page](https://computer-systems.gr/products/upsiren-u6-pro-10g/)
- A commonly cited enthusiast combo for GPU boards: PTM7950 on the die + Upsiren
  UX Pro Ultra or U6 Pro on surrounding VRAM/VRM — i.e. putty is a die-adjacent, not
  die-primary, solution. K5 Pro: mentioned alongside U6 Pro/UX Pro in the same putty
  ecosystem but no independent measured comparison was found in this pass — unverified.

---

## 3. MSI Crosshair 15 B12U teardown facts

**Heatsink/heatpipe layout:**
Confidence: Medium (single non-primary secondary source, could not independently confirm
via a primary teardown video/photo in this pass; laptopmedia.com's own disassembly article
returned HTTP 403 to automated fetch, so this is via search-snippet only, not the full
article text).
- Reported layout: **2 heatpipes dedicated to CPU, 3 heatpipes dedicated to GPU, and a 6th
  heatpipe for VRM/VRAM** — and notably that 6th heatpipe is **not connected to either of
  the two fans/three main heatsink blocks**, i.e. VRM/VRAM cooling on this chassis is
  reported to be comparatively passive/isolated from the active airflow path. If accurate,
  this is a plausible explanation for VRM-adjacent heat but does not by itself explain a
  96°C **CPU package** idle reading. [LaptopMedia disassembly article](https://laptopmedia.com/highlights/inside-msi-crosshair-15-b12ux-disassembly-and-upgrade-options/) (snippet-only; full page blocked to fetch, re-verify manually before relying on exact pipe count)
- Two-fan design confirmed by multiple independent parts listings (replacement fan+heatsink
  assemblies sold as a pair for B12U/B12UEZ/B12UGZ SKUs). [Amazon replacement fan listing](https://www.amazon.com/SYW%C2%B7pcparts-Dual-Cooling-Fans-Crosshair/dp/B0FWYQNDS7), [eBay part listing](https://www.ebay.com/itm/256862163018)
- Disassembly note (secondary/generic, not Crosshair-specific confirmation): bottom panel
  reportedly held by 13 Phillips screws, requires prying with a plastic tool — standard MSI
  practice but exact screw count for the Crosshair 15 specifically not independently
  confirmed here.

**Shared chassis/heatsink with Pulse GL66 / Katana GF66 / Vector GP66 / Raider GE66:**
Confidence: Medium-High for Pulse GL66 and Katana GF66 sharing parts with Crosshair 15;
**no evidence found for Vector GP66 or Raider GE66 sharing the same heatsink assembly** —
those appear to be a tier up (GE66 in particular is MSI's flagship 15" chassis with
different, typically more heatpipe/vapor-chamber cooling) and this research found nothing
supporting a drop-in upgrade path.
- Replacement heatsink part **E32-2500871-HH7** is explicitly listed as compatible across
  "Katana GF66, Sword 15, Pulse GL66, WF66, Creator M16, **Crosshair 15**" — i.e. these
  share a common heatsink assembly part number, supporting the idea that Crosshair 15
  (a rebadged/repositioned Pulse-family chassis) is mechanically the same as the GF66/GL66
  cooling hardware, not a distinct design. [Amazon part listing](https://www.amazon.com/Heatsink-E32-2500871-HH7-Compatible-Replacement-Crosshair/dp/B0DNNK9V9X)
- A second heatsink+fan pair (E33-0801180-MC2 & E33-0401790-MC2) is separately listed as
  cross-compatible among Pulse GL66/GL76 and Katana GF66/GF76 — reinforcing that this is one
  parts family, though this specific listing doesn't explicitly name Crosshair 15.
  [eBay listing](https://www.ebay.de/itm/116496256442)
- **No evidence found of a "known drop-in vapor-chamber/higher-tier heatsink upgrade"** for
  this chassis family. Did not find community mod threads describing swapping in a
  GE66/GP66 heatsink. This should be treated as an open question / unsupported until
  someone finds and confirms mechanical (screw hole, port cutout, VRM height) compatibility
  — MSI higher-tier 15" chassis (GE66 Raider) is generally a materially different chassis,
  not just a heatsink swap, based on comparison listings found (nanoreview.net spec
  comparisons show GE66 and Crosshair 15 as distinct product lines with different
  generations of internals, not siblings). [nanoreview.net GE66 vs Crosshair comparison](https://nanoreview.net/en/laptop-compare/msi-ge66-raider-vs-msi-crosshair-15)

**Known issues / community warnings for this chassis:**
Confidence: Medium — one concrete forum report found, not broad statistical evidence of a
"known" widespread failure.
- MSI Global Forum (Sept 2023, Crosshair 15 C12VE — same generation family as B12U):
  reported **2nd M.2 slot missing its ground screw hole**, and separately a **loose/play-y
  DC-in barrel connector causing the laptop to fully power off if the charger cable moved**,
  user found pushing the DC-in contact strips gave a temporary fix. This is anecdotal
  (n=1 forum post) but is a named, chassis-specific hardware defect report, not
  speculation. [MSI Global Forum thread](https://forum-en.msi.com/index.php?threads/2nd-m-2-screw-hole-not-available-and-dc-in-connector-has-a-lot-of-play-msi-crosshair-15-c12ve.389373/)
- **Did not find** any specific repaste result thread, screw-torque-order warning, or
  thermal-pad-thickness spec for the Crosshair 15/B12U in this research pass — this is a
  genuine gap. Before repasting, treat MSI's official service guide as the authority on
  screw order (a Crosshair-family MS-15P2 service guide PDF exists and should be consulted
  directly — [MSI service guide PDF](https://storage-asset.msi.com/global/pdf/ServiceGuide_15P2_Crosshair+(GL)_v1.0_English_0614.pdf) — note this PDF's exact model code (15P2) should be cross-checked against the B12UGSZ's actual board code before relying on it, since Crosshair 15 has spanned multiple hardware generations (A11, B12, C12) under one marketing name).

---

## 4. Mount-pressure fixes for uneven die contact

**Claim: uneven core temps / high idle temps on a laptop can stem from insufficient or
uneven heatsink clamping pressure, and shims (thin copper or aluminum plates between
heatsink and die, or added washers under the spring-loaded screws) are a legitimate,
commonly-discussed fix — but with real limits and risks.**
Confidence: Medium-High on the mechanism (widely discussed and mechanically sound —
directly relevant to the reported 29°C core spread), Medium on how often it actually helps
versus just repasting.
- Forum consensus (Overclock.net, Tom's Hardware/Guide, AnandTech forums — multiple
  independent threads converge): **stacking extra washers is explicitly discouraged**
  because uneven washer stacking is *itself* a common cause of uneven pressure, i.e. a
  naive "add more washers" mod can make core-to-core spread worse, not better, if not done
  symmetrically and with equal torque on all screws. [Overclock.net washer/pressure thread](https://www.overclock.net/threads/extra-or-thicker-washers-to-increase-heatsink-gpu-pressure.1775188/)
- A CPU/GPU shim (thin flat copper or aluminum plate under the heatsink) is described as
  useful specifically when "the copper heat sink may not be touching the full area of the
  CPU" — i.e. exactly the failure mode implied by a 29°C inter-core spread (partial
  contact). Community guidance: if paste hasn't spread thinly and evenly after a mount
  cycle, that is itself diagnostic evidence of insufficient/uneven clamping force, and a
  shim (secured to the heatsink or die with a thin paste layer) is the typical next step
  before trying more exotic TIMs. [Tom's Hardware Forum mounting-pressure thread](https://forums.tomshardware.com/threads/increasing-mounting-pressure-of-a-laptops-heatsink-what-do-you-think.2662481/), [Wikipedia — CPU shim](https://en.wikipedia.org/wiki/CPU_shim), [Tom's Guide copper-mod thread](https://forums.tomsguide.com/threads/general-copper-mod-shim-question.276618/latest)
- Risk noted explicitly in these threads: over-tightening/over-shimming without addressing
  the root cause (bent heatsink base, warped baseplate, or a die that sits measurably lower
  than the surrounding SMDs on the PCB) risks cracking the die or PCB, and gains are capped
  once TIM quality is no longer the bottleneck — i.e. shimming has diminishing/negative
  returns past a certain point and is not a substitute for diagnosing *why* contact is
  uneven in the first place.
- **Heatsink lapping** (flattening/polishing the heatsink's contact surface) was mentioned
  only in passing in general CPU-shim contexts (mostly a desktop-cooler practice); no
  laptop-specific lapping case study or before/after data was found in this research pass.
  Treat laptop lapping as plausible-but-unverified by measured evidence here — most laptop
  heatsink baseplates are copper block or vapor chamber sections that are thinner and more
  failure-prone to lap than a desktop tower cooler base, so risk is likely higher than the
  desktop case, but this is inference, not a sourced claim.

**Direct relevance to the reported symptom:** a 29°C core-to-core spread at idle is a
textbook signature of partial/uneven die contact (some cores under the heatsink's better-
contacted region run cool, others near a gap or overly-thick paste layer run hot even at
idle). The forum consensus above supports diagnosing this as a mounting-pressure/contact
problem before assuming it's a TIM-formulation problem — i.e. before upgrading to PTM7950
or liquid metal, first confirm (via a paste spread/"squish" pattern check on removal, or a
Kapton-taped shim test) whether the heatsink base itself is contacting the IHS evenly.

---

## 5. External water cooling for laptops

Confidence: Low-Medium across this whole section — this is a much smaller enthusiast niche
than desktop watercooling, and current (2024+) turnkey products are scarce.
- **Copper tube kits clamped over the laptop's own heatpipes**, routed externally to a
  radiator/reservoir, are a documented DIY approach (forum project logs exist), typically
  using ~1/4" soft copper tubing clamped/soldered onto an exposed section of the existing
  heatpipe, not replacing the laptop's internal loop. [Tom's Hardware DIY thread](https://forums.tomshardware.com/threads/diy-heatsink-with-copper-tube-for-laptop-cooling.2619529/)
- Raw heatpipe stock (flat or round, 150-400mm) is commercially available on AliExpress for
  building such adapters, but this is component-level, not a packaged product.
- **Quick-disconnect fittings** (Alphacool G1/4 and G3/8 Eiszapfen "no drip/no spill" QDCs)
  are real, mature desktop-watercooling products that could mechanically be adapted to a
  laptop external loop, but no product or build log was found that specifically packages
  this for laptops — this would be a from-scratch enthusiast build using desktop parts, not
  an off-the-shelf "laptop water cooling kit."
- **No current (2024-2026) turnkey commercial external-water-cooling-for-laptop product**
  was found in this research pass. The one historical example surfaced (a "liquid-cooled
  laptop" desktop-sized concept, via a Yahoo Tech reprint) reads as a novelty/one-off, not
  an available product — could not verify vendor, price, or availability, treat as
  effectively a myth/discontinued concept for purchasing purposes.
- **Chiller/TEC loop dew-point guidance** (from sub-ambient overclocking community, not
  laptop-specific, but the physics transfers directly): the standard rule is **coolant
  target temperature = ambient dew point + safety margin**, with practical sub-ambient
  builds commonly targeting dew point ≤8°C and loop coolant ≤10°C, inside an insulated/
  sealed enclosure with humidity control, and sometimes deliberately re-warming return
  fluid above dew point before it reaches components. None of the sources found describe
  this being done inside an actual laptop chassis (the enclosure/insulation requirements
  described are desktop-open-loop-bench scale) — applying chiller-level sub-ambient cooling
  inside a sealed laptop chassis without redesigning the whole enclosure for condensation
  control would be a novel, unverified undertaking, not a documented practice. [Overclockers UK DIY chiller thread](https://forums.overclockers.co.uk/threads/i-built-a-diy-sub-ambient-water-chiller-with-dew-point-control.19011177/), [Overclock.net sub-ambient condensation thread](https://www.overclock.net/threads/advice-sub-ambient-condesnation-prevention.1583708/), [US6205796B1 patent — sub-dew-point cooling](https://patents.google.com/patent/US6205796B1)

---

## 6. Desktop-cooler-on-laptop "Frankenstein" builds and Peltier/TEC on laptops

**Desktop cooler bolted directly to a laptop board:**
Confidence: Medium (real, documented examples exist; but small sample, mostly single
YouTube/enthusiast projects rather than a body of repeated evidence).
- A documented example: a YouTuber removed a laptop's chassis/case and bolted a full
  desktop CPU air cooler onto the **GPU** of a laptop with a GTX 1060, specifically testing
  whether cooling alone could eliminate thermal throttling in Cyberpunk 2077. Reported
  outcome per secondary summary: it "worked very well" for eliminating throttling — but
  full numeric before/after data was not independently re-verified here (would need to pull
  the actual video). [YouTube: "I Bolted a Desktop CPU Cooler to a GTX 1060 Laptop"](https://www.youtube.com/watch?v=slLSCf4WP7g)
- General pattern described across several forum threads (Tom's Hardware/Guide,
  Overclockers.com "Laptop Cooler Mod"): removing the laptop's bottom panel/case
  entirely and mounting a desktop heatsink means giving up portability and the sealed form
  factor entirely — these are one-off enthusiast projects, not repeatable products, and
  none of the sources found report a *packaged kit* for doing this safely (mounting bracket
  compatibility, keeping the board rigid, keeping ports/battery functional) — treat as
  "possible, has been done, no standardized safe method exists." [Overclockers.com Laptop Cooler Mod](https://www.overclockers.com/laptop-cooler-mod/)
- Failure modes flagged across sources (inference from the general DIY-mod discussion, not
  one single citation): board flex/cracking from an unsupported heavy cooler hanging off
  the die, connector strain, and loss of the sealed chassis's dust/spill protection.

**Peltier/TEC on laptops:**
Confidence: Medium-High on the condensation risk being real and laptop-specific dangerous;
Medium on mitigation techniques actually working reliably.
- Community consensus across several forum threads (Overclock.net, Tom's Hardware,
  AnandTech, LinusTechTips forum): **most TECs will go sub-ambient even at modest power,
  and condensation is close to inevitable without active mitigation** — and "water and
  electricity don't mix well" was explicitly raised in the context of a **laptop**
  application specifically, because there is far less clearance and no drip tray/gasketing
  the way a desktop open bench build can have. [Overclock.net laptop-Peltier thread](https://www.overclock.net/threads/laptop-cooling-with-peltier.1401395/), [Overclock.net condensation-on-Peltier thread](https://www.overclock.net/threads/condensation-on-peltier.506120/)
- Mitigation techniques discussed (desktop-context, extrapolated to laptop by the
  community, not laptop-proven): (1) controlling TEC voltage/duty cycle so it isn't running
  cold at idle when the CPU isn't generating heat to keep the cold side above dew point,
  (2) heavy silicone sealing around the socket/TEC plate, (3) Plasti-Dip coating the
  motherboard as a moisture-tolerant backstop (explicitly noted to reduce cooling
  performance somewhat as a trade-off). None of these were found demonstrated on an actual
  laptop motherboard in the sources gathered — they are desktop-forum techniques being
  reasoned about for laptop feasibility, not confirmed laptop outcomes.
  Confidence downgraded accordingly: plausible engineering approach, **not evidenced on a
  real laptop build** in anything found here.
- One tangential but relevant real product: Cooler Master shipped a commercial closed-loop
  **desktop** thermoelectric CPU cooler (a "mini-fridge for your CPU") — evidence that TEC
  CPU cooling is a real, shipping (if niche) desktop technology, which lends some plausibility
  to a hypothetical laptop adaptation, but it is not itself a laptop product. [PCWorld coverage](https://www.pcworld.com/article/402079/cooler-master-thermoelectric-cooler.html) (older, 2018-era article — dated, confirm current availability before citing as "current")

---

## Dropped as myth / unsupported

- **IETS "GT700"** — no evidence this product exists; do not budget for it as a real SKU.
- **Llano V12 marketing claim of "44°C drop in 90 seconds"** — internally inconsistent with
  every independent-style measurement found (which cluster around 10°C); treat as
  unsupported marketing copy, not a real expectation.
- **KryoSheet as a "safe non-conductive" alternative to liquid metal** — false; it is
  electrically conductive and requires the same containment precautions (Kapton shielding,
  precise trimming) as liquid metal, just without liquid-metal's migration/spreading risk.
- **A commercial, current (2024-2026), off-the-shelf "external laptop water cooling kit"**
  — not found. What exists is either desktop watercooling parts repurposed by individual
  enthusiasts, or historical novelty projects with no clear ongoing product line.
- **A confirmed "drop-in" higher-tier vapor-chamber heatsink upgrade (e.g. from a
  Raider GE66) for the Crosshair 15/Pulse GL66/Katana GF66 chassis family** — no community
  mod thread or parts-compatibility evidence found; GE66 appears to be a mechanically
  distinct chassis, not a heatsink-only step up from this family.
- **Chiller/TEC sub-ambient loops as a demonstrated-safe technique inside a sealed laptop
  chassis** — the dew-point control math is real and used on desktop benches, but no source
  found actually implements it inside a laptop's enclosure; treat full sub-ambient cooling
  in a laptop as unproven/high-risk rather than a known-working mod.
- **"Tryone" laptop coolers** — could not verify this brand/product exists with any
  independent coverage at all; not evaluated, not recommended, not debunked — simply
  unverifiable in this pass.
- **SYY-157 and TF8 thick pastes** — no independent measured data found in this pass;
  neither confirmed nor debunked, flagged as a research gap rather than a myth.

---

## Sources

1. Amazon — IETS GT600 product listing: https://www.amazon.com/IETS-Equipped-Turbo-Fan%EF%BC%885-5inch-Diameter%EF%BC%89-14-1-19-3/dp/B0CDC3KBC1
2. shantoreview.com — IETS GT600 RGB review: https://shantoreview.com/iets-gt600-rgb-laptop-cooling-pad-review/
3. tensorscience.com — IETS GT600 hands-on notes: https://www.tensorscience.com/cooling/my-thoughts-on-using-the-iets-gt600-turbo-fan-laptop-cooling-pad-with-usb-hub
4. techreviewz.blog — IETS GT500 review (2026): https://techreviewz.blog/iets-gt500-review/
5. Amazon — Llano V12 (RGB) listing: https://www.amazon.com/llano-V12-Gaming-Laptop-Cooling/dp/B0C69BVWGB
6. craftingworlds.com — Llano V12 Ultra review: https://craftingworlds.com/llano-v12-ultra-laptop-cooling-pad-review-a-laptop-cooler-that-actually-works/
7. medium.com (Muteeb Hussain) — KLIM Ultimate review: https://medium.com/@muteeb.com/klim-ultimate-rgb-laptop-cooling-pad-with-led-rim-review-17c98b4b00f7
8. Amazon — KLIM Ultimate listing: https://www.amazon.com/KLIM-Gaming-Compatible-17-inch-Laptops/dp/B07NNQXTQT
9. Notebookcheck — "How well does a laptop cooling pad work?" (2020): https://www.notebookcheck.net/How-well-does-a-laptop-cooling-pad-work-We-Amazon-d-one-ourselves-to-find-out.464231.0.html
10. Amazon — IETS GT202UB vacuum cooler listing: https://www.amazon.com/IETS-temperature-intelligent-measurement-2600-5000RPM/dp/B0991V82S3
11. Tom's Guide forum — notebook exhaust vacuum fan thread: https://forums.tomsguide.com/threads/notebook-exhaust-vacuum-fan-any-thoughts.364354/latest
12. Apex Tech — Honeywell PTM7950 product/spec page: https://apextech101.com/product/ptm-7950/
13. Overclock.net — "PTM7950 or liquid metal on direct die?" thread: https://www.overclock.net/threads/ptm7950-or-liquid-metal-on-direct-die.1811663/
14. Framework — PTM7958 thermal pad store page: https://frame.work/products/ptm7958-thermal-pad?v=FRAMCZ0001
15. MODDIY — Honeywell PTM7958 SP paste, 1kg listing: https://www.moddiy.com/products/6702/Honeywell-PTM7958-SP-Super-Highly-Thermally-Conductive-PCM-Paste-1KG.html
16. Igor'sLab — Thermal Grizzly KryoSheet lab/field test: https://www.igorslab.de/en/thermal-grizzly-cryosheet-in-lab-and-field-test-durable-all-purpose-weapon-with-minor-limitations/6/
17. Tom's Hardware forum — KryoSheet graphene cooling pad discussion: https://forums.tomshardware.com/threads/thermal-grizzly-kryosheet-graphene-cooling-pad.3808893/
18. Thermal Grizzly — official KryoSheet product page: https://www.thermal-grizzly.com/en/kryosheet/s-tg-ks-24-12
19. Overclock.net — "PTM7950 vs Liquid metal vs Kryosheet" thread: https://www.overclock.net/threads/ptm7950-vs-liquid-metal-vs-kryosheet.1808499/
20. Igor'sLab — 5-way phase-change pad roundup (PTM7950/7950SP/PCM5000/PCM8500/Heilos), Aug 2024: https://www.igorslab.de/en/5-phasenwechsel-pads-im-test-honeywell-ptm7950-ptm7950sp-vs-pcm5000-pcm8500-und-thermalright-heilos/
21. Overclock.net — Thermalright Heilos thread: https://www.overclock.net/threads/thermalright-heilos-thermal-pads.1807207/
22. e-catalog.com — Conductonaut Extreme vs Conductonaut spec comparison: https://e-catalog.com/cmp/142454/conductonaut-extreme-1g-vs-conductonaut-1g/
23. LinusTechTips forum — "Thermal Grizzly PTM vs Conductonaut Extreme" thread: https://linustechtips.com/topic/1586126-thermal-grizzly-ptm-vs-conductonaut-extreme-liquid-metal/
24. Overclock.net — "Beware of misleading information ... regarding Thermal Putty" thread: https://www.overclock.net/threads/beware-of-misleading-information-from-computer-systems-gr-regarding-thermal-putty.1809275/
25. Overclock.net — Thermal Putty vs Thermal Pads comparison thread: https://www.overclock.net/threads/thermal-putty-vs-thermal-pads-comparison-chart.1810430/
26. Computer Systems (Greece) — Upsiren U6 Pro product page: https://computer-systems.gr/products/upsiren-u6-pro-10g/
27. LaptopMedia — "Inside MSI Crosshair 15 (B12Ux)" disassembly article (fetch blocked by site, cited via search snippet — re-verify manually): https://laptopmedia.com/highlights/inside-msi-crosshair-15-b12ux-disassembly-and-upgrade-options/
28. Amazon — replacement dual fan assembly for Crosshair 15 B12U/B12UX/B12UGSZ/B12UGZ/B12UEZ: https://www.amazon.com/SYW%C2%B7pcparts-Dual-Cooling-Fans-Crosshair/dp/B0FWYQNDS7
29. eBay — Crosshair 15 R6E B12UEZ/B12UGZ fan+heatsink part listing: https://www.ebay.com/itm/256862163018
30. Amazon — heatsink part E32-2500871-HH7, listed compatible across Katana GF66/Pulse GL66/WF66/Creator M16/Crosshair 15: https://www.amazon.com/Heatsink-E32-2500871-HH7-Compatible-Replacement-Crosshair/dp/B0DNNK9V9X
31. eBay (DE) — Pulse GL66/GL76, Katana GF66/GF76 heatsink+fan part listing: https://www.ebay.de/itm/116496256442
32. nanoreview.net — MSI GE66 Raider vs Crosshair 15 comparison: https://nanoreview.net/en/laptop-compare/msi-ge66-raider-vs-msi-crosshair-15
33. MSI Global Forum — "2nd M.2 screw hole not available and DC-in connector has a lot of play," Crosshair 15 C12VE, Sept 2023: https://forum-en.msi.com/index.php?threads/2nd-m-2-screw-hole-not-available-and-dc-in-connector-has-a-lot-of-play-msi-crosshair-15-c12ve.389373/
34. MSI — MS-15P2 (Crosshair/GL) official service guide PDF: https://storage-asset.msi.com/global/pdf/ServiceGuide_15P2_Crosshair+(GL)_v1.0_English_0614.pdf
35. Overclock.net — "Extra or thicker washers to increase heatsink GPU pressure" thread: https://www.overclock.net/threads/extra-or-thicker-washers-to-increase-heatsink-gpu-pressure.1775188/
36. Tom's Hardware forum — "Increasing mounting pressure of a laptop's heatsink" thread: https://forums.tomshardware.com/threads/increasing-mounting-pressure-of-a-laptops-heatsink-what-do-you-think.2662481/
37. Wikipedia — CPU shim: https://en.wikipedia.org/wiki/CPU_shim
38. Tom's Guide forum — "General Copper Mod (Shim) Question": https://forums.tomsguide.com/threads/general-copper-mod-shim-question.276618/latest
39. Tom's Hardware forum — "DIY Heatsink with copper tube for Laptop cooling?" thread: https://forums.tomshardware.com/threads/diy-heatsink-with-copper-tube-for-laptop-cooling.2619529/
40. Overclockers UK forum — "DIY sub-ambient water chiller with dew point control" build log: https://forums.overclockers.co.uk/threads/i-built-a-diy-sub-ambient-water-chiller-with-dew-point-control.19011177/
41. Overclock.net — "Sub Ambient condensation prevention" thread: https://www.overclock.net/threads/advice-sub-ambient-condesnation-prevention.1583708/
42. Google Patents — US6205796B1, "Sub-dew point cooling of electronic systems": https://patents.google.com/patent/US6205796B1
43. YouTube — "I Bolted a Desktop CPU Cooler to a GTX 1060 Laptop": https://www.youtube.com/watch?v=slLSCf4WP7g
44. Overclockers.com — "Laptop Cooler Mod" article: https://www.overclockers.com/laptop-cooler-mod/
45. Overclock.net — "Laptop cooling with peltier" thread: https://www.overclock.net/threads/laptop-cooling-with-peltier.1401395/
46. Overclock.net — "Condensation on peltier" thread: https://www.overclock.net/threads/condensation-on-peltier.506120/
47. PCWorld — Cooler Master thermoelectric closed-loop desktop CPU cooler coverage (2018, dated): https://www.pcworld.com/article/402079/cooler-master-thermoelectric-cooler.html
