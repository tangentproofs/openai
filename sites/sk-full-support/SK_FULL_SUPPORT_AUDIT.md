OVERALL: PASS WITH FIXES

# Honesty / faithfulness audit: sk-full-support

Auditor: an independent model session (Claude), not the session that drafted the site. Brief:
`prompts/honesty-audit.md`. Subject: openai/math at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, the vendored copy
in `projects/openai-math/`. Ground truth: the Lean source and `build/sk-full-support/data/decls.json`. **No Lean
build was run**; the audit reads the source. After the fixes, `engine/build.sh sk-full-support` ends with
`built _site/sk-full-support` and prints no `error:` lines (52 nodes, 1360 declarations).

## Summary of findings

- **Headline is faithful.** `full_support` (Main.lean 35–59) has exactly one hypothesis, `hmin : IsMinimizer W γ`
  (a global minimum over all `OrderParameter`s). No hypothesis assumes support, monotonicity or regularity, so nothing
  smuggles in the conclusion. The **CONDITIONAL** label (a minimizer is assumed, never shown to exist) appears on the
  home lead, the headline caveats, Review and Roadmap. That is adequate.
- **Definitions are the real objects, not stubs.** All 16 Model.lean definitions are genuine: the `sSup` control
  value, `deriv`-based gradient and curvature, the Stieltjes condition and an SDE in integral form. None is a zero
  map, `True` or a free variable. The site states the Lean total-function conventions (`deriv` = 0, `sSup` = 0,
  integral = 0) as caveats.
- **All line references hold.** All 52 nodes' "(File, lines a–b)" references match `decls.json` exactly. I checked
  these with a script. I also checked the secondary references (CDFParameters 81–100 and 102–105, Curvature 36–49,
  Certificate 10–60, 62–69, 107–122, 124 and 165–194, ProgressiveBrownian 93–110, Model.lean line citations in
  quizzes, and Main.lean lines 23, 24, 26, 30–32, 36, 39 and 44–59) against the files. They are correct.
- **Proof-structure claims match the Lean.** I checked the hypotheses of `full_support_of_contact_and_gap_curvature`,
  `contact_conditions`, `no_positive_constant_gap`/`no_zero_constant_gap`, `positive_gap_curvature`,
  `zero_gap_curvature`, `minimizer_no_terminal_plateau`, `stripThird_pos`, `actual_coercivity`, `rational_identity`,
  `pointwise_coercivity`, `diffusion`, `diffusion_isDiffusion`, `diffusion_uniqueness`, `parameterMeasure(_isStieltjes)`
  and `squareMoment_*`. The descriptions match.
- **Every quiz answer key is correct.** One key could be read as wrong (diffusion_isDiffusion Q3) and was rewritten.
- **A few paper citations were imprecise**: one misquote (q vs q′ in Proposition 5.1), two wrong locations, and one
  paraphrase shown in quotation marks. All are fixed.

## Trust-page checks, re-run by the auditor

| Claim on Trust | Re-run result |
|---|---|
| 135 `.lean` files, 20,357 lines | **Holds** (135 files. `wc -l` over SKSupport plus the target gives 20,455; minus the target's 98 lines that is 20,357) |
| Only `import Mathlib` from outside | **Holds** (every distinct `import` line is `Mathlib` or `OAI.Probability.SKSupport.*`) |
| `sorry`, `admit`: 0 | **Holds** |
| `axiom`: 0 | **Holds** |
| `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `opaque`, `unsafe`, `partial def`: 0 | **Holds** |
| `set_option`, `attribute [`, `local instance`, `macro`/`elab`/`syntax`, `#eval`, `run_cmd`: 0 | **Holds** (`#print` is also 0) |
| `decide`: 2, at StrictMoments.lean 101 and IntegratedCompletionSquare.lean 56 | **Holds** (both are `0 < 1`-style ℕ facts) |
| Target lines 1–89 identical to Model.lean | **Holds** (`diff` of the first 89 lines is empty. The full diff is just the target's `theorem … sorry` at lines 90–93) |
| Main.lean 35–36 matches target 90–91 | **Holds** |
| Comparator JSON contents | **Holds** (theorem name, solution module `OAI.Probability.SKSupport.Main`, 3 permitted axioms, `definition_names: []`) |
| Same tree at `adc7f12` and `fd4aeeb` | **Holds** (checked through the GitHub API: SKSupport tree `560a5aa…`, target `.lean`/`.json` blobs, `lake-manifest.json` and `lean-toolchain` are identical at both commits) |
| Vendored copy = upstream | **Holds** (local `HEAD:` tree id is `560a5aa…`, and the local target blob ids match) |
| MathVet row | **Holds** (the row at the cited commit reads comparator-sandboxed-pass, built, closure ok, no-shadowing, axioms `Classical.choice ; Quot.sound ; propext`, cone 20,357, no external code, finished 2026-10-08) |
| cert-machine entry | **Holds** (CERTIFIED, run 38040214623, 2026-10-10, 0 definition holes, maxRss about 7.1 GB, and the quoted "does not mean the paper's claim is proved") |
| `formalization.yaml` at `adc7f12` has no entry for this manuscript | **Holds** (it has only a different SK manuscript, "Critical slowing down") |
| Plectis Atlas and Prove2Me descriptions | **Not re-checked** (web pages; no fetch was made) |

Trust says clearly that the Lean was not built and `#print axioms` was not run here, and it attributes the kernel
claims to outside reports. Its wording is not stronger than what was checked.

## Per-item verdicts

### Nodes: statement.py

| Node | Verdict |
|---|---|
| full_support | PASS WITH FIXES (Q4 explanation now says the Lean never defines the SK Hamiltonian) |
| Time | PASS |
| extend | PASS |
| OrderParameter | PASS |
| BrownianSystem | PASS |
| incrementFiltration | PASS |
| Control | PASS |
| controlPayoff | PASS |
| value | PASS |
| gradient | PASS |
| curvature | PASS |
| parisi | PASS |
| IsMinimizer | PASS WITH FIXES (added that minimality is of `parisi W ·` for the same `W` as in the conclusion) |
| IsStieltjesMeasure | PASS |
| IsDiffusion | PASS |
| squareMoment | PASS |
| FullSupportConclusion | PASS |

### Nodes: proof.py

| Node | Verdict |
|---|---|
| minimizer_full_support_actual | PASS |
| SupportDeterministic.Time | PASS |
| SupportDeterministic.IsOrderParameter | PASS |
| SupportDeterministic.IsStieltjesMeasure | PASS |
| SupportDeterministic.InSupport | PASS |
| Variation.full_support_of_contact_and_gap_curvature | PASS |
| Variation.no_positive_constant_gap | PASS |
| Variation.no_zero_constant_gap | PASS |
| Variation.contact_conditions | PASS (omits the `hμ` hypothesis in the prose, which is harmless) |
| Variation.derivative_eq_one_of_full_contact | PASS |
| contactPotential | PASS |
| minimizer_variational_inequality | PASS WITH FIXES (a Lemma 6.1 paraphrase was in quotation marks; now marked as a paraphrase with the exact admissibility condition) |
| contactPotential_nonneg | PASS |
| minimizer_contact | PASS |
| minimizer_no_terminal_plateau | PASS |
| positive_gap_curvature | PASS WITH FIXES (Proposition 5.1 misquote "q is strictly convex" corrected to "q′ is strictly convex") |
| zero_gap_curvature | PASS |
| stripThird | PASS |
| stripThird_pos | PASS |
| actual_coercivity | PASS WITH FIXES (the paper pointer now names Lemma 4.1 as the identity and Proposition 4.2 as the integrated form) |
| coerciveJetPolynomial | PASS |
| actualJet | PASS |
| Certificate.rational_identity | PASS WITH FIXES (the quote is from Section 1.2, not Section 4, so the location is corrected. "checked by `ring`" now reads "the source proves it with `ring`" plus a pointer to Trust. Quiz wording follows) |
| parameterMeasure | PASS |
| parameterMeasure_isStieltjes | PASS |
| diffusion | PASS WITH FIXES (the quote is from page 2, which cites Lemma 2.2; the location is corrected) |
| diffusion_isDiffusion | PASS WITH FIXES (the Q3 key "Is X = B a.s.? No" is false when γ = 0; rewritten as "not in general") |
| diffusion_uniqueness | PASS WITH FIXES (the quote attributed to Lemma 2.2 replaced by Lemma 2.2's own words, "unique strong solution on [0,1]") |
| curvatureMoment | PASS |
| squareMoment_eq_integral_curvatureMoment | PASS |
| squareMoment_hasDerivAt | PASS |
| quarticJetPolynomial | PASS |
| BrownianSystem.driver | PASS |
| rawFeedback | PASS |
| parameterStieltjes | PASS |

### Site-wide text and pages

| Item | Verdict |
|---|---|
| site.json lead | PASS (states the CONDITIONAL assumption) |
| site.json startNote | PASS WITH FIXES (it said "the statement and its 16 definitions" are identical in Model.lean, but the theorem is not in Model.lean. It now says the 16 definitions are identical and Main.lean 35–36 repeats target 90–91) |
| site.json desc / sizeNote | PASS |
| pages/about.md | PASS (authorship limited to "OpenAI" and "produced by an internal OpenAI model") |
| pages/review.md | PASS (clause table and caveats checked against the paper, pp. 1–2. Placeholder left untouched) |
| pages/trust.md | PASS (all cheap checks re-run and holding, as tabled above) |
| pages/roadmap.md | PASS WITH FIXES ("(checked by `ring`)" changed to "(proved by `ring` in the source)". File counts 30/39/21/9 verified) |
| Widgets (two Main.lean walkthroughs) | PASS (they describe proof steps and quote the actual Lean lines; they present no data as evidence) |

### Escape-hatch grep (brief item 4)

Over `lean/OAI/Probability/SKSupport/**`: `sorry` 0, `admit` 0, `axiom` 0, `opaque` 0, `native_decide` 0,
`implemented_by` 0, `extern` 0, `unsafe` 0. `decide` appears twice, both harmless (listed above). There is one global
`instance` (`timeCompactIccSpace`, Support/GapCurvature.lean line 83), which is an ordinary proved instance, not an
escape hatch. The only `sorry` in scope is the target file's deliberate one (ComparatorChallenges/SKFullSupport.lean
line 92).

## Fixes made (file: before → after)

1. `nodes_src/proof.py` (positive_gap_curvature, paper quote): "If c > 0, then q is strictly convex on I" → "… q′ is strictly convex on I".
2. `nodes_src/proof.py` (Certificate.rational_identity, paper location): `Section 4` → `Section 1.2, summarizing Lemma 4.1 (4.11) and Proposition 4.2`.
3. `nodes_src/proof.py` (actual_coercivity): "the exact coercive identity (Section 4, Proposition 4.2)" → "the exact coercive identity and its integrated form (Section 4, Lemma 4.1 and Proposition 4.2)".
4. `nodes_src/proof.py` (minimizer_variational_inequality): the quoted "“d/dε P(γ + εη) at ε = 0+ equals …”" → the location "Lemma 6.1, (6.1)" and an explicit paraphrase with the admissibility condition (η ∈ L¹, γ + εη ∈ U for small ε ≥ 0).
5. `nodes_src/proof.py` (diffusion): location `Lemma 2.2` → `page 2, citing Lemma 2.2`, with the full sentence "… up to time one, as proved in Lemma 2.2."
6. `nodes_src/proof.py` (diffusion_uniqueness): "Lemma 2.2: “a unique strong solution up to time one.”" → "Lemma 2.2: (2.10) “has a unique strong solution on [0,1].”"
7. `nodes_src/proof.py` (diffusion_isDiffusion Q3): "Is X = B almost surely? [No, X = B + drift]" → "Is the constructed X simply B? [Not in general: … reduces to B only if that drift vanishes (e.g. γ = 0)]".
8. `nodes_src/proof.py` (Certificate.rational_identity): "It's checked by Lean's `ring` tactic" → "The source proves it with Lean's `ring` tactic", plus "(This site did not build the Lean; see Trust.)". Quiz "How is the identity verified in Lean?" → "How does the Lean source prove the identity?".
9. `nodes_src/statement.py` (full_support Q4 explanation): added "The Lean itself never defines the SK Hamiltonian: it states the result for the explicitly defined functional with this normalization."
10. `nodes_src/statement.py` (IsMinimizer body): added a paragraph saying `IsMinimizer W γ` is minimality of `parisi W ·` for the same `W` as the conclusion, and that the Lean does not separately state that P is independent of `W`.
11. `pages/roadmap.md`: "(checked by `ring`)" → "(proved by `ring` in the source)".
12. `site.json` startNote: "The statement and its 16 definitions are identical … The proof itself is in Main.lean." → "The 16 definitions the statement uses are identical … The theorem itself, with its proof, is in Main.lean, whose lines 35–36 repeat the challenge's lines 90–91."

## Remaining concerns and decisions for the project owner

1. **Existence of a minimizer is not in Lean** (already labelled CONDITIONAL everywhere). Whether to say more, for
   example that a vacuous reading is possible in principle if the Lean functional had no minimizer, is the owner's
   choice. Review caveat 1 already says this.
2. **Dependence on W.** Both `parisi` and `IsMinimizer` are defined relative to the given Brownian system `W`. The
   theorem is internally consistent because one `W` is used throughout, and fix 10 now says so. But the Lean never
   proves that P(γ) is the same for all `W`, so "γ minimizes P" in Lean is minimality for that `W`'s control problem.
   This is not an overclaim on the site. Consider adding it as a Review caveat.
3. **Not re-verified:** the Plectis Atlas and Prove2Me descriptions on Trust (web pages, not fetched in this audit).
   The GitHub-hosted MathVet and cert-machine rows were checked and match.
4. **Proof-graph edges** come from a text scan (as Trust says). The audit did not check edges node by node.
5. **Uncommitted changes outside the site.** `git diff` showed changes to `README.md` and `hub.json` that this audit
   did not make. They were left untouched. The coordinator should check whose they are.
