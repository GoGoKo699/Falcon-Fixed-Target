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

The coefficient of $`u`$ is the identity, so $`F_h`$ is surjective for every $`h`$. Consequently $`N=[\mathbb Z^d:\Lambda_h]=q^n`$ and $`Y=\mathbb Z^d/\Lambda_h`$ is identified with $`\mathcal R_q`$. This fact does not require $`h`$ to be a unit.

The norm predicate uses an integer threshold $`T`$. Its complement begins at $`K=T+1`$ because the squared norm is integral:

```math
A=\{z:\|z\|^2\le T\},
\qquad
A^c=\{z:\|z\|^2\ge K\}.
```

| Parameter | Degree 512 | Degree 1024 |
|---|---:|---:|
| Coefficient dimension $`d`$ | 1024 | 2048 |
| Modulus $`q`$ | 12289 | 12289 |
| Gaussian width parameter $`\sigma`$, approximately | 165.7366171829776 | 168.38857144654394 |
| Accepted squared norm $`T`$ | 34,034,726 | 70,265,242 |
| First rejected squared norm $`K`$ | 34,034,727 | 70,265,243 |
| Salt length $`\kappa`$ | 320 bits | 320 bits |
| Sampler width-design parameter $`\varepsilon_{\mathrm{des}}`$ | $`2^{-35.5}`$ | $`2^{-36}`$ |

The exact width is defined by the formula in [the parameter page](falcon_parameters.md). The ambient integer Gaussian is

```math
G(z)=\frac{\exp(-\|z\|^2/(2\sigma^2))}
{\sum_{x\in\mathbb Z^d}\exp(-\|x\|^2/(2\sigma^2))}.
```

The symbol $`\sigma`$ is the Gaussian width parameter in the continuous-Gaussian standard-deviation convention; it need not equal the standard deviation of a discrete Gaussian law. A source using $`\exp(-\pi\|z\|^2/s^2)`$ has $`s=\sqrt{2\pi}\sigma`$.

## 2. Key-generation and sampler contracts

Let $`\mathsf{Gen}`$ be the mathematical Falcon NTRU trapdoor-generation distribution used in the cited analysis. It returns $`h=g/f\pmod q`$, with $`f`$ invertible modulo $`q`$, and a secret module basis together with its FFO sampling tree. The assumptions below hold for every key in its support.

First, the generated lattice admits the expanded integral basis with

```math
\|\widehat B\|_{\mathrm{GS}}\le B_0,
\qquad B_0=\frac{117}{100}\sqrt q.
```

Second, the FFO leaf widths satisfy the hypothesis of the FFO sampling theorem. The expanded-basis bound controls the dual theta series; the leaf-width bound permits the imported FFO distributional estimate. The coefficient-splitting operator and leaf identity in Fouque et al., Appendix F.3, pp. 42–43, connect the FFO tree to the Gram–Schmidt lengths of the expanded basis. [The parameter page](falcon_parameters.md#the-ffo-leaf-width-hypothesis) gives the basis-order argument. This uses the FFO normalization law and its actual coefficient expansion. [Fouque et al., Lemma 7 and §F.3](https://eprint.iacr.org/2024/1769).

For each syndrome $`y`$, define the ideal coset Gaussian

```math
\mu(y)=\Pr_{Z\leftarrow G}[F_h(Z)=y],
\qquad
G_y(z)=\frac{G(z)}{\mu(y)}\mathbf 1[F_h(z)=y].
```

Write $`P_y`$ for the exact-arithmetic FFO preimage distribution at that syndrome. The imported FFO theorem and its proof give a uniform pointwise sandwich

```math
a\le\frac{P_y(z)}{G_y(z)}\le b,
\qquad
b=
\left(\frac{1+\varepsilon_{\mathrm{des}}/d}{1-\varepsilon_{\mathrm{des}}/d}\right)^d,
\qquad
a=b^{-1}.
```

The reciprocal lower bound uses the normalization-product argument in the proof of Lemma 20, printed p. 41, transported to FFO by its exact product formula in Lemma 22 and the conclusion of Appendix F.3, pp. 43–45. The relative-error statement in Lemma 7 alone would give the weaker lower bound $`2-b`$.

This is the profile used by the numerical security calculation. The leaf identity gives $`\sqrt{D_i}\le B_0`$ and hence leaf widths $`\sigma_i=\sigma/\sqrt{D_i}\ge\sigma/B_0`$. The exact standard width formula satisfies the source's leaf-smoothing hypothesis, as checked in [the parameter account](falcon_parameters.md#the-ffo-leaf-width-hypothesis). The profile concerns the mathematical FFO algorithm with its specified one-dimensional Gaussian draws. An implementation needs its own profile for finite-precision sampling, random-bit generation, and platform effects. [Fouque et al., Lemmas 3–4 and 7, §4.1, and Lemma 22](https://eprint.iacr.org/2024/1769).

## 3. Hash and query model

The hash is an ideal random oracle

```math
H:\mathsf{PK}\times\{0,1\}^{\kappa}\times\mathsf{Msg}\longrightarrow Y.
```

Tuples have an unambiguous encoding and the protocol's domain separation. The theorem concerns one honestly generated public key. Including that public key in the hash input matches the CoreFalcon framework; a one-key theorem can also use the legacy fixed-key domain by identifying its inputs with the corresponding slice. This observation is not a multi-user or cross-protocol reduction.

The adversary makes at most $`q_S`$ **classical** signing queries and $`q_H`$ hash queries. In the ROM, hash queries are classical. In the QROM, they may be quantum superposition queries. Signing messages may depend adaptively on the entire previous interaction. Initial quantum advice is independent of the random oracle; oracle-dependent preparation is charged to the query budget.

For every signing query, the signer draws its salt uniformly and independently after receiving the message. Sampler coins are fresh and independent across attempts and queries. The adversary receives the final signature or a declared public error. It does not receive retry counts, intermediate preimages, or running times. If bounded-time signing is used, the attempt cap and its error behavior are specified separately below.

For finite adversarial running time, the hash domain may be restricted to encodings of the permitted length. The reduction implements its random oracle with the resource accounting in [the security proof](security_transfer.md).

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

For odd $`q`$, let $`\mathrm{ctr}_q`$ denote coefficientwise reduction into
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

Let $`U`$ be uniform on $`Y`$, and use the ambient law $`G`$, image $`\mu`$, and coset law $`G_y`$ defined above. Write

```math
a_y=G_y(A),
\qquad
\widehat a_y=P_y(A).
```

The quotient densities and global rejection probability are

```math
p(y)=N\mu(y),
\qquad
r(y)=N\Pr_{Z\leftarrow G}[F_h(Z)=y,\,A^c],
\qquad
\delta=\mathbb E_U r=\Pr_G[A^c].
```

Thus $`a_y=1-r(y)/p(y)`$. The norm theorem bounds the actual quantities

```math
Q_0=\|p-1\|_{L^2(U)},
\qquad
R=\|r-\delta\|_{L^2(U)},
```

and supplies a uniform bound $`1-a_y\le D_0`$.

After refreshing the initial target to an independent uniform value in the proof, the real accepted joint law is

```math
L(y,z)=U(y)P_y(z\mid A).
```

The public simulator uses a different, exactly sampleable law:

```math
M(y,z)=\nu(y)G_y(z\mid A)
      =G(z\mid A)\mathbf 1[F_h(z)=y],
\qquad
\nu(y)=\frac{\mu(y)a_y}{1-\delta}.
```

It samples an ambient Gaussian until the norm test succeeds, computes its syndrome, and programs that syndrome at the fresh salt/message input. Its accepted-image density is

```math
w(y):=\frac{\nu(y)}{U(y)}=N\nu(y)=\frac{p(y)-r(y)}{1-\delta}.
```

For comparison, repeatedly choosing a *uniform syndrome*, drawing from its ideal coset Gaussian, and restarting both on failure would give target law

```math
\widetilde\nu(y)=\frac{U(y)a_y}{\mathbb E_U a_y}.
```

In general $`\widetilde\nu\ne\nu`$. Variance bounds for $`a_y`$ alone compare fixed-target signing with the uniformly chosen-target retry experiment. The public law $`M`$ also contains the unconditioned image weights $`\mu(y)`$, so its density $`w`$ is controlled through both $`Q_0`$ and $`R`$. The [security proof](security_transfer.md) accounts for the fresh-salt programming cost before making this joint-law comparison.

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

For EUF-CMA, the wrapper and verifier are handled by the explicit decoding/extraction map. For SUF-CMA, the sufficient buffer ensures that an encoding error means the hidden transmitted component has no admitted encoding. At a programmed input, take the vector used in the latest program. If its signing request returned a signature, uniqueness of encoding means a new canonical signature has a different $`v`$. If it returned $`\bot`$, its hidden $`v`$ was not encodable, so a valid forged $`v`$ again differs. In both cases the reconstructed full preimage differs from that challenge vector, regardless of recentering.

An undersized caller buffer does not satisfy this SUF argument. Neither does a verifier that accepts multiple equivalent compressed, padded, or constant-time encodings as distinct signatures. A scheme allowing such representations needs either an equivalence-aware freshness definition or a separate analysis.

## 7. Unforgeability and termination

In EUF-CMA, a successful forgery verifies and its message was never submitted to the signing oracle. This definition records all requested messages, including requests that returned a public error. In SUF-CMA, a successful forgery verifies and its exact message/signature pair was never returned successfully. The signing queries remain classical in both the ROM and QROM formulations.

The accepted-law model uses an unbounded retry loop with finite expected trial count under the declared Gaussian primitive. The sampler profile gives

```math
P_y(A^c)\le bD_0<1
```

uniformly in the key and syndrome. An implementation of the mathematical model may cap each query at $`\ell`$ attempts and return $`\bot`$ when the cap is reached. Coupling it with the unbounded signer changes any adversarial success probability by at most

```math
\varepsilon_{\mathrm{cap}}\le q_S(bD_0)^\ell.
```

For $`q_S\le2^{64}`$, the certified choices $`\ell=32`$ at degree 512 and $`\ell=16`$ at degree 1024 make this error smaller than $`2^{-390}`$. The public reduction has its own finite Gaussian-pool budget, treated separately in [the security proof](security_transfer.md#6-a-finite-public-gaussian-pool).

The model establishes no retry-count or timing-leakage guarantee. It also does not cover caller-chosen or reused salts, deterministic signing, fixed padded-length rejection, or finite-precision sampling. Those changes affect a stated hypothesis or distribution and need their own proof.

## Sources

- Fouque, Gajland, de Groote, Janneck, Kiltz, [*A Closer Look at Falcon*](https://eprint.iacr.org/2024/1769), full version dated 2 March 2026. Relevant locations: Lemmas 3–4 and 7; Figure 6 and §4.1; Appendix F.3, especially the leaf identity and Lemma 22.
- Beckmann, Majenz, [*Quantum Oracle Distribution Switching and Applications to Falcon and Ring Signatures*, v3](https://arxiv.org/pdf/2602.16268v3), 9 September 2026. Relevant locations: Figure 9 and Appendix E.1.
- Falcon reference implementation: [codec](https://falcon-sign.info/impl/codec.c.html), [signing and verification API](https://falcon-sign.info/impl/falcon.c.html), and [format and buffer definitions](https://falcon-sign.info/impl/falcon.h.html).
