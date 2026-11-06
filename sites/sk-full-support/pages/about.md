# About this site

**What this is.** An unofficial, AI-assisted, plain-English reading of one Lean 4 theorem published by OpenAI in
[openai/math](https://github.com/openai/math): `OAI.ZeroTemperatureSK.full_support`, the formal version of
Theorem 1.1 of the manuscript
[*Full support of the zero-temperature Sherrington–Kirkpatrick order parameter*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Full-support-of-the-zero-temperature-Sherrington-Kirkpatrick-order-parameter-September-27-2026/main.pdf)
(OpenAI, September 27, 2026). Everything is pinned to commit
[`adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a).

**Who made the proof.** The manuscript's README names its author as OpenAI. The repository README says its
contents are "mathematical manuscripts and supporting proof artifacts produced by an internal OpenAI model". This
site claims nothing more specific than that about authorship.

**What the Lean covers.** Three upstream pieces matter:

- **The target:** ComparatorChallenges/SKFullSupport.lean, the statement and its 16 definitions, ending in a
  deliberate `sorry`. It is the challenge a proof has to match (checked with the
  [Comparator](https://github.com/leanprover/comparator) tool), and the source of the Prove2Me mission
  [Full support of the zero-temperature Sherrington–Kirkpatrick order parameter](https://prove2.me/missions/Full_support_of_the_zero-temperature_Sherrington-Kirkpatrick_order_parameter).
- **The model:** Model.lean in `lean/OAI/Probability/SKSupport/`, which repeats those definitions character for
  character (lines 12–88 of both files are identical).
- **The proof:** Main.lean (`minimizer_full_support_actual` and `full_support`) and the other 133 files in
  `lean/OAI/Probability/SKSupport/`, about 20,000 lines, importing only Mathlib.

Prove2Me also lists a separately submitted solution to this target. This site does **not** describe that
submission; it explains the proof OpenAI published in openai/math.

**Where to start.** [Start here](#/start) shows the theorem and the definitions it needs, simplest first. The
[proof graph](#/) shows how the declarations depend on each other.
