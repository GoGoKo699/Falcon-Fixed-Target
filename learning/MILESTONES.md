# Thirty milestones for fixed-target Falcon

This map follows one scientific question: can a public simulator reproduce the accepted outputs of a lattice signer that keeps its hash target fixed while retrying a norm test? The route connects the geometry of Gaussian preimages to an exact discrete norm-tail estimate, then carries that estimate through a signature-security reduction.

The single educational anchor is Chris Peikert, [*A Decade of Lattice Cryptography*](https://eprint.iacr.org/2015/939), using the author version dated 17 February 2016. Section numbers and page numbers below refer to that version's printed pagination. The [anchor and project bridge](ANCHOR.md) explains the notation and the additional arguments needed here. Peikert supplies the lattice, Gaussian, trapdoor, and hash-and-sign foundations. The sharp integer cutoff, explicit Fourier bounds, certified arithmetic, conditional Rényi argument, and modern QROM reduction are supplied by the canonical project pages and their cited primary research dependencies.

## Structure of the map

| Phase | Milestones | Scientific role |
|---|---|---|
| Background/preliminaries | M01–M14 | Assemble integer geometry, Gaussian sampling, and the security model into the distinction between the three accepted laws. |
| Narrative/innovation | M15–M30 | Build the norm-conditioned estimate from its local analytic ingredients, certify its constants, and integrate it with the sampler, representation, and forgery reductions. |

The allocation is 14 background milestones and 16 narrative milestones because the project joins two frameworks: finite-quotient Gaussian analysis and concrete signature simulation. The background phase ends when those frameworks express one precise distributional question. The narrative needs separate treatment of the contour's arithmetic regions, the numerical enclosures, and the cryptographic interfaces before they can be combined into a complete statement. The final milestone of each phase is a synthesis of its preceding components.

The map records conceptual understanding targets and their dependencies. Detailed proofs, implementation contracts, and reproducible calculations remain in the linked scientific sources; the map does not attempt to enumerate every technical step or neighboring topic. Milestone dependencies always refer to earlier IDs. Research papers cited by the canonical pages remain proof dependencies, without becoming additional educational anchors.

## Background/preliminaries — M01–M14

### M01 — Integer lattices and the meaning of a short vector

- **ID and phase:** M01; background/preliminaries.
- **Central question:** What is the mathematical object in which a lattice signature is required to be short?
- **Understanding target:** Distinguish an integer vector, its Euclidean norm, an integer lattice, and a basis of that lattice. Explain why the same lattice can have different bases and why a bound on squared norm is a property of the vector rather than its representation in a basis.
- **Dependencies and story role:** No earlier milestones. This supplies the local geometric objects used by every later statement.
- **Conceptual connection:** The signature's norm predicate is a geometric constraint on coefficient vectors; the trapdoor is additional information about the lattice, not a different set of valid vectors.
- **Source pointers:** Peikert §§2.1–2.2.1, pp. 6–7; [signing model §1: ring, lattice, and parameters](../science/signing_model.md#1-ring-lattice-and-parameters).

### M02 — Cosets, modular equations, and syndromes

- **ID and phase:** M02; background/preliminaries.
- **Central question:** How does a public hash target select the set from which a signature must be sampled?
- **Understanding target:** Explain a coset as a translated lattice and a syndrome as its public label. For $`F_h(u,v)=u+hv\bmod q`$, distinguish the kernel lattice from a target fiber and explain why the quotient is finite and the map is surjective.
- **Dependencies and story role:** M01. This changes the picture from one lattice to the family of target fibers on which signing operates.
- **Conceptual connection:** Solving a modular equation with a short vector is the bridge between geometric preimages and public verification.
- **Source pointers:** Peikert §2.2.1, p. 7, and §5.4.2, the integer preimage-sampleable construction on p. 48; [signing model §1](../science/signing_model.md#1-ring-lattice-and-parameters).

### M03 — Dual lattices and characters of the quotient

- **ID and phase:** M03; background/preliminaries.
- **Central question:** How can oscillating functions detect that some syndromes occur more often than others?
- **Understanding target:** Relate the dual lattice's integer inner-product condition to characters that are constant on lattice cosets. Identify the quotient characters with $`\Lambda^*/\mathbb Z^d`$ and distinguish the trivial character, which records total mass, from nontrivial characters, which record bias.
- **Dependencies and story role:** M01–M02. This introduces the local frequency coordinates in which the later distributional question becomes manageable.
- **Conceptual connection:** The geometry of a dual lattice controls Fourier coefficients of probabilities on the finite syndrome quotient.
- **Source pointers:** Peikert §2.2.1, “The dual lattice,” p. 7; the project supplies the finite-character identification in [norm-tail notation and equation (2)](../science/norm_tail_smoothing.md#notation-and-the-two-image-distributions).

### M04 — Discrete Gaussian laws and width conventions

- **ID and phase:** M04; background/preliminaries.
- **Central question:** What does Gaussian sampling mean on integer vectors or on a lattice coset?
- **Understanding target:** Distinguish an unnormalized Gaussian mass function from its normalized probability law, and an ambient Gaussian from its restriction to a coset. Translate Peikert's $`\exp(-\pi\|z\|^2/s^2)`$ convention to the project's $`\exp(-\|z\|^2/(2\sigma^2))`$ by $`s=\sqrt{2\pi}\sigma`$, without identifying the width with the exact variance of a discrete law.
- **Dependencies and story role:** M01–M02. This specifies the probability distributions whose images and accepted outputs will be compared.
- **Conceptual connection:** The same Gaussian weight can produce different laws when normalized on different supports.
- **Source pointers:** Peikert §2.3, pp. 8–10; [signing model §§1–2](../science/signing_model.md#1-ring-lattice-and-parameters); [parameter conventions](../science/falcon_parameters.md#1-conventions-and-exact-parameters).

### M05 — Gram–Schmidt geometry and basis quality

- **ID and phase:** M05; background/preliminaries.
- **Central question:** Which feature of a secret basis controls the Gaussian widths needed by the proof?
- **Understanding target:** Explain orthogonal projection in an ordered basis and distinguish basis-vector lengths from Gram–Schmidt lengths. Relate an upper bound on those lengths to smoothing and sampling hypotheses, while keeping basis order and the underlying lattice separate.
- **Dependencies and story role:** M01 and M04. This identifies the geometric interface between key generation and the analytic estimates.
- **Conceptual connection:** A concrete key-quality bound becomes a uniform bound over all permitted keys, rather than an assumption about a typical lattice.
- **Source pointers:** Peikert Theorem 2.3.2, p. 9, and the setup for Theorem 5.4.2, p. 46; [Falcon basis hypothesis](../science/falcon_parameters.md#2-why-the-generated-lattice-satisfies-the-gs-hypothesis).

### M06 — Trapdoors and canonical preimage sampling

- **ID and phase:** M06; background/preliminaries.
- **Central question:** Why does a trapdoor signer sample a distribution of preimages instead of choosing an arbitrary short solution?
- **Understanding target:** Explain the forward and reverse sampling experiments in a preimage-sampleable function. Distinguish the exact coset Gaussian $`G_y`$ from an algorithmic sampler $`P_y`$ whose law must be bounded relative to it; shortness alone does not establish the needed distributional property.
- **Dependencies and story role:** M02, M04, and M05. This places the geometric and probabilistic ingredients inside the signing mechanism.
- **Conceptual connection:** Security simulation needs a public forward experiment that matches the trapdoor's reverse experiment closely enough.
- **Source pointers:** Peikert §5.4.1, p. 44; Theorem 5.4.2, p. 46; Definition 5.4.3 and its lattice instantiation, pp. 47–48; [key-generation and sampler contracts](../science/signing_model.md#2-key-generation-and-sampler-contracts).

### M07 — Smoothing and the Poisson connection

- **ID and phase:** M07; background/preliminaries.
- **Central question:** Why can a sufficiently wide Gaussian have an almost uniform image modulo a lattice?
- **Understanding target:** Connect small nonzero dual Gaussian mass to nearly equal Gaussian masses of translated cosets. Explain the role of Poisson summation in moving between spatial coset sums and dual frequencies, and why the width hypothesis must be checked quantitatively.
- **Dependencies and story role:** M03–M05. This supplies the familiar unconditioned smoothing mechanism before the norm cutoff changes the problem.
- **Conceptual connection:** A short-basis guarantee controls a probability distribution through dual-lattice geometry.
- **Source pointers:** Peikert §2.3, smoothing parameter and Theorem 2.3.2, p. 9; the explicit Poisson calculation is in [dual mass and translated mass, equations (3)–(5)](../science/norm_tail_smoothing.md#dual-mass-and-translated-mass).

### M08 — Fourier energy, density error, and chi-square distance

- **ID and phase:** M08; background/preliminaries.
- **Central question:** How can many small target biases be summarized by one quantity that remains useful in a security proof?
- **Understanding target:** Explain density relative to the uniform quotient law and its centered $`L^2`$ norm. Use the meaning of Parseval's identity to connect this norm to nontrivial Fourier energy, and identify chi-square distance as the squared density error for a normalized distribution.
- **Dependencies and story role:** M03 and M07. This selects the quantitative language for the new smoothing estimate.
- **Conceptual connection:** Fourier energy measures total distributional bias without requiring a separate worst-case estimate for every syndrome.
- **Source pointers:** Peikert §2.3, p. 9, provides the Gaussian/Fourier context; the finite-quotient energy identity is supplied in [norm-tail notation, equation (2)](../science/norm_tail_smoothing.md#notation-and-the-two-image-distributions), and the density interpretation in [security transfer §3](../science/security_transfer.md#3-the-accepted-ambient-image-and-the-required-reverse-moment).

### M09 — Conditioning and what a retry rule changes

- **ID and phase:** M09; background/preliminaries.
- **Central question:** Does accepting only short samples leave the distribution of targets unchanged?
- **Understanding target:** Explain conditional probability and how an acceptance probability $`a_y`$ weights target frequencies. Distinguish retrying the sample at a fixed target from restarting the target and sample together. Recognize why a small average rejection rate alone does not bound variation between targets.
- **Dependencies and story role:** M02, M04, and M06. This introduces the precise obstruction that the project addresses.
- **Conceptual connection:** The forward/reverse sampling correspondence can change after a public acceptance predicate is imposed.
- **Source pointers:** Peikert Definition 5.4.3 and its conditional-law explanation, pp. 47–48, supply the unconditioned comparison; the retry distinction is supplied by [the interpretation's opening example](../science/interpretation.md#a-retry-rule-changes-which-targets-are-seen) and [the three accepted laws](../science/signing_model.md#5-three-accepted-laws-that-must-remain-distinct).

### M10 — Signatures and the two freshness notions

- **ID and phase:** M10; background/preliminaries.
- **Central question:** What must a successful attacker produce, and how does that depend on the definition of forgery?
- **Understanding target:** Explain the roles of key generation, signing, verification, and chosen-message access. Distinguish EUF-CMA, which requires a previously unrequested message here, from SUF-CMA, which forbids any new valid message/signature pair even for an already requested message; include the stated treatment of public signing errors.
- **Dependencies and story role:** M02 and M06. This identifies the final event whose probability the distributional proof must preserve.
- **Conceptual connection:** A valid short preimage becomes a security violation only when it satisfies the appropriate freshness condition.
- **Source pointers:** Peikert §5.5.1 and Theorem 5.5.1, pp. 53–54, for hash-and-sign and chosen-message unforgeability; the project's exact EUF/SUF and error conventions are in [signing model §7](../science/signing_model.md#7-unforgeability-and-termination).

### M11 — Random-oracle access and the role of a fresh salt

- **ID and phase:** M11; background/preliminaries.
- **Central question:** What lets a reduction assign a new hash target at a signing input without making an uncontrolled change to the adversary's view?
- **Understanding target:** Explain programmable random-oracle simulation and why a uniform salt drawn after the message supplies fresh input uncertainty. Distinguish classical signing queries from hash queries, which may be classical in the ROM or quantum in the QROM; identify which private retry information is absent from the model.
- **Dependencies and story role:** M06 and M10. This connects the sampling comparison to an interactive adversary and its permitted observations.
- **Conceptual connection:** Public randomness, query order, and the oracle interface determine whether the distributional comparison can be used during signing.
- **Source pointers:** Peikert §5.5.1, pp. 53–54, including footnote 10 on randomized hashing; the precise salt, access, and leakage conventions are in [signing model §3](../science/signing_model.md#3-hash-and-query-model). QROM details are a project addition.

### M12 — Rényi moments and event-probability transfer

- **ID and phase:** M12; background/preliminaries.
- **Central question:** How can a small multiplicative distribution mismatch yield a useful bound on a rare forgery event?
- **Understanding target:** Distinguish the unrooted moment $`M_\rho`$, multiplicative Rényi divergence, and logarithmic Rényi divergence. Explain the direction of the likelihood ratio and the event-probability exponent in Hölder's inequality, including the tradeoff in selecting the order $`\rho>1`$.
- **Dependencies and story role:** M08–M10. This provides the transfer mechanism needed when additive statistical-distance costs would be too coarse.
- **Conceptual connection:** The approximate equality of forward and reverse experiments in a preimage-sampleable function is replaced by an explicit quantitative comparison for rare events.
- **Source pointers:** Peikert Definition 5.4.3, p. 47, motivates the comparison but does not supply this Rényi argument; use [security transfer §1](../science/security_transfer.md#1-analytic-and-sampler-hypotheses) for conventions and [§5](../science/security_transfer.md#5-adaptive-signing-is-a-common-channel-on-independent-pairs) for the event inequality.

### M13 — The NTRU key and concrete Falcon framework

- **ID and phase:** M13; background/preliminaries.
- **Central question:** Which algebraic structure and exact parameters make this a Falcon question rather than an arbitrary lattice-signature question?
- **Understanding target:** Relate polynomial pairs in $`\mathbb Z[X]/(X^n+1)`$ to integer coefficient vectors of dimension $`d=2n`$. Identify the generated-key distribution, modulus, Gaussian width, norm threshold, and basis-quality promise; distinguish assumptions on this NTRU distribution from claims about uniformly random SIS matrices.
- **Dependencies and story role:** M01–M02, M05–M06, and M10–M11. This assembles the general objects into the concrete model to which the result will apply.
- **Conceptual connection:** Ring notation provides compact public equations, while the proof uses ordinary integer geometry and an explicitly specified hardness distribution.
- **Source pointers:** Peikert §3.2, pp. 14–15, and §§4.3.1–4.3.3, pp. 27–29, for NTRU and ring geometry; [exact Falcon parameters](../science/falcon_parameters.md#1-conventions-and-exact-parameters) and [the project's hardness games](../science/security_transfer.md#7-hardness-games-and-extraction).

### M14 — Synthesis: the three accepted laws and the fixed-target question

- **ID and phase:** M14; background/preliminaries.
- **Central question:** Which two experiments must the proof compare, and which tempting third experiment must remain distinct?
- **Understanding target:** Distinguish the fixed uniform-target law $`U(y)P_y(z\mid A)`$, the public accepted ambient law $`J(y,z)=\nu(y)G_y(z\mid A)`$, and the comparator that chooses a fresh uniform syndrome and samples its ideal coset Gaussian $`G_y`$ after each rejection. Explain why control of acceptance variance alone does not identify the public simulator's image $`\nu`$.
- **Dependencies and story role:** M02, M06–M13. This completes the background phase by expressing the geometry, retry policy, and security objective as one joint-distribution problem.
- **Conceptual connection:** The PSF forward/reverse correspondence now includes a sharp norm predicate, a concrete sampler, and an adaptive signing interface. Those additions specify exactly what the narrative must establish.
- **Source pointers:** Peikert Definition 5.4.3, pp. 47–48, and §5.5.1, pp. 53–54; [signing model §5](../science/signing_model.md#5-three-accepted-laws-that-must-remain-distinct) and [scientific overview: the distribution to simulate](../science/README.md#the-distribution-that-the-proof-must-simulate).

## Narrative/innovation — M15–M30

### M15 — From key quality to ordinary GS bounds and FFO leaves

- **ID and phase:** M15; narrative/innovation.
- **Central question:** Why does the actual key-quality promise satisfy both the analytic basis hypothesis and the sampler's leaf-width hypothesis?
- **Understanding target:** Follow the expansion of the two polynomial columns into their negacyclic shifts and the projection argument bounding ordinary Gram–Schmidt lengths. Explain the coefficient-isometric FFO expansion and leaf identity, while keeping the geometric bound separate from the theorem controlling the sampler's output law.
- **Dependencies and story role:** M05–M06 and M13–M14. This establishes the first concrete input to the narrative for every key in the specified support.
- **Conceptual connection:** Peikert's short-basis sampling framework becomes applicable through a verified Falcon-specific geometry argument, not through an assumed equality between FFO and an arbitrarily ordered Klein sampler.
- **Source pointers:** Peikert Theorems 2.3.2 and 5.4.2, pp. 9 and 46, provide the framework; [parameter page §2](../science/falcon_parameters.md#2-why-the-generated-lattice-satisfies-the-gs-hypothesis), especially [the FFO leaf-width hypothesis](../science/falcon_parameters.md#the-ffo-leaf-width-hypothesis), supplies the bridge and its primary-source attribution.

### M16 — Quantitative flatness of the untruncated image

- **ID and phase:** M16; narrative/innovation.
- **Central question:** What can ordinary Gaussian smoothing already prove before any samples are rejected?
- **Understanding target:** Explain the pointwise bound on $`p(y)-1`$ and the separate Fourier-energy bound on $`Q_0`$. Identify why the integer dual contributions must be canceled before taking absolute values and how weighted Cauchy–Schwarz improves the energy estimate.
- **Dependencies and story role:** M07–M08 and M15. This establishes the baseline image control that the accepted-image theorem will later combine with the tail estimate.
- **Conceptual connection:** The anchor's qualitative smoothing picture is converted into explicit theta expressions suitable for the fixed Falcon widths.
- **Source pointers:** Peikert §2.3, p. 9, for smoothing; [unconditioned quotient image, equations (6)–(8)](../science/norm_tail_smoothing.md#unconditioned-quotient-image) for the quantitative derivation.

### M17 — An exact contour for the integer norm tail

- **ID and phase:** M17; narrative/innovation.
- **Central question:** How can the sharp rejection event be represented without replacing an integer Gaussian by a continuous approximation?
- **Understanding target:** Explain why rejection begins at $`K=T+1`$ and how a geometric-series kernel selects precisely the integer squared norms at least $`K`$. Identify the purpose of the positive tilt, the product of one-dimensional theta functions, and the passage from individual coefficients to their joint Fourier norm.
- **Dependencies and story role:** M04, M08–M09, and M16. This introduces the representation from which the new tail bound is derived.
- **Conceptual connection:** Exact conditioning turns an ordinary Gaussian smoothing problem into a discrete Fourier integral with arithmetic structure.
- **Source pointers:** Peikert §2.3, pp. 8–9, provides the Gaussian conventions only; the project supplies [the exact contour, equation (9), and its convergence justification](../science/norm_tail_smoothing.md#an-exact-contour-for-the-rejected-tail).

### M18 — Rational angles and twisted quadratic Gauss sums

- **ID and phase:** M18; narrative/innovation.
- **Central question:** Why do rational contour angles admit a controlled finite Fourier expansion?
- **Understanding target:** Explain the periodic or antiperiodic behavior of the quadratic phase at $`\theta=\pi a/b`$. Relate the half-frequency shift to the parity of $`ab`$ and the coefficient magnitude $`b^{-1/2}`$ to cancellation in the autocorrelation sum; then identify the role of complex Poisson summation.
- **Dependencies and story role:** M03 and M17. This supplies a local estimate near each rational angle before summing over quotient characters.
- **Conceptual connection:** Integer quadratic phases, rather than continuous radial symmetry, determine the useful frequency decomposition.
- **Source pointers:** Peikert §2.2.1, p. 7, provides dual-lattice context; the additional harmonic analysis is in [twisted quadratic Gauss sums, equations (10)–(11)](../science/norm_tail_smoothing.md#twisted-quadratic-gauss-sums), with methodological attribution in [the discrete circle method](../references/related_work.md#the-discrete-circle-method).

### M19 — The coprime finite-quotient identity

- **ID and phase:** M19; narrative/innovation.
- **Central question:** How can the proof sum over every syndrome character without paying the quotient's enormous cardinality?
- **Understanding target:** Explain why multiplication by $`b`$ permutes the dual quotient when $`\gcd(b,|Y|)=1`$. Follow the disjoint coset merger into one translated dual-lattice mass, and identify the kernel multiplicity that appears when coprimality fails.
- **Dependencies and story role:** M02–M03 and M18. This turns local rational-angle control into an aggregate Fourier-energy bound.
- **Conceptual connection:** A finite-group automorphism removes a potentially fatal cardinality factor; the arithmetic hypothesis is part of the theorem, not a cosmetic condition.
- **Source pointers:** Peikert §2.2.1, p. 7, for quotients and duals; [merging the character sum, equations (12)–(14)](../science/norm_tail_smoothing.md#merging-the-character-sum), including equation (13) for the noncoprime case.

### M20 — Controlling the minor arcs uniformly

- **ID and phase:** M20; narrative/innovation.
- **Central question:** How are all angles away from the two main regions bounded without enumerating them one by one?
- **Understanding target:** Explain how Dirichlet approximation provides denominators at most $`Q=512`$, why these are coprime to $`12289^n`$, and why denominators away from the main arcs are at least two. Identify how theta bounds and convexity reduce the remaining continuum to an endpoint envelope.
- **Dependencies and story role:** M13 and M17–M19. This completes one of the three contributions to the tail-energy bound.
- **Conceptual connection:** Arithmetic approximation and geometric decay together control a whole angular region with an explicit conservative bound.
- **Source pointers:** Peikert's Gaussian and quotient background in §§2.2.1–2.3 supports the objects; the additional arc argument is [minor arcs, equation (15)](../science/norm_tail_smoothing.md#minor-arcs), with its numerical domain checks in [the certificate](../science/numerical_certificate.md#parameter-and-domain-checks).

### M21 — The zero arc and removal of the trivial character

- **ID and phase:** M21; narrative/innovation.
- **Central question:** Why is the origin treated more carefully than an ordinary rational angle?
- **Understanding target:** Distinguish the total Fourier mass from the nontrivial energy that measures target variation. Explain why subtracting the integer dual contribution removes the large zero term near the origin and how that subtraction enters the zero-arc integral.
- **Dependencies and story role:** M03, M08, M16, and M17–M19. This obtains the first main-arc contribution while preserving the centered quantity the theorem actually needs.
- **Conceptual connection:** The same distinction between normalization and bias that defined $`Q_0`$ now controls the rejected tail.
- **Source pointers:** Peikert §2.3, p. 9, gives the nonzero-dual-mass smoothing context; [removing the zero term, equation (16)](../science/norm_tail_smoothing.md#removing-the-zero-term-at-the-origin) and [major-arc integrals, equation (18)](../science/norm_tail_smoothing.md#major-arc-integrals) give the project step.

### M22 — The parity arc and the odd-order quotient

- **ID and phase:** M22; narrative/innovation.
- **Central question:** What arithmetic contribution occurs at the parity angle, and why does the odd quotient order matter there?
- **Understanding target:** Explain $`(-1)^{\|x\|^2}=(-1)^{\sum_jx_j}`$ and the resulting half-character shift. Follow the doubling injection into the nonzero dual lattice and distinguish this use of odd quotient order from the denominator-coprimality condition in M19.
- **Dependencies and story role:** M03, M13, and M17–M21. This supplies the second main-arc contribution and completes the analytic decomposition of the tail norm.
- **Conceptual connection:** Integer parity creates a term that a continuous approximation would omit; the finite quotient's arithmetic lets the proof bound it.
- **Source pointers:** Peikert §2.2.1, p. 7, provides the quotient and dual definitions; [the half-character argument, equation (17)](../science/norm_tail_smoothing.md#the-half-character-at-the-parity-angle) and [equations (19)–(20)](../science/norm_tail_smoothing.md#major-arc-integrals) supply the parity bound and its combination with the other arcs.

### M23 — Certified numerical enclosures

- **ID and phase:** M23; narrative/innovation.
- **Central question:** What makes the concrete numerical inequalities consequences of the analytic bounds rather than numerical observations?
- **Understanding target:** Distinguish an enclosure of an upper-bound expression from the unknown lattice's actual variance or divergence. Explain the roles of exact parameter intervals, explicit theta-series remainders, proved upper rectangles, and Arb ball arithmetic; distinguish identity checks from the inequalities that establish the certificate.
- **Dependencies and story role:** M13 and M16–M22. This turns the analytic decomposition into reproducible bounds at the two parameter sets.
- **Conceptual connection:** Numerical evaluation is a controlled final step of the proof, with explicit interfaces such as the certified bounds on $`R`$.
- **Source pointers:** Peikert §2.3 provides the Gaussian setting but no certificate for these parameters; use [what the arithmetic encloses](../science/numerical_certificate.md#what-the-arithmetic-encloses), [the theta-series remainder](../science/numerical_certificate.md#an-explicit-theta-series-remainder), [upper rectangles](../science/numerical_certificate.md#upper-rectangles-for-the-two-major-arcs), and [the verification guide](../verification/README.md).

### M24 — Acceptance variance and the accepted ambient image

- **ID and phase:** M24; narrative/innovation.
- **Central question:** What does the certified tail bound establish about the distributions that signing simulation needs?
- **Understanding target:** Explain the distinct roles of $`R`$, $`Q_0`$, and the uniform coset rejection bound $`D_0`$. Derive conceptually how they control both the variance of $`a_y`$ under uniform targets and $`\chi^2(\nu\|U)`$; keep the ambient rejection mean separate from the uniform-coset mean.
- **Dependencies and story role:** M08–M09, M14, M16, and M23. This synthesizes the analytic narrative into the two probabilistic consequences stated by the norm theorem.
- **Conceptual connection:** The rejected-tail estimate answers both a retry-bias question and the stronger accepted-image question required for a public simulator.
- **Source pointers:** Peikert Definition 5.4.3, pp. 47–48, supplies the forward/reverse motivation; [uniform tail, variance, and accepted-image bounds, equations (21)–(23)](../science/norm_tail_smoothing.md#from-tail-smoothing-to-acceptance-variance) supply the project's consequences.

### M25 — Coordinate caps and the public signature representation

- **ID and phase:** M25; narrative/innovation.
- **Central question:** Which changes from sampled vectors to encoded signatures preserve the analyzed model, and which impose a new acceptance predicate?
- **Understanding target:** Distinguish an individual coefficient cap from a bound on total encoded length. Explain the optional cap extension, the norm-only signer's canonical compressed output with sufficient buffers and public errors, and the reconstruction of a centered omitted component. Identify why SUF extraction needs uniqueness of the admitted representation and why padded-length retries require a separate analysis.
- **Dependencies and story role:** M09–M10, M13–M14, and M24. This connects the analytic vectors to the actual public objects used in the security event.
- **Conceptual connection:** Representation preserves the norm bound and second-preimage argument under the stated decoding, buffer, and error semantics; recentering can strictly decrease the sampled norm.
- **Source pointers:** Peikert §5.5.1, p. 53, provides the abstract vector-signature setting; the project supplies [the coordinate-cap extension](../science/norm_tail_smoothing.md#optional-individual-coordinate-cap), [verification and reconstruction](../science/signing_model.md#verification-and-extraction), and [canonical compressed output](../science/signing_model.md#6-canonical-compressed-output).

### M26 — Conditioning the actual FFO sampler without a rejection floor

- **ID and phase:** M26; narrative/innovation.
- **Central question:** How does a proven unconditioned sampler profile survive the fixed-target norm-rejection loop?
- **Understanding target:** Explain the conditional-excess lemma for $`M_\rho-1`$ and why it avoids paying an acceptance-normalization penalty when the two input laws already agree. Combine the FFO likelihood-ratio profile with the uniform acceptance lower bound, keeping the exact-arithmetic sampler contract separate from finite-precision implementation claims.
- **Dependencies and story role:** M06, M09, M12, M15, and M24. This transfers the ideal Gaussian result to the mathematical sampler used by the stated signer.
- **Conceptual connection:** The proof uses rejection to condition an already close pair of laws; controlling their excess moment preserves the small error scale.
- **Source pointers:** Peikert Theorem 5.4.2, p. 46, supplies general Gaussian-sampling context; [security transfer §2](../science/security_transfer.md#2-conditioning-preserves-the-small-excess-above-one) proves the conditioning lemma, and [§4](../science/security_transfer.md#4-an-exact-moment-profile-for-the-ideal-ffo-sampler) records the exact FFO profile and primary-source proof locations.

### M27 — One joint-law comparison for adaptive signing

- **ID and phase:** M27; narrative/innovation.
- **Central question:** Why does the one-query distribution bound remain valid when later messages depend on earlier signatures and hash queries?
- **Understanding target:** Explain how the accepted-image chi-square bound and a density lower bound control the required reverse Rényi moment. Combine target and preimage in one joint law, then view an independent pre-sampled pair list as input to a common interaction procedure. Identify why adaptivity and a quantum output do not require changing every cell of the random oracle's distribution.
- **Dependencies and story role:** M11–M12, M14, and M24–M26. This integrates the analytic and sampler results into a transcript-level event bound.
- **Conceptual connection:** The public and trapdoor experiments differ in one classical source of randomness, while the same channel handles adaptive interaction and public representation.
- **Source pointers:** Peikert Definition 5.4.3 and §5.5.1, pp. 47 and 53–54, motivate joint-pair simulation; [security transfer §3](../science/security_transfer.md#3-the-accepted-ambient-image-and-the-required-reverse-moment) supplies the reverse moment, and [§5](../science/security_transfer.md#5-adaptive-signing-is-a-common-channel-on-independent-pairs) proves adaptive composition.

### M28 — A finite public pool and classical forgery extraction

- **ID and phase:** M28; narrative/innovation.
- **Central question:** How does the distributional simulator become a reduction with explicit sampling and oracle budgets to precisely stated lattice problems?
- **Understanding target:** Explain why conditioning a sufficiently large ambient Gaussian pool on having enough accepted vectors leaves the retained list's law unchanged. Track the pool-failure factor, fresh-salt programming term, and distinction between programmed and unprogrammed forgery inputs. Match EUF extraction to uniform-target NTRU-ISIS and the additional SUF case to unconditioned Gaussian NTRU-SPISIS*, with their actual key distribution and resource counts. Distinguish this signing-program comparison from Peikert's GPV proof that prepares preimages for hash inputs and subtracts a hidden preimage under its SIS setup.
- **Dependencies and story role:** M10–M13, M25, and M27. This completes the main classical security corollary by connecting simulation to the declared hardness games.
- **Conceptual connection:** The Gaussian distribution used for the simulator and the challenge distribution used by the hardness assumption must agree at the level of the whole finite experiment.
- **Source pointers:** Peikert §5.5.1, pp. 53–54, supplies the public-simulation and extraction paradigm; [finite pool](../science/security_transfer.md#6-a-finite-public-gaussian-pool), [hardness games and extraction](../science/security_transfer.md#7-hardness-games-and-extraction), and [the ROM theorem](../science/security_transfer.md#8-classical-rom-theorem) give the project's precise reduction.

### M29 — Quantum-oracle costs and the conservative QROM corollary

- **ID and phase:** M29; narrative/innovation.
- **Central question:** Which additional costs arise when the adversary can query the hash in quantum superposition?
- **Understanding target:** Distinguish classical signing from quantum hash access, the fresh-salt reprogramming term, and the measure-and-reprogram extraction loss. Explain the static background oracle with a mutable classical override table, why $`Q=q_H+q_S+1`$ is charged, and why an ordinary reversible lookup has nonconstant local work. Keep these costs separate from the small Rényi-transfer loss and from a lattice work-factor estimate.
- **Dependencies and story role:** M11–M12 and M27–M28. This extends the same simulation architecture to its stated quantum-oracle model while exposing the remaining quantitative costs.
- **Conceptual connection:** The distributional result is reusable, but quantum oracle access changes the programming and extraction mechanisms and their resource accounting.
- **Source pointers:** Peikert §5.5.1, pp. 53–54, supplies only the classical ROM background; the project and its cited primary results supply [the QROM corollary and oracle semantics](../science/security_transfer.md#9-qrom-corollary-and-explicit-oracle-semantics), [quantum runtime](../science/security_transfer.md#quantum-runtime-and-scope-of-the-corollary), and [probability-versus-work-factor interpretation](../science/security_transfer.md#10-certified-transfer-values-and-their-interpretation).

### M30 — Synthesis: contribution, assumptions, and scope

- **ID and phase:** M30; narrative/innovation.
- **Central question:** What has the full argument established, which ingredients does it inherit, and where does the conclusion stop?
- **Understanding target:** Connect the key-quality promise, exact integer-tail analysis, certified bounds, conditioned FFO profile, adaptive simulation, and forgery extraction into one conditional security statement. Distinguish the new norm-conditioned estimate and its use from inherited smoothing, Gauss-sum, sampling, and oracle-reduction tools. Explain why the result covers fresh-initial-salt, fixed-target norm retries under the declared model, while finite precision, padded-length retries, chosen or reused salts, timing exposure, and aggregate or multi-user interfaces need additional arguments.
- **Dependencies and story role:** M14–M29, with M24 and M28–M29 providing the main analytic and security conclusions. This completes the narrative by integrating local mechanisms into the contribution, its concrete interpretation, and its limits.
- **Conceptual connection:** Peikert's forward/reverse sampling principle remains the organizing idea; the project supplies the missing norm-conditioned comparison and explicitly accounts for what is needed to turn it into security.
- **Source pointers:** Peikert Definition 5.4.3 and §5.5.1, pp. 47–48 and 53–54; [scientific overview](../science/README.md), [interpretation](../science/interpretation.md), [the precise security scope](../science/security_transfer.md#11-what-the-theorem-establishes), and [related work and the contribution boundary](../references/related_work.md).
