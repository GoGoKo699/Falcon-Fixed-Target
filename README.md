# Falcon Fixed Target

**Can a Falcon signer keep the same hash target while retrying its norm test?**

This project gives a concrete security argument for the fixed-target **CoreFalcon** model: each signing query receives one fresh random salt, and unsuccessful norm trials reuse that salt and target. The main result controls how conditioning an integer Gaussian on Falcon's norm cutoff changes its distribution across NTRU cosets. It applies uniformly to keys satisfying the specification's Gram–Schmidt bound, at the original Falcon-512 and Falcon-1024 parameters.

The security result uses an explicit ideal-sampler contract and NTRU hardness assumptions. Its primary application is the classical random-oracle model. A quantum-random-oracle corollary retains its programming and extraction costs.

## Principal results

For a target $`y`$, let $`a_y`$ be the probability that an exact coset Gaussian passes the norm test. Let $`\nu`$ be the syndrome distribution of a public integer Gaussian conditioned on passing that test, and let $`U`$ be uniform over syndromes.

| Quantity | Falcon-512 parameters | Falcon-1024 parameters |
|---|---:|---:|
| Ring degree $`n`$; vector dimension $`d=2n`$ | 512; 1024 | 1024; 2048 |
| Gaussian width $`\sigma`$ | $`165.736617\ldots`$ | $`168.388571\ldots`$ |
| Accepted squared norm $`\lVert z\rVert^2\le T`$ | 34,034,726 | 70,265,242 |
| Variance over uniform targets $`\mathrm{Var}_{y\sim U}(a_y)`$ | $`<2^{-90}`$ | $`<2^{-120}`$ |
| Accepted-image distance $`\chi^2(\nu\Vert U)`$ | $`<2^{-81}`$ | $`<2^{-83}`$ |

These are analytical upper bounds with reproducible numerical certificates, rather than sampled estimates of key quality. The variance statement concerns variation across targets; it does not say that the rejection probability itself is as small as that variance.

The proof combines a discrete norm-tail contour with quadratic Gauss sums and dual-lattice theta estimates. A finite-quotient summation identity controls all target characters together, without multiplying the bound by the number of targets. The treatment of the parity arc preserves the arithmetic effects of the integer norm.

The accepted-image estimate then supplies a public simulator: sample a short integer Gaussian vector, compute its syndrome, and program one fresh salt/message input per signature. An excess-preserving conditioning lemma accounts for the sampler's deviation from the exact coset Gaussian. The resulting [security theorem](science/security_transfer.md) states the assumptions, direction of the distribution comparison, query counts, runtime, and additive errors.

## Read the science

Start with the [scientific overview](science/README.md) and the [signing model](science/signing_model.md).

| Question | Authoritative account |
|---|---|
| Which algorithm, adversary, and signature representation are covered? | [Signing model](science/signing_model.md) |
| Why do Falcon's generated keys satisfy the geometric hypotheses? | [Keys and parameters](science/falcon_parameters.md) |
| How is the sharp norm cutoff handled on an integer lattice? | [Norm-tail smoothing theorem and proof](science/norm_tail_smoothing.md) |
| How are the concrete constants certified? | [Numerical certificate](science/numerical_certificate.md) |
| How does the distribution bound imply unforgeability? | [Security transfer](science/security_transfer.md) |
| What does fixing the target change, and how should the bounds be interpreted? | [Interpretation](science/interpretation.md) |
| Which ingredients are inherited, and how does this compare with Falcon+? | [Related work](references/related_work.md) and [bibliography](references/bibliography.bib) |
| Which calculations can be reproduced? | [Verification](verification/README.md) |

## Reproduce the calculations

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The verification account distinguishes rigorous numerical enclosures from floating-point identity diagnostics. The general lattice theorem and security reduction are established by the written arguments; finite checks test the specified formulas and instances.

## Scope

The signing queries are classical, including in the quantum random-oracle model. Each salt is independent and sampled after the message is chosen. The signing interface returns only the final result. The concrete sampler application is the exact-arithmetic FFO abstraction, using its published probability-ratio bounds.

Norm rejection is the acceptance predicate in the central theorem. A separate estimate covers individual coefficient caps. The total padded encoding budget, caller-chosen or reused salts, exposed retry counts, and finite-precision implementation errors require additional analysis. The [signing model](science/signing_model.md) covers canonical compressed encoding with a public error return and specifies the sufficient-buffer and unique-format conditions needed for byte-string strong unforgeability.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
