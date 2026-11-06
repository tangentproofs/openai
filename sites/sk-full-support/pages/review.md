# Review: does the Lean say what Theorem 1.1 says?

## Verdict: faithful, CONDITIONAL on a minimizer existing, with scope caveats

`OAI.ZeroTemperatureSK.full_support` states the paper's Theorem 1.1 for the pure, zero-field SK model with
ξ(t) = t²/2. Its one hypothesis is that γ globally minimizes the Parisi functional. No hypothesis assumes support,
monotonicity or regularity, so nothing smuggles in the conclusion. The proof contains no `sorry`, `axiom` or
`native_decide` (see [Trust](#/trust)). Two outside groups report that the Lean kernel accepts it; this site did not
re-run that.

The independent honesty audit of every page and node on this site is summarized at the bottom.

## Clause by clause

| Paper, Theorem 1.1 (p. 2) | Lean (Model.lean) | Match |
|---|---|---|
| γ ∈ U: nonnegative, nondecreasing, right-continuous on [0,1), ∫₀¹ γ < ∞ | [OrderParameter](#/node/OrderParameter), lines 17–22 | Same four conditions |
| Φγ(t,x) = sup over controls \|a\| ≤ 1, progressively measurable and adapted to increments after t, of E[\|x + B₁ − B_t + ∫ γa\| − ½∫ γa²] (1.1) | [value](#/node/value), [controlPayoff](#/node/controlPayoff), [Control](#/node/Control), [incrementFiltration](#/node/incrementFiltration) | Same formula, written as a supremum over a set of expectations |
| P(γ) = Φγ(0,0) − ½∫₀¹ tγ(t) dt (1.3) | [parisi](#/node/parisi), lines 59–60 | Same |
| "γ minimizes P" over U | [IsMinimizer](#/node/IsMinimizer): P(γ) ≤ P(η) for **every** order parameter η | Same (global minimum) |
| μγ([0,t]) = γ(t), relative topology of [0,1) | [IsStieltjesMeasure](#/node/IsStieltjesMeasure) on [Time](#/node/Time) = [0,1) | Same; Lean also proves such a μ **exists** and the claim holds for **every** such μ |
| supp μγ = [0,1) | `μ.support = Set.univ` | Same |
| γ(b) > γ(a) for 0 ≤ a < b < 1 | `∀ a b : Time, a < b → γ.val a < γ.val b` | Same |
| X solves dX = γ uγ(t,X) dt + dB, X₀ = 0 (1.5) | [IsDiffusion](#/node/IsDiffusion): progressive, a.s. continuous, X₀ = 0, integral equation for all t ∈ [0,1] | Same, in integral form; Lean proves a solution **exists** and states the identities for **every** solution |
| E[uγ(t,X_t)²] = t, E[Φγ,xx(t,X_t)²] = 1 for 0 ≤ t < 1 (1.6) | [squareMoment](#/node/squareMoment) = t and ∫ [curvature](#/node/curvature)² = 1, for all t : Time | Same |

In two places the Lean says **more** than the paper's sentence: it asserts existence of the measure and of the
diffusion, and it quantifies over all of them instead of "the" measure and "the" solution.

## Caveats (what the Lean does not say)

1. **CONDITIONAL on a minimizer.** The theorem assumes a minimizer; nothing in the Lean proves one exists. The paper
   takes existence from Auffinger and Chen ((1.4), citing [3]). If the Lean-defined functional had no minimizer, the
   theorem would hold vacuously. No reason to expect that is known here, but it is not ruled out in Lean.
2. **No link to spin glasses in Lean.** The SK Hamiltonian and the formula "limit of the ground-state energy = min P"
   (1.4) are cited background in the paper and do not appear in the Lean. The Lean theorem is about the explicitly
   defined control problem and functional; the paper likewise says "the proof of the support assertion itself applies to any minimizer of the
   explicitly defined functional (1.3)".
3. **[0,1), not [0,1].** Support is relative to [0,1); the statement says nothing at t = 1. The measure need not be a
   probability measure and may have infinite mass near 1.
4. **Lean's total operations.** `gradient` and `curvature` use `deriv` (0 where not differentiable), `value` uses `sSup`
   (0 for an unbounded set) and the Bochner integral (0 for a non-integrable function). These conventions are part of
   the definitions; the identities in the conclusion are proved about these exact Lean functions. Proving them requires
   the real differentiability and integrability, which the proof establishes rather than assumes.
5. **Not the whole paper.** Smoothness and positivity of γ′, γ(0) = 0 (Corollary 6.4), and the Section 7 consequences
   are not part of this theorem. Neither is any nonzero-field or mixed-spin version; the paper says neither is implied.
6. **Not the first proof of the support claim.** The paper itself says Chen [7, Theorem 1.3] proved the same
   full-relative-support conclusion; its stated contribution is a different argument (the explicit coercive identity).
7. **Which proof.** This site explains the proof OpenAI published in openai/math. Prove2Me lists a separately submitted
   accepted solution to the same target; its source isn't public on the mission page, and nothing here describes it.

8. **One Brownian system at a time.** `parisi W γ` is computed with a given Brownian system `W`, and `IsMinimizer W γ`
   compares order parameters for that same `W`. Mathematically the value depends only on the law of Brownian motion,
   but the Lean never proves that P is the same for every `W`. The theorem simply fixes one `W` in the hypothesis and
   the conclusion, so nothing is lost; it just isn't stated as a fact about P alone.

## Honesty audit of this site

An independent model session (a separate Claude agent, not the one that wrote the nodes) audited every node, quiz
answer key and page against the Lean, following
[prompts/honesty-audit.md](https://github.com/tangentproofs/openai/blob/main/prompts/honesty-audit.md). Its full report
is [sites/sk-full-support/SK_FULL_SUPPORT_AUDIT.md](https://github.com/tangentproofs/openai/blob/main/sites/sk-full-support/SK_FULL_SUPPORT_AUDIT.md).

**Verdict: PASS WITH FIXES.** The auditor found the headline and all 16 definitions faithful to the Lean, with no
hypothesis that smuggles in the conclusion. It checked every node's line references against the source (all 52
matched), re-ran the Trust page's source checks (all held), and found no authorship claims beyond the upstream
README. It made 12 fixes, all already applied:

- six paper citations corrected (e.g. Proposition 5.1 says q′, not q, is strictly convex; a paraphrase had been shown as a quote);
- one wrong quiz answer key: it had implied the constructed X never equals B, which fails when γ = 0;
- "checked by `ring`" reworded to "proved by `ring` in the source", because this site did not build the Lean;
- two clarifications: the Lean never defines the SK Hamiltonian, and minimality is for the same `W` as in the conclusion;
- the Start-page note no longer suggests the theorem itself is in Model.lean.

Remaining concerns it raised: the minimizer-existence gap (caveat 1); the dependence on `W` (caveat 8); the Atlas and
Prove2Me descriptions on Trust were checked by a separate fetch, not by the auditor; and the proof-graph edges come from
a text scan and were not audited.
