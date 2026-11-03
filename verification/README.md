# Reproduce the bounds

The checks distinguish repository integrity, certified arithmetic, finite diagnostics, and plot reproducibility. The Arb programs certify numerical inequalities that occur in the analytic proof. The standard-library identity program checks phases and normalizations in small examples using ordinary floating-point arithmetic. Its agreement is a diagnostic, not an interval certificate. The plot check regenerates the committed vector assets and their numerical data.

## Environment and commands

Use Python 3.12, as in CI. The dependencies are pinned in [requirements.txt](requirements.txt): `python-flint==0.8.0` supplies Arb arithmetic, while Matplotlib, NumPy, and FontTools reproduce the vector plot. FontTools is pinned because PDF font subsetting affects the asset bytes. The checked python-flint wheel reports FLINT 3.3.1. The certificate programs print the backend and precision used by each run.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The runner first checks report/source integrity, relative links, and the settled milestone map, then executes the norm certificate before the security calculation that consumes its bounds. It runs the identity diagnostics and checks plot regeneration afterward. It prints one success line per program, writes full outputs to `verification/output/`, and returns a nonzero exit status if any program fails. Reference certificate outputs are committed under [expected](expected/). The internal inequality gates, rather than a string comparison against those outputs, establish a successful numerical run. The read-only GitHub Actions workflow runs the same command on pushes and pull requests.

## What each program establishes

| Program | Calculation | Meaning of success |
|---|---|---|
| [check_repository.py](check_repository.py) | Report/source hashes, local links and heading targets, and the 30-milestone dependency order | The checked files agree with [report_manifest.json](report_manifest.json), navigation resolves, and the existing learning-map structure is intact; this does not validate proofs or rendered layout |
| [norm_circle_interval.py](norm_circle_interval.py) | Theta upper bounds, exact rational integration grid, major-arc upper rectangles, minor-arc bound, and Gaussian parameter enclosures | The evaluated upper expressions imply the declared tail, variance, and accepted-image inequalities at both parameter sets, including the optional individual coefficient cap |
| [core_transfer_bounds.py](core_transfer_bounds.py) | Accepted sampler moments, reverse image moments, conditional bit losses, retry-pool bounds, and encoding-size arithmetic | The concrete arithmetic in the security account satisfies its stated ceilings, using the norm certificate's contracts |
| [norm_circle_identity_checks.py](norm_circle_identity_checks.py) | Twisted quadratic Gauss expansions, the scaled dual-coset identity, and the tail contour on a small lattice | The specified finite examples agree within the program's floating-point tolerances |
| [Graph/generate_plots.py](Graph/generate_plots.py) `--check` | Analytic transfer curves at 256-bit Arb precision, all nine transfer-table ceilings, and regeneration of PDF/SVG/data assets | The committed assets agree byte-for-byte with a fresh calculation and rendering; this does not establish a measured divergence or an end-to-end security level |

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

## Reproduce the transfer plot

The [vector PDF](Graph/transfer.pdf), [SVG preview](Graph/transfer.svg), and [Arb data](Graph/transfer_data.json) describe the conditional distribution-transfer calculation in the [security account](../science/security_transfer.md#10-certified-transfer-values-and-their-interpretation). At $`q_S=2^{64}`$, the three curves use $`(n,\lambda_{\mathrm{sim}})=(512,120),(512,128),(1024,256)`$. Markers identify the stated orders 73, 75, and 151; they do not certify an optimal order. The drawn range is 40–220, while the data retain integer orders 20–240.

From the repository root:

```bash
python3 verification/Graph/generate_plots.py --check
python3 verification/Graph/generate_plots.py
```

The first command regenerates all three assets in a temporary directory and compares their exact bytes without changing the committed files. The second updates the assets after an intentional input or presentation change. The generator imports the canonical parameters from [core_transfer_bounds.py](core_transfer_bounds.py), uses its stated moment formulas, and checks the total-loss, image, and conditioning-increment ceilings for all three rows.

The JSON stores the source-module hash, parameter enclosures, all curve-value balls, and the floating-point midpoints used for plotting. The curves visualize analytic upper-bound expressions. Oracle-programming errors, lattice-hardness work factors, and the other reduction costs are accounted for separately in the theorem.

## Capture hosted mathematics

The separate read-only CI job uses [hosted/capture_math.cjs](hosted/capture_math.cjs) with Playwright 1.56.1 and fresh anonymous browser contexts. It visits each tracked Markdown page at the exact checked-out commit on GitHub, at 1440 × 1000 and 760 × 1000 pixels. For pull requests, the checkout is the actual PR head rather than GitHub's synthetic merge commit.

After asynchronous MathML hydration, the job retains every expression, including table cells, with its MathML, rendered text, measured geometry and renderer errors. It also records source hashes, observed URLs, browser/runtime versions, full-page screenshots and HTML under `verification/output/hosted/`. The one-day CI artifact contains `raw-capture-1440.json` and `raw-capture-760.json` plus their referenced files.

These are raw observations, not a mathematical-rendering verdict. A complete capture still requires source-to-render comparison and visual review. An unavailable or incomplete capture cannot establish a hosted-rendering pass. The collector uses no existing browser profile or account, and stops on access or transport failures without retries or alternative routes.

## Analytical obligations

The [norm-tail proof](../science/norm_tail_smoothing.md) establishes the contour identity, the rational-arc bounds, the quotient summation, and the passage to accepted distributions. The [parameter account](../science/falcon_parameters.md) proves that the mathematical Falcon key-generation test supplies the required basis. The [security account](../science/security_transfer.md) proves the distribution comparison and reduction.

The programs do not enumerate Falcon keys, estimate cryptanalytic hardness, audit a floating-point signer, or prove a statement about a total padded encoding budget. Their scope is the integrity checks, explicit arithmetic, and finite diagnostics described above.

## Rebuild the explanatory report

The report's editable source is [Falcon_Fixed_Target_Report.tex](../learning/source/Falcon_Fixed_Target_Report.tex). It is self-contained, including the probability diagram, and requires pdfLaTeX from **TeX Live 2025** with the packages declared in its preamble. The [manifest](report_manifest.json) records the matching source/PDF hashes, page count, engine, and scientific source revision.

From the repository root:

```bash
python3 verification/build_report.py
```

If the required engine is outside `PATH`, specify it explicitly:

```bash
python3 verification/build_report.py --engine /path/to/texlive/2025/bin/x86_64-linux/pdflatex
```

The script checks the engine version and source identity, compiles three times into `verification/output/report/`, checks the final log, and reports the fresh PDF/log paths and whether the rebuilt PDF is byte-identical to the stored report. It never overwrites the stored PDF. A difference requires inspection of the fresh output; a successful compile or matching hash alone does not establish scientific validity. After source or layout changes, render and inspect every page before updating the stored pair and its manifest.

The standard Python verification suite does not require TeX. Report compilation is a separate check, with its fresh output and final log retained together.
