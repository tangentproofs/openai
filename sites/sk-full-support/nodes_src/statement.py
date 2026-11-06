# The headline theorem and the 16 definitions its statement uses (the "Start here" set).
# Lean ground truth: lean/OAI/Probability/SKSupport/Model.lean (lines 12-88 are character-for-character the
# same as lean/ComparatorChallenges/SKFullSupport.lean lines 12-88) and .../SKSupport/Main.lean.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_adder, q, paper, PAPER

NODES = []
node = node_adder(NODES)

SAME = "The same text is the Comparator target, ComparatorChallenges/SKFullSupport.lean lines {}."

# ---------------------------------------------------------------- headline
node("full_support",
 "Headline: every minimizer has full support (Theorem 1.1)",
 "If γ **minimizes** the Parisi functional, its Stieltjes measure has support all of [0,1), γ strictly increases, "
 "and along every diffusion E[gradient²] = t and E[curvature²] = 1. A minimizer is assumed, not shown to exist.",
 r"""## Plain English

**Theorem (`full_support`, Main.lean lines 35–59).** For every sample space Ω with a
[Brownian system](#/node/BrownianSystem) `W`, and every [order parameter](#/node/OrderParameter) `γ`:
if `γ` [is a minimizer](#/node/IsMinimizer) of the [Parisi functional](#/node/parisi), then the
[five-part conclusion](#/node/FullSupportConclusion) holds:

1. some measure on [0,1) [represents γ](#/node/IsStieltjesMeasure) (its mass on [0,t] is γ(t));
2. some random path `X` [is a diffusion](#/node/IsDiffusion) for `W` and `γ` (the optimally steered path);
3. **every** such representing measure has **support equal to all of [0,1)**: no overlap scale below one is missing;
4. γ is **strictly** increasing on [0,1): `a < b` gives `γ(a) < γ(b)`;
5. for **every** such diffusion `X` and every time `t` in [0,1), the expected square of the
   [gradient](#/node/gradient) at `(t, X_t)` equals `t` ([squareMoment](#/node/squareMoment)), and the expected
   square of the [curvature](#/node/curvature) at `(t, X_t)` equals `1`.

That is the paper's **Theorem 1.1**, stated with the paper's normalization ξ(t) = t²/2, for the pure
Sherrington–Kirkpatrick model with **no external field**.

The same statement, with the proof replaced by a deliberate `sorry`, is the Comparator challenge in
ComparatorChallenges/SKFullSupport.lean lines 90–92: that file is the *target* a solution must match. The proof
shown here is OpenAI's own, in `Main.lean`, published in the same repository at the same commit.
""" + paper("page 2, Theorem 1.1",
 "“If γ ∈ U minimizes P, then supp μ<sub>γ</sub> = [0,1). In particular γ(b) > γ(a) whenever 0 ≤ a < b < 1. "
 "For the solution of (1.5), E[u<sub>γ</sub>(t,X<sub>t</sub>)²] = t, E[Φ<sub>γ,xx</sub>(t,X<sub>t</sub>)²] = 1, 0 ≤ t < 1.” "
 "The paper also notes that Chen [7, Theorem 1.3] proves the same full-relative-support conclusion by a different route.") + r"""
**How the proof goes.** `full_support` is a short wrapper (see the walkthrough below). The real work is in
[minimizer_full_support_actual](#/node/minimizer_full_support_actual), which proves support, strict monotonicity and
both moment identities for one particular measure and one particular diffusion that the proof builds. `full_support`
then transfers the moment identities to *any* diffusion using
[uniqueness of the diffusion](#/node/diffusion_uniqueness). The [Roadmap](#/roadmap) gives the whole plan.
""",
 [q("What does `full_support` assume about γ?",
    ["That γ minimizes the Parisi functional over all order parameters",
     "That γ already has full support",
     "That γ is smooth with γ(0) = 0",
     "Nothing: it proves a minimizer exists and has full support"], 0,
    "The only hypothesis is `hmin : IsMinimizer W γ` (Main.lean line 36). Full support is the conclusion, and existence of a minimizer is not proved here."),
  q("Which interval is the support claimed to equal?",
    ["[0,1), with its own (relative) topology", "[0,1]", "(0,1)", "the whole real line"], 0,
    "`Time` is the subtype `Set.Ico 0 1`, i.e. [0,1), and `μ.support = Set.univ` means all of `Time` (Model.lean line 84)."),
  q("Does the theorem say the moment identities hold for one particular diffusion, or for all of them?",
    ["For every X satisfying IsDiffusion W γ X (and at least one such X exists)",
     "Only for the diffusion the proof constructs",
     "For every random process X whatsoever",
     "Only at t = 0"], 0,
    "Part 2 says a diffusion exists; part 5 quantifies over every `X` with `IsDiffusion W γ X` (Model.lean lines 83 and 86–88)."),
  q("Which model does this cover?",
    ["The pure SK model with no external field, ξ(t) = t²/2",
     "Any mixed p-spin model",
     "SK with an arbitrary external field h",
     "The SK model at positive temperature"], 0,
    "The paper fixes ξ(t)=t²/2 and zero field, and says neither a nonzero-field nor a mixed-spin extension is implied (p. 2)."),
  q("What is the role of the file ComparatorChallenges/SKFullSupport.lean?",
    ["It is the target statement (ending in `sorry`) that a proof must match",
     "It is the proof",
     "It is an unrelated benchmark",
     "It adds extra axioms"], 0,
    "The challenge file states the theorem with `sorry` as a placeholder; its JSON names `OAI.Probability.SKSupport.Main` as the solution module."),
 ],
 caveats=[
   "**Conditional on a minimizer.** The theorem assumes `IsMinimizer W γ`. Nothing in this Lean development proves that a minimizer exists; the paper takes existence from Auffinger and Chen (its (1.4)). If the Lean functional had no minimizer, the theorem would be true but empty.",
   "Support is relative to [0,1); the theorem says nothing about the point 1. The representing measure need not be a probability measure and may have infinite total mass near 1.",
   "The paper's further results (smooth positive density γ′ > 0, γ(0) = 0, Section 7 consequences) are **not** part of this Lean statement.",
   "The Lean `gradient` and `curvature` are built from `deriv`, which returns 0 where a function is not differentiable. The theorem's moment identities are about these Lean functions; the proof has to establish the real differentiability, and nothing here assumes it.",
 ],
 widgets=[{"type": "walkthrough", "title": "How full_support is proved (Main.lean, lines 35-59)",
   "config": {"steps": [
     {"text": "Take the measure the proof builds from γ (parameterMeasure γ) and its proof that it represents γ.",
      "link": "parameterMeasure_isStieltjes", "lean": "have hμ := parameterMeasure_isStieltjes γ"},
     {"text": "Apply the main lemma to it: full support, strict monotonicity and the two moment identities for the constructed diffusion.",
      "link": "minimizer_full_support_actual", "lean": "have hs := minimizer_full_support_actual W γ hmin hμ"},
     {"text": "Parts 1–3: the measure exists, the constructed diffusion W γ is a diffusion, and every representing measure has full support (the main lemma works for any representing μ).",
      "link": "diffusion_isDiffusion", "lean": "fun μ hμ => (minimizer_full_support_actual W γ hmin hμ).1,?_,?_⟩"},
     {"text": "Part 4: strict monotonicity of the zero-extension on [0,1) gives strict monotonicity of γ on the subtype.",
      "lean": "simpa only [extend,dite_eq_left a.property,dite_eq_left b.property] using hh"},
     {"text": "Part 5: any other diffusion X agrees almost surely with the constructed one up to time 1 (uniqueness).",
      "link": "diffusion_uniqueness", "lean": "filter_upwards [diffusion_uniqueness W γ hX] with ξ hξ"},
     {"text": "So the two expectations agree (integrals of almost-everywhere-equal functions), and the identities proved for the constructed diffusion hold for X.",
      "lean": "apply integral_congr_ae"},
   ]}}])

# ---------------------------------------------------------------- definitions (Model.lean)
node("Time",
 "Time: the overlap interval [0,1)",
 "`Time` is the set of real numbers t with 0 ≤ t < 1, used as a type. Zero is in it, one is not; all support statements use this space's own topology.",
 r"""## Plain English

**Definition (`Time`, Model.lean line 12).** `Time` is the subtype of real numbers `t` with `0 ≤ t < 1`
(Mathlib's `Set.Ico 0 1`). Zero is included; one is excluded.

The order parameter γ lives on `Time`, and the measures in the theorem are measures on `Time`. So "full support"
is relative to [0,1): neighbourhoods of 0 are taken inside [0,1), and the point t = 1 is simply not in the space.
""" + paper("page 1", "γ is a function on [0,1), and “all support statements below use the relative topology of [0,1).”")
 + "\n" + SAME.format("line 12") + "\n",
 [q("Is t = 1 an element of `Time`?", ["No", "Yes", "Only for some γ"], 0,
    "`Set.Ico 0 1` is the half-open interval [0,1): it excludes 1 (Model.lean line 12)."),
  q("Is t = 0 an element of `Time`?", ["Yes", "No"], 0, "`Ico` is closed on the left, so 0 ∈ [0,1)."),
  q("When the theorem says a measure has support all of `Time`, what does that say about the point 1?",
    ["Nothing: 1 is not in the space", "That the measure has an atom at 1", "That the measure is zero near 1"], 0,
    "The support is a subset of `Time` = [0,1), so the statement is silent about 1."),
 ])

node("extend",
 "extend: a function on [0,1), extended by zero to the real line",
 "`extend γ t` is γ(t) when 0 ≤ t < 1 and 0 otherwise. It lets Lean integrate γ over real intervals.",
 r"""## Plain English

**Definition (`extend`, Model.lean lines 14–15).** Given a function `γ` on [Time](#/node/Time), `extend γ` is the
function on all real numbers that equals `γ t` for `t` in [0,1) and `0` everywhere else.

This is bookkeeping: Lean's real integrals `∫ s in a..b, f s` want a function defined on all reals. In particular
`extend γ 1 = 0`. That is a convention for integration, not a claim about a limit of γ at 1 (γ may even blow up near 1).
""" + paper("page 1", "γ is defined on [0,1) and required to satisfy ∫₀¹ γ(t) dt < ∞; the zero extension is Lean bookkeeping and has no separate name in the paper.")
 + "\n" + SAME.format("lines 14–15") + "\n",
 [q("What is `extend γ 2`?", ["0", "γ(1)", "undefined", "the limit of γ at 1"], 0,
    "2 is outside [0,1), so the `else` branch gives 0 (Model.lean line 15)."),
  q("What is `extend γ 0.5`?", ["γ(0.5)", "0", "0.5"], 0, "0.5 ∈ [0,1), so the value is γ at that point."),
  q("Does `extend γ 1 = 0` say that γ tends to 0 near 1?", ["No, it's only the value of the extension at 1", "Yes"], 0,
    "The extension is 0 at 1 by definition; γ itself is only defined on [0,1) and can grow without bound there."),
 ])

node("OrderParameter",
 "OrderParameter: an admissible γ",
 "An order parameter is a function γ on [0,1) that is nonnegative, nondecreasing, right-continuous, and integrable "
 "(after zero extension). It may grow without bound near 1, and flat stretches are allowed by this definition.",
 r"""## Plain English

**Structure (`OrderParameter`, Model.lean lines 17–22).** An order parameter bundles a real function `val` on
[Time](#/node/Time) with four facts:

- `nonneg`: `0 ≤ γ(t)` for every t;
- `monotone`: γ is nondecreasing (s ≤ t gives γ(s) ≤ γ(t));
- `right_continuous`: at every t, γ is continuous from the right;
- `integrable`: its [zero extension](#/node/extend) is integrable on the real line, i.e. ∫₀¹ γ < ∞.

Monotone allows constant stretches ("plateaus" or "gaps" in the support). Ruling those out for a minimizer is what
the theorem proves; it is **not** built into this definition.
""" + paper("page 1", "“Let U be the set of nonnegative, nondecreasing, right-continuous functions γ : [0,1) → [0,∞) satisfying ∫₀¹ γ(t) dt < ∞.”")
 + "\n" + SAME.format("lines 17–22") + "\n",
 [q("Can an order parameter be constant on an interval?", ["Yes, the definition allows it", "No, it must be strictly increasing"], 0,
    "`monotone` only asks for nondecreasing. Strict increase is part of the theorem's conclusion, for minimizers."),
  q("Must an order parameter be bounded?", ["No: only ∫₀¹ γ < ∞ is required", "Yes, by 1", "Yes, by some constant"], 0,
    "The only size condition is `integrable` (Model.lean line 22), so γ can blow up near 1 as long as its integral is finite."),
  q("Which continuity condition is required?", ["Continuity from the right at every point", "Continuity everywhere", "None"], 0,
    "`right_continuous : ∀ t, ContinuousWithinAt val (Set.Ici t) t` (Model.lean line 21)."),
  q("Is this the same class as the paper's set U?", ["Yes, the same four conditions", "No, Lean adds a smoothness condition", "No, Lean drops integrability"], 0,
    "The four fields match the paper's definition of U on page 1."),
 ])

node("BrownianSystem",
 "BrownianSystem: the randomness",
 "A Brownian system is a probability space with a measurable standard real Brownian motion B indexed by times t ≥ 0.",
 r"""## Plain English

**Structure (`BrownianSystem`, Model.lean lines 24–29).** For a sample space `Ω`, a Brownian system `W` consists of

- `law`: a measure on Ω, which is a probability measure (`isProbability`);
- `B`: a real-valued process indexed by nonnegative reals (`ℝ≥0`);
- `measurable`: each `B t` is a measurable function of the sample;
- `brownian`: `B` is a standard real Brownian motion under `law` (Mathlib's `IsBrownianReal`).

The theorem is stated for **every** Ω and every such `W`, so it doesn't depend on one particular construction
of Brownian motion.
""" + paper("page 1", "“Here B is standard Brownian motion”, in the definition (1.1) of the value function.")
 + "\n" + SAME.format("lines 24–29") + "\n",
 [q("Is `law` required to be a probability measure?", ["Yes", "No, any measure"], 0, "`isProbability : IsProbabilityMeasure law` (Model.lean line 26)."),
  q("What index set does the Brownian motion B use?", ["Nonnegative reals ℝ≥0", "Only [0,1]", "The integers"], 0,
    "`B : ℝ≥0 → Ω → ℝ` (Model.lean line 27)."),
  q("Does the theorem fix a particular sample space?", ["No, it holds for every Ω and every Brownian system on it", "Yes, Wiener space"], 0,
    "`full_support` takes `W : BrownianSystem Ω` for an arbitrary measurable space Ω."),
 ])

node("incrementFiltration",
 "incrementFiltration: what the controller may see after time t",
 "Starting at time t, the information available after elapsed time s is generated by the increments B(t+r) − B(t) for r ≤ s.",
 r"""## Plain English

**Definition (`incrementFiltration`, Model.lean lines 33–36).** Fix a starting time `t`. Look at the increments
`B(t+s) − B(t)` for elapsed times `s ≥ 0`. Their **natural filtration** says, for each `s`, which events are
determined by the increments up to elapsed time `s`.

This is the information a [control](#/node/Control) started at time t is allowed to use: the Brownian moves since
t, up to now, and nothing from the future. (The second argument in the Lean is just the proof that each increment is
measurable.)
""" + paper("page 1", "controls are “progressively measurable … adapted to its increments after time t.”")
 + "\n" + SAME.format("lines 33–36") + "\n",
 [q("Which random variables generate this filtration at elapsed time s?",
    ["The increments B(t+r) − B(t) for 0 ≤ r ≤ s", "All of B, past and future", "B(r) for r ≤ s, from time 0"], 0,
    "It's `Filtration.natural` of `fun s ω => W.B (t + s) ω - W.B t ω` (Model.lean line 35)."),
  q("Is time measured from 0 or from the starting time t here?", ["Elapsed time since t", "Absolute time from 0"], 0,
    "The index `s` is elapsed time: the increment at index s is B(t+s) − B(t)."),
  q("Can a control adapted to this filtration see B(t+1) − B(t) at elapsed time 1/2?", ["No", "Yes"], 0,
    "At elapsed time 1/2 only increments up to t + 1/2 are known."),
 ])

node("Control",
 "Control: an admissible steering strategy",
 "A control started at time t is a random process α, progressively measurable for the increment filtration, with |α| ≤ 1 everywhere.",
 r"""## Plain English

**Structure (`Control`, Model.lean lines 38–41).** A control for `W` started at time `t` is a process
`α(s, ω)` (elapsed time `s ≥ 0`, sample `ω`) such that

- `progressive`: it is progressively measurable for the [increment filtration](#/node/incrementFiltration) at `t`
  (it uses only past increments, in a way that is jointly measurable in time and sample);
- `bound`: `|α(s, ω)| ≤ 1` for every `s` and `ω`.

The bound limits how hard the controller may steer.
""" + paper("page 1", "the supremum in (1.1) “is over progressively measurable controls a<sub>s</sub> ∈ [−1,1], adapted to its increments after time t.”")
 + "\n" + SAME.format("lines 38–41") + "\n",
 [q("What bound does a control satisfy?", ["|α| ≤ 1 everywhere", "|α| ≤ γ", "no bound"], 0, "`bound : ∀ s ω, |val s ω| ≤ 1` (Model.lean line 41)."),
  q("Which filtration must a control be progressive for?", ["The increment filtration started at t", "The full natural filtration of B from time 0"], 0,
    "`progressive : IsProgressive (incrementFiltration W t) val` (Model.lean line 40)."),
  q("Is the control's time index absolute or elapsed?", ["Elapsed since t", "Absolute"], 0,
    "In `controlPayoff`, physical time s ∈ [t,1] uses `α.val (Real.toNNReal (s - t))`, i.e. elapsed time s − t."),
 ])

node("controlPayoff",
 "controlPayoff: reward minus steering cost",
 "For start (t, x) and control α: |x + (B₁ − B_t) + ∫ₜ¹ γ(s) α(s−t) ds| − ½ ∫ₜ¹ γ(s) α(s−t)² ds, sample by sample.",
 r"""## Plain English

**Definition (`controlPayoff`, Model.lean lines 43–47).** Start at time `t` at position `x`, and steer with a
[control](#/node/Control) α. On each sample ω:

- the **final position** is `x + (B(1) − B(t)) + ∫ₜ¹ γ(s)·α(s − t) ds`: the start, plus the Brownian increment,
  plus the steering weighted by γ;
- the **reward** is the absolute value of the final position;
- the **cost** is `½ ∫ₜ¹ γ(s)·α(s − t)² ds`.

The payoff is reward minus cost. Inside the integrals `s` is physical time and `s − t` is elapsed control time.
Lean writes γ(s) as `extend γ.val s` ([extend](#/node/extend)).
""" + paper("page 1, equation (1.1)", "the expression inside the expectation in (1.1): |x + B₁ − B<sub>t</sub> + ∫ₜ¹ γ(s)a<sub>s</sub> ds| − ½ ∫ₜ¹ γ(s)a<sub>s</sub>² ds.")
 + "\n" + SAME.format("lines 43–47") + "\n",
 [q("What is rewarded?", ["The absolute value of the final position", "The final position itself", "The time spent"], 0,
    "The first term is `|x + W.B 1 ω - W.B (Real.toNNReal t) ω + ∫ …|` (Model.lean lines 45–46)."),
  q("What does the cost term penalize?", ["½ ∫ γ(s) α² ds, weighted steering effort", "The size of the Brownian increment", "Nothing"], 0,
    "`(1 / 2 : ℝ) * ∫ s in t..1, extend γ.val s * (α.val (Real.toNNReal (s - t)) ω)^2` (Model.lean line 47)."),
  q("Is this an expectation?", ["No, it is the payoff on one sample ω; `value` takes the expectation", "Yes"], 0,
    "`controlPayoff` takes the sample `ω` as an argument; [value](#/node/value) integrates it against `W.law`."),
 ])

node("value",
 "value: the best expected payoff (Φγ)",
 "value(t, x) is the supremum, over all controls started at t, of the expected control payoff. It is the paper's Φγ(t, x).",
 r"""## Plain English

**Definition (`value`, Model.lean lines 49–51).** For time `t` and position `x`, take every
[control](#/node/Control) α started at t, compute the expected [payoff](#/node/controlPayoff)
`∫ controlPayoff … dW.law`, and take the supremum (`sSup`) of all these numbers.

This is the paper's **Parisi value function** Φγ(t, x), defined directly as a stochastic control problem. That it
solves the Parisi PDE (1.2), and how smooth it is, are things the proof has to establish; they do not follow from
the definition's name.
""" + paper("page 1, equations (1.1)–(1.2)", "Φγ(t,x) = sup<sub>|a|≤1</sub> E[…], which “is the solution, obtained by monotone-coefficient approximation, of Φ<sub>t</sub> = −½(Φ<sub>xx</sub> + γ(t)Φ<sub>x</sub>²), Φ(1,x) = |x|.”")
 + "\n" + SAME.format("lines 49–51") + "\n",
 [q("How is the value defined?", ["Supremum over controls of the expected payoff", "As the solution of a PDE", "As an infimum over controls"], 0,
    "`sSup (Set.range (fun α => ∫ ω, controlPayoff W γ t x α ω ∂W.law))` (Model.lean lines 50–51)."),
  q("Does the definition itself say the value is differentiable in x?", ["No, that must be proved", "Yes"], 0,
    "The definition is a supremum; smoothness is established in the proof (the paper's Lemma 2.1)."),
  q("Which paper object is this?", ["Φγ(t, x) from (1.1)", "P(γ) from (1.3)", "q(t)"], 0, "It is the control formula (1.1)."),
 ],
 caveats=["Lean's `sSup` of a set of reals that is unbounded above, and Lean's integral of a non-integrable function, are both 0 by convention. The proof has to show neither convention is triggered (the payoffs are integrable and bounded above); the definition does not assume it."])

node("gradient",
 "gradient: the first x-derivative of the value (uγ)",
 "gradient(t, x) is the derivative of value(t, ·) at x, with t fixed: the paper's uγ = Φγ,x.",
 r"""## Plain English

**Definition (`gradient`, Model.lean lines 53–54).** `gradient W γ t x = deriv (value W γ t) x`: hold the time
`t` fixed and differentiate the [value](#/node/value) with respect to the position `x`.

Lean's `deriv` is total: where a function isn't differentiable it returns 0. So this is the true derivative
wherever one exists. The proof establishes the differentiability it needs; the definition does not assume it.
""" + paper("page 2", "“Write u<sub>γ</sub> = Φ<sub>γ,x</sub>”; its regularity is proved in Lemma 2.1.")
 + "\n" + SAME.format("lines 53–54") + "\n",
 [q("With respect to which variable is the derivative taken?", ["Position x, with t fixed", "Time t", "γ"], 0,
    "`deriv (value W γ t) x`: the function differentiated is x ↦ value(t, x)."),
  q("What does Lean's `deriv` return at a point of non-differentiability?", ["0", "an error", "+∞"], 0,
    "Mathlib's `deriv` is defined as 0 where no derivative exists."),
  q("Which paper symbol is this?", ["uγ = Φγ,x", "Φγ,xx", "γ′"], 0, "Page 2 writes uγ = Φγ,x."),
 ])

node("curvature",
 "curvature: the second x-derivative of the value (Φγ,xx)",
 "curvature(t, x) is the x-derivative of the gradient: the paper's Φγ,xx. Not a time derivative.",
 r"""## Plain English

**Definition (`curvature`, Model.lean lines 56–57).** `curvature W γ t x = deriv (gradient W γ t) x`: the
x-derivative of the [gradient](#/node/gradient), i.e. the second spatial derivative of the [value](#/node/value).

The theorem says its square has expectation exactly 1 along the diffusion, at every t in [0,1).
""" + paper("page 2, (1.6)", "E[Φ<sub>γ,xx</sub>(t,X<sub>t</sub>)²] = 1 for 0 ≤ t < 1.")
 + "\n" + SAME.format("lines 56–57") + "\n",
 [q("Is `curvature` a derivative in time?", ["No, the second derivative in x", "Yes"], 0, "Both derivatives are in x with t fixed (Model.lean lines 54 and 57)."),
  q("What does the theorem say about E[curvature(t, X_t)²]?", ["It equals 1", "It equals t", "It is positive"], 0, "Model.lean line 88: the integral equals 1."),
  q("Is the curvature defined using `deriv` twice?", ["Yes", "No, using a PDE"], 0, "`deriv (gradient W γ t) x`, and `gradient` is itself a `deriv`."),
 ])

node("parisi",
 "parisi: the zero-temperature Parisi functional P(γ)",
 "P(γ) = value(0, 0) − ½ ∫₀¹ t γ(t) dt.",
 r"""## Plain English

**Definition (`parisi`, Model.lean lines 59–60).** For an [order parameter](#/node/OrderParameter) γ, the Parisi
functional is the [value](#/node/value) at time 0 and position 0, minus half the integral of t·γ(t) over [0,1].

The factor ½ and the weight t come from the normalization ξ(t) = t²/2 used throughout. The paper explains that
the limiting ground-state energy per spin of the SK model equals the **minimum** of this functional (the
zero-temperature Parisi formula, which the paper cites from Auffinger and Chen); that formula is not part of the
Lean statement.
""" + paper("page 2, equation (1.3)", "P(γ) = Φγ(0,0) − ½ ∫₀¹ t γ(t) dt. Then (1.4): P* := lim (1/n) E max H<sub>n</sub>(σ) = min<sub>γ∈U</sub> P(γ), cited from Auffinger and Chen.")
 + "\n" + SAME.format("lines 59–60") + "\n",
 [q("Where is the value function evaluated in P(γ)?", ["At t = 0, x = 0", "At t = 1, x = 0", "Averaged over x"], 0, "`value W γ 0 0` (Model.lean line 60)."),
  q("What is subtracted?", ["½ ∫₀¹ t γ(t) dt", "∫₀¹ γ(t) dt", "½ γ(1)"], 0, "`(1 / 2 : ℝ) * ∫ t in (0 : ℝ)..1, t * extend γ.val t`."),
  q("Does the Lean statement include the theorem that min P equals the SK ground-state energy?", ["No; that is cited background in the paper", "Yes"], 0,
    "The Lean defines only the functional. The ground-state formula (1.4) is taken from the literature in the paper and is not formalized here."),
 ])

node("IsMinimizer",
 "IsMinimizer: no competitor does better",
 "γ is a minimizer when P(γ) ≤ P(η) for every order parameter η: a global minimum over all admissible γ.",
 r"""## Plain English

**Definition (`IsMinimizer`, Model.lean lines 62–63).** `IsMinimizer W γ` says: for **every**
[order parameter](#/node/OrderParameter) η, `parisi W γ ≤ parisi W η`.

This is a genuine global minimum. It is not a local minimum, not a stationarity condition, and it does not mention
support. Nothing smuggles the conclusion into this hypothesis.
""" + paper("page 2, Theorem 1.1", "“If γ ∈ U minimizes P …”")
 + "\n" + SAME.format("lines 62–63") + "\n",
 [q("Over which set is γ compared?", ["All order parameters η", "Order parameters close to γ", "Step functions only"], 0, "`∀ η : OrderParameter, …` (Model.lean line 63)."),
  q("Does `IsMinimizer` assume anything about the support of γ?", ["No", "Yes, full support"], 0, "It only compares Parisi values."),
  q("Does this definition guarantee that a minimizer exists?", ["No, it is just a property γ may or may not have", "Yes"], 0,
    "A definition of a property proves nothing about existence. The paper cites existence from Auffinger and Chen; the Lean does not prove it."),
 ])

node("IsStieltjesMeasure",
 "IsStieltjesMeasure: γ as the distribution function of a measure",
 "A measure μ on [0,1) represents γ when μ([0,t]) = γ(t) for every t in [0,1). In particular μ({0}) = γ(0); μ need not be a probability measure.",
 r"""## Plain English

**Definition (`IsStieltjesMeasure`, Model.lean lines 65–66).** A measure `μ` on [Time](#/node/Time) represents
the [order parameter](#/node/OrderParameter) γ when, for every `t` in [0,1),

μ([0, t]) = γ(t).

Lean writes the left side as `μ (Set.Iic t)`, the set of points of `Time` that are ≤ t, which is [0,t]. The right
side is `ENNReal.ofReal (γ.val t)`; since γ ≥ 0 this is just γ(t) as an extended nonnegative real.

Taking t = 0 gives μ({0}) = γ(0): an atom at 0 when γ(0) > 0. μ need not be a probability measure, and since γ may
grow without bound near 1, μ may have infinite total mass.
""" + paper("page 1", "“The Stieltjes measure μ<sub>γ</sub> on [0,1) is defined by μ<sub>γ</sub>([0,t]) = γ(t), 0 ≤ t < 1. In particular μ<sub>γ</sub>({0}) = γ(0). It is locally finite, but need not be a probability measure or have finite total mass.”")
 + "\n" + SAME.format("lines 65–66") + "\n",
 [q("What is μ({0}) for a representing measure?", ["γ(0)", "0", "1"], 0, "[0,0] = {0}, so μ({0}) = γ(0)."),
  q("Must μ be a probability measure?", ["No", "Yes"], 0, "Only μ([0,t]) = γ(t) is required; total mass can exceed 1 or be infinite."),
  q("Why is `ENNReal.ofReal` harmless here?", ["Because γ ≥ 0, so nothing is truncated", "Because γ ≤ 1"], 0,
    "`ENNReal.ofReal` sends negative numbers to 0; γ is nonnegative, so the conversion is exact."),
 ])

node("IsDiffusion",
 "IsDiffusion: the optimally steered random path",
 "X is a diffusion for W and γ when it is progressive and, almost surely, is continuous on [0,1], starts at 0, and solves "
 "X_t = B_t + ∫₀ᵗ γ(s)·gradient(s, X_s) ds for all t in [0,1].",
 r"""## Plain English

**Definition (`IsDiffusion`, Model.lean lines 68–75).** A process `X` (indexed by `ℝ≥0`) is a diffusion for `W` and
γ when:

1. it is progressively measurable for the natural filtration of the Brownian motion `B`; and
2. for almost every sample ω, all of the following hold:
   - t ↦ X_t(ω) is continuous on [0,1];
   - X_0(ω) = 0;
   - for every t in [0,1]: X_t = B_t + ∫₀ᵗ γ(s)·[gradient](#/node/gradient)(s, X_s) ds.

That last line is the integral form of the paper's SDE dX = γ(t)·uγ(t, X_t) dt + dB, X₀ = 0. The drift uses the
gradient of the [value function](#/node/value) itself, so the diffusion follows the optimal steering. "Almost
surely" sits outside "for every t": there is one null set off which the equation holds at all times at once.
""" + paper("page 2, equation (1.5)", "“dX<sub>t</sub> = γ(t)u<sub>γ</sub>(t,X<sub>t</sub>)dt + dB<sub>t</sub>, X<sub>0</sub> = 0.” The paper shows it has a unique strong solution up to time one (Lemma 2.2).")
 + "\n" + SAME.format("lines 68–75") + "\n",
 [q("Where does the diffusion start?", ["At 0", "At x", "At B_1"], 0, "`X 0 ω = 0` (Model.lean line 72)."),
  q("What is the drift coefficient?", ["γ(s)·gradient(s, X_s)", "gradient(s, X_s) alone", "γ(s)"], 0,
    "`extend γ.val s * gradient W γ s (X (Real.toNNReal s) ω)` (Model.lean lines 74–75)."),
  q("Does the equation have to hold for all t at once, almost surely?", ["Yes: one almost-sure set works for every t in [0,1]", "Only for each t separately"], 0,
    "`∀ᵐ ω, … ∧ ∀ t ∈ Set.Icc 0 1, …`: the `∀ t` is inside the almost-sure statement."),
  q("Does this definition say the diffusion is unique?", ["No; uniqueness is proved separately", "Yes"], 0,
    "It is a property of X. Uniqueness is the proof's lemma [diffusion_uniqueness](#/node/diffusion_uniqueness)."),
 ])

node("squareMoment",
 "squareMoment: E[gradient(t, X_t)²]",
 "squareMoment(X, t) is the expectation of the square of the gradient at (t, X_t): the paper's q(t) = E[uγ(t, X_t)²].",
 r"""## Plain English

**Definition (`squareMoment`, Model.lean lines 77–79).** For a process `X` and time `t`, `squareMoment W γ X t`
is the integral, against the probability law of `W`, of `gradient(t, X_t)²`. That is, E[uγ(t, X_t)²].

It is the expectation **of a square**, not the square of an expectation. The theorem says it equals t along any
diffusion, for every t in [0,1). In the paper's proof this is the function q(t), the main character.
""" + paper("page 2, (1.6), and Section 1.2", "E[uγ(t,X<sub>t</sub>)²] = t; the proof sets q(t) = E uγ(t,X<sub>t</sub>)².")
 + "\n" + SAME.format("lines 77–79") + "\n",
 [q("Which is it?", ["E[gradient²]", "(E[gradient])²"], 0, "`∫ ω, (gradient W γ t (X …))^2 ∂W.law` (Model.lean line 79)."),
  q("What does the theorem say squareMoment equals at time t?", ["t", "1", "0"], 0, "Model.lean line 87: `squareMoment W γ X t = (t : ℝ)`."),
  q("Is the curvature moment also given a name in Model.lean?", ["No, the conclusion writes its integral out directly", "Yes, curvatureMoment"], 0,
    "The target writes the integral of curvature² inline (line 88). The proof's own `curvatureMoment` is a separate definition."),
 ])

node("FullSupportConclusion",
 "FullSupportConclusion: the five-part conclusion",
 "Five claims: a representing measure exists; a diffusion exists; every representing measure has full support; γ is strictly increasing; "
 "along every diffusion E[gradient²] = t and E[curvature²] = 1 for all t in [0,1).",
 r"""## Plain English

**Definition (`FullSupportConclusion`, Model.lean lines 81–88).** For `W` and γ, this is the conjunction of:

1. **Existence of a measure:** some μ on [0,1) [represents γ](#/node/IsStieltjesMeasure).
2. **Existence of a diffusion:** some X [is a diffusion](#/node/IsDiffusion) for W and γ.
3. **Full support:** every representing μ has `μ.support = Set.univ`, i.e. every point of [0,1) is in the support.
4. **Strict increase:** for all a < b in [0,1), γ(a) < γ(b).
5. **Moment identities:** for every diffusion X and every t in [0,1),
   [squareMoment](#/node/squareMoment)(X, t) = t and E[[curvature](#/node/curvature)(t, X_t)²] = 1.

The two existence clauses matter: without them, the "for every μ" and "for every X" clauses could be true just
because no μ or X exists.

**Support.** The support of a measure is the set of points every open neighbourhood of which has positive measure
(Mathlib's `Measure.support`; here neighbourhoods are taken inside [0,1)). Full support does **not** say single points
have positive mass: a measure with a positive continuous density has full support and no atoms.
""" + paper("page 2, Theorem 1.1", "supp μγ = [0,1); γ(b) > γ(a) for 0 ≤ a < b < 1; and the identities (1.6) for the solution of (1.5). The paper speaks of *the* Stieltjes measure and *the* solution; the Lean states existence and then quantifies over all of them.")
 + "\n" + SAME.format("lines 81–88") + "\n",
 [q("Why include the existence clauses 1 and 2?", ["So the universal clauses aren't vacuously true", "They are redundant decorations", "To assume existence"], 0,
    "If no μ or X existed, “every μ …” and “every X …” would hold trivially. Clauses 1–2 rule that out."),
  q("Does full support mean μ({t}) > 0 for every t?", ["No: every open neighbourhood has positive mass, not every point", "Yes"], 0,
    "Support is about neighbourhoods. A measure with continuous positive density has full support and μ({t}) = 0 for every t."),
  q("For which t do the moment identities hold?", ["Every t in [0,1)", "Only t = 0", "Every t in [0,1]"], 0, "`∀ t : Time` (Model.lean line 86), and Time = [0,1)."),
  q("Is strict monotonicity stated for all of [0,1)?", ["Yes, for all a < b in Time", "Only on (0,1)"], 0, "`∀ a b : Time, a < b → γ.val a < γ.val b` (Model.lean line 85)."),
 ])
