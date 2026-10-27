# Why fixed-target norm rejection can be simulated

## A retry rule changes which targets are seen

Consider a signer that receives a hash target, samples a preimage, and rejects that preimage when its norm is too large. There are two possible retry rules. It can keep the target and sample another preimage in the same coset, or it can choose a fresh salt and therefore a new target before trying again. These are different distributions, even if the preimage sampler is exact.

With a fixed target, every initially uniform target eventually produces an accepted preimage. With fresh targets, the final target is more likely to be one for which a preimage passes the test easily. That preference is proportional to the target's acceptance probability.

A two-target example makes the issue visible. Suppose the initial targets are equally likely, and their acceptance probabilities are $`1`$ and $`1/2`$. Keeping the target gives final probabilities $`1/2`$ and $`1/2`$. Redrawing it after rejection gives final probabilities $`2/3`$ and $`1/3`$. Both procedures return valid outputs, but a simulator for one procedure is not automatically a simulator for the other.

For the public Gaussian sampler used here, the exact target law also includes the unconditioned Gaussian image:

```math
\nu(y)=\frac{\mu(y)a_y}{\sum_{y'}\mu(y')a_{y'}},
\qquad \mu=f_h(D),
\qquad a_y=\Pr_{D_y}[A].
```

The proof must control both factors. The [security account](security_transfer.md) keeps this law separate from a retry experiment whose proposals start with exactly uniform targets.

## What the small variance means

The [main theorem](norm_tail_smoothing.md) bounds the variance of $`a_y`$ over uniform targets by $`2^{-90}`$ and $`2^{-120}`$ at the two Falcon parameter sets. This says that acceptance depends very little on the target in a squared-average sense. It does not identify the true acceptance probability of each target, and it does not turn the variance into a pointwise bound.

A separate uniform Chernoff estimate bounds rejection in every coset. That estimate serves two purposes: it guarantees that the retry loop terminates with finite expected cost, and it gives a lower bound on the accepted-image density. The latter is needed when the security argument compares uniform targets **to** the accepted-image distribution. A small forward chi-square distance alone would not control every reverse higher-order moment without such a density floor.

The concrete accepted-image estimates are

```math
\chi^2(\nu\Vert U)<2^{-81}\quad(n=512),
\qquad
\chi^2(\nu\Vert U)<2^{-83}\quad(n=1024).
```

They are uniform over keys satisfying the stated geometric hypotheses. No average-key heuristic or measured Gram–Schmidt profile is used to obtain these bounds.

## Why an integer norm requires its own analysis

The squared norm of an integer vector takes integer values. Its cutoff therefore interacts with arithmetic phases, including parity. A continuous Gaussian ball calculation does not by itself control these effects after reduction modulo an integer lattice.

The proof writes the rejected tail as an exact contour integral. Near rational phases, a quadratic Gauss-sum expansion expresses the integrand in terms of shifted Gaussian masses. The finite quotient then supplies the useful cancellation in the bookkeeping: when a denominator is coprime to the quotient order, multiplication by that denominator permutes the character classes. Their sum becomes one dual-lattice Gaussian mass. This avoids a bound proportional to the enormous number of syndromes.

The neighborhoods of zero and parity require separate estimates. Falcon's odd quotient order excludes an exact half-character from the dual lattice, allowing its mass to be bounded through nonzero dual vectors. The other rational neighborhoods admit a simpler uniform estimate. The resulting calculation uses established circle-method tools; the [related-work account](../references/related_work.md) credits those methods explicitly.

## What the security transfer pays for

After a fresh salt has isolated a signing input, the proof replaces one joint target/preimage law by another. The public law is sampled by drawing an ordinary integer Gaussian until its norm passes, then computing its syndrome. The sampler error and accepted-image error enter a single moment bound. This gives one probability exponent for the combined change of distribution.

The full bound also contains the cost of random-oracle reprogramming and the reduction from a simulated forgery to an explicit NTRU problem. Strong unforgeability additionally concerns a new signature on an already signed message and uses the stated second-preimage assumption. These terms remain part of the security conclusion.

The numerical transfer table in the [security account](security_transfer.md) isolates the loss due to the joint distribution comparison. Its roughly 3.3-bit figures at $`2^{64}`$ signing queries are conditional on a specified bound for the public simulator's success. They are not estimates of NTRU hardness or complete security levels for the implementation.

This distinction is particularly relevant in the QROM. With $`q_S=2^{64}`$, $`q_H=2^{128}`$, and a 320-bit salt, the retained conservative reprogramming term is about $`2^{-31.4}`$. A small Rényi transfer loss cannot remove that additive term. The theorem makes the quantum costs visible rather than deriving a full security level from the sampler comparison alone.

## The algorithm and implementation boundary

The result justifies the fixed-target norm-retry rule in the declared model. It does not introduce a different modulus, reduce the signature length, or establish a measured speed improvement.

The concrete sampler application uses the published pointwise analysis of ideal exact-arithmetic FFO. An implementation can be covered by the abstract theorem if a suitable profile for its actual sampler is established and composed with the other costs. Floating-point arithmetic and low-level sampling routines have their own proof obligations.

Returning a canonical compressed representation, or a public error when encoding fails, is handled with an explicit representation map. The strong-unforgeability argument requires a sufficient output buffer and a verifier accepting one canonical format, as specified in the [signing model](signing_model.md#6-canonical-compressed-output). Retrying until a total padded encoding budget is met changes the conditioning event and needs a corresponding distribution estimate. Individual coefficient overflow has a separate small-probability bound, but that bound does not control the sum of encoded lengths.

Fresh salt generation and the output-only signing interface are also part of the model. A caller-selected target or an exposed retry count changes the adversary's information and requires a different argument. These boundaries identify the precise security statement established by the project.
