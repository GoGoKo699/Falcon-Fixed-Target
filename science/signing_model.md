# Signing model and public representation

The scheme analyzed here draws a fresh random salt for each signing query, hashes the message once, and keeps that target throughout its private norm-rejection loop. The mathematical sampler is the exact-arithmetic FFO sampler analyzed by Fouque et al. The security argument returns to the original fixed-target retry policy without changing the lattice parameters.

The norm-conditioned distribution is the subject of [the smoothing theorem](norm_tail_smoothing.md). [The security-transfer theorem](security_transfer.md) connects that distribution to unforgeability. This page defines the algorithms, oracle access, sampler contract, and representation map on which that connection depends.

## 1. Ring, lattice, and parameters

Let $`n\in\{512,1024\}`$, $`d=2n`$, $`q=12289`$, and

```math
\mathcal R=\mathbb Z[X]/(X^n+1),
\qquad \mathcal R_q=\mathcal R/q\mathcal R.
```

All Euclidean norms use coefficient embeddings. Write a preimage as $`z=(u,v)\in\mathcal R^2\simeq\mathbb Z^d`$, with syndrome map

```math
F_h(u,v)=u+hv\pmod q,
\qquad
\Lambda_h=\ker F_h.
```

The coefficient of $`u`$ is the identity, so $`F_h`$ is surjective for every $`h`$. Consequently $`[\mathbb Z^d:\Lambda_h]=q^n`$ and $`Y=\mathbb Z^d/\Lambda_h`$ is identified with $`\mathcal R_q`$. This fact does not require $`h`$ to be a unit.

The norm predicate uses an integer threshold $`T`$. Its complement begins at $`K=T+1`$ because the squared norm is integral:

```math
A(z)=\mathbf 1[\|z\|^2\le T],
\qquad
\neg A(z)=\mathbf 1[\|z\|^2\ge K].
```

| Parameter | Degree 512 | Degree 1024 |
|---|---:|---:|
| Coefficient dimension $`d`$ | 1024 | 2048 |
| Modulus $`q`$ | 12289 | 12289 |
| Gaussian width parameter $`\sigma`$, approximately | 165.73661718297759 | 168.38857144654394 |
| Accepted squared norm $`T`$ | 34,034,726 | 70,265,242 |
| First rejected squared norm $`K`$ | 34,034,727 | 70,265,243 |
| Salt length $`\kappa`$ | 320 bits | 320 bits |
| FFO smoothing parameter $`\epsilon`$ | $`2^{-35.5}`$ | $`2^{-36}`$ |

The exact width is defined by the formula in [the parameter page](falcon_parameters.md), rather than by the displayed decimal approximation. Gaussian masses in these pages use

```math
\rho_\sigma(z)=\exp\!\left(-\frac{\|z\|^2}{2\sigma^2}\right).
```

The symbol $`\sigma`$ is the Gaussian width parameter in the continuous-Gaussian standard-deviation convention; it need not equal the standard deviation of a discrete Gaussian law. A source using $`\exp(-\pi\|z\|^2/s^2)`$ has $`s=\sqrt{2\pi}\sigma`$.

## 2. Key-generation and sampler contracts

Let $`\mathsf{Gen}`$ be the idealized NTRU trapdoor-generation distribution used in the Falcon analysis. It returns a public key $`h`$ and a secret module basis, together with its FFO sampling tree. The assumptions below are required for every key in its support.

First, the generated lattice admits the expanded integral basis with

```math
\|\widehat B\|_{\mathrm{GS}}\le\gamma,
\qquad \gamma=1.17\sqrt q.
```

Second, the FFO leaf widths satisfy the hypothesis of the FFO sampling theorem. These are compatible consequences of the key-quality condition, but they serve different purposes: the expanded-basis bound controls the dual theta series; the leaf-width bound controls the actual FFO distribution. The coefficient-splitting operator and leaf identity in Fouque et al., Appendix F.3, pp. 42–43, connect the FFO tree to the Gram–Schmidt lengths of the expanded basis. [The parameter page](falcon_parameters.md#the-ffo-leaf-width-hypothesis) gives the basis-order argument explicitly. No equality between the output laws of an arbitrarily ordered Klein sampler and FFO is assumed. [Fouque et al., Lemma 7 and §F.3](https://eprint.iacr.org/2024/1769).

For each syndrome $`y`$, define the ideal coset Gaussian

```math
G_y(z)=
\frac{\rho_\sigma(z)}{\rho_\sigma(F_h^{-1}(y))}
\mathbf 1[F_h(z)=y].
```

Write $`P_y`$ for the exact-arithmetic FFO preimage distribution at that syndrome. The imported FFO theorem and its proof give a uniform pointwise sandwich

```math
a_{\mathrm{FFO}}\le\frac{P_y(z)}{G_y(z)}\le b_{\mathrm{FFO}},
\qquad
b_{\mathrm{FFO}}=
\left(\frac{1+\epsilon/d}{1-\epsilon/d}\right)^d,
\qquad
a_{\mathrm{FFO}}=b_{\mathrm{FFO}}^{-1}.
```

The reciprocal lower bound uses the normalization-product argument in the proof of Lemma 20, printed p. 41, transported to FFO by its exact product formula in Lemma 22 and the conclusion of Appendix F.3, pp. 43–45. The relative-error statement in Lemma 7 alone would give the weaker lower bound $`2-b_{\mathrm{FFO}}`$.

This is the profile used by the numerical security calculation. Its hypothesis is $`\sigma\ge\eta_\epsilon(\mathbb Z^d)\gamma`$ in the source's Gaussian convention, which the exact standard parameter formula satisfies. The profile concerns the mathematical FFO algorithm with its specified one-dimensional Gaussian draws. Floating-point rounding, finite-precision Bernoulli routines, PRNG instantiations, and platform-specific behavior require their own distributional analysis before an implementation inherits the theorem. [Fouque et al., Lemmas 3–4 and 7, §4.1, and Lemma 22](https://eprint.iacr.org/2024/1769).

## 3. Hash and query model

The hash is an ideal random oracle

```math
H:\mathsf{PK}\times\{0,1\}^{\kappa}\times\mathsf M\longrightarrow\mathcal R_q.
```

Tuples have an unambiguous encoding and the protocol's domain separation. The theorem concerns one honestly generated public key. Including that public key in the hash input matches the CoreFalcon framework; a one-key theorem can also use the legacy fixed-key domain by identifying its inputs with the corresponding slice. This observation is not a multi-user or cross-protocol reduction.

The adversary makes at most $`q_S`$ **classical** signing queries and $`q_H`$ hash queries. In the ROM, hash queries are classical. In the QROM, they may be quantum superposition queries. Signing messages may depend adaptively on the entire previous interaction.

For every signing query, the signer draws its salt uniformly and independently after receiving the message. Sampler coins are fresh and independent across attempts and queries. The adversary receives the final signature or a declared public error. It does not receive retry counts, intermediate preimages, or running times. If bounded-time signing is used, the attempt cap and its error behavior are specified separately below.

For finite adversarial running time, the hash domain may be restricted to the finite set of encodings of the permitted length. The reduction does not require sampling or storing an exponential random-oracle table.

## 4. Mathematical signing and verification

### Signing

The core signature is the pair $`(r,v)`$.

```text
Sign(sk, h, m):
    sample r uniformly from {0,1}^kappa
    y := H(h, r, m)
    repeat:
        sample (u, v) from P_y using fresh private coins
    until ||(u, v)||^2 <= T
    return (r, v)
```

The same salt and syndrome are used in every iteration. This is the `Sign`/`Sgn` policy called CoreFalcon in the cited analyses, whereas CoreFalcon+ resamples a salt and target on every iteration. [Fouque et al., Figure 6 and §4](https://eprint.iacr.org/2024/1769); [Beckmann–Majenz, Figure 9, p. 70](https://arxiv.org/pdf/2602.16268v3).

### Verification and extraction

For odd $`q`$, let $`\operatorname{ctr}_q`$ denote coefficientwise reduction into
$`\{-(q-1)/2,\ldots,(q-1)/2\}`$. Verification reconstructs the omitted component:

```text
Verify(h, m, (r, v)):
    check the declared salt and signature syntax
    y := H(h, r, m)
    u_hat := ctr_q(y - h*v)
    return [||(u_hat, v)||^2 <= T]
```

A valid signature therefore supplies the short preimage $`(\widehat u,v)`$ of its hash target.

The sampled component $`u`$ need not equal $`\widehat u`$. Each centered representative minimizes absolute value among its integer lifts, so

```math
F_h(\widehat u,v)=F_h(u,v),
\qquad
\|(\widehat u,v)\|\le\|(u,v)\|.
```

This distinction matters for degree 1024, where $`\sqrt T>q/2`$. For degree 512, the accepted norm bound is below $`q/2`$, so every accepted $`u`$ is already centered. The distributional proof always analyzes the original sampled pair; the representation and extraction maps are then applied explicitly.

## 5. Three accepted laws that must remain distinct

Let $`G=D_{\mathbb Z^d,\sigma}`$ be the ambient spherical integer Gaussian, and let $`U`$ be uniform on $`Y`$. Define

```math
\mu(y)=\Pr_{Z\leftarrow G}[F_h(Z)=y],
\qquad
a_y=\Pr_{Z\leftarrow G_y}[A(Z)],
\qquad
\widehat a_y=\Pr_{Z\leftarrow P_y}[A(Z)].
```

The quotient densities and global rejection probability are

```math
p(y)=|Y|\mu(y),
\qquad
r(y)=|Y|\Pr_{Z\leftarrow G}[F_h(Z)=y,\neg A(Z)],
\qquad
\delta=\mathbb E_U r=\Pr_{Z\leftarrow G}[\neg A(Z)].
```

Thus $`a_y=1-r(y)/p(y)`$. The norm theorem bounds the actual quantities

```math
Q_0=\|p-1\|_{L^2(U)},
\qquad
R=\|r-\delta\|_{L^2(U)},
```

and supplies a uniform bound $`1-a_y\le D_0`$.

After fresh-target resampling in the proof, the real accepted joint law is

```math
L(y,z)=U(y)P_y(z\mid A).
```

The public simulator uses a different, exactly sampleable law:

```math
J(y,z)=\nu(y)G_y(z\mid A)
      =G(z\mid A)\mathbf 1[F_h(z)=y],
\qquad
\nu(y)=\frac{\mu(y)a_y}{1-\delta}.
```

It samples an ambient Gaussian until the norm test succeeds, computes its syndrome, and programs that syndrome at the fresh salt/message input. Its accepted-image density is

```math
|Y|\nu(y)=\frac{p(y)-r(y)}{1-\delta}.
```

For comparison, repeatedly choosing a *uniform syndrome*, drawing from its ideal coset Gaussian, and restarting both on failure would give target law

```math
\widetilde\nu(y)=\frac{U(y)a_y}{\mathbb E_U a_y}.
```

In general $`\widetilde\nu\ne\nu`$. Variance bounds for $`a_y`$ alone compare fixed-target signing with this uniformly chosen-target retry experiment. They do not identify the public simulator's law. The security theorem uses $`J`$ and controls $`\nu`$ through both $`Q_0`$ and $`R`$.

## 6. Canonical compressed output

A concrete representation can apply the canonical compressed codec to the mathematical signature. The explicit wrapper analyzed here uses the full sufficient output buffer, emits the unique compressed representation when it exists, and returns $`\bot`$ on encoding failure. Verification accepts this one compressed format only.

The reference codec requires $`|v_i|\le2047`$. A coefficient uses one sign bit, seven low bits, and a unary encoding of the high part, for a total of

```math
9+\left\lfloor\frac{|v_i|}{128}\right\rfloor
```

bits. The signature also contains a one-byte header and the 40-byte salt. If $`\|v\|^2\le T`$, Cauchy–Schwarz gives

```math
\sum_i\left\lfloor\frac{|v_i|}{128}\right\rfloor
\le
\left\lfloor\frac{\sqrt{nT}}{128}\right\rfloor.
```

Therefore any norm-passing, coefficient-encodable vector fits in

```math
41+
\left\lceil
\frac{9n+\lfloor\sqrt{nT}/128\rfloor}{8}
\right\rceil
```

bytes: 746 for degree 512 and 1455 for degree 1024. Both fit inside the reference maximum compressed buffers of 752 and 1462 bytes. These integer checks are included in [the transfer certificate](../verification/core_transfer_bounds.py). The reference compressed signing path returns an error rather than retrying when compression fails; the padded path has an additional retry policy. [Reference codec](https://falcon-sign.info/impl/codec.c.html); [signing API](https://falcon-sign.info/impl/falcon.c.html); [size definitions](https://falcon-sign.info/impl/falcon.h.html).

For EUF-CMA, the wrapper and verifier are handled by the explicit decoding/extraction map. For SUF-CMA, arbitrary public postprocessing is not sufficient: a hidden vector that caused an error must not have a valid admissible encoding of the same transmitted component. The sufficient buffer and coefficient restriction ensure this condition. A successful new canonical compressed signature at an already signed input has a different $`v`$ from the returned one. If the signer returned $`\bot`$, its hidden $`v`$ was not encodable in the admitted format, so a valid forged $`v`$ is again different. In both cases the extracted full preimage differs from the challenge preimage, regardless of whether the omitted component is recentered.

An undersized caller buffer does not satisfy this SUF argument. Neither does a verifier that accepts multiple equivalent compressed, padded, or constant-time encodings as distinct signatures. A scheme allowing such representations needs either an equivalence-aware freshness definition or a separate analysis.

## 7. Unforgeability and termination

In EUF-CMA, a successful forgery verifies and its message was never submitted to the signing oracle. This definition records all requested messages, including requests that returned a public error. In SUF-CMA, a successful forgery verifies and its exact message/signature pair was never returned successfully. The signing queries remain classical in both the ROM and QROM formulations.

The accepted-law model uses an unbounded retry loop with bounded expected running time. Indeed, the sampler profile gives

```math
\Pr_{P_y}[\neg A]\le b_{\mathrm{FFO}}D_0<1
```

uniformly in the key and syndrome. An implementation of the mathematical model may cap each query at $`\ell`$ attempts and return $`\bot`$ when the cap is reached. Coupling it with the unbounded signer changes any adversarial success probability by at most

```math
q_S(b_{\mathrm{FFO}}D_0)^\ell.
```

For $`q_S\le2^{64}`$, the certified choices $`\ell=32`$ at degree 512 and $`\ell=16`$ at degree 1024 make this error smaller than $`2^{-390}`$. The public reduction has its own finite Gaussian-pool budget, treated separately in [the security proof](security_transfer.md#6-a-finite-public-gaussian-pool).

The model establishes no retry-count or timing-leakage guarantee. It also does not cover caller-chosen or reused salts, deterministic signing, fixed padded-length rejection, or finite-precision sampling. Those changes affect a stated hypothesis or distribution and need their own proof.

## Sources

- Fouque, Gajland, de Groote, Janneck, Kiltz, [*A Closer Look at Falcon*](https://eprint.iacr.org/2024/1769), full version dated 2 March 2026. Relevant locations: Lemmas 3–4 and 7; Figure 6 and §4.1; Appendix F.3, especially the leaf identity and Lemma 22.
- Beckmann, Majenz, [*Quantum Oracle Distribution Switching and Applications to Falcon and Ring Signatures*, v3](https://arxiv.org/pdf/2602.16268v3), 9 September 2026. Relevant locations: Figure 9 and Appendix E.1.
- Falcon reference implementation: [codec](https://falcon-sign.info/impl/codec.c.html), [signing and verification API](https://falcon-sign.info/impl/falcon.c.html), and [format and buffer definitions](https://falcon-sign.info/impl/falcon.h.html).
