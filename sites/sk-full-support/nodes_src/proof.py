# The proof spine: from full_support down through the main lemma, the deterministic closure argument,
# the contact conditions, gap curvature (and the coercive identity behind it), and the diffusion.
# Ground truth: lean/OAI/Probability/SKSupport/** at openai/math@adc7f12.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_adder, q, paper

NODES = []
node = node_adder(NODES)
V = "SupportDeterministic.Variation."
SD = "SupportDeterministic."
Q_ = "q(t) = [squareMoment](#/node/squareMoment)(diffusion, t) = E[gradient(t, X_t)²]"

# ================================================================ main lemma
node("minimizer_full_support_actual",
 "Main lemma: full support and the identities for the constructed diffusion",
 "For a minimizer γ and any measure μ representing it: μ has full support, γ (extended by 0) is strictly increasing on [0,1), "
 "and for the constructed diffusion, E[gradient²] = t and E[curvature²] = 1 for all t in [0,1).",
 r"""## Plain English

**Theorem (`minimizer_full_support_actual`, Main.lean lines 19–33).** Let γ be a [minimizer](#/node/IsMinimizer) and μ any
measure that [represents γ](#/node/IsStieltjesMeasure). Then

- `μ.support = univ`;
- the zero-extension of γ is strictly increasing on [0,1);
- for every t in [0,1): [squareMoment](#/node/squareMoment) of the **constructed** [diffusion](#/node/diffusion) at t equals t,
  and [curvatureMoment](#/node/curvatureMoment) at t equals 1.

Write q(t) = E[gradient(t, X_t)²] and q′(t) = E[curvature(t, X_t)²] (the second is the derivative of the first, see
[squareMoment_hasDerivAt](#/node/squareMoment_hasDerivAt)). The proof is two calls:

1. The purely deterministic theorem
   [full_support_of_contact_and_gap_curvature](#/node/SupportDeterministic.Variation.full_support_of_contact_and_gap_curvature)
   says: if q is continuous with derivative q′, q(0) = 0, the **contact conditions** hold on the support, there is **no
   terminal plateau**, and q′ is strictly convex on any positive constant stretch of γ (strictly increasing on a zero
   stretch), then μ has full support, γ strictly increases, and q(t) = t on [0,1). Main.lean feeds it each hypothesis:
   [minimizer_contact](#/node/minimizer_contact), [minimizer_no_terminal_plateau](#/node/minimizer_no_terminal_plateau),
   [positive_gap_curvature](#/node/positive_gap_curvature) and [zero_gap_curvature](#/node/zero_gap_curvature), plus
   continuity and differentiability facts about the moments.
2. Since q(t) = t on all of [0,1), its derivative is 1:
   [derivative_eq_one_of_full_contact](#/node/SupportDeterministic.Variation.derivative_eq_one_of_full_contact) gives
   q′(t) = 1, i.e. E[curvature²] = 1.
""" + paper("Section 1.2 and the proof of Theorem 1.1 (Section 6)", "the same plan: contact conditions from the first variation, strict convexity of q′ on a positive constant interval, then the mean value contradiction."),
 [q("Which diffusion do the identities in this lemma talk about?", ["The one the proof constructs, `diffusion W γ`", "Every diffusion"], 0,
    "It says `squareMoment W γ (diffusion W γ) t = t`. Passing to every diffusion is done afterwards in [full_support](#/node/full_support) via uniqueness."),
  q("Which theorem does the logical heavy lifting from the hypotheses to full support?", ["full_support_of_contact_and_gap_curvature", "diffusion_uniqueness", "parameterMeasure_isStieltjes"], 0,
    "Main.lean line 23 calls it with all the analytic inputs."),
  q("How is E[curvature²] = 1 obtained?", ["By differentiating q(t) = t", "By a separate computation", "It is assumed"], 0,
    "q′ = curvatureMoment and q = id on [0,1), so q′ = 1 (Main.lean lines 30–32)."),
 ],
 widgets=[{"type": "walkthrough", "title": "The proof of minimizer_full_support_actual (Main.lean, lines 19-33)",
   "config": {"steps": [
     {"text": "Call the deterministic closure theorem with γ's zero extension and μ.", "link": V + "full_support_of_contact_and_gap_curvature",
      "lean": "have hh := SupportDeterministic.Variation.full_support_of_contact_and_gap_curvature"},
     {"text": "Regularity of q and q′: continuity, q′ is the derivative of q, and q(0) = 0.", "link": "squareMoment_hasDerivAt",
      "lean": "(fun t ht => squareMoment_hasDerivAt W γ ht.1 ht.2) (squareMoment_zero W γ)"},
     {"text": "Contact conditions and no terminal plateau, both from minimality.", "link": "minimizer_contact",
      "lean": "(minimizer_contact W γ hmin hμ) (minimizer_no_terminal_plateau W γ hmin)"},
     {"text": "Curvature on a positive constant stretch of γ.", "link": "positive_gap_curvature",
      "lean": "(fun a b c ha hab hb hc hconst => positive_gap_curvature W γ ha hab hb hc hconst)"},
     {"text": "Curvature on a zero stretch of γ.", "link": "zero_gap_curvature",
      "lean": "(fun a b ha hab hb hconst => zero_gap_curvature W γ ha hab hb hconst)"},
     {"text": "From q(t) = t everywhere, the derivative q′ is 1 everywhere.", "link": V + "derivative_eq_one_of_full_contact",
      "lean": "have ha := SupportDeterministic.Variation.derivative_eq_one_of_full_contact hh.2.2"},
   ]}}])

# ================================================================ deterministic closure (Closure.lean)
node(SD + "Time", "Time (deterministic copy): [0,1)",
 "A second, identical abbreviation `Time := Set.Ico 0 1` inside the namespace SupportDeterministic.",
 r"""## Plain English

**Definition (`SupportDeterministic.Time`, Support/Closure.lean line 11).** The same subtype [0,1) as the model's
[Time](#/node/Time), declared again so that the deterministic part of the proof (which knows nothing about Brownian
motion) is self-contained. Both unfold to `Set.Ico (0 : ℝ) 1`, so they are the same type.
""",
 [q("Is this a different interval from the model's Time?", ["No, both are [0,1)", "Yes, [0,1]"], 0, "Both are `Set.Ico (0 : ℝ) 1`."),
  q("Why repeat it?", ["To keep the deterministic part self-contained", "Because the model's Time is wrong"], 0, "The Closure.lean file works with plain functions ℝ → ℝ and its own copies of the notions."),
  q("Does it matter for the main theorem which copy is used?", ["No, they are definitionally the same type", "Yes"], 0, "An `abbrev` unfolds; both are the same subtype."),
 ])

node(SD + "IsOrderParameter", "IsOrderParameter: the order-parameter conditions for a plain function",
 "For a function γ : ℝ → ℝ: nonnegative, monotone, right-continuous on [0,1), and integrable on [0,1).",
 r"""## Plain English

**Structure (`SupportDeterministic.IsOrderParameter`, Support/Closure.lean lines 13–17).** The four conditions of an
[OrderParameter](#/node/OrderParameter), stated for a plain real function γ and only on [0,1): nonnegative there, monotone
there, right-continuous at each point there, integrable on [0,1).

The bridge lemma `OrderParameter.original_deterministic` (Support/CDFParameters.lean lines 81–100) proves that the zero
extension of every bundled order parameter satisfies these conditions.
""",
 [q("On which set are the conditions imposed?", ["[0,1)", "all of ℝ"], 0, "Every field quantifies over `Set.Ico 0 1`."),
  q("Is this stronger than OrderParameter?", ["No, it is the same four conditions, for a plain function", "Yes, it adds smoothness"], 0, "Same conditions, different packaging."),
  q("Which object is fed to the deterministic theorem in Main.lean?", ["`extend γ.val`, via original_deterministic", "γ itself"], 0, "Main.lean line 24: `(γ.original_deterministic)`."),
 ])

node(SD + "IsStieltjesMeasure", "IsStieltjesMeasure (deterministic copy)",
 "μ([0,t]) = γ(t) for every t in [0,1), for a plain function γ : ℝ → ℝ.",
 r"""## Plain English

**Definition (`SupportDeterministic.IsStieltjesMeasure`, Support/Closure.lean lines 19–20).** The same condition as the
model's [IsStieltjesMeasure](#/node/IsStieltjesMeasure), for a plain function γ on ℝ. The lemma
`stieltjes_deterministic` (Support/CDFParameters.lean lines 102–105) shows the model's version for γ gives this version
for `extend γ.val`.
""",
 [q("What does it require?", ["μ([0,t]) = γ(t) for t in [0,1)", "μ is a probability measure"], 0, "`μ (Set.Iic t) = ENNReal.ofReal (γ t)` for every t : Time."),
  q("Is it the same condition as the model's version?", ["Yes, after extending γ by zero", "No"], 0, "On [0,1), `extend γ.val t = γ.val t`."),
  q("Can μ have infinite total mass?", ["Yes", "No"], 0, "Only the masses of [0,t] for t < 1 are pinned down."),
 ])

node(SD + "InSupport", "InSupport: t is a support point",
 "`InSupport μ t` says t is in [0,1) and the point t of Time is in the support of μ.",
 r"""## Plain English

**Definition (`SupportDeterministic.InSupport`, Support/Closure.lean lines 71–72).** For a real number t, `InSupport μ t`
means: t lies in [0,1), and, viewed as a point of [Time](#/node/SupportDeterministic.Time), it belongs to `μ.support`
(every open neighbourhood of it has positive μ-mass).
""",
 [q("Can a t outside [0,1) be InSupport?", ["No", "Yes"], 0, "The definition includes `t ∈ Ico 0 1`."),
  q("What does membership in the support mean?", ["Every neighbourhood has positive mass", "μ({t}) > 0"], 0, "That's Mathlib's `Measure.support`."),
  q("Why wrap it this way?", ["To talk about real numbers t rather than subtype elements", "To change the meaning of support"], 0, "It is a convenience for real-variable arguments."),
 ])

node(V + "full_support_of_contact_and_gap_curvature",
 "Closure theorem: contact + gap curvature ⇒ full support",
 "A purely real-analysis theorem: if q, q′ satisfy the contact conditions on the support of μ, γ has no terminal plateau, and q′ "
 "is strictly convex (or increasing) on every constant stretch of γ, then μ has full support, γ strictly increases and q(t) = t.",
 r"""## Plain English

**Theorem (`full_support_of_contact_and_gap_curvature`, Support/Closure.lean lines 411–460).** Take real functions γ, q, q′
and a measure μ on [0,1) with

- γ an [order parameter](#/node/SupportDeterministic.IsOrderParameter) and μ [representing](#/node/SupportDeterministic.IsStieltjesMeasure) it;
- q, q′ continuous on [0,1), q′ the derivative of q on (0,1), and q(0) = 0;
- **contact:** at every support point t, q(t) = t and q′(t) ≤ 1;
- **no terminal plateau:** γ is not constant on any interval (a, 1);
- **positive gaps curve:** if γ = c > 0 on (a,b) with 0 ≤ a < b < 1, then the second derivative of q′ is positive on (a,b);
- **zero gaps curve:** if γ = 0 on (a,b), then the derivative of q′ is positive on (a,b).

Then μ.support is all of [0,1), γ is strictly increasing on [0,1), and q(t) = t for every t in [0,1).

**Why.** Suppose some x is missing from the support. Because there's no terminal plateau, support points exist beyond x,
so there is a **gap** (a,b) with no support inside and a, b on the support (or a = 0). On a gap the measure has no mass,
so γ is constant there, say c. Contact at the ends gives q(a) = a, q(b) = b and q′(b) ≤ 1 (and q′(a) ≤ 1 when c > 0).

- If c > 0: q′ is strictly convex on [a,b], so inside it lies strictly below max(q′(a), q′(b)) ≤ 1
  ([no_positive_constant_gap](#/node/SupportDeterministic.Variation.no_positive_constant_gap)).
- If c = 0: q′ is strictly increasing, so it lies below q′(b) ≤ 1 inside
  ([no_zero_constant_gap](#/node/SupportDeterministic.Variation.no_zero_constant_gap)).

Either way q′ < 1 on (a,b), but by the mean value theorem some point has q′ = (q(b) − q(a))/(b − a) = 1. Contradiction.
Once the support is everything, strict monotonicity and q(t) = t follow from the definitions.
""" + paper("Section 1.2 and Section 6", "“If q′ is strictly convex there, it lies below its endpoint chord and hence below 1 inside. Integrating gives q(b) − q(a) < b − a, contradicting contact at the endpoints.”"),
 [q("Does this theorem mention Brownian motion or the SK model?", ["No, it is pure real analysis about γ, q, q′, μ", "Yes"], 0,
    "All of its inputs are real functions and a measure; the stochastic content is supplied by Main.lean."),
  q("On a gap of the support, what is γ?", ["Constant", "Strictly increasing", "Zero"], 0, "No mass on the gap means the distribution function doesn't move (constant_on_support_gap)."),
  q("What contradiction ends the argument?", ["Mean value theorem: q′ = 1 somewhere, but q′ < 1 throughout the gap", "q becomes negative", "μ has infinite mass"], 0,
    "q(a) = a and q(b) = b force average slope 1 (no_gap_of_derivative_lt_one)."),
  q("Why is the no-terminal-plateau hypothesis needed?", ["To make sure there is a support point to the right of a missing point", "For integrability"], 0,
    "A missing interval reaching up to 1 would have no right endpoint in the support (support_cofinal_of_no_terminal_plateau)."),
 ],
 caveats=["The curvature hypothesis is stated as `0 < (deriv^[2] q') t`: the second derivative of q′ (i.e. q‴) is positive, which makes q′ strictly convex."])

node(V + "no_positive_constant_gap", "No positive constant gap",
 "If q(a) = a, q(b) = b, q′(a), q′(b) ≤ 1 and q′ has positive second derivative on (a,b), that's impossible.",
 r"""## Plain English

**Theorem (`no_positive_constant_gap`, Support/Closure.lean lines 382–391).** For a < b: if q is continuous on [a,b] with
derivative q′ on (a,b), q′ is continuous on [a,b], q(a) = a, q(b) = b, q′(a) ≤ 1, q′(b) ≤ 1, and the second derivative of q′
is positive on (a,b), then **False**.

Positive second derivative makes q′ strictly convex, so on the open interval it is strictly below the larger endpoint value,
which is ≤ 1. Then q′ < 1 on (a,b), which contradicts the mean value theorem (average slope (b − a)/(b − a) = 1).
""",
 [q("What does the conclusion `False` mean here?", ["The hypotheses can't all hold", "q is zero"], 0, "It's a proof by contradiction lemma."),
  q("Which endpoint conditions are needed?", ["q′ ≤ 1 at both ends", "only at b"], 0, "Both `hda` and `hdb` are hypotheses."),
  q("Which classical theorem supplies the contradiction?", ["The mean value theorem", "Fubini"], 0, "`exists_hasDerivAt_eq_slope` in no_gap_of_derivative_lt_one."),
 ])

node(V + "no_zero_constant_gap", "No zero gap",
 "If q(a) = a, q(b) = b, q′(b) ≤ 1 and q′ is strictly increasing on (a,b), that's impossible.",
 r"""## Plain English

**Theorem (`no_zero_constant_gap`, Support/Closure.lean lines 393–405).** Same setting as
[no_positive_constant_gap](#/node/SupportDeterministic.Variation.no_positive_constant_gap), but with **positive first
derivative** of q′ on (a,b) and only the right-hand condition q′(b) ≤ 1. q′ is then strictly increasing, so q′ < q′(b) ≤ 1
inside, contradicting the mean value theorem.

This handles stretches where γ = 0, where the curvature argument for c > 0 doesn't apply.
""" + paper("Proposition 5.1", "“If c = 0, then q′ is strictly increasing on I.”"),
 [q("Which endpoint conditions on q′ are used?", ["Only q′(b) ≤ 1", "Both ends"], 0, "Only `hdb` appears."),
  q("What property of q′ is assumed?", ["Strictly increasing (positive derivative)", "Strictly convex"], 0, "`0 < deriv q' t` on (a,b)."),
  q("When does the main argument use this lemma?", ["When γ is 0 on the gap", "When γ is positive on the gap"], 0, "The c = 0 branch in the closure theorem."),
 ])

node(V + "contact_conditions", "Contact conditions from a nonnegative potential",
 "If the potential G(s) = ∫ₛ¹ (q − t) is ≥ 0, cannot be lowered by removing mass, and q has the right derivatives, then at each support point q(t) = t and q′(t) ≤ 1.",
 r"""## Plain English

**Theorem (`contact_conditions`, Support/Closure.lean lines 295–313).** Let G be continuous and nonnegative on [0,1), with
∫_K G dμ ≤ 0 for every compact K, q(0) = 0, q with right derivative q′ on [0,1), and G′(t) = t − q(t) on (0,1). Then every
support point t of μ has q(t) = t and q′(t) ≤ 1.

**Why.** G ≥ 0 and ∫_K G dμ ≤ 0 force G = 0 μ-almost everywhere, hence (G continuous) G = 0 on the support. A support
point in (0,1) is then a minimum of G, so G′(t) = t − q(t) = 0; and a second-order look at the minimum gives q′(t) ≤ 1.
At t = 0 the value q(0) = 0 is a hypothesis.
""" + paper("Lemma 6.2", "“Then G ≥ 0 on [0,1) and G = 0 on S. At every s ∈ S ∩ (0,1), q(s) = s, q′(s) ≤ 1.”"),
 [q("Where does G vanish?", ["On the support of μ", "Everywhere", "Nowhere"], 0, "zero_on_support_of_compact_mass_removal."),
  q("Why is q(t) = t at an interior support point?", ["It's a minimum of G and G′ = t − q", "By assumption"], 0, "value_contact_of_potential_min."),
  q("Is this lemma about SK specifically?", ["No, it is deterministic; minimizer_contact supplies the SK inputs", "Yes"], 0, "Its inputs are real functions and a measure."),
 ])

node(V + "derivative_eq_one_of_full_contact", "If q(t) = t everywhere, then q′ = 1",
 "If q(t) = t on [0,1) and q′ is its derivative (right derivative at 0), then q′(t) = 1 on [0,1).",
 r"""## Plain English

**Theorem (`derivative_eq_one_of_full_contact`, Support/Closure.lean lines 462–482).** If q agrees with the identity on
[0,1), q has derivative q′(t) at each t in (0,1), and right derivative q′(0) at 0, then q′(t) = 1 for every t in [0,1).
Derivatives are unique, and the identity function has derivative 1.

In Main.lean, q′ is [curvatureMoment](#/node/curvatureMoment), so this gives E[curvature(t, X_t)²] = 1.
""",
 [q("What extra care is needed at t = 0?", ["Use the right derivative, since q is only known on [0,1)", "None"], 0, "The hypothesis hd0 is a derivative within Ici 0."),
  q("Which conclusion of the headline does this give?", ["E[curvature²] = 1", "Full support"], 0, "q′ is the curvature moment."),
  q("Is any SK-specific fact used here?", ["No", "Yes"], 0, "Pure calculus."),
 ])

# ================================================================ contact from minimality
node("contactPotential", "contactPotential G(s) = ∫ₛ¹ (q(t) − t) dt",
 "G(s) is the integral from s to 1 of q(t) − t, where q(t) = E[gradient(t, X_t)²] along the constructed diffusion.",
 r"""## Plain English

**Definition (`contactPotential`, Support/ContactPotential.lean lines 18–19).** For s in [0,1],
G(s) = ∫ₛ¹ (q(t) − t) dt with """ + Q_ + r""" for the [constructed diffusion](#/node/diffusion).

This is the first variation of the Parisi functional in the direction "add mass at s": adding an atom at s raises γ by a
constant on [s,1), and to first order changes P by ½ G(s) (see [minimizer_variational_inequality](#/node/minimizer_variational_inequality)).
""" + paper("Section 1.2 and Lemma 6.2", "G(s) = ∫ₛ¹ (q(t) − t) dt, “nonnegative and vanishes on supp μγ.”"),
 [q("What is integrated?", ["q(t) − t", "γ(t)", "q′(t)"], 0, "`squareMoment W γ (diffusion W γ) t - t`."),
  q("Over which range?", ["From s to 1", "From 0 to s"], 0, "`∫ t in s..1`."),
  q("What is G′(s)?", ["s − q(s)", "q(s)"], 0, "Differentiating the lower limit; contactPotential_hasDerivAt."),
 ])

node("minimizer_variational_inequality", "First variation: a minimizer can't be improved in any direction",
 "If γ minimizes P, then for every order parameter β: ∫₀¹ (β − γ)(t)·(q(t) − t) dt ≥ 0.",
 r"""## Plain English

**Theorem (`minimizer_variational_inequality`, Support/VariationIntegrals.lean lines 170–175).** If γ
[is a minimizer](#/node/IsMinimizer), then for every [order parameter](#/node/OrderParameter) β,

∫₀¹ (β(t) − γ(t))·(q(t) − t) dt ≥ 0, with """ + Q_ + r""".

**Why.** Move from γ toward β along the segment γ + ε(β − γ). Every point of that segment is again an order parameter,
so it can't beat γ. Dividing the (nonnegative) change in P by ε and letting ε → 0 gives the derivative of P in that
direction, which the proof computes as ½ ∫ (β − γ)(q − t) (`parisi_chord_derivative`). That is the hard analytic step:
differentiating the value function with respect to the order parameter.
""" + paper("Lemma 6.1, (6.1)", "the right derivative at ε = 0 of P(γ + εη) equals ½ ∫₀¹ η(t)(q(t) − t) dt, for every η ∈ L¹(0,1) such that γ + εη ∈ U for all small ε ≥ 0 (paraphrase)."),
 [q("Which directions are compared?", ["Toward any other order parameter β", "Only small bumps"], 0, "β ranges over all OrderParameters."),
  q("Why stay inside order parameters along the way?", ["The segment between two order parameters consists of order parameters", "It doesn't"], 0, "Nonnegativity, monotonicity, right-continuity and integrability survive convex combinations."),
  q("How does this differ slightly from the paper's Lemma 6.1?", ["Lean uses chords toward another order parameter; the paper allows any admissible integrable direction", "No difference"], 0,
    "The Lean statement is the chord version, which is what the contact argument needs."),
 ])

node("contactPotential_nonneg", "G ≥ 0 at a minimizer",
 "If γ minimizes P then G(s) ≥ 0 for every s in [0,1): adding mass at s cannot lower P.",
 r"""## Plain English

**Theorem (`contactPotential_nonneg`, Support/ContactPotential.lean lines 57–62).** Apply the
[first variation](#/node/minimizer_variational_inequality) with β = γ plus an atom of mass 1 at s (so β − γ = 1 on [s,1)).
Then ∫ₛ¹ (q − t) ≥ 0, i.e. [G](#/node/contactPotential)(s) ≥ 0.
""" + paper("Lemma 6.2, proof", "“the direction η = 1[s,1) adds an atom to μ and is admissible. Minimality and Lemma 6.1 give G(s) ≥ 0.”"),
 [q("Which competitor β is used?", ["γ plus an atom at s", "γ minus an atom"], 0, "`γ.addCDF (Measure.dirac s)`."),
  q("What is β − γ?", ["1 on [s,1), 0 before", "γ"], 0, "Adding a unit atom at s raises the distribution function by 1 from s on."),
  q("Does this use minimality?", ["Yes", "No"], 0, "Through minimizer_variational_inequality."),
 ])

node("minimizer_contact", "Contact conditions for a minimizer",
 "If γ minimizes P and μ represents γ, then at every support point t: q(t) = t and E[curvature(t, X_t)²] ≤ 1.",
 r"""## Plain English

**Theorem (`minimizer_contact`, Support/ContactPotential.lean lines 80–92).** Feeds the SK facts into the deterministic
[contact_conditions](#/node/SupportDeterministic.Variation.contact_conditions):

- G is continuous and [nonnegative](#/node/contactPotential_nonneg);
- removing the mass of μ on a compact set can't lower P either, giving ∫_K G dμ ≤ 0
  (`contactPotential_compact_mass_removal`, again from the first variation);
- q(0) = 0 and q has derivative [curvatureMoment](#/node/curvatureMoment).

Conclusion: at each support point t, [squareMoment](#/node/squareMoment)(t) = t and curvatureMoment(t) ≤ 1.
""" + paper("Lemma 6.2", "(6.4): q(s) = s, q′(s) ≤ 1 at support points."),
 [q("Which two perturbations are used?", ["Adding an atom, and removing μ's mass on a compact set", "Only adding mass"], 0, "contactPotential_nonneg and contactPotential_compact_mass_removal."),
  q("Why remove mass only on compact sets?", ["μ may have infinite total mass near 1; on compacts it is finite", "No reason"], 0, "The paper restricts μ to compact K so the removed part is finite."),
  q("What is the curvature condition at a support point?", ["E[curvature²] ≤ 1", "= 1"], 0, "Equality comes only at the end, once full support is known."),
 ])

node("minimizer_no_terminal_plateau", "No terminal plateau",
 "A minimizer γ is not constant on any interval (a, 1) with 0 ≤ a < 1.",
 r"""## Plain English

**Theorem (`minimizer_no_terminal_plateau`, Support/NoTerminalPlateau.lean lines 53–78).** If γ is a minimizer, there are
no a in [0,1) and c ≥ 0 with γ = c on (a,1).

**Why.** If γ were constant near 1, a boundary-layer estimate (`terminal_plateau_q_lt_near_one`) shows q(t) < t for t close
to 1. Then G(s) = ∫ₛ¹ (q − t) < 0 for s close to 1, contradicting [G ≥ 0](#/node/contactPotential_nonneg).
""" + paper("Lemma 6.3", "“For a minimizer γ, there is no a < 1 and finite c ≥ 0 such that γ = c on (a,1).” The paper also credits Auffinger, Chen and Zeng [4, Remark 7] for the endpoint fact."),
 [q("Why is the end near 1 treated separately?", ["A gap reaching 1 has no right endpoint in the support, so the gap argument can't run", "It isn't"], 0,
    "The closure theorem needs a support point to the right of every missing point."),
  q("Does c = 0 count?", ["Yes, c ≥ 0", "No"], 0, "The statement says `0 ≤ c`."),
  q("What contradiction is reached?", ["G < 0 near 1, but G ≥ 0", "γ is negative"], 0, "The paper's (6.5): 1 − q(t) ≥ C√(1 − t)."),
 ])

# ================================================================ curvature on constant stretches
node("positive_gap_curvature", "Gap curvature: q′ strictly convex where γ = c > 0",
 "If γ = c > 0 on (a,b) ⊂ [0,1), then the second derivative of the curvature moment is positive on (a,b).",
 r"""## Plain English

**Theorem (`positive_gap_curvature`, Support/GapCurvature.lean lines 48–61).** If 0 ≤ a < b < 1, c > 0 and γ = c on (a,b),
then for every t in (a,b): (d/dt)² [curvatureMoment](#/node/curvatureMoment)(t) > 0, i.e. q‴(t) > 0, so q′ is strictly
convex there.

**Why.** On a constant stretch, the second derivative of q′ is computed explicitly as `stripThird … c t`, the expectation of
c⁻²·(z² − 12 v w² + 6 v⁴) in the paper's notation ([stripThird](#/node/stripThird)). Its positivity is
[stripThird_pos](#/node/stripThird_pos), which rests on the coercive identity. This is the heart of the paper.
""" + paper("Proposition 5.1", "“If c > 0, then q′ is strictly convex on I; more precisely … q‴(t) ≥ (1/(1000c²)) E v(t,X_t)⁴ > 0.”"),
 [q("What is positive?", ["The second derivative of q′ (= q‴)", "q′ itself"], 0, "`0 < (deriv^[2] (curvatureMoment W γ)) t`."),
  q("Is the constant c allowed to be 0 here?", ["No, c > 0; zero_gap_curvature handles 0", "Yes"], 0, "The hypothesis `hc0 : 0 < c`."),
  q("Does this assume anything about the support?", ["No", "Yes, full support"], 0, "Only that γ is constant on (a,b). The paper stresses this is unconditional."),
 ])

node("zero_gap_curvature", "Zero gaps: q′ strictly increasing where γ = 0",
 "If γ = 0 on (a,b), then the derivative of the curvature moment is positive on (a,b).",
 r"""## Plain English

**Theorem (`zero_gap_curvature`, Support/GapCurvature.lean lines 63–71).** If 0 ≤ a < b < 1 and γ = 0 on (a,b), then
q″(t) > 0 on (a,b). With γ = 0 there is no steering, the value function evolves by the heat equation, and q″ is the expected
square of the third x-derivative, which is positive (`stripSecond_zero_pos`).
""" + paper("Proposition 5.1 / Lemma 2.3", "“The assertion for c = 0 is the last part of Lemma 2.3; it is not obtained by dividing by c.”"),
 [q("What is positive here?", ["The derivative of q′", "The second derivative of q′"], 0, "`0 < deriv (curvatureMoment W γ) t`."),
  q("Why a separate argument for c = 0?", ["The c > 0 bound involves c and degenerates at 0", "It's the same"], 0, "The paper says it is not obtained by dividing by c."),
  q("Which deterministic lemma consumes this?", ["no_zero_constant_gap", "no_positive_constant_gap"], 0, "The c = 0 branch."),
 ])

node("stripThird", "stripThird: the explicit third derivative of q on a constant stretch",
 "On a stretch where γ = c, stripThird(c, t) = E[Φ⁗² − 12c·Φ″·Φ‴² + 6c²·Φ″⁴] along the diffusion (x-derivatives of the value).",
 r"""## Plain English

**Definition (`stripThird`, Moments/ThirdFields.lean lines 76–77).** Formally, the expectation along the strip drift of a
"third curvature field". What it equals is proved in `stripThird_eq_actual` (Moments/Curvature.lean lines 36–49): writing
Φ⁽ⁿ⁾ for the n-th x-derivative of the [value](#/node/value) at (t, X_t),

stripThird(c, t) = E[ (Φ⁽⁴⁾)² − 12c·Φ⁽²⁾·(Φ⁽³⁾)² + 6c²·(Φ⁽²⁾)⁴ ].

On a stretch where γ = c it is the derivative of q″ (`curvatureMoment_deriv_hasDerivAt_on_constant`). Multiplying by c²
gives the paper's E[z² − 12 v w² + 6 v⁴] with v = cΦ_xx, w = cΦ_xxx, z = cΦ_xxxx.
""" + paper("Section 1.2", "“q‴(t) = c⁻² E[z² − 12 v w² + 6 v⁴](t, X_t). The expression inside this expectation has a negative term and is not controlled pointwise by convexity of Φ alone.”"),
 [q("Which term can be negative?", ["−12c·Φ″·(Φ‴)²", "(Φ⁗)²", "6c²(Φ″)⁴"], 0, "Φ″ ≥ 0 by convexity, so the middle term is ≤ 0; the other two are squares."),
  q("Where is the identification with x-derivatives proved?", ["stripThird_eq_actual", "In the definition itself"], 0, "The definition goes through an auxiliary field; the lemma unpacks it."),
  q("Why is positivity hard?", ["Because of the negative middle term", "It isn't"], 0, "A pointwise bound fails; the coercive identity is needed."),
 ])

node("stripThird_pos", "q‴ > 0 on a positive constant stretch",
 "If γ is continuous at t > 0 with γ(t) > 0, then stripThird(γ(t), t) > 0.",
 r"""## Plain English

**Theorem (`stripThird_pos`, Moments/Curvature.lean lines 84–90).** Combines two facts:

- the **coercive bound** `stripThird_coercive`: (1/1000)·c⁴·E[(Φ″)⁴] ≤ c²·stripThird(c, t), with c = γ(t)
  (from [actual_coercivity](#/node/actual_coercivity));
- E[(Φ″)⁴] > 0 (`actualQuartic_pos`): the curvature isn't identically zero and the diffusion spreads over every interval.

Since c > 0, stripThird > 0.
""" + paper("Proposition 5.1", "(5.1): q‴(t) ≥ (1/(1000c²)) E v(t,X_t)⁴ > 0."),
 [q("Where does the constant 1/1000 come from?", ["The coercive identity's remainder, 1661507/1521000000 > 1/1000", "It's arbitrary"], 0, "Certificate.coercivity_constant."),
  q("Why is E[(Φ″)⁴] positive?", ["Φ″ is not identically zero and X_t charges every interval", "By assumption"], 0, "actualQuartic_pos."),
  q("Is continuity of γ at t needed?", ["Yes, as a hypothesis (automatic inside a constant stretch)", "No"], 0, "`hcont : ContinuousAt γ.val t`; GapCurvature supplies it."),
 ])

node("actual_coercivity", "The coercive inequality for the true value function",
 "(1/1000)·E[c⁴(Φ″)⁴] ≤ E[c²(Φ⁗)² − 12c³Φ″(Φ‴)² + 6c⁴(Φ″)⁴] at time t, with c = γ(t), for any t > 0 where γ is continuous.",
 r"""## Plain English

**Theorem (`actual_coercivity`, Density/SampleJets.lean lines 135–143).** For t > 0 with γ continuous at t, and c = γ(t),

(1/1000)·E[c⁴·(Φ″)⁴] ≤ E[ [coerciveJetPolynomial](#/node/coerciveJetPolynomial)(c, Φ″, Φ‴, Φ⁗) ],

all evaluated at (t, X_t) ([actualJet](#/node/actualJet)).

**Why.** First prove it for smooth, positive, finite-step coefficients with a smoothed terminal condition
(`sample_coercivity`, via `Heat.finite_feedback_coercivity`): there, backward shape inequalities for the value, forward
inequalities for the density of X, and the exact [rational identity](#/node/Certificate.rational_identity) plus one
integration by parts give the bound. Then pass to the limit along approximations of γ: both sides converge, and the
inequality survives.
""" + paper("Sections 3–5", "finite-step shape inequalities (Section 3), the exact coercive identity and its integrated form (Section 4, Lemma 4.1 and Proposition 4.2), and the transfer to arbitrary integrable coefficients (Section 5)."),
 [q("How is the inequality obtained for general γ?", ["Proved for smooth finite-step approximations, then a limit", "Directly"], 0, "le_of_tendsto_of_tendsto with sample_coercivity."),
  q("Is any convergence of the auxiliary density scores needed?", ["No, only the two integrals converge", "Yes"], 0, "The paper stresses only the integrated inequality is transferred."),
  q("What is c?", ["γ(t)", "1"], 0, "`γ.val t`."),
 ])

node("coerciveJetPolynomial", "The coercive polynomial c²C² − 12c³AB² + 6c⁴A⁴",
 "coerciveJetPolynomial(c, A, B, C) = c²C² − 12c³AB² + 6c⁴A⁴; with A, B, C the 2nd, 3rd, 4th x-derivatives it is c² times the integrand of q‴.",
 r"""## Plain English

**Definition (`coerciveJetPolynomial`, Density/CoerciveMoments.lean line 15).** A polynomial in four real numbers:
c²·C² − 12·c³·A·B² + 6·c⁴·A⁴. With v = cA, w = cB, z = cC this is z² − 12 v w² + 6 v⁴, the paper's integrand.
""",
 [q("With v = cA, w = cB, z = cC, what is it?", ["z² − 12vw² + 6v⁴", "z² + v⁴"], 0, "Expand: c²C² − 12c³AB² + 6c⁴A⁴."),
  q("Is it always nonnegative pointwise?", ["No, the middle term can win", "Yes"], 0, "That's why the coercive identity is needed."),
  q("Which A is used in the theorem?", ["The second x-derivative of the value", "The value itself"], 0, "actualJet 2."),
 ])

node("actualJet", "actualJet: x-derivatives of the value along the diffusion",
 "actualJet(t, m, ω) is the m-th x-derivative of value(t, ·) evaluated at the diffusion's position X_t(ω).",
 r"""## Plain English

**Definition (`actualJet`, Density/SampleJets.lean lines 32–33).** `iteratedDeriv m (value W γ t)` at the point
`diffusion W γ t ω`. So m = 1 is the [gradient](#/node/gradient), m = 2 the [curvature](#/node/curvature), and m = 3, 4 the
next two x-derivatives, all at (t, X_t).
""",
 [q("What is actualJet with m = 2?", ["The curvature at (t, X_t)", "The gradient"], 0, "Second x-derivative of the value."),
  q("At which position?", ["The constructed diffusion's position at time t", "x = 0"], 0, "`diffusion W γ … ξ`."),
  q("Is it random?", ["Yes, it depends on the sample ω", "No"], 0, "It's evaluated at X_t(ω)."),
 ])

node("Certificate.rational_identity", "The exact rational identity",
 "An algebraic identity, proved by `ring`, expressing z² − 12Rvb² + 6v⁴ as a sum of squares, sign-controlled terms, a derivative "
 "correction and an explicit remainder whose v⁴ coefficient is 1661507/1521000000 > 1/1000.",
 r"""## Plain English

**Theorem (`rational_identity`, Density/Certificate.lean lines 62–69).** For all real numbers R, K, v, b, j, z, L,

z² − 12·R·v·b² + 6·v⁴ = (z + Q)² + (z + bv − 2Rb)·T + (weighted squares) + WF₂ + L·(x₀v² + hbv) + (remainder),

where Q, T, the weighted squares P₀…P₄, the correction WF₂ and the remainder are explicit polynomials with rational
coefficients defined at the top of the file (Density/Certificate.lean lines 10–60). The source proves it with Lean's `ring` tactic:
pure algebra, no numerical approximation. (This site did not build the Lean; see [Trust](#/trust).)

`pointwise_coercivity` (lines 107–122) then uses the sign information that the shape inequalities provide
(R, K, v, j, L ≥ 0, b ≥ 2v, z + bv − 2Rb ≥ 0) to drop the nonnegative terms and keep (1661507/1521000000)·v⁴ + WF₂.
After weighting by the density of X and integrating in x, the WF₂ term is the derivative of a flux that vanishes at ±∞
(`integrated_coercivity_of_flux`, lines 165–194), so it integrates to zero, leaving the coercive bound.
""" + paper("Section 1.2, summarizing Lemma 4.1 (4.11) and Proposition 4.2", "“an exact rational polynomial identity [that is] nonnegative after one spatial integration by parts, retaining the lower bound 10⁻³ E v⁴.”"),
 [q("How does the Lean source prove the identity?", ["`ring`: symbolic algebra", "`native_decide`", "numerically"], 0, "Density/Certificate.lean line 69."),
  q("Which coefficient gives the final constant?", ["1661507/1521000000 on v⁴, which exceeds 1/1000", "1/2"], 0, "coercivity_constant (line 124) checks it by `norm_num`."),
  q("Are the sign conditions part of the identity?", ["No, the identity holds for all reals; signs are used afterwards", "Yes"], 0, "The identity is unconditional; pointwise_coercivity adds hypotheses."),
 ],
 caveats=["This node summarizes the shape of the identity; the exact polynomials are in the source and are not retyped here."])

# ================================================================ measure and diffusion
node("parameterMeasure", "parameterMeasure: the measure built from γ",
 "The Stieltjes measure of γ (on the increments of γ) plus an atom of mass γ(0) at 0.",
 r"""## Plain English

**Definition (`parameterMeasure`, Support/GapCurvature.lean lines 109–110).** Mathlib turns the monotone right-continuous
function γ into a Stieltjes measure that gives (a, b] mass γ(b) − γ(a). That measure gives [0,t] mass γ(t) − γ(0), so the
definition adds an atom of size γ(0) at 0. The sum has μ([0,t]) = γ(t) ([parameterMeasure_isStieltjes](#/node/parameterMeasure_isStieltjes)).
""" + paper("page 1", "“µγ([0,t]) = γ(t), 0 ≤ t < 1. In particular µγ({0}) = γ(0).”"),
 [q("Why add an atom at 0?", ["Mathlib's Stieltjes measure only records increments, missing γ(0)", "For normalization"], 0, "Its mass on [0,t] is γ(t) − γ(0)."),
  q("What is the mass of the atom?", ["γ(0)", "1"], 0, "`ENNReal.ofReal (γ.val ⊥) • Measure.dirac ⊥`, and ⊥ = 0."),
  q("Does this prove a representing measure exists?", ["Yes, with parameterMeasure_isStieltjes", "No"], 0, "That is part 1 of the conclusion."),
 ])

node("parameterMeasure_isStieltjes", "parameterMeasure represents γ",
 "parameterMeasure γ gives every [0,t] mass γ(t).",
 r"""## Plain English

**Theorem (`parameterMeasure_isStieltjes`, Support/GapCurvature.lean lines 112–119).** `IsStieltjesMeasure γ (parameterMeasure γ)`:
the measure [built from γ](#/node/parameterMeasure) has μ([0,t]) = (γ(t) − γ(0)) + γ(0) = γ(t). This gives part 1 of the
[conclusion](#/node/FullSupportConclusion).
""",
 [q("Which part of the conclusion does it supply?", ["Existence of a representing measure", "Full support"], 0, "Used in full_support, Main.lean line 39."),
  q("What two masses add up to γ(t)?", ["γ(t) − γ(0) from the Stieltjes part and γ(0) from the atom", "γ(t) and 0"], 0, "The final `sub_add_cancel`."),
  q("Does it use minimality?", ["No, any order parameter has one", "Yes"], 0, "It's a general construction."),
 ])

node("diffusion", "diffusion: the constructed optimally steered path",
 "X_t = B_t + ∫₀ᵗ γ(s)·g(s, X̃_s) ds, where g is the gradient (|g| ≤ 1, set to 0 from time 1 on) along an auxiliary strip-by-strip solution X̃.",
 r"""## Plain English

**Definition (`diffusion`, Diffusion/CompactDrift.lean lines 275–276).** The process the proof builds:

diffusion(t) = driver(t) + ∫₀ᵗ γ(s)·rawFeedback(s) ds,

where `driver` is a progressively measurable version of the Brownian motion that starts at 0 on every path and equals B almost surely,
and `rawFeedback(s)` is the [gradient](#/node/gradient) at (s, X̃_s) for an auxiliary solution X̃ (`rawDiffusion`), built by
Picard iteration on compact time strips [0, T], T < 1 (set to 0 from time 1 on; the gradient is proved to satisfy |gradient| ≤ 1).
[diffusion_isDiffusion](#/node/diffusion_isDiffusion) shows it satisfies [IsDiffusion](#/node/IsDiffusion).
""" + paper("page 2, citing Lemma 2.2", "the drift is bounded and Lipschitz in space on every compact time strip, so (1.5) “has a unique strong solution up to time one, as proved in Lemma 2.2.”"),
 [q("What is `driver`?", ["A progressively measurable version of B, equal to B almost surely", "A different Brownian motion"], 0, "driver_progressive and driver_indistinguishable (Diffusion/ProgressiveBrownian.lean lines 93–110)."),
  q("How is the solution built?", ["Picard iteration on compact strips [0,T] with T < 1", "Euler scheme only"], 0, "Diffusion/PicardDiffusion.lean and CompactDrift.lean."),
  q("Why is the drift integrable even though γ may blow up near 1?", ["|gradient| ≤ 1 and γ is integrable", "It isn't"], 0, "rawDrift_integrable uses `γ.integrable.mul_bdd`."),
 ])

node("diffusion_isDiffusion", "The constructed path is a diffusion",
 "`IsDiffusion W γ (diffusion W γ)`: progressive, almost surely continuous, starting at 0, and solving the integral equation.",
 r"""## Plain English

**Theorem (`diffusion_isDiffusion`, Diffusion/CompactDrift.lean lines 309–327).** Checks each clause of [IsDiffusion](#/node/IsDiffusion)
for the [constructed diffusion](#/node/diffusion): progressive measurability; and almost surely, continuity on [0,1],
X₀ = 0, and X_t = B_t + ∫₀ᵗ γ(s)·gradient(s, X_s) ds. The integrands agree because the feedback equals the gradient at the
diffusion's own position for s < 1, and γ's zero extension vanishes at s = 1.
""",
 [q("Which part of the conclusion does this give?", ["Existence of a diffusion", "Uniqueness"], 0, "Part 2 of FullSupportConclusion."),
  q("What happens at s = 1?", ["extend γ 1 = 0, so the integrand is 0 there anyway", "Nothing special"], 0, "The last case of the proof."),
  q("Is the constructed X simply B?", ["Not in general: X = B + ∫ γ·feedback, which reduces to B only if that drift vanishes (e.g. γ = 0)", "Yes, always"], 0, "The drift is part of X; it is zero only when γ times the feedback integrates to 0."),
 ])

node("diffusion_uniqueness", "Uniqueness: every diffusion equals the constructed one",
 "If X is any diffusion for W and γ, then almost surely X_t = diffusion(t) for all t ≤ 1.",
 r"""## Plain English

**Theorem (`diffusion_uniqueness`, Diffusion/Uniqueness.lean lines 13–63).** Any X with [IsDiffusion](#/node/IsDiffusion) W γ X
agrees with the [constructed diffusion](#/node/diffusion), on one almost-sure event, at every time t ≤ 1. On each strip [0,T]
with T < 1 the drift is bounded and Lipschitz in space, so the Picard solution is unique there; at t = 1 both processes satisfy the same integral equation, whose integrand agrees with the constructed one for s < 1 (and vanishes at s = 1).

This is what lets [full_support](#/node/full_support) state the moment identities for **every** diffusion.
""" + paper("Lemma 2.2", "(2.10) “has a unique strong solution on [0,1].”"),
 [q("What does uniqueness give the headline theorem?", ["The identities for every diffusion, not just the constructed one", "Full support"], 0, "Main.lean lines 44–59."),
  q("Why do the moments then agree?", ["The two processes are a.s. equal at time t, so the integrals agree", "By symmetry"], 0, "integral_congr_ae."),
  q("Is uniqueness assumed anywhere?", ["No, it's proved", "Yes"], 0, "It's a theorem in Diffusion/Uniqueness.lean."),
 ])

node("curvatureMoment", "curvatureMoment: E[curvature(t, X_t)²] (the paper's q′)",
 "curvatureMoment(t) is the expectation of curvature² at (t, X_t) along the constructed diffusion.",
 r"""## Plain English

**Definition (`curvatureMoment`, Moments/StripSquareMoment.lean lines 112–113).** E[[curvature](#/node/curvature)(t, X_t)²] for
the [constructed diffusion](#/node/diffusion). It is the derivative of q(t) = E[gradient²]
([squareMoment_hasDerivAt](#/node/squareMoment_hasDerivAt)), which is why the proof calls it q′.
""" + paper("Section 1.2", "“The gradient-martingale identity gives q′(t) = E Φγ,xx(t,X_t)².”"),
 [q("Which diffusion does it use?", ["The constructed one", "Any"], 0, "`diffusion W γ`."),
  q("What is it the derivative of?", ["q(t) = E[gradient²]", "γ"], 0, "squareMoment_hasDerivAt."),
  q("Is it the same integral as in the headline's last clause?", ["Yes, for the constructed diffusion", "No"], 0, "Model.lean line 88 has the same integrand for a general X."),
 ])

node("squareMoment_eq_integral_curvatureMoment", "q(t) = ∫₀ᵗ q′",
 "For 0 ≤ t < 1: E[gradient(t, X_t)²] = ∫₀ᵗ E[curvature(s, X_s)²] ds.",
 r"""## Plain English

**Theorem (`squareMoment_eq_integral_curvatureMoment`, Moments/StripSquareMoment.lean lines 136–144).** Along the
constructed diffusion, the square moment of the gradient is the integral of the
[curvature moment](#/node/curvatureMoment) from 0 to t. In stochastic terms: the gradient along the optimal path is a
martingale whose quadratic variation grows at rate curvature², so (by Itô's isometry) E[u²] accumulates E[Φ_xx²]. In
particular q(0) = 0.
""" + paper("Lemma 2.2", "the square-martingale identity."),
 [q("What is q(0)?", ["0", "1"], 0, "The integral from 0 to 0 vanishes (squareMoment_zero)."),
  q("Which object is integrated?", ["curvatureMoment", "γ"], 0, "`∫ s in 0..t, curvatureMoment W γ s`."),
  q("For which t?", ["0 ≤ t < 1", "all t"], 0, "Hypotheses ht0, ht1."),
 ])

node("squareMoment_hasDerivAt", "q′ = E[curvature²]",
 "For 0 < t < 1, q(t) = E[gradient(t, X_t)²] has derivative curvatureMoment(t) at t.",
 r"""## Plain English

**Theorem (`squareMoment_hasDerivAt`, Moments/PerturbationLimits.lean lines 154–157).** Differentiating
[q(t) = ∫₀ᵗ q′](#/node/squareMoment_eq_integral_curvatureMoment), with the integrand continuous: q has derivative
[curvatureMoment](#/node/curvatureMoment)(t) at every t in (0,1) (and a right derivative at 0, `squareMoment_hasDerivWithinAt`).
""",
 [q("Why is the derivative the curvature moment?", ["Fundamental theorem of calculus applied to q = ∫ q′", "By definition"], 0, "With continuity of curvatureMoment."),
  q("What happens at t = 0?", ["Only a right derivative", "Two-sided derivative"], 0, "squareMoment_hasDerivWithinAt on Ici 0."),
  q("Which closure hypothesis does this provide?", ["q′ is the derivative of q", "contact"], 0, "Main.lean line 26."),
 ])

# ================================================================ small leaves (so the spine's mentions are explained)
node("quarticJetPolynomial", "quarticJetPolynomial c⁴A⁴",
 "quarticJetPolynomial(c, A) = c⁴·A⁴; with A = Φ″ it is v⁴ for v = cΦ_xx.",
 r"""## Plain English

**Definition (`quarticJetPolynomial`, Density/CoerciveMoments.lean line 17).** c⁴·A⁴. Its expectation is the lower
bound in the [coercive inequality](#/node/actual_coercivity): E[v⁴] with v = cΦ_xx.
""",
 [q("What is quarticJetPolynomial(2, 1)?", ["16", "8", "2"], 0, "2⁴·1⁴ = 16."),
  q("Can it be negative?", ["No, it's a fourth power", "Yes"], 0, "c⁴A⁴ = (cA)⁴ ≥ 0."),
  q("Which paper quantity is it?", ["v⁴", "z²"], 0, "v = cΦ_xx."),
 ])

node("BrownianSystem.driver", "driver: a progressive version of B",
 "driver(t) = V(t) − V(0) for a progressively measurable version V of B; it starts at 0 on every path and equals B almost surely.",
 r"""## Plain English

**Definition (`BrownianSystem.driver`, Diffusion/ProgressiveBrownian.lean lines 93–94).** The structure
[BrownianSystem](#/node/BrownianSystem) only says B is measurable at each time. To integrate along paths the proof needs a
version that is progressively measurable; `progressiveVersion` is built as a limit of left-endpoint discretizations, and
`driver` subtracts its value at 0. Lemmas show `driver` is progressive, is 0 at time 0 on every path, and equals B at all
times almost surely (`driver_indistinguishable`).
""",
 [q("Is driver equal to B?", ["Almost surely, at all times simultaneously", "Only at t = 0", "Never"], 0, "driver_indistinguishable."),
  q("Why not use B directly?", ["B is not assumed progressively measurable", "B is wrong"], 0, "Only per-time measurability is in the structure."),
  q("What is driver at time 0?", ["0 on every path", "B₀"], 0, "driver_zero: V(0) − V(0)."),
 ])

node("rawFeedback", "rawFeedback: the drift's feedback term",
 "rawFeedback(t) is the gradient at (t, X̃_t) for t < 1 and 0 for t ≥ 1, where X̃ is the strip-by-strip solution.",
 r"""## Plain English

**Definition (`rawFeedback`, Diffusion/CompactDrift.lean lines 251–252).** `beforeOneGradient` evaluated at the auxiliary
solution `rawDiffusion` (a limit of Picard solutions on growing strips [0, Tₙ], Tₙ → 1): the [gradient](#/node/gradient)
for times before 1, and 0 from time 1 on. It is bounded by 1 in absolute value (`rawFeedback_bound`, from
`gradient_abs_le_one`) and progressively measurable.
""",
 [q("What is rawFeedback at time 1?", ["0", "the gradient at 1"], 0, "beforeOneGradient is 0 when t ≥ 1."),
  q("What bound does it satisfy?", ["|rawFeedback| ≤ 1", "none"], 0, "rawFeedback_bound."),
  q("Where is it used?", ["In the drift of the constructed diffusion", "In the Parisi functional"], 0, "See [diffusion](#/node/diffusion)."),
 ])

node("parameterStieltjes", "parameterStieltjes: γ as a Mathlib Stieltjes function",
 "Packages γ (monotone and right-continuous on Time) as a Mathlib `StieltjesFunction` on Time.",
 r"""## Plain English

**Definition (`parameterStieltjes`, Support/GapCurvature.lean lines 96–99).** Mathlib's `StieltjesFunction` is a
monotone right-continuous function; it comes with a measure giving (a, b] mass f(b) − f(a). The fields of an
[order parameter](#/node/OrderParameter) are exactly what is needed. [parameterMeasure](#/node/parameterMeasure) uses it.
""",
 [q("Which two properties does a Stieltjes function need?", ["Monotone and right-continuous", "Smooth and bounded"], 0, "`mono'` and `right_continuous'`."),
  q("What mass does its measure give (a, b]?", ["γ(b) − γ(a)", "γ(b)"], 0, "Standard Stieltjes measure."),
  q("Does it see γ(0) by itself?", ["No, hence the atom added in parameterMeasure", "Yes"], 0, "Only increments are recorded."),
 ])
