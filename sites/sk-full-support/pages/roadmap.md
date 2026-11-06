# Roadmap: how the proof is organized

The Lean proof of [full_support](#/node/full_support) follows the paper's plan closely. This page is a reading order
through it, in three stages. Every link goes to a node with a plain-English explanation, the exact Lean statement and
a link to the highlighted source. It is a guide to the proof's structure, not a check of it: see [Trust](#/trust).

Throughout, X is the constructed diffusion and

- **q(t)** = E[gradient(t, X_t)²] ([squareMoment](#/node/squareMoment) of the constructed diffusion),
- **q′(t)** = E[curvature(t, X_t)²] ([curvatureMoment](#/node/curvatureMoment)).

The goal is to show that the support of γ's measure has no gaps, and that q(t) = t and q′(t) = 1.

## Stage 1. Build the objects: the measure and the diffusion

Before anything about minimizers, the proof constructs the two objects the conclusion says exist.

| Step | Node | Where |
|---|---|---|
| γ as a Mathlib Stieltjes function | [parameterStieltjes](#/node/parameterStieltjes) | Support/GapCurvature.lean lines 96–99 |
| Its measure, plus an atom γ(0) at 0 | [parameterMeasure](#/node/parameterMeasure) | Support/GapCurvature.lean lines 109–110 |
| …which represents γ: μ([0,t]) = γ(t) | [parameterMeasure_isStieltjes](#/node/parameterMeasure_isStieltjes) | Support/GapCurvature.lean lines 112–119 |
| A progressive version of B | [BrownianSystem.driver](#/node/BrownianSystem.driver) | Diffusion/ProgressiveBrownian.lean lines 93–94 |
| The feedback (gradient along the path, \|·\| ≤ 1) | [rawFeedback](#/node/rawFeedback) | Diffusion/CompactDrift.lean lines 251–252 |
| The diffusion X = B + ∫ γ·gradient | [diffusion](#/node/diffusion) | Diffusion/CompactDrift.lean lines 275–276 |
| …which satisfies IsDiffusion | [diffusion_isDiffusion](#/node/diffusion_isDiffusion) | Diffusion/CompactDrift.lean lines 309–327 |
| q(t) = ∫₀ᵗ q′, so q(0) = 0 and q′ is q's derivative | [squareMoment_eq_integral_curvatureMoment](#/node/squareMoment_eq_integral_curvatureMoment), [squareMoment_hasDerivAt](#/node/squareMoment_hasDerivAt) | Moments/StripSquareMoment.lean, Moments/PerturbationLimits.lean |

Behind these sit the analytic foundations, most of the code by line count: `Foundations/` (30 files), `Regularity/`,
`Parabolic/` and `Backward/` (39 files) for the value function's regularity on compact time strips [0,T] with T < 1,
`Diffusion/` (21 files) for Picard iteration and uniqueness of the SDE, and `Control/` (9 files) for the control
problem and approximation of γ by step functions. The paper does this in Section 2. These files are on the
[proof graph](#/) (switch to "Files" or "All declarations") but mostly don't have plain-English nodes.

## Stage 2. Contact and gap curvature

**Contact (from minimality).** Moving γ toward any other order parameter can't lower P. Differentiating P along such
a chord gives the [first variation](#/node/minimizer_variational_inequality): ∫ (β − γ)(q − t) ≥ 0.

| Step | Node | Paper |
|---|---|---|
| The potential G(s) = ∫ₛ¹ (q − t) | [contactPotential](#/node/contactPotential) | (6.3) |
| First variation ≥ 0 at a minimizer | [minimizer_variational_inequality](#/node/minimizer_variational_inequality) | Lemma 6.1 |
| Adding an atom: G ≥ 0 | [contactPotential_nonneg](#/node/contactPotential_nonneg) | Lemma 6.2 |
| Contact: q(t) = t and q′(t) ≤ 1 on the support | [minimizer_contact](#/node/minimizer_contact), via [contact_conditions](#/node/SupportDeterministic.Variation.contact_conditions) | Lemma 6.2, (6.4) |
| No constant stretch reaching 1 | [minimizer_no_terminal_plateau](#/node/minimizer_no_terminal_plateau) | Lemma 6.3 |

**Gap curvature (the heart of the paper).** On a stretch where γ is a constant c > 0, q′ is strictly convex. The third
derivative of q there is an explicit expectation, [stripThird](#/node/stripThird), whose integrand
z² − 12 v w² + 6 v⁴ has a negative middle term. An exact [rational identity](#/node/Certificate.rational_identity)
(proved by `ring` in the source), together with sign information about the value function and the density of X on smooth
finite-step approximations, shows its expectation is at least (1/1000)·E[v⁴] > 0. The inequality then passes to the
limit for the actual γ.

| Step | Node | Paper |
|---|---|---|
| The polynomial z² − 12vw² + 6v⁴ | [coerciveJetPolynomial](#/node/coerciveJetPolynomial) | Section 1.2 |
| The algebraic certificate | [Certificate.rational_identity](#/node/Certificate.rational_identity) | Section 4 |
| Coercive inequality for the true value function | [actual_coercivity](#/node/actual_coercivity) | Sections 3–5 |
| q‴ > 0 at a point where γ(t) > 0 is continuous | [stripThird_pos](#/node/stripThird_pos) | (5.1) |
| q′ strictly convex on a positive constant stretch | [positive_gap_curvature](#/node/positive_gap_curvature) | Proposition 5.1 |
| q′ strictly increasing on a zero stretch | [zero_gap_curvature](#/node/zero_gap_curvature) | Proposition 5.1 (c = 0) |

## Stage 3. Close the gaps, then transfer via uniqueness

**Close the gaps (pure real analysis).** [full_support_of_contact_and_gap_curvature](#/node/SupportDeterministic.Variation.full_support_of_contact_and_gap_curvature)
takes all of the above as hypotheses. A missing point would sit in a gap (a,b) with support points at the ends, where γ
is constant; contact gives q(a) = a, q(b) = b and q′ ≤ 1 at the ends; convexity (or monotonicity) of q′ then forces
q′ < 1 inside, contradicting the mean value theorem
([no_positive_constant_gap](#/node/SupportDeterministic.Variation.no_positive_constant_gap),
[no_zero_constant_gap](#/node/SupportDeterministic.Variation.no_zero_constant_gap)). So the support is everything, γ is
strictly increasing, and q(t) = t; then [q′ = 1](#/node/SupportDeterministic.Variation.derivative_eq_one_of_full_contact).
This is assembled in [minimizer_full_support_actual](#/node/minimizer_full_support_actual) (Main.lean lines 19–33).

**Transfer via uniqueness.** So far the identities are about the *constructed* diffusion. [full_support](#/node/full_support)
(Main.lean lines 35–59) applies the main lemma to every representing measure, and uses
[diffusion_uniqueness](#/node/diffusion_uniqueness) (any diffusion equals the constructed one almost surely) and
equality of integrals of almost-everywhere-equal functions to get both identities for **every** diffusion.

## What the Lean does not cover

- Existence of a minimizer (the paper cites Auffinger and Chen); the theorem assumes one.
- The paper's later results: smoothness and positivity of γ′, γ(0) = 0 (Corollary 6.4), and Section 7.
- The link between P and the SK ground-state energy, (1.4), which the paper cites from the literature.
