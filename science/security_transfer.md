# Security transfer for fresh-salt, fixed-target signing

This page proves how the norm-conditioned smoothing bound gives an unforgeability reduction for the [signing model](signing_model.md). The principal corollary is in the classical random-oracle model. A QROM corollary uses established adaptive reprogramming and measure-and-reprogram techniques, with their query and runtime costs stated explicitly.

The reduction samples the accepted **ambient** Gaussian distribution. Its target law contains both the unconditioned Gaussian-image weights and the norm-acceptance probabilities. The [signing model](signing_model.md#5-three-accepted-laws-that-must-remain-distinct) distinguishes it from uniform-target retry experiments.

## 1. Analytic and sampler hypotheses

Fix a key generated as in [the model](signing_model.md). The dimension is $`d=2n`$, the quotient has size $`N=|Y|=q^n`$, the accepted squared norm is $`T`$, and the first rejected squared norm is $`K=T+1`$. Let

```math
G=D_{\mathbb Z^d,\sigma},\qquad
A=\{z:\|z\|^2\le T\},\qquad
U=U(Y).
```

For the syndrome map $`F_h`$, use the densities

```math
p(y)=N\Pr_G[F_h(Z)=y],
\qquad
r(y)=N\Pr_G[F_h(Z)=y,A^c],
\qquad
\delta=\mathbb E_U r=\Pr_G[A^c].
```

The actual $`L^2(U)`$ norms are $`Q_0=\|p-1\|_2`$ and $`R=\|r-\delta\|_2`$. The [norm theorem](norm_tail_smoothing.md) supplies certified upper bounds $`\overline Q_0,\overline R`$, together with

```math
Q_0\le\overline Q_0,\qquad
R\le\overline R,\qquad
p(y)\ge1-\eta>0,\qquad
\Pr_{G_y}[A^c]\le D_0<1.
```

The sampler $`P_y`$ is the ideal FFO law, or another explicitly specified sampler satisfying the same declared profile. For a Rényi order $`\rho>1`$, assume

```math
\sup_y\bigl(M_\rho(P_y\|G_y)-1\bigr)\le e_p(\rho),
\qquad
\frac{P_y(z)}{G_y(z)}\le b,
\qquad bD_0<1.
```

All bounds are uniform over the support of key generation, with $`0\le\eta<1`$. Normalization implies $`b\ge1`$. The exact FFO choices for $`b`$ and $`e_p`$ are given in §4.

We use the following three distinct Rényi quantities:

```math
M_\rho(P\|Q)=\sum_x P(x)^\rho Q(x)^{1-\rho},
\qquad
\mathcal R_\rho(P\|Q)=M_\rho(P\|Q)^{1/(\rho-1)},
\qquad
D_\rho(P\|Q)=\ln\mathcal R_\rho(P\|Q).
```

Here $`M_\rho`$ is the unrooted power moment. The multiplicative divergence denoted $`R_\rho`$ in the cited Falcon papers is $`\mathcal R_\rho`$ here; the plain symbol $`R`$ remains the norm-tail $`L^2`$ quantity. The order $`\rho`$ is unrelated to the Gaussian contour exponent used in the analytic proof.

## 2. Conditioning preserves the small excess above one

**Lemma 1 — conditional excess.** Let $`P,Q`$ be distributions, $`M_\rho(P\|Q)<\infty`$, and let $`E`$ have probabilities $`s=P(E)>0`$ and $`t=Q(E)>0`$. Then

```math
M_\rho(P\mid E\;\|\;Q\mid E)-1
\le
\frac{t^{\rho-1}}{s^\rho}
\bigl(M_\rho(P\|Q)-1\bigr).
```

**Proof.** Split the moment over $`E`$ and its complement. When both complementary probabilities are nonzero,

```math
M_\rho(P\|Q)
=s^\rho t^{1-\rho}M_\rho(P_E\|Q_E)
 +(1-s)^\rho(1-t)^{1-\rho}M_\rho(P_{E^c}\|Q_{E^c}).
```

Each conditional moment is at least one. Subtract the corresponding Bernoulli moment
$`s^\rho t^{1-\rho}+(1-s)^\rho(1-t)^{1-\rho}`$, which is also at least one. This gives

```math
M_\rho(P\|Q)-1
\ge s^\rho t^{1-\rho}
       \bigl(M_\rho(P_E\|Q_E)-1\bigr).
```

The cases with a zero complementary probability follow by omitting its zero contribution or by continuity. If $`Q(E)=1`$, finite divergence forces $`P(E)=1`$. This proves the claim.

The lemma bounds the **excess** $`M_\rho-1`$. Multiplying the entire moment by an inverse acceptance probability would introduce a false cost even when $`P=Q`$.

For the signing predicate, put $`d_y=G_y(A^c)`$. The pointwise sampler profile implies

```math
G_y(A)=1-d_y,
\qquad
P_y(A)\ge1-bd_y,
\qquad 0\le d_y\le D_0.
```

The function $`(1-x)^{\rho-1}/(1-bx)^\rho`$ increases for $`0\le x<1/b`$: the numerator of its logarithmic derivative, after putting terms over a common denominator, is $`\rho b-(\rho-1)-bx>0`$. Hence

```math
M_\rho(P_y\mid A\;\|\;G_y\mid A)-1
\le C_\rho e_p(\rho),
\qquad
C_\rho=
\frac{(1-D_0)^{\rho-1}}{(1-bD_0)^\rho}.
```

When $`b`$ is close to one, this factor is close to $`1/(1-D_0)`$. It amplifies the existing moment excess and leaves a zero excess when the two input laws agree.

This lemma concerns the accepted output law. It does not simulate the geometric retry count, which is absent from the signing-oracle output in the model.

## 3. The accepted ambient image and the required reverse moment

Let $`\nu`$ be the syndrome distribution of $`G\mid A`$, and write its density relative to $`U`$ as $`w(y)=N\nu(y)`$. Then

```math
w(y)=\frac{p(y)-r(y)}{1-\delta}.
```

The analytic hypotheses imply

```math
\chi^2(\nu\|U)
=\mathbb E_U[(w-1)^2]
\le\frac{(\overline Q_0+\overline R)^2}{(1-D_0)^2}
=:X_0.
```

Indeed, the numerator of $`w-1`$ is $`(p-1)-(r-\delta)`$, and $`\delta\le D_0`$. Also,

```math
w(y)=\frac{p(y)G_y(A)}{1-\delta}
\ge (1-\eta)(1-D_0)=:m_0>0.
```

The moment needed for changing a uniform hash target to an accepted ambient target is $`M_\rho(U\|\nu)`$, in the reverse direction from the displayed chi-square divergence. A lower bound on $`w`$ is therefore part of the argument.

**Lemma 2 — reverse moment from a density lower bound.** If $`\mathbb E_U w=1`$, $`w\ge m_0>0`$ with $`m_0\le1`$, and $`\mathbb E_U(w-1)^2\le X_0`$, then

```math
M_\rho(U\|\nu)-1
\le
\frac{\rho(\rho-1)}2 m_0^{-\rho-1}X_0
=:e_u(\rho).
```

**Proof.** For $`f(x)=x^{1-\rho}`$, the second derivative is
$`f''(x)=\rho(\rho-1)x^{-\rho-1}`$. Every point between $`1`$ and $`w(y)`$ is at least $`m_0`$. Taylor's theorem at one gives a remainder bounded by $`\rho(\rho-1)m_0^{-\rho-1}(w-1)^2/2`$. On averaging, the linear term vanishes. Finally $`M_\rho(U\|\nu)=\mathbb E_U w^{1-\rho}`$.

The certified parameter bounds permit the convenient outward rounding

```math
X_0<2^{-81}\quad(n=512),
\qquad
X_0<2^{-83}\quad(n=1024).
```

These bounds use both the untruncated Gaussian image and the rejected-tail profile. A bound on $`\mathrm{Var}_U(G_y(A))`$ alone would compare a different pair of experiments; see [the distribution definitions](signing_model.md#5-three-accepted-laws-that-must-remain-distinct).

## 4. An exact moment profile for the ideal FFO sampler

With $`\varepsilon_{\mathrm{des}}=2^{-35.5}`$ at degree 512 and $`2^{-36}`$ at degree 1024, Fouque et al., Lemma 7 and its Appendix F.3 proof, supply

```math
a\le\frac{P_y(z)}{G_y(z)}\le b,
\qquad
b=\left(\frac{1+\varepsilon_{\mathrm{des}}/d}{1-\varepsilon_{\mathrm{des}}/d}\right)^d,
\qquad a=b^{-1}.
```

The reciprocal lower bound comes from the normalization-product argument in the proof of Lemma 20, printed p. 41. The FFO product formula in Lemma 22 transports that argument to FFO in Appendix F.3, pp. 43–45. The published product formula has likelihood ratio $`c_y\prod_i\xi_i(z)^{-1}`$, where each normalized leaf factor satisfies $`\xi_i(z)\in[(1-\varepsilon_{\mathrm{des}}/d)/(1+\varepsilon_{\mathrm{des}}/d),1]`$. The product lies in $`[1,b]`$; its expectation under $`G_y`$ normalizes the ratio, so $`c_y\in[b^{-1},1]`$. This gives both sides of the sandwich. Lemma 7's relative-error statement alone would only give the lower bound $`2-b`$.

The parameter and leaf-width hypotheses are checked in [the parameter page](falcon_parameters.md). The profile uses the FFO-specific product formula and its coefficient expansion. [Fouque et al., Lemma 7; the proof of Lemma 20, p. 41; and Appendix F.3, pp. 43–45](https://eprint.iacr.org/2024/1769).

Under $`G_y`$, the likelihood ratio $`W=P_y/G_y`$ has mean one. Since $`(W-a)(b-W)\ge0`$,

```math
\mathbb E_{G_y}(W-1)^2\le(b-1)(1-a).
```

Taylor expansion of $`x^\rho`$ at one therefore gives the exact finite-order bound

```math
e_p(\rho)=
\frac{\rho(\rho-1)}2
\max\{a^{\rho-2},b^{\rho-2}\}
(b-1)(1-a).
```

For $`\rho\ge2`$, the maximum is $`b^{\rho-2}`$. The certificate evaluates this finite-order expression. The abstract theorem can use another proven sampler profile by replacing $`e_p`$ and the acceptance lower bound, including its finite-precision effects when applying it to an implementation.

## 5. Adaptive signing is a common channel on independent pairs

After resampling the hash value at each fresh signing input, one signing query uses the joint law

```math
L(y,z)=U(y)P_y(z\mid A).
```

The public simulator uses

```math
M(y,z)=\nu(y)G_y(z\mid A)
      =G(z\mid A)\mathbf 1[F_h(z)=y].
```

Conditioning on $`y`$ and applying the previous lemmas gives

```math
\begin{aligned}
M_\rho(L\|M)
&=\sum_y U(y)^\rho\nu(y)^{1-\rho}
       M_\rho(P_y\mid A\;\|\;G_y\mid A)\\
&\le(1+C_\rho e_p(\rho))(1+e_u(\rho))
=:M_*.
\end{aligned}
```

This compares the target and preimage jointly, so it introduces one event-probability exponent.

### Why adaptive messages do not invalidate the product bound

Fix a generated key pair $`(\mathsf{sk},h)`$. The distributions $`L`$ and $`M`$ depend on that key but not on the message: in the resampled game the target is newly drawn, and the preimage sampler depends on the target and trapdoor. Thus one may sample a list of $`q_S`$ independent pairs before the interaction starts.

A single common procedure consumes the next pair when a signing query arrives. It samples the fresh salt, associates the pair's target with the current message, programs the oracle, and returns the specified representation of the pair's preimage. The procedure also runs the adversary, answers hash queries, and checks freshness and verification at the end. It treats the two input lists identically. Adaptive message selection and repeated messages are internal to this procedure.

The product moment of the two lists is at most $`M_*^{q_S}`$. The key-generation distribution is the same in both games; averaging over keys preserves this bound because it is uniform over their support. The common procedure needs the public key and the supplied pairs, so after the distribution change it does not need the secret key.

For a quantum adversary, condition on a classical pair list and average over the common background oracle and all other randomness. The resulting probability of any final test is a number $`g(\text{list})\in[0,1]`$. Hölder's inequality gives

```math
\Pr_L[E]
\le
M_*^{q_S/\rho}\Pr_M[E]^{(\rho-1)/\rho}.
```

This is classical Rényi data processing through a common interaction procedure with quantum output. Only the classical pair list changes; the procedure handles the adaptive messages and oracle interaction.

The adversary's initial quantum advice is independent of the random oracle. Any oracle-dependent preparation must be included in its query count. Signing queries are classical throughout.

## 6. A finite public Gaussian pool

The public simulator can be described without any trapdoor:

```text
Before running the adversary:
    sample C independent vectors from G
    retain the first q_S vectors satisfying the norm predicate A
    if fewer than q_S were retained, abort the simulation

On the j-th signing query m:
    take retained vector z_j=(u_j,v_j)
    sample a fresh uniform salt r_j
    program H(h,r_j,m) := F_h(z_j)
    return the specified representation of (r_j,v_j)
```

Here $`C\ge q_S`$. Let $`\pi_C`$ be the probability that preprocessing obtains enough accepted vectors. Since the ambient norm rejection probability is $`\delta`$,

```math
1-\pi_C
=\Pr[\mathrm{Bin}(C,\delta)>C-q_S]
\le
\Pr[\mathrm{Bin}(C,D_0)>C-q_S]
=:\varepsilon_{\mathrm{pool}}.
```

**Lemma 3 — exact pool conditioning.** Conditional on successful preprocessing, the retained list has law $`(G\mid A)^{q_S}`$. Its conditional law is identical for every successful acceptance pattern.

**Proof.** Conditional on the entire Boolean acceptance pattern of the $`C`$ independent draws, the accepted values are independent with law $`G\mid A`$; the rejected values have law $`G\mid A^c`$. The retained list always consists of the first $`q_S`$ accepted values. Its law is therefore the same for every successful pattern. The ambient Gaussian and norm predicate do not depend on the key or oracle, so the retained-list statement also holds jointly with the key, background oracle, and adversary's initialization.

If $`\varepsilon_\infty`$ is the public simulator's forging probability with an unlimited accepted list and $`\varepsilon_C`$ its probability with the finite pool, then

```math
\varepsilon_C=\pi_C\varepsilon_\infty,
\qquad
\varepsilon_\infty
\le\frac{\varepsilon_C}{1-\varepsilon_{\mathrm{pool}}}.
```

The displayed theorems use this exact multiplicative pool factor.

The pool consumes at most $`Cd`$ one-dimensional public Gaussian draws and $`q_S`$ syndrome computations. Only the accepted list is programmed, so the number of oracle programs is $`q_S`$, not $`C`$. The Gaussian sampling primitive retains its declared expected running time; bounding the number of calls alone is not a finite-precision implementation proof.

For $`q_S=2^{64}`$, the certified budgets

```math
C=2^{64}+2^{50}\quad(n=512),
\qquad
C=2^{64}+2^{36}\quad(n=1024)
```

give $`\varepsilon_{\mathrm{pool}}<2^{-1000}`$. The certificate uses the binomial Chernoff bound at the first failing integer count $`C-q_S+1`$.

## 7. Hardness games and extraction

Both hardness games use the signer's actual $`\mathsf{Gen}`$ distribution for the public key.

### Uniform-target NTRU-ISIS

The game $`t\text{-}\mathsf{NTRU\mbox{-}ISIS}_{n,q,T}`$ is:

1. Draw $`(\mathsf{sk},h)\leftarrow\mathsf{Gen}`$ and discard the secret key.
2. Independently sample $`c_1,\ldots,c_t\leftarrow U(\mathcal R_q)`$.
3. Give $`(h,c_1,\ldots,c_t)`$ to the solver.
4. The solver returns $`(j,u,v)`$ and wins if $`j\in\{1,\ldots,t\}`$, $`u+hv=c_j\bmod q`$, and $`\|(u,v)\|^2\le T`$.

Write its solver advantage as $`I_t(B)=\mathrm{Adv}^{t\text{-}\mathrm{ISIS}}(B)`$. A quantum solver receives the same classical challenge. This is the one-key inhomogeneous NTRU problem used in the cited Falcon analyses. Its relationship to ordinary NTRU-SIS hardness must be supplied separately when making a numerical hardness estimate. [Fouque et al., Definition 10 and Figure 5](https://eprint.iacr.org/2024/1769); [Beckmann–Majenz, Definition 20 and Figure 6](https://arxiv.org/pdf/2602.16268v3).

### Unconditioned Gaussian NTRU-SPISIS*

The game $`C\text{-}\mathsf{NTRU\mbox{-}SPISIS}^{*}_{n,q,\sigma,T}`$ is:

1. Draw $`(\mathsf{sk},h)\leftarrow\mathsf{Gen}`$ and discard the secret key.
2. Independently sample $`z_i=(u_i,v_i)\leftarrow G`$ for $`i=1,\ldots,C`$ and set $`c_i=F_h(z_i)`$.
3. Give $`h`$ and every triple $`(c_i,u_i,v_i)`$ to the solver.
4. The solver returns $`(j,u,v)`$ and wins if $`j\in\{1,\ldots,C\}`$, $`F_h(u,v)=c_j`$, $`\|(u,v)\|^2\le T`$, and $`(u,v)\ne(u_j,v_j)`$.

Write its solver advantage as $`S_C(B)=\mathrm{Adv}^{C\text{-}\mathrm{SPISIS}^{*}}(B)`$. The supplied vectors are **not** conditioned on their norms. This is the starred game of Beckmann–Majenz, Figure 6, printed p. 49. It differs from the earlier conditioned-target SPISIS formulation, and the distinction is part of the assumption. [Definition 21 and Remark 2](https://arxiv.org/pdf/2602.16268v3).

The reduction filters these unconditioned challenge vectors using the public pool construction and programs only the retained ones.

### Why the SUF extraction is valid

Separate a successful public-simulator forgery by whether its hash **input** was programmed. At an unprogrammed input, an ISIS reduction applies. At a programmed input, select the challenge index used in the latest program at that input.

For the mathematical signature, a new signature at that same message/salt input has a different transmitted component $`v`$ from any identical signature already returned. Its reconstructed preimage therefore differs from the corresponding challenge vector. Recentring the omitted $`u`$ cannot invalidate this argument because the difference is already in $`v`$.

For canonical compressed signatures, use the sufficient-buffer condition in [the model](signing_model.md#6-canonical-compressed-output). If the signing query returned a signature, uniqueness of encoding gives the same conclusion. If it returned an encoding error, its hidden $`v`$ has no admitted canonical encoding; a valid forged signature cannot encode that same $`v`$. Arbitrary public error-producing postprocessing would not justify this step.

EUF-CMA excludes programmed-input forgeries altogether: every programmed position contains a message previously submitted to the signing oracle. The SPISIS* assumption is therefore needed only for the SUF statement.

## 8. Classical ROM theorem

Let $`\varepsilon_{\mathrm{repr}}^{\mathrm{ROM}}`$ be

```math
\varepsilon_{\mathrm{repr}}^{\mathrm{ROM}}
=\frac{q_Sq_H+\binom{q_S}{2}}{2^\kappa}.
```

At signing query $`j`$, the new salt is independent of the prior transcript. For the chosen message, at most $`q_H+j-1`$ inputs are already present in the oracle table. Until one of those inputs is selected, replacing its target by a newly sampled uniform value is exact. Summing these collision probabilities gives the displayed bound. Later hash queries may depend arbitrarily on the released salt.

**Theorem 1 — ROM security.** Assume the model and the §1 contracts uniformly over the support of $`\mathsf{Gen}`$. Fix $`\rho>1`$ and an integer $`C\ge q_S`$ with $`\varepsilon_{\mathrm{pool}}<1`$. For every classical adversary $`\mathcal A`$ making at most $`q_S`$ signing and $`q_H`$ hash queries, there are classical solvers $`B_{\mathrm I}`$ and, for SUF-CMA, $`B_{\mathrm S}`$ such that

```math
\mathrm{Adv}^{\mathrm{EUF}}(\mathcal A)
\le
\varepsilon_{\mathrm{repr}}^{\mathrm{ROM}}
+M_*^{q_S/\rho}
\left(
\frac{I_{q_H+1}(B_{\mathrm I})}
     {1-\varepsilon_{\mathrm{pool}}}
\right)^{(\rho-1)/\rho},
```

and

```math
\mathrm{Adv}^{\mathrm{SUF}}(\mathcal A)
\le
\varepsilon_{\mathrm{repr}}^{\mathrm{ROM}}
+M_*^{q_S/\rho}
\left(
\frac{
I_{q_H+1}(B_{\mathrm I})
+S_C(B_{\mathrm S})}
{1-\varepsilon_{\mathrm{pool}}}
\right)^{(\rho-1)/\rho}.
```

The theorem covers mathematical signatures and the specified canonical compressed wrapper. A real signer capped at $`\ell`$ trials adds at most $`\varepsilon_{\mathrm{cap}}\le q_S(bD_0)^\ell`$, as in [the model](signing_model.md#7-unforgeability-and-termination). Each bound may be capped at one.

**Proof.** First resample the signing targets, paying $`\varepsilon_{\mathrm{repr}}^{\mathrm{ROM}}`$. Apply the joint-list comparison in §5. Replace the unlimited public simulator by its finite-pool version using Lemma 3.

For the ISIS reduction, assign the supplied independent uniform challenge targets to new, unprogrammed hash inputs as they are first queried. Reserve one additional target for evaluating the final forgery if necessary. Signing programs use the public accepted pairs. A forgery at an unprogrammed input therefore supplies a short preimage of one of the $`q_H+1`$ challenges. The programmed-input SUF case is extracted from the unconditioned SPISIS* pool as described in §7. Summing the disjoint cases proves the bounds.

### Classical resource accounting

Each reduction runs the signature adversary once. It uses at most $`Cd`$ one-dimensional Gaussian draws, $`q_S`$ syndrome evaluations, and a classical oracle table of at most $`q_H+q_S+1`$ entries. An ISIS solver must also read the challenge targets that it uses; the SPISIS* solver receives the Gaussian pool as its challenge input. Balanced-tree or hash-table bookkeeping has the usual dependence on the encoded input length.

The reduction has a finite Gaussian-call budget and ordinary classical storage. Its local work includes public Gaussian sampling, ring arithmetic, and encoded-input handling. Concrete hardness estimates evaluate $`I_t`$ and $`S_C`$ at these full solver resources.

## 9. QROM corollary and explicit oracle semantics

The public program list remains classical. The adversary's hash queries may be quantum, while its signing requests are classical. The adaptive reprogramming result used by Beckmann–Majenz, Lemmas 4 and 6, gives

```math
\varepsilon_{\mathrm{repr}}^{\mathrm{QROM}}
\le
\frac{3q_S}{2}
\sqrt{\frac{q_H+q_S+1}{2^\kappa}}.
```

The signer obtains its target once per signing request. Its private retries add no hash queries or programs. The salt is fresh after the adaptively chosen message, which supplies the required min-entropy. The initial uniform-target reprogramming comparison may use the secret key to generate the real accepted preimage; only after this comparison is the joint classical list changed to the public law. [Beckmann–Majenz, Lemmas 4 and 6, pp. 11 and 16–17](https://arxiv.org/pdf/2602.16268v3).

### A static background oracle with a mutable classical table

For extraction, represent the simulated oracle using a static background function $`H_0`$ and a classical table of overrides. When programming an input $`x`$ for the first time, make one classical query to obtain $`H_0(x)`$ and store both that original value and the desired current value. Reprogramming the same input updates its desired value while preserving its original value.

A quantum query first applies the standard oracle unitary

```math
|x,b\rangle\longmapsto
|x,b\mathbin\oplus\mathrm{enc}(H_0(x))\rangle.
```

A reversible table lookup then XORs $`\mathrm{enc}(H_0(x))\oplus\mathrm{enc}(h_x)`$ at a matching entry, where $`h_x`$ is its desired current value. It acts trivially off the table. This implements the current programmed oracle exactly. It uses one background query per adversarial hash query and at most one extra background query per signing program. Including final verification, the complete oracle algorithm makes at most

```math
Q=q_H+q_S+1
```

queries to $`H_0`$.

The lookup can be compiled as an ordinary reversible circuit containing the classical table. This description requires no QRAM instruction. A straightforward implementation scans up to $`q_S`$ entries per query, so its gate cost is polynomial but not a constant-overhead oracle simulation.

### Extraction from unprogrammed inputs

Apply the single-input measure-and-reprogram theorem to this complete public simulator. Its classical output may include the forged input and signature, the set of programmed inputs, and the list of queried messages. The success predicate checks the appropriate freshness condition, absence of the forged input from the override domain, and the norm equation against the newly supplied uniform target. The theorem permits this auxiliary output. On a successful run, centering the omitted component produces the required ISIS solution.

If the measured point is later overridden by signing, it fails the unprogrammed-input predicate. The static-oracle implementation accounts for the extra queries used to maintain overrides.

For a conservative comparison with Beckmann–Majenz, retain their target-value collision allowance

```math
\varepsilon_{\mathrm{hit}}=
\frac{10Q^2q_S}{|Y|}.
```

The at most $`q_S`$ programmed target values are determined by the pre-sampled accepted Gaussian list, independently of the background oracle. Their compressed-oracle search bound therefore applies. The other unprogrammed-input cases are covered by measure-and-reprogram with loss $`(2Q+1)^2`$. This follows the extraction split in their Appendix E.1, pp. 71–72; the extra nonnegative collision allowance is retained rather than used to claim a tighter quantum reduction. [Beckmann–Majenz, Theorem 1 and Appendix E.1](https://arxiv.org/pdf/2602.16268v3).

**Corollary 2 — QROM security with the single-target reduction.** Under the analytic, sampler, pool, representation, and interface hypotheses of Theorem 1, for every quantum adversary $`\mathcal A`$ with at most $`q_S`$ classical signing requests and $`q_H`$ quantum hash queries, and advice independent of the oracle, there are quantum hardness solvers $`B_{\mathrm I}`$ and, for SUF-CMA, $`B_{\mathrm S}`$ satisfying the following bounds. Define

```math
\varepsilon_{\mathrm{hard}}^{\mathrm{EUF}}
=(2Q+1)^2I_1(B_{\mathrm I})
+\varepsilon_{\mathrm{hit}},
```

and, for SUF-CMA,

```math
\varepsilon_{\mathrm{hard}}^{\mathrm{SUF}}
=\varepsilon_{\mathrm{hard}}^{\mathrm{EUF}}
+S_C(B_{\mathrm S}).
```

Then for either freshness notion,

```math
\mathrm{Adv}(\mathcal A)
\le
\varepsilon_{\mathrm{repr}}^{\mathrm{QROM}}
+M_*^{q_S/\rho}
\left(
\frac{\varepsilon_{\mathrm{hard}}}
     {1-\varepsilon_{\mathrm{pool}}}
\right)^{(\rho-1)/\rho}.
```

**Proof.** Apply the adaptive reprogramming bound to reach the fresh uniform-target game. Use the common classical-list comparison from §5, which applies to the quantum success function, and then the exact finite-pool factor from §6. In the public finite-pool experiment, the unprogrammed-input success probability is bounded by the single-target measure-and-reprogram reduction and the target-hit allowance. A programmed-input SUF forgery gives a SPISIS* solution as in the classical proof; the supplied Gaussian vectors and override list remain classical. EUF excludes this programmed-input case. Substituting the appropriate sum of hardness contributions gives the bound.

The real-signer cap error, when present, is added separately as in Theorem 1.

### Quantum runtime and scope of the corollary

The measure-and-reprogram construction has the explicit query factor above and polynomial local overhead. It also uses the finite public Gaussian pool. To eliminate the ideal background oracle from the hardness solver, a bounded-query random-function simulation can use a sufficiently independent function family evaluated reversibly. This gives polynomial overhead; it is not a claim of near-linear runtime in $`Q`$. The published single-target reduction is likewise stated with runtime polynomial in the query and sampling budgets. [Beckmann–Majenz, Table 1, p. 19](https://arxiv.org/pdf/2602.16268v3).

The optional multi-target small-range alternative in that paper explicitly loads $`t`$ targets into QRAM, uses $`\Theta(t)`$ additional setup work, and changes the resource model. It is not part of the corollary above or an algorithm proposed here. [Beckmann–Majenz, Appendix E.1, p. 72](https://arxiv.org/pdf/2602.16268v3).

Consequently, the classical theorem is the main concrete-security application. The QROM statement carries its programming probability term, quadratic extraction loss, and polynomial simulation overhead; these costs must be included in any quantum work-factor estimate.

## 10. Certified transfer values and their interpretation

If the unlimited public simulator's forging probability is bounded by $`2^{-\lambda_{\mathrm{sim}}}`$, the joint distribution change contributes the exact logarithmic loss

```math
\mathcal L(\rho)
=\frac{\lambda_{\mathrm{sim}}}{\rho}
 +\frac{q_S}{\rho}\log_2 M_*.
```

The [Arb certificate](../verification/core_transfer_bounds.py) evaluates the analytic expressions with rigorous ball arithmetic and checks the following outward-rounded inequalities. For this table, it uses the conservative accepted-image contracts $`X_0=2^{-81}`$ and $`X_0=2^{-83}`$ in the reverse-moment bound. It imports the independently certified norm-tail contracts $`\overline R<2^{-45.59}`$ and $`\overline R<2^{-60.41}`$, then rechecks the accepted-image bounds used here.

| Degree | $`q_S`$ | $`\lambda_{\mathrm{sim}}`$ | Order $`\rho`$ | Transfer loss | Image contribution | Additional sampler cost from norm conditioning |
|---|---:|---:|---:|---:|---:|---:|
| 512 | $`2^{64}`$ | 120 | 73 | $`<3.268`$ bits | $`<0.000398`$ bits | $`<0.000080`$ bits |
| 512 | $`2^{64}`$ | 128 | 75 | $`<3.376`$ bits | $`<0.000409`$ bits | $`<0.000082`$ bits |
| 1024 | $`2^{64}`$ | 256 | 151 | $`<3.387`$ bits | $`<0.000207`$ bits | $`<5\cdot10^{-9}`$ bits |

The values of $`\lambda_{\mathrm{sim}}`$ describe a probability bound entering the transfer. They are not an assertion that the underlying lattice assumptions have those work factors. If a hardness estimate is expressed as $`\mathrm{Adv}(t)\le t\,2^{-\lambda_{\mathrm{hard}}}`$, it must first be evaluated at the reduction's actual work $`t`$ and substituted into the theorem. Query limits, target count, Gaussian-pool size, and reduction runtime remain part of that calculation.

The oracle terms are separate. For $`q_S=2^{64}`$ and $`\kappa=320`$, the certificate gives these illustrative upper-bound expressions:

| Hash-query budget | ROM programming term | QROM programming term |
|---|---:|---:|
| $`q_H=2^{64}`$ | approximately $`2^{-191.415}`$ | approximately $`2^{-62.915}`$ |
| $`q_H=2^{128}`$ | approximately $`2^{-128}`$ | approximately $`2^{-31.415}`$ |

These additive oracle terms, the quantum extraction factor, and simulation work enter separately from the conditional distribution-transfer loss.

## 11. What the theorem establishes

The theorem gives an accepted-output simulation and unforgeability reduction for fresh-initial-salt, fixed-target norm retries at the stated mathematical parameters. It uses the published FFO profile, the new norm-conditioned image estimate, and explicitly stated NTRU-ISIS/SPISIS* games.

The full finite-precision implementation, padded-length retry policy, caller-chosen or reusable salts, deterministic signing, and retry-count or timing exposure are separate models. A multi-user or aggregate-signature theorem also requires its own key and oracle interfaces. None of these extensions is implied solely by the one-key distributional result.

## Sources

- Fouque, Gajland, de Groote, Janneck, Kiltz, [*A Closer Look at Falcon*](https://eprint.iacr.org/2024/1769), full version dated 2 March 2026: sampler profile in Lemma 7 and Appendix F.3; hardness games in Definition 10 and Figure 5; classical proof in Appendix C.
- Beckmann, Majenz, [*Quantum Oracle Distribution Switching and Applications to Falcon and Ring Signatures*, v3](https://arxiv.org/pdf/2602.16268v3), 9 September 2026: measure-and-reprogram in Theorem 1; adaptive reprogramming in Lemmas 4 and 6; starred SPISIS game in Figure 6; Falcon extraction in Appendix E.1.
- Don, Fehr, Majenz, [*The Measure-and-Reprogram Technique 2.0: Multi-round Fiat–Shamir and More*](https://doi.org/10.1007/978-3-030-56877-1_21), CRYPTO 2020: the measure-and-reprogram result quoted as Theorem 1 by Beckmann–Majenz.
