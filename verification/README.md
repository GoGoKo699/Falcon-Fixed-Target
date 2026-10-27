# Reproduce the bounds

The scripts serve two distinct purposes. The Arb programs certify numerical inequalities that occur in the analytic proof. The standard-library identity program checks phases and normalizations in small examples using ordinary floating-point arithmetic. Its agreement is a diagnostic, not an interval certificate.

## Environment and commands

Use Python 3.11 or newer. The only external dependency is pinned in [requirements.txt](requirements.txt): `python-flint==0.8.0`. The checked python-flint wheel reports FLINT 3.3.1. The certificate programs print the backend and precision used by each run.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The runner executes the norm certificate before the security calculation that consumes its bounds. It prints one success line per program, writes full outputs to `verification/output/`, and returns a nonzero exit status if any program fails. Reference certificate outputs are committed under [expected](expected/). The internal inequality gates, rather than a string comparison against those outputs, establish a successful numerical run.

## What each program establishes

| Program | Calculation | Meaning of success |
|---|---|---|
| [norm_circle_interval.py](norm_circle_interval.py) | Theta upper bounds, exact rational integration grid, major-arc upper rectangles, minor-arc bound, and Gaussian parameter enclosures | The evaluated upper expressions imply the declared tail, variance, and accepted-image inequalities at both parameter sets, including the optional individual coefficient cap |
| [core_transfer_bounds.py](core_transfer_bounds.py) | Accepted sampler moments, reverse image moments, conditional bit losses, retry-pool bounds, and encoding-size arithmetic | The concrete arithmetic in the security account satisfies its stated ceilings, using the norm certificate's contracts |
| [norm_circle_identity_checks.py](norm_circle_identity_checks.py) | Twisted quadratic Gauss expansions, the scaled dual-coset identity, and the tail contour on a small lattice | The specified finite examples agree within the program's floating-point tolerances |

The [numerical-method page](../science/numerical_certificate.md) derives the theta truncation bound and explains why the rectangles enclose the integrals. A displayed Arb ball encloses an **upper-bound expression**. It is not an interval measurement of a particular Falcon key's actual acceptance variance.

## Main numerical contracts

| Certified upper bound | Degree 512 | Degree 1024 |
|---|---:|---:|
| Rejected-image root mean-square deviation $`R`$ | $`<2^{-45.59}`$ | $`<2^{-60.41}`$ |
| Norm-acceptance variance | $`<2^{-90}`$ | $`<2^{-120}`$ |
| Accepted-image chi-square distance | $`<2^{-81}`$ | $`<2^{-83}`$ |
| Variance after adding the individual coefficient cap | $`<2^{-90}`$ | $`<2^{-120}`$ |
| Accepted-image chi-square distance after adding that cap | $`<2^{-81}`$ | $`<2^{-83}`$ |

The security-transfer table uses the following conditional calculations at $`q_S=2^{64}`$:

| Degree | Assumed simulator success | Rényi order | Certified transfer loss |
|---|---:|---:|---:|
| 512 | $`2^{-120}`$ | 73 | Below 3.268 bits |
| 512 | $`2^{-128}`$ | 75 | Below 3.376 bits |
| 1024 | $`2^{-256}`$ | 151 | Below 3.387 bits |

The simulator-success column is an input to this calculation. Hardness of the NTRU problems, oracle reprogramming, and other reduction costs belong to the [security theorem](../science/security_transfer.md). They are not validated by substituting these numbers into the moment bound.

## Reproduce individual calculations

```bash
python3 verification/norm_circle_interval.py
python3 verification/core_transfer_bounds.py
python3 verification/norm_circle_identity_checks.py
```

The norm program also accepts `--n 512` or `--n 1024`, `--precision-bits`, and `--pieces`. Its reference run uses 256-bit precision and 512 rectangles in each of ten intervals per major arc. Reducing the rectangle count can make a conservative bound fail; that means the chosen upper bound is insufficient, not that the mathematical quantity violates the theorem.

## Analytical obligations

The [norm-tail proof](../science/norm_tail_smoothing.md) establishes the contour identity, the rational-arc bounds, the quotient summation, and the passage to accepted distributions. The [parameter account](../science/falcon_parameters.md) proves that the mathematical Falcon key-generation test supplies the required basis. The [security account](../science/security_transfer.md) proves the distribution comparison and reduction.

The programs do not enumerate Falcon keys, estimate cryptanalytic hardness, audit a floating-point signer, or prove a statement about a total padded encoding budget. Their scope is the explicit arithmetic and finite diagnostics described above.
