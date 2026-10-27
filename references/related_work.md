# Related work and the contribution boundary

This repository addresses the **fixed-target CoreFalcon** signing loop: one
fresh salt determines a syndrome, and private Gaussian sampling repeats at
that syndrome until the norm test passes. The additional analytic result is
a concrete bound on how much the norm-acceptance probability varies across
syndromes, uniformly over the stated short-basis lattice class. Together with
an accepted-image density bound, this supplies the reverse Rényi moments
used in [the security transfer](../science/security_transfer.md).

The problem, the signature framework, and the main analytic tools have
substantial prior history. The contribution claimed here is the quantitative
coset estimate at the original Falcon parameters and its consequence for the
named fixed-target model. It is not the invention of Gaussian smoothing,
the circle method, accepted-distribution analysis, or Rényi-based security
reductions. [The analytic theorem](../science/norm_tail_smoothing.md) and
[the parameter note](../science/falcon_parameters.md) state its exact scope.

## 1. The closest signature results

### A Closer Look at Falcon

[Fouque, Gajland, de Groote, Janneck, and Kiltz](https://eprint.iacr.org/2024/1769)
explicitly identify the difficulty of simulating norm-conditioned preimages
at a fixed target. Their §4, Figure 6, defines **CoreFalcon** and
**CoreFalcon+**; the latter refreshes its salt after rejection. The discussion
on printed pages 6 and 16 explains why their proof covers the refreshing
variant. Footnote 11 separates compression retries from this norm-only
abstraction.

We inherit their formulation of the problem, the multi-target R-ISIS
framework, and their FFO sampler analysis (Lemma 7 and Appendix F.3).
Our SUF theorem uses Beckmann--Majenz's unconditioned Gaussian SPISIS*
variant, rather than the norm-conditioned R-SPISIS game in Fouque et al.,
Figure 5. Their Appendix C applies distribution changes
before the norm test and counts attempted samples. The new estimate instead
controls the accepted law at one retained target. This distinction is what
allows the original CoreFalcon retry rule to be analysed. It does not turn
the underlying NTRU hardness assumptions into reductions from ordinary SIS.

### Quantum oracle distribution switching

[Beckmann and Majenz, arXiv v3](https://arxiv.org/abs/2602.16268v3),
Theorem 5 and Appendix E.1, analyse **CoreFalcon+**; Figure 9 on printed
page 70 displays both retry rules. Their Lemma 6 supplies adaptive
reprogramming with distribution switching. We use that established technique
when discussing quantum hash access, with classical signing queries.

An accepted-image estimate does not remove quantum reprogramming or
extraction costs. In particular, the Rényi loss reported for a transcript
transfer is not by itself an overall concrete QROM security level. The
separate terms are retained in the security theorem.

### Basis-specific improvements

[Jia, Zhang, Yu, and Tang](https://eprint.iacr.org/2026/096) improve the
concrete analysis by using the GS profile of each basis. In the inspected
full version, Theorem 2 and Corollary 1, page 12, bound the unconditioned
Klein--GPV sampler; Theorem 3, pages 13--14, bounds dual Gaussian mass; and
Theorem 4, page 14, bounds unconditioned quotient uniformity. Their §3.1,
page 8, retains the fresh-salt retry rule.

These estimates are relevant refinements of the sampler and image terms.
They do not supply the norm-conditioned acceptance profile needed here.
Our uniform theorem uses the key-generation GS ceiling, without an empirical
typical-key profile. Basis-specific refinements could be combined with it;
the present claim does not depend on doing so.

### FALCON++

[Yan and Zhao](https://eprint.iacr.org/2026/2226) directly analyse accepted
preimages and construct a corrected, clipped Klein--GPV sampler at smaller
parameters. Their Algorithm 2 and Theorem 1 concern the ambient distribution
after correction acceptance, using fresh syndromes. Theorem 2 bounds
correction-factor moments. The subsequent norm test remains a separate
stage; Figure 4 refreshes the salt after norm rejection.

Appendix A, Claim 4, page 32, erases rejected oracle points and relies on
fresh uniform syndromes. Claim 5 charges candidate transitions before their
norm tests. Lemma 5 and Appendix C.1 provide a global norm-tail bound. These
statements do not bound the variation of norm acceptance across fixed
syndromes. We credit their accepted-law analysis while distinguishing its
correction mechanism and distribution from the unchanged coset Gaussian
conditioned on the norm. Their §5.2 explicitly states the transition
assumptions attached to their security theorems.

## 2. The analytic predecessors

### Gaussian smoothing and Rényi analysis

The Gaussian trapdoor and hash-and-sign framework is due to
[Gentry, Peikert, and Vaikuntanathan](https://eprint.iacr.org/2007/432),
building on lattice smoothing developed by
[Micciancio and Regev](https://doi.org/10.1137/S0097539705447360).
The use of Rényi divergence for tighter lattice security proofs predates
this work; see
[Bai et al.](https://doi.org/10.1007/978-3-662-48797-6_1) and
[Prest](https://doi.org/10.1007/978-3-319-70694-8_13).
Fast Fourier orthogonalization is due to
[Ducas and Prest](https://doi.org/10.1145/2930889.2930923).
Our sampler profile is imported through the later explicit FFO analysis of
Fouque et al.; it is not a new sampler theorem.

### Smoothing codes and lattices

[Debris-Alazard, Ducas, Resch, and Tillich](https://eprint.iacr.org/2022/615)
systematically combine Parseval, Cauchy--Schwarz, geometric counting, and
mixtures of uniform-ball distributions. In the inspected full version,
Proposition 4.1 gives Fourier smoothing for densities on the continuous
quotient, Proposition 4.5 transfers ball bounds to Gaussian bounds, and
Theorems 4.17--4.19 give worst-case lattice estimates.

The present distribution is discrete, on the finite quotient
$`\mathbb Z^d/\Lambda`$. Its hard integer-norm cutoff creates rational
frequency aliases, including the parity arc. A continuous-ball estimate
does not automatically control those aliases. We inherit the Fourier
smoothing strategy and use a short-GS-basis promise and explicit arithmetic
of the finite quotient to obtain the concrete estimate needed here.

### Discrete Gaussians modulo sublattices

[Jin, Liu, Wang, and Gu](https://eprint.iacr.org/2024/1695) give entropy
bounds for Gaussians modulo sublattices and new leftover hash lemmas.
Theorems 4.1 and 4.5 concern untruncated Gaussian entropy. Corollary 5,
page 20, treats truncation at radius $`s\sqrt N`$ in the
$`\exp(-\pi\|x\|^2/s^2)`$ convention: this is
$`\sqrt{2\pi}`$ times the corresponding Gaussian scale times $`\sqrt N`$,
rather than Falcon's factor 1.1. Its proof uses retained total mass and an
upper bound on each coset mass.

That argument does not establish the small variance of the rejection
profile or the reverse moments required here. Their Theorem 5.3 and
Corollary 9 additionally use an independent uniform matrix; they do not
quantify over every honestly generated NTRU map with the GS promise.
These are differences in the stated hypotheses and conclusions, not a
claim that their techniques cannot be adapted.

### The discrete circle method

[Magyar's 1997 paper](https://ems.press/journals/rmi/articles/5173) is a
direct precursor for the method. Equations (5) and (9), printed pages
308--309, express discrete spherical measures through Gaussian kernels and
apply Minkowski's inequality. The rational-arc analysis and Lemma 1,
pages 309--311, use Poisson summation and quadratic Gauss sums.

The present proof adapts those established tools to a Gaussian-weighted
integer-norm tail on a finite lattice quotient. The additional work is the
coset summation without a quotient-size factor, the GS-based theta bounds,
separate treatment of the zero and parity arcs, and explicit constants
usable in a signature proof. Calling the circle method itself new would
misidentify the contribution.

## 3. What the new estimate must provide

A small overall rejection probability is insufficient for the signing
argument. Let $`a_y`$ be the probability of passing the norm test under the
ideal Gaussian in syndrome $`y`$. Fixed-target signing keeps the target
uniform and returns an accepted conditional preimage. Sampling an ambient
Gaussian until acceptance instead reweights targets by their Gaussian mass
and their $`a_y`$. The proof must control this reweighting.

At the original Falcon parameter sets, the
[validated numerical certificate](../science/numerical_certificate.md)
establishes the sufficient bounds
$`\mathrm{Var}_{U}(a_y)<2^{-90}`$ and $`2^{-120}`$, respectively.
It also bounds the accepted ambient image's chi-square distance from uniform
by $`2^{-81}`$ and $`2^{-83}`$. A positive pointwise density floor then
converts that estimate into the required reverse Rényi moments. The security
argument also accounts for conditioning the approximate sampler; it does
not discard sampler error when introducing the norm test.

The resulting scope is narrower than that of
[Aerie](https://eprint.iacr.org/2026/2501), Appendix C: Aerie's
common/caller-controlled salt and padded byte-format setting is not covered
by the fresh-initial-salt norm theorem. In particular, this work does not
discharge Aerie's Assumption C.8. The coordinate-cap extension likewise does
not establish a theorem for a fixed total byte budget.

## 4. Versions and inspection provenance

The comparisons above refer to the following primary versions. Page and
theorem numbers refer to the inspected full text, not to a later proceedings
layout. Metadata and links were checked on **27 October 2026**.

| Work | Inspected version and principal locations |
|---|---|
| Falcon specification | [v1.2, 1 October 2020](https://falcon-sign.info/falcon.pdf); parameter formulas, key generation, signing, verification, and formats. |
| A Closer Look at Falcon | Full version revised 2 March 2026; [primary PDF capture, 20 April 2026](https://web.archive.org/web/20260420175834id_/https://eprint.iacr.org/2024/1769.pdf); pp. 4--7, §4, Appendix C, and Appendix F.3. |
| Beckmann--Majenz | [arXiv:2602.16268v3, 9 September 2026](https://arxiv.org/abs/2602.16268v3); Lemma 6, Theorem 5, and Appendix E.1. |
| Jia et al. | EPrint received 21 January 2026; [primary PDF capture, 25 January 2026](https://web.archive.org/web/20260125000957id_/https://eprint.iacr.org/2026/096.pdf); §3.1 and Theorems 2--4. Publication metadata separately verified at [PKC 2026, pp. 334--363](https://doi.org/10.1007/978-3-032-26731-3_11). The proceedings full text was not used for the comparison. |
| FALCON++ | EPrint received 26 September 2026; [primary PDF capture, 28 September 2026](https://web.archive.org/web/20260928162343id_/https://eprint.iacr.org/2026/2226.pdf); §§2.3--5, §6.1, Appendix A, and Appendix C.1. |
| Jin et al. | Full version revised 4 July 2025, associated with PKC 2025; [primary PDF capture, 7 March 2026](https://web.archive.org/web/20260307233136id_/https://eprint.iacr.org/2024/1695.pdf); Theorems 4.1, 4.5, and 5.3, Corollaries 5 and 9, and Remark 5.4. |
| Smoothing Codes and Lattices | [CWI-hosted full version, 8 September 2022](https://ir.cwi.nl/pub/32681/32681D.pdf), especially §4; journal publication is [IEEE TIT 69(9), 2023](https://doi.org/10.1109/TIT.2023.3276921). |
| Magyar | [Published 1997 article](https://ems.press/journals/rmi/articles/5173), pp. 307--317; especially the Gaussian contour and rational-arc estimates on pp. 308--311. |

Archived primary PDFs were used where live ePrint PDF retrieval was
unavailable. Their bytes are not asserted to be identical to any unexamined
live endpoint. This comparison identifies the relevant statements in the
listed versions; it is not an exhaustive absence claim about the literature.
Machine-readable citations, including the numerical backend, are in
[bibliography.bib](bibliography.bib).
