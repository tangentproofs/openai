# tangentproofs/openai

**Unofficial, AI-assisted, plain-English explainers of Lean proofs published in
[openai/math](https://github.com/openai/math).**

Live site: **<https://tangentproofs.github.io/openai/>**

> **Not official documentation.** Nothing here is written, reviewed, endorsed or maintained by OpenAI, by the
> authors or maintainers of openai/math, by Prove2Me, or by any mathematician cited in the papers. The
> explanations were drafted by Claude (an AI model) and may contain mistakes. The Lean source and the papers are the
> ground truth. Each explainer pins the exact upstream commit it describes and links every claim back to it.

## Explainers

| Explainer | Lean theorem | Upstream | Nodes |
|---|---|---|---|
| [Zero-temperature SK full support](https://tangentproofs.github.io/openai/sk-full-support/) | `OAI.ZeroTemperatureSK.full_support` | [openai/math@adc7f12](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/Probability/SKSupport), manuscript *Full support of the zero-temperature Sherrington–Kirkpatrick order parameter* (OpenAI, 2026-09-27) | 52 |

The site root is an index that can hold more explainers; each lives at `/<slug>/`.

### SK full support in one paragraph

If γ minimizes the zero-temperature Parisi functional for the pure, zero-field Sherrington–Kirkpatrick model, then
γ's Stieltjes measure has support all of [0,1), γ strictly increases, and along the optimally controlled diffusion
E[gradient²] = t and E[curvature²] = 1. The Lean theorem assumes a minimizer (it does not prove one exists). The proof
is 135 files / 20,357 lines importing only Mathlib, with no `sorry`, `axiom` or `native_decide`. **It was not built
for this site**; two outside groups (MathVet, cert-machine) report that it passes Comparator, the second with two
independent kernels. See the site's [Review](https://tangentproofs.github.io/openai/sk-full-support/#/review) and
[Trust](https://tangentproofs.github.io/openai/sk-full-support/#/trust) pages for exactly what was and wasn't checked.

Each explainer has:

- **Start here**: the theorem and every definition its statement uses, simplest first, each beside its exact Lean and
  the paper's wording;
- **Proof graph**: declarations from the headline down, with plain-English nodes and short quizzes;
- **Roadmap**: a reading order through the proof;
- **Source**: the highlighted Lean (Apache-2.0, unmodified), with line anchors;
- **Review** and **Trust**: statement-vs-paper comparison, honesty-audit verdict, and what was checked by whom;
- **Comments** on every node via [giscus](https://giscus.app) (GitHub Discussions on this repository).

## Repository layout

| path | what |
|---|---|
| `sites/<slug>/` | one explainer: `site.json` (config), `nodes_src/*.py` (the explainer nodes), `pages/*.md` (About, Roadmap, Review, Trust), the honesty-audit report |
| `projects/openai-math/` | an **unmodified** subset of openai/math (Apache-2.0); provenance and git object ids in [`VENDORED.md`](projects/openai-math/VENDORED.md) |
| `engine/` | the site engine (browser app, build tools, declaration scanner) from [tangentproofs/informalization-tools](https://github.com/tangentproofs/informalization-tools), with small local fixes |
| `tools/` | hub tools: `update.mjs` renders the root `index.html` from `projects.json` + `hub.json` |
| `hub.json`, `projects.json`, `index.html`, `assets/` | the root index page |
| `prompts/`, `docs/`, `skill/` | the drafting/audit briefs and conventions the explainers follow |
| `.github/workflows/pages.yml` | builds every site and deploys GitHub Pages (no Lean build in CI) |

### Local engine changes (relative to informalization-tools `3663ef6`)

- `engine/build.sh`: a site may set `"vendored": true` to use a plain directory copied from upstream instead of a git
  submodule (openai/math is about 1 GB).
- `engine/tools/scan_decls.py`: does not guess an unrelated lemma for structure-field access such as `W.measurable`;
  optional `"defBodies": true` shows short definitions with their bodies; headers shown without their body/proof are
  marked "proof omitted".
- `engine/tools/write_nodes.py`: skips `_*.py` helper files in `nodes_src/`, as documented.
- `engine/gen.py`, `engine/assets/style.css`: the banner on every explainer page opens with a large **Not official
  documentation** heading.

## Building locally

```sh
(cd engine && npm ci)
pip install pyyaml
engine/build.sh sk-full-support                     # -> _site/sk-full-support/
python3 tools/sync_projects.py && node tools/update.mjs   # -> index.html (root index)
mkdir -p _site && cp index.html _site/ && cp -R assets _site/
python3 -m http.server -d _site 8765                # http://localhost:8765/
```

No Lean toolchain is needed: declarations are scanned from the source text. The build fails if a node cites a line
range outside its file or a quiz key is invalid.

## Adding an explainer

1. Copy the needed upstream files into `projects/<name>/` unmodified, with the upstream LICENSE and a `VENDORED.md`
   (commit, paths, git object ids). Only do this for a licence that permits reproduction.
2. Add `sites/<slug>/site.json` (see `docs/site-config.schema.json`) and a `projects.json` entry.
3. Write nodes in `sites/<slug>/nodes_src/` following `prompts/draft-explainer.md`; headline first, then the
   statement set, then the proof spine.
4. Run an independent honesty audit (`prompts/honesty-audit.md`) and commit its report next to the site.
5. Build, check, push to `main`; the workflow deploys.

## Corrections and take-down requests

Open an [issue](https://github.com/tangentproofs/openai/issues) or comment on any node. Authors who want an explainer
changed or removed: say so and it will be done.

## Licence

- **Explainer code and text** (everything except `projects/`): [MIT](LICENSE), Copyright (c) 2026 Michal Wallace.
  The engine is adapted from tangentproofs/informalization-tools, which is MIT-licensed by the same copyright holder.
- **Quoted proof sources** (`projects/openai-math/`, and the Lean shown on the site): © OpenAI, [Apache License
  2.0](projects/openai-math/LICENSE), unmodified. The MIT licence does not apply to them.
- The manuscripts are linked, not copied; short quotations are attributed to the paper with page numbers.
- Authorship of the mathematics and the Lean belongs to OpenAI; the openai/math README says its contents were
  "produced by an internal OpenAI model". This repository claims no part of it.
