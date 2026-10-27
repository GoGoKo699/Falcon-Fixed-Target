# From Peikert's lattice foundations to fixed-target Falcon

A signer must produce a short integer vector satisfying a public equation.
Its secret lattice basis makes that sampling task efficient. A security proof
must explain how to produce a matching public distribution without the secret
basis. This project studies what happens to that comparison when the signer
keeps the equation's target fixed and repeatedly samples until a norm test
passes.

The educational anchor is **Chris Peikert, _A Decade of Lattice
Cryptography_**: [canonical ePrint record](https://eprint.iacr.org/2015/939),
[published version](https://doi.org/10.1561/0400000074). The section and printed
page numbers below refer to the author version dated **17 February 2016**,
whose ePrint revision is recorded on 18 February 2016. The published survey
appears in _Foundations and Trends in Theoretical Computer Science_ 10(4),
283–424; its pagination differs from the author PDF.

This is the project's one educational anchor. The bridge below supplies the
connections to the current result; the primary papers cited in
[related work](../references/related_work.md) remain the sources for imported
research theorems. The [scientific overview](../science/README.md) and
[signing model](../science/signing_model.md) are authoritative for the
project's definitions and claims.

## 1. The relevant route through the source

The useful route is from lattice cosets, through Gaussian sampling, to the
forward-versus-reverse experiment in a signature proof. It does not require
reading the survey's encryption or advanced-construction chapters.

| Source location in the author version | Foundation it supplies | Connection to this project |
|---|---|---|
| §2.1, p. 6; §2.2.1, pp. 6–7 | Integer vectors, lattices, bases, cosets, and the dual lattice | The kernel lattice, its shifted preimage sets, and the dual frequencies in the [norm-tail proof](../science/norm_tail_smoothing.md) |
| §2.3, pp. 8–10; especially p. 9 and Theorems 2.3.1–2.3.2 | Discrete Gaussian masses, smoothing, and the role of short Gram–Schmidt vectors | The width translation and dual-mass bounds explained below |
| §4.1.1, pp. 18–19; Definition 4.1.1 and equations (4.1.1)–(4.1.2) | The map $`x\mapsto Ax\bmod q`$, its kernel, and inhomogeneous solution cosets | The coefficient form of $`F_h(u,v)=u+hv\bmod q`$ |
| §§4.3.1–4.3.3, pp. 27–29 | Ring elements as blocks of coefficients, structured multiplication matrices, and embedding-dependent norms | The translation from two ring elements to a $`2n`$-dimensional integer vector |
| §5.4.1, p. 44; §5.4.2, Theorem 5.4.2 on p. 46 | A short basis enables sampling from a Gaussian on a chosen coset | Why a secret trapdoor can sample a preimage; the explicit FFO profile is a separate research input |
| §5.4.2, Definition 5.4.3 on p. 47 and the integer instantiation on p. 48 | Preimage-sampleable functions: matching forward and reverse joint distributions | The starting point for comparing the real signer with the public accepted-Gaussian simulator |
| §5.5.1, pp. 53–54; Theorem 5.5.1 | Hash-and-sign, programmable random oracles, and a forgery reduction | The foundation for the project's separately quantified [security transfer](../science/security_transfer.md) |

These pointers identify the statements being used. The exact Falcon
parameters, sharp cutoff estimates, and modern oracle costs come from the
project's science pages, rather than from the 2016 survey.

## 2. From an integer equation to a lattice coset

Peikert's integer construction starts with a matrix $`A`$ and the equation
$`Ax=y\bmod q`$. The solutions for $`y=0`$ form the kernel lattice
$`L^\perp(A)`$. If $`x_y`$ is any solution for a target $`y`$, all solutions
for that target form the translated lattice $`x_y+L^\perp(A)`$.
Thus a target selects a whole set of possible signatures, rather than one
particular vector. [Source: §4.1.1, p. 19; §5.4.2, p. 48.]

Here the public key is a polynomial $`h`$ in

```math
\mathcal R_q=\mathbb Z_q[X]/(X^n+1),
\qquad q=12289,
\qquad n\in\{512,1024\}.
```

The unknown preimage is a pair of integer polynomials $`(u,v)`$. Writing
their coefficients consecutively gives an integer vector $`z\in\mathbb Z^d`$
with $`d=2n`$. The public equation is

```math
F_h(u,v)=u+hv\pmod q=y.
```

If $`M_h`$ is the coefficient matrix for multiplication by $`h`$, this is
exactly the integer equation with matrix $`A_h=[I_n\mid M_h]`$. Its identity
block makes the map surjective. Its kernel $`\Lambda_h`$ therefore has
index $`q^n`$ in $`\mathbb Z^d`$, and the finite quotient
$`Y=\mathbb Z^d/\Lambda_h`$ is identified with the set of syndromes
$`\mathcal R_q`$. The [parameter page](../science/falcon_parameters.md)
establishes these facts and the trapdoor basis bound for mathematical Falcon
keys.

### Notation map

| Peikert's notation or object | Notation and meaning here |
|---|---|
| An input vector in $`\mathbb Z^m`$ | $`z=(u,v)\in\mathbb Z^d`$, with $`d=2n`$ coefficient coordinates |
| $`A\in\mathbb Z_q^{n\times m}`$ and $`f_A(x)=Ax`$ | The structured matrix $`A_h=[I_n\mid M_h]`$ and map $`F_h`$ |
| $`L^\perp(A)`$ | $`\Lambda_h=\ker F_h`$ |
| $`L_y^\perp(A)=x_y+L^\perp(A)`$ | The preimage coset $`F_h^{-1}(y)=x_y+\Lambda_h`$ |
| $`L^*`$ | $`\Lambda_h^*=\{w:\langle w,\lambda\rangle\in\mathbb Z\text{ for every }\lambda\in\Lambda_h\}`$ |
| A short basis $`S`$ and its orthogonalized vectors $`\widetilde S`$ | An expanded integral basis $`\widehat B`$ with every GS length at most $`B_0=1.17\sqrt q`$ |
| $`D_{x_y+L,s}`$ | The ideal coset Gaussian $`G_y`$ in the signing and security pages, with the width conversion below |
| $`R=\mathbb Z[X]/(f(X))`$ in §4.3 | $`\mathcal R=\mathbb Z[X]/(X^n+1)`$; a pair in $`\mathcal R^2`$ supplies $`2n`$ coefficients |
| The canonical embedding denoted $`\sigma`$ in §4.3.3 | An embedding map, distinct from this project's scalar Gaussian width $`\sigma`$ |

The ambient dimension and the ring degree are different quantities. The
survey uses dimension symbols locally; substituting Falcon's degree for every
occurrence of an ambient dimension would lose the factor of two.

The science pages also have a local symbol difference: the norm-tail proof
uses $`G`$ for the finite quotient, whereas the signing and security pages
use $`G`$ for the ambient Gaussian and $`Y`$ for the quotient. This bridge
follows the latter convention.

### The norm and the dual frequencies

This project measures ordinary Euclidean length in the coefficient embedding.
Multiplication by $`X`$ modulo $`X^n+1`$ shifts coefficients and changes one
sign, so it preserves that length. The canonical embedding discussed in
§4.3.3 is useful context, but its norm must not be substituted without a
normalization. For the full **unnormalized** evaluation map at all $`n`$
roots $`\zeta_j`$ of $`X^n+1`$, Fourier orthogonality gives

```math
\sum_{j=0}^{n-1}|a(\zeta_j)|^2
=n\sum_{k=0}^{n-1}|a_k|^2.
```

Under that convention, canonical length is $`\sqrt n`$ times coefficient
length. The Falcon constants in this repository always use coefficient
length. This identity is a local translation of the embedding conventions;
it is not an additional assumption about Falcon keys.

Peikert's dual-lattice definition also explains the frequencies in the
analytic proof. A vector $`w\in\Lambda_h^*`$ defines a character
$`z\mapsto e^{2\pi i\langle w,z\rangle}`$ of the finite quotient. Two dual
vectors differing by an integer vector give the same character on integer
inputs. The character classes are therefore
$`\Lambda_h^*/\mathbb Z^d`$. This is why the proof sums over dual cosets
even though signatures themselves are integer vectors.

## 3. Gaussian width and smoothing: translate before substituting

Peikert's §2.3 uses the Gaussian mass

```math
\rho_s(x)=\exp\!\left(-\pi\|x\|^2/s^2\right).
```

The project uses

```math
\exp\!\left(-\|x\|^2/(2\sigma^2)\right)
=\exp(-\alpha\|x\|^2),
\qquad
s=\sqrt{2\pi}\,\sigma,
\qquad
\alpha=\frac{1}{2\sigma^2}=\frac{\pi}{s^2}.
```

For a continuous Gaussian, the standard deviation of each coordinate is
$`s/\sqrt{2\pi}=\sigma`$. For a discrete Gaussian, these symbols specify
the exponent; its exact variance is not defined to equal $`\sigma^2`$.
The project's displayed widths of about 165.737 and 168.389 are in the
$`\sigma`$ convention. [Source: §2.3, p. 9;
project: [exact parameters](../science/falcon_parameters.md#1-conventions-and-exact-parameters).]

Peikert defines the smoothing parameter $`\eta_\varepsilon(L)`$ as the
smallest width $`s>0`$ for which

```math
\sum_{w\in L^*\setminus\{0\}}
e^{-\pi s^2\|w\|^2}\le\varepsilon.
```

It is a **width threshold**, at a specified tolerance. Its meaning is that
the nonconstant dual frequencies are small enough to make Gaussian masses
on translated copies of the lattice nearly equal. Theorem 2.3.2 relates
this threshold to the largest Gram–Schmidt length, with an asymptotic
$`\sqrt{\log O(d/\varepsilon)}`$ factor. That theorem explains the role of
a short basis; it does not supply the explicit constants used here.

The analytic page instead writes $`\eta_\alpha`$ for a **dimensionless
upper bound on dual mass**. With
$`\vartheta(t)=\sum_{k\in\mathbb Z}e^{-tk^2}`$, its bound is

```math
\sum_{w\in\Lambda_h^*\setminus\{0\}}
e^{-\pi^2\|w\|^2/\alpha}
\le
\vartheta\!\left(\frac{\pi^2}{\alpha B_0^2}\right)^d-1
=:\eta_\alpha.
```

The exponents agree with Peikert's after $`s^2=\pi/\alpha`$.
Consequently, establishing $`\eta_\alpha\le\varepsilon`$ would certify
that $`\sqrt{2\pi}\sigma`$ is at least his smoothing threshold.
But $`\eta_\alpha`$ is not itself that threshold, and the symbols must not
be interchanged. The sampler tolerance and each analytic error bound retain
their explicit values in the local proofs. [Project:
[Gaussian estimates](../science/norm_tail_smoothing.md#gaussian-estimates-from-the-basis-hypothesis).]

There is a second consequential scale difference. The illustrative signature
cutoff in §5.5.1 is $`s\sqrt m`$. With $`m=d`$, this becomes
$`\sqrt{2\pi}\sigma\sqrt d`$. Falcon's cutoff is approximately
$`1.1\sigma\sqrt d`$, with the exact squared threshold
$`T=\lfloor1.1^2d\sigma^2\rfloor`$. A tail statement for the survey's
larger radius cannot be substituted for a statement at Falcon's radius.
The local theorem handles the actual integer event
$`\|z\|^2\ge T+1`$.

## 4. A complete finite example of the three target laws

The following example is an illustrative probability model, not a small
Falcon instance or evidence for a Gaussian bound. It makes the conditioning
operation visible without lattice calculations.

There are two targets, $`0`$ and $`1`$. A public proposal distribution has
three possible outcomes:

| Outcome | Target | Passes the test? | Proposal probability |
|---|---:|---|---:|
| $`z_0^+`$ | 0 | Yes | $`3/8`$ |
| $`z_0^-`$ | 0 | No | $`3/8`$ |
| $`z_1^+`$ | 1 | Yes | $`1/4`$ |

Its unconditioned target distribution is therefore
$`\mu=(3/4,1/4)`$. Conditional on target 0, either of its two outcomes is
equally likely, so its acceptance probability is $`a_0=1/2`$. Target 1
always passes, so $`a_1=1`$. These two vectors, $`\mu`$ and $`a`$, encode
different information: how often a target is proposed and how often a
proposal passes once that target has been selected.

**Fixed uniform target.** Choose the target once with probabilities
$`U=(1/2,1/2)`$, and keep drawing from its conditional distribution until
the test passes. Both targets eventually succeed. The final target law
remains $`(1/2,1/2)`$; the outputs are $`z_0^+`$ and $`z_1^+`$ with those
probabilities.

**Fresh uniform target after each rejection.** Each attempt starts again
with a uniform target. The successful masses per attempt are
$`(U(0)a_0,U(1)a_1)=(1/4,1/2)`$. Their sum is $`3/4`$, so conditioning
on success gives

```math
\widetilde\nu
=\frac{(1/4,1/2)}{3/4}
=(1/3,2/3).
```

**Accepted public proposal.** Draw from the three-row public distribution
until a proposal passes. Now the successful masses are
$`(\mu(0)a_0,\mu(1)a_1)=(3/8,1/4)`$. Their sum is $`5/8`$, giving

```math
\nu
=\frac{(3/8,1/4)}{5/8}
=(3/5,2/5).
```

All three procedures return valid outcomes. Their target probabilities
differ because they make different choices about what to redraw. Counting
one proposal as one attempt, their expected attempt counts also follow
directly:

| Procedure | Final target law | Expected attempts |
|---|---|---:|
| Keep an initially uniform target | $`(1/2,1/2)`$ | $`(1/2)\cdot2+(1/2)\cdot1=3/2`$ |
| Redraw a uniform target each attempt | $`(1/3,2/3)`$ | $`1/(3/4)=4/3`$ |
| Redraw the public proposal each attempt | $`(3/5,2/5)`$ | $`1/(5/8)=8/5`$ |

These counts describe only the toy model. They are not runtime estimates
for Falcon or a comparison of implementation speeds.

For the project, replace the three-row proposal by the ambient integer
Gaussian $`G`$, and the pass test by $`A=\{z:\|z\|^2\le T\}`$. Then

```math
\mu(y)=\Pr_{Z\leftarrow G}[F_h(Z)=y],
\qquad
a_y=\Pr_{Z\leftarrow G_y}[A],
\qquad
\nu(y)=\frac{\mu(y)a_y}{\sum_{y'}\mu(y')a_{y'}}.
```

In the ideal fixed-target signer, targets stay uniform and the accepted
preimage in target $`y`$ has law $`G_y\mid A`$. The public simulator has
that same conditional preimage law but selects targets with probability
$`\nu(y)`$. Uniform-target fresh retries instead give
$`\widetilde\nu(y)=U(y)a_y/\sum_{y'}U(y')a_{y'}`$.
Peikert's forward-versus-reverse perspective identifies the comparison to
make. The new work quantifies it after the sharper acceptance test.
[Project: [the three accepted laws](../science/signing_model.md#5-three-accepted-laws-that-must-remain-distinct).]

## 5. What the anchor supplies and what the project must add

**From short bases to the actual Falcon sampler.** Theorem 5.4.2 explains
why Gram–Schmidt lengths govern Gaussian sampling. The project must still
show that Falcon's polynomial key-quality check implies the needed ordinary
basis bound, and that the FFO leaves meet the sampler theorem's hypotheses.
Those bridges are proved in [keys and parameters](../science/falcon_parameters.md).
The exact-arithmetic FFO probability-ratio profile is imported from the
research literature, not inferred from the survey's asymptotic statistical
distance statement. Finite-precision sampler errors remain separate.

**From ordinary smoothing to the sharp norm cutoff.** Smoothing makes the
unconditioned image $`\mu`$ nearly uniform. Once the norm test is imposed,
the factor $`a_y`$ also matters. The
[norm-tail theorem](../science/norm_tail_smoothing.md) controls the variation
of $`a_y`$ and the accepted image directly, using integer-norm contours,
quadratic Gauss sums, and dual theta bounds. It proves acceptance variances
below $`2^{-90}`$ and $`2^{-120}`$, and accepted-image chi-square distances
below $`2^{-81}`$ and $`2^{-83}`$, at the two parameter sets.
The [numerical certificate](../science/numerical_certificate.md) validates
the explicit inequalities. These statements are additional to the anchor's
smoothing discussion.

**From a forward image bound to the comparison a reduction needs.** The
public simulator chooses $`\nu`$, while the ideal fixed-target signer
chooses $`U`$. If $`v(y)=|Y|\nu(y)`$, the relevant reverse power moment is

```math
M_\rho(U\|\nu)=\mathbb E_{y\leftarrow U}[v(y)^{1-\rho}],
\qquad \rho>1.
```

The exponent is negative, so targets with very small $`v(y)`$ would be
costly. The project combines its forward chi-square bound with a positive
pointwise density floor to control this reverse moment. A separate
conditioning lemma preserves the small excess above one in the actual
sampler's moment bound. These are the local steps in
[security transfer §§2–5](../science/security_transfer.md#2-conditioning-preserves-the-small-excess-above-one);
the survey does not provide their concrete values.

**From a programmable oracle argument to the stated query model.** The
signature explanation in §5.5.1 shows why public forward sampling is useful
to a reduction. Here each signing query receives a fresh 320-bit salt after
its message is chosen, and all norm retries keep the resulting target.
The proof programs one input per signing query and changes the distribution
of a classical list of target/preimage pairs. The
[ROM theorem](../science/security_transfer.md#8-classical-rom-theorem) and
[QROM corollary](../science/security_transfer.md#9-qrom-corollary-and-explicit-oracle-semantics)
account for their distinct programming, extraction, and runtime costs.
Signing queries are classical in both models; quantum hash access is not
permission to make quantum signing queries.

This differs from the informal proof on pp. 53–54, which prepares a pair
for each distinct message queried to its hash oracle. The project pays for
the list change at signing inputs and handles the remaining forgery cases
through its explicit extraction games. Fresh salt generation makes an input
collision unlikely; it does not guarantee distinct inputs or distinct
syndrome values. The oracle bounds retain those collision and programming
costs.

**From the SIS framework to the actual hardness assumptions.** The survey's
integer PSF example uses a nearly uniform public matrix and its corresponding
SIS assumptions. Falcon uses a trapdoor-generated structured NTRU key.
This project's [hardness games](../science/security_transfer.md#7-hardness-games-and-extraction)
retain that key distribution and specify uniform-target NTRU-ISIS and, for
strong unforgeability, unconditioned Gaussian NTRU-SPISIS*. The anchor's
generic SIS discussion does not establish the hardness or concrete work
factor of those games.

These additions lead to the result stated in the
[interpretation](../science/interpretation.md): a security transfer for
fresh-initial-salt, private fixed-target norm retries under the declared
sampler and hardness hypotheses. Canonical compressed output has explicit
buffer and format conditions. Caller-selected or reused salts, padded-length
retries, retry-count leakage, and implementation precision require their
own analysis. The anchor explains the foundations; the linked science
pages establish this particular scope.
