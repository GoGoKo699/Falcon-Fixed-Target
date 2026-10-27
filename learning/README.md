# Learn Falcon Fixed Target

The scientific question is how to prove security when a lattice signer keeps the same hash target throughout its norm-rejection loop. Understanding the answer requires both geometry and probability: the lattice defines the possible preimages of each target, while conditioning on a short norm changes how likely those targets are under a public sampler.

The single educational anchor is **Chris Peikert, *A Decade of Lattice Cryptography* (2016)**. The [source bridge](ANCHOR.md) uses the author's 17 February 2016 version, identifies a focused set of sections, and translates their notation into this project's conventions. Those sections can be read alongside the project; the route does not require reading the entire survey first.

## The common understanding map

The [milestone map](MILESTONES.md) contains exactly **M01–M30**. Each milestone records a central question, an understanding target, earlier dependencies, its role in the argument, a conceptual connection, and source pointers.

| Phase | Milestones | How the ideas connect |
|---|---|---|
| Background/preliminaries | M01–M14 | Integer lattices and cosets lead to Gaussian preimages, smoothing, probability comparisons, and the complete fixed-target signing question. |
| Narrative/innovation | M15–M30 | The key geometry and discrete tail analysis establish concrete accepted-image bounds, which feed the sampler comparison and unforgeability reduction. |

The first phase ends by assembling the three accepted laws that the proof must keep distinct. The second ends by joining the analytic result, its numerical certificate, the cryptographic assumptions, and the resource costs. This allocation follows the structure of the project and is common to every reader.

## Choose a reading route

| Purpose | Route |
|---|---|
| Understand why the retry policy matters | Read [the interpretation](../science/interpretation.md), then the worked target-law example in [the bridge](ANCHOR.md). |
| Build the mathematical framework | Follow M01–M09 with the bridge's lattice and Gaussian conventions; continue through M15–M24 and the [norm-tail proof](../science/norm_tail_smoothing.md). |
| Follow the security argument | Use M10–M14 to assemble the signing model, then M25–M30 alongside [the security transfer](../science/security_transfer.md). |
| Check exactly which Falcon abstraction is covered | Read [the signing model](../science/signing_model.md) and [the parameter account](../science/falcon_parameters.md). |
| Reproduce the concrete inequalities | Read [the numerical method](../science/numerical_certificate.md), then use [the verification commands](../verification/README.md). |
| Review the full contribution | Follow [the scientific overview](../science/README.md) and [the related-work comparison](../references/related_work.md). |

## What the bridge adds

Peikert supplies the language of Gaussian lattice sampling, short-basis trapdoors, and forward/reverse preimage experiments. The bridge connects those foundations to Falcon's structured key distribution, its explicit norm cutoff, and the comparison between a fixed uniform target and the target obtained from an accepted ambient Gaussian.

The project supplies the discrete norm-tail analysis, concrete numerical bounds, exact sampler-conditioning calculation, and the stated ROM/QROM reductions. Their primary research dependencies remain cited in the scientific pages. The milestone targets organize those arguments; the canonical claims and complete proofs remain under [science/](../science/README.md).

When comparing the final security bounds, keep the model's resources together: signing queries, hash queries, salt length, Gaussian sampling, hardness assumptions, and oracle-simulation costs. The small distribution-transfer loss is one term in that account. The [interpretation](../science/interpretation.md#what-the-security-transfer-pays-for) explains how to read it.
