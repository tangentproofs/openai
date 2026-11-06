# Trust: what was checked, and by whom

This page separates three things: what **this site checked itself**, what **other people report** having checked, and
what **nobody here checked**. Nothing on this site is official, and the plain-English nodes are AI-written drafts
(`review: draft`) that no person has reviewed.

## Checked for this site (November 2026)

All of these are source-level checks on openai/math at commit
[`adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a). **The Lean was not built
for this site**, and `#print axioms` was not run here.

| Check | Result |
|---|---|
| Lean built / kernel-checked here | **No.** (An outside run reports about 7 GB peak memory for this check; it was not attempted on the small shared machine used to write this site.) |
| Files in the proof | 135 `.lean` files, 20,357 lines, in `lean/OAI/Probability/SKSupport/` |
| Imports outside that directory | Only `Mathlib` (every `import` line checked) |
| `sorry`, `admit` | **0** in all 135 files |
| `axiom` declarations | **0** |
| `native_decide`, `Lean.ofReduceBool`, `implemented_by`, `extern`, `opaque`, `unsafe`, `partial def` | **0** |
| `set_option`, `attribute [...]`, `local instance`, macros/`elab`/`syntax`, `#eval`, `run_cmd` | **0** |
| `decide` | **2**, both proving small facts about natural numbers (`0 < 1`-style), checked by the kernel: Moments/StrictMoments.lean line 101 and Moments/IntegratedCompletionSquare.lean line 56 |
| Target statement vs proof's definitions | Lines 1–89 of ComparatorChallenges/SKFullSupport.lean and Model.lean are **character-for-character identical** (checked with `diff`). The theorem signature in Main.lean lines 35–36 matches the target's lines 90–91. |
| Comparator configuration | ComparatorChallenges/SKFullSupport.json names theorem `OAI.ZeroTemperatureSK.full_support`, solution module `OAI.Probability.SKSupport.Main`, permitted axioms `propext`, `Quot.sound`, `Classical.choice`, no definition holes. |
| Same source as the commit the outside reports checked | **Yes.** At `adc7f12` and at `fd4aeeb` (the commit the reports below use), the git object ids of `lean/OAI/Probability/SKSupport/` (tree `560a5aa…`), the target `.lean` and `.json`, `lake-manifest.json` and `lean-toolchain` are identical. |
| Copy on this site matches upstream | The vendored files have the same git tree id as upstream ([VENDORED.md](https://github.com/tangentproofs/openai/blob/main/projects/openai-math/VENDORED.md)). |

A keyword search is not a proof check: it can't tell you that the kernel accepts the proof. It does tell you there is no
explicit escape hatch in the source.

## Reported by others (not repeated here)

These are other people's runs. This site read their published reports (rows quoted below) but did **not** repeat them.

| Who | What they report | Commit | Source |
|---|---|---|---|
| MathVet | Comparator run in a sandbox: `comparator-sandboxed-pass`, built, closure ok, no shadowing, axioms printed `Classical.choice ; Quot.sound ; propext`, proof cone 20,357 lines of OAI code and no external code. Finished 2026-10-08. | `fd4aeeb` | [challenge-status.csv](https://github.com/mathvet/mathvet/blob/14c7f918cd336d0da03a02aae5a0eed4a429d4db/reviews/openai-math/challenge-status.csv) (row `SKFullSupport`) |
| cert-machine (Carlos Toledo) | `CERTIFIED`: "Comparator exit 0; nanoda and Lean's kernel both accept", run 38040214623 on 2026-10-10, 0 definition holes. Their definition of CERTIFIED: the theorem states exactly the challenge statement, uses only the three standard axioms, and two independent kernels accept it. They also say it "does not mean the paper's claim is proved". | `fd4aeeb` | [openai-math-kernel.json](https://github.com/carlostoledo1891/cert-machine/blob/9814e4c06281e34a113ce853d7d99ccce160b750/certs/openai-math-kernel.json) (entry `SKFullSupport`) |
| Plectis Atlas | Collects the two reports above and links them; it states it runs no checks itself. | `fd4aeeb` | [SKFullSupport](https://wcook04.github.io/plectis-atlas/statements/SKFullSupport.html) |
| Prove2Me | The mission page shows the target `OAI.ZeroTemperatureSK.full_support` as PROVED, while other text on the same page still says the target is Open. It lists an accepted submission in its activity feed. That submission's source is not public on the page, and this site does not describe it. | `adc7f12` | [mission page](https://prove2.me/missions/Full_support_of_the_zero-temperature_Sherrington-Kirkpatrick_order_parameter) |

The outside reports are about whether the Lean proof checks against the Lean target. Both MathVet and cert-machine
also give **family-level** verdicts ("supporting-only", "different") for openai/math family 281 as a whole. The Atlas
explains that these concern the family's QAOA headline result, not a mismatch between this theorem and the paper's
Theorem 1.1. The Atlas also records that no human review of whether the Lean matches the paper's theorem exists, and
that OpenAI's own formalization catalogue (`lean/formalization.yaml`) does not list this as a main result. We
confirmed the second point: the catalogue at `adc7f12` has no entry for this manuscript.

## Not checked by anyone here

- Whether the Lean kernel accepts the proof (see the outside reports above).
- The mathematics of the paper beyond Theorem 1.1 and the outline of its proof.
- Whether this explainer's English is right. The [Review](#/review) page and an independent model audit look at that,
  but no person has reviewed it.
- How the declarations relate to each other: the [proof graph](#/) is built by scanning the source **text**, not from a
  Lean build. Every declaration is marked `extracted: false`. Some edges will be missing or wrong (for example, a scan
  can miss a lemma used only through a `let` or `show`).

## Authorship and licence

The Lean source and the manuscript are OpenAI's, published in [openai/math](https://github.com/openai/math) under the
Apache License 2.0; the repository README says its contents were "produced by an internal OpenAI model". This site
shows the source unmodified under that licence ([licence text](src/LICENSE.txt)). The upstream repository has no
NOTICE file. The explainer's own code is MIT-licensed; that licence does not cover the quoted Lean.
