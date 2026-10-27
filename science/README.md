# Scientific overview

The project studies a specific step in a lattice signature: repeated private sampling at the **same public target** until a norm test succeeds. Its mathematical contribution bounds the target bias produced by a sharp norm cutoff. Its cryptographic consequence is a security transfer for the fixed-target CoreFalcon model under explicit sampler and hardness assumptions.

## The distribution that the proof must simulate

A public key defines a syndrome map $`f_h:\mathbb Z^{2n}\to R_q`$, where $`R_q=\mathbb Z_q[X]/(X^n+1)`$. Its kernel is an integer lattice $`\Lambda_h`$. A target $`y`$ specifies the coset $`f_h^{-1}(y)`$.

For an exact discrete Gaussian $`D`$ on $`\mathbb Z^{2n}`$, write $`D_y=D\mid f_h(z)=y`$. Define the public norm event

```math
A=\{z:\lVert z\rVert^2\le T\},
\qquad a_y=\Pr_{D_y}[A].
```

An ideal signer first obtains a uniform target and then samples from $`D_y\mid A`$. A public simulator can instead sample from $`D\mid A`$ and compute the target. These procedures give the same conditional vector law within a target, but they select targets with different probabilities:

```math
\Pr_{D\mid A}[f_h(z)=y]
=\frac{\Pr_D[f_h(z)=y]\,a_y}{\Pr_D[A]}.
```

The factor $`a_y`$ is why an unconditioned Gaussian image estimate is insufficient on its own. The [norm-tail theorem](norm_tail_smoothing.md) bounds its variation and, directly, the distance of the accepted image from uniform. The [security transfer](security_transfer.md) combines that estimate with the actual sampler's probability-ratio profile.

## Common notation

| Symbol | Meaning |
|---|---|
| $`n`$, $`d=2n`$ | Ring degree and ordinary integer-vector dimension |
| $`q=12289`$ | Falcon modulus |
| $`\Lambda_h`$; $`\mathbb Z^d/\Lambda_h`$ | Kernel lattice and finite syndrome quotient |
| $`B=1.17\sqrt q`$ | Upper bound on ordinary Gram–Schmidt lengths of an available basis |
| $`\sigma`$ | Width in the mass function $`\exp(-\lVert z\rVert^2/(2\sigma^2))`$ |
| $`T`$, $`K=T+1`$ | Largest accepted squared norm and first rejected integer squared norm |
| $`p(y)`$ | Density of the unconditioned Gaussian image relative to uniform |
| $`r(y)`$, $`\delta`$ | Rejected Gaussian image density and its mean |
| $`Q_0`$, $`R`$ | The quantities $`\lVert p-1\rVert_2`$ and $`\lVert r-\delta\rVert_2`$, respectively |
| $`D_0`$ | Uniform upper bound on rejection probability in every coset |
| $`\nu`$ | Syndrome law of the accepted public Gaussian $`D\mid A`$ |
| $`q_S`$, $`q_H`$, $`\kappa`$ | Signing queries, adversarial hash queries, and salt length |

All norms of integer vectors are Euclidean. Norms of quotient densities use the uniform probability measure. The Gaussian exponent parameter and the Rényi order have separate local definitions in their respective proofs; they are not interchangeable.

## How the argument fits together

| Step | Input | Output |
|---|---|---|
| [Key geometry](falcon_parameters.md) | The mathematical Falcon key-generation test | The short Gram–Schmidt basis and quotient arithmetic needed below |
| [Discrete smoothing](norm_tail_smoothing.md) | That basis, the Gaussian width, and the integer norm cutoff | Uniform rejection, tail Fourier energy, acceptance variance, and accepted-image bounds |
| [Concrete evaluation](numerical_certificate.md) | Explicit theta and arc inequalities | Enclosures supporting the stated Falcon-512 and Falcon-1024 constants |
| [Sampler conditioning](security_transfer.md) | An established unconditioned sampler profile | A bound on the accepted conditional sampler law |
| [Signing simulation](security_transfer.md) | The accepted-image and sampler bounds, plus fresh salts | A joint Rényi moment for all signing outputs |
| [Forgery extraction](security_transfer.md) | The public simulator and an adversary | Conditional ROM and QROM unforgeability bounds under stated NTRU problems |

The [interpretation](interpretation.md) explains why the resulting statement addresses fixed-target norm retries and how to read its concrete losses. The [related-work account](../references/related_work.md) identifies the inherited harmonic-analysis and cryptographic tools and the difference from the closest signature analyses.

For the prerequisites and their connections to this sequence, use the [Peikert bridge](../learning/ANCHOR.md) alongside the [30-milestone map](../learning/MILESTONES.md). The [learning entrypoint](../learning/README.md) offers routes through the geometric and cryptographic parts of the project.
