# Numerical certificate for the norm-tail bounds

## Certified statements

The program [norm_circle_interval.py](../verification/norm_circle_interval.py)
evaluates the explicit bounds in
[norm_tail_smoothing.md](norm_tail_smoothing.md) using Arb ball arithmetic.
With the stated lattice hypotheses and parameter intervals, its successful
default run certifies the following inequalities.

| Quantity | $`n=512`$ | $`n=1024`$ |
|---|---:|---:|
| Rejected-tail image norm $`R`$ | $`<2^{-45.59}`$ | $`<2^{-60.41}`$ |
| Variance of the coset acceptance probability | $`<2^{-90}`$ | $`<2^{-120}`$ |
| Accepted ambient image $`\chi^2(\nu\|U)`$ | $`<2^{-81}`$ | $`<2^{-83}`$ |
| Acceptance variance with the individual coordinate cap | $`<2^{-90}`$ | $`<2^{-120}`$ |
| Accepted-image $`\chi^2`$ with the individual coordinate cap | $`<2^{-81}`$ | $`<2^{-83}`$ |

The coordinate cap is $`|X_j|\le2047`$ on a fixed set of $`n`$ coordinates.
The calculation does not cover a summed padded-encoding budget.

The complete default output is
[norm_circle_interval.txt](../verification/expected/norm_circle_interval.txt).
The exponent contracts $`-45.59=-4559/100`$ and $`-60.41=-6041/100`$ are
checked using exact rational inputs. They are also the interface consumed
by [core_transfer_bounds.py](../verification/core_transfer_bounds.py).

## Reproduction

The checked environment uses Python 3.12, python-flint 0.8.0, and the bundled
FLINT 3.3.1. The program requires python-flint and the Python standard library.
Its default precision is 256 bits. From the repository root, run the
following commands in a Python environment:

~~~sh
python -m pip install python-flint==0.8.0
python verification/norm_circle_interval.py
~~~

To evaluate a single parameter set, use:

~~~sh
python verification/norm_circle_interval.py --n 512
~~~

The options --precision-bits and --pieces change the arithmetic precision
and the number of upper rectangles per dyadic interval. The recorded
certificate uses 256 bits and 512 pieces. A modified run is successful only
if every numerical contract is still established. In particular, choosing
a coarser partition is permitted to fail a contract.

The program prints its python-flint version, linked FLINT version,
precision, bounds, and a final CERTIFIED line for each parameter set.
Every gate uses an explicit conditional exception, so running Python with
optimization enabled does not disable the checks.

## What the arithmetic encloses

An Arb real ball represents a set $`[m-r,m+r]`$. Arithmetic, elementary
functions, and constants enlarge the radius to account for input uncertainty
and rounding. The inclusion contract is documented in the
[FLINT real-ball reference](https://flintlib.org/doc/arb.html) and the
[python-flint Arb interface](https://python-flint.readthedocs.io/en/stable/arb.html).
The checked dependency versions are pinned above; the certificate's software
trust includes those implementations. This is a computer-assisted numerical
proof of explicit inequalities, not a formal verification of the arithmetic
library.

All noninteger constants enter as exact decimal or rational strings.
For example, the program constructs $`1.17`$ as the rational string
117/100, and constructs the two endpoints of each $`\sigma`$ interval from
their decimal strings. It then takes a ball containing both endpoints.
No binary floating-point approximation is used to construct these inputs.

The printed balls enclose the values of **upper-bound expressions**.
For example, a ball printed for log2_R_bound encloses the base-two
logarithm of the computed expression that bounds $`R`$ from above.
Its lower endpoint is not a lower bound on the actual $`R`$ of an
unspecified lattice. The actual quantity can be much smaller.

The same distinction applies to the theta calculation described next:
the finite expression is a proved upper bound for the infinite sum,
rather than an equality with it.

## An explicit theta-series remainder

For every $`x>0`$,

```math
\vartheta(x)-1
=2\sum_{k=1}^{\infty}e^{-xk^2}.
```

For $`k\ge12`$, the ratio of successive summands is
$`e^{-x(2k+1)}\le e^{-25x}`$. Therefore

```math
\vartheta(x)-1
\le
E(x):=
2\sum_{k=1}^{11}e^{-xk^2}
+
\frac{2e^{-144x}}{1-e^{-25x}}.
\qquad\text{(1)}
```

This bound is valid for every positive $`x`$. To keep it sharp for small
arguments, the program also uses Jacobi's identity

```math
\vartheta(x)=\sqrt{\frac\pi x}\,
\vartheta\!\left(\frac{\pi^2}{x}\right).
\qquad\text{(2)}
```

If the entire input ball lies below $`1`$, it evaluates the upper expression

```math
\vartheta(x)-1
\le
\sqrt{\frac\pi x}
\left(1+E\!\left(\frac{\pi^2}{x}\right)\right)-1.
\qquad\text{(3)}
```

The transformed argument is then greater than $`\pi^2`$, so one transformation
suffices. If the input ball meets or lies above $`1`$, the program uses (1)
directly. Both choices are valid on every point of the corresponding input
ball.

Let $`U_\vartheta(x)`$ denote the resulting upper expression for
$`\vartheta(x)-1`$. Powers close to $`1`$ are evaluated as

```math
\begin{aligned}
\vartheta(x)^m
&\le\exp\!\left(m\log(1+U_\vartheta(x))\right),\\
\vartheta(x)^m-1
&\le\mathrm{expm1}\!\left(
m\mathrm{log1p}(U_\vartheta(x))\right).
\end{aligned}
\qquad\text{(4)}
```

Arb's log1p and expm1 functions preserve accuracy when the correction is
small. This also avoids subtracting nearly equal ball values to form
$`\vartheta(x)^m-1`$. The finite geometric remainder, rather than a
floating-point stopping criterion, accounts for the omitted infinite tail.

Every occurrence of a theta expression in the proof is increasing in the
theta value being substituted. Replacing it by (1) or (3), and then taking
the upper endpoint of the enclosing ball, therefore preserves the direction
of the proved inequality.

## Upper rectangles for the two major arcs

Use the notation of the proof:

```math
\beta=\frac{d}{2K},\quad t=\alpha-\beta,\quad
L=\frac\pi{512},\quad
h(v)=\sqrt{\beta^2+v^2},\quad
A(v)=\frac{\pi^2\beta}{\beta^2+v^2}.
```

The program extends both major-arc integrals to
$`L_{\max}=512\beta`$. It verifies with ball comparisons that

```math
0<L\le L_{\max}<\pi,\qquad t>0.
```

The integrands are nonnegative. Extending their ranges and weakening the
parity denominator to $`1+e^{-t}\cos L_{\max}`$ can only enlarge the bounds.

### Partition

The interval $`[0,\beta]`$ is divided into 512 equal pieces. Each of

```math
[\beta,2\beta],\ [2\beta,4\beta],\ \ldots,\
[256\beta,512\beta]
```

is also divided into 512 equal pieces. There are ten such blocks in total,
including $`[0,\beta]`$, and therefore 5120 rectangles for each major arc.
Every endpoint is an exact rational multiple of $`\beta`$.

The Cauchy–Schwarz parameter is $`\varepsilon=1/100`$ throughout
$`[0,\beta]`$, and $`\varepsilon=1/2`$ on the remaining blocks. Each
pointwise bound in the proof is valid for either choice.

### Endpoint bounds

For one interval $`[\ell,h]`$, with $`\varepsilon`$ fixed on that interval,

- $`(\alpha/\sqrt{\beta^2+v^2})^{d/2}`$ is largest at $`\ell`$;
- $`\vartheta(\varepsilon A(v))`$ is largest at $`h`$;
- $`\vartheta((2-\varepsilon)A(v)/(sB^2))^d-1`$ is largest at $`h`$;
- the zero-arc denominator
  $`\sqrt{(1-e^{-t})^2+4e^{-t}\sin^2(v/2)}`$ is smallest at $`\ell`$,
  because $`0\le v\le L_{\max}<\pi`$.

Thus the contribution of this interval to the zero-arc bound is at most

```math
\begin{aligned}
&\frac{e^{-tK}}{\pi}(h-\ell)
\left(\frac{\alpha}{\sqrt{\beta^2+\ell^2}}\right)^{d/2}
\vartheta(\varepsilon A(h))^{d/2}\\
&\qquad{}\times
\frac{
\sqrt{\vartheta((2-\varepsilon)A(h)/B^2)^d-1}
}{
\sqrt{(1-e^{-t})^2+4e^{-t}\sin^2(\ell/2)}
}.
\end{aligned}
\qquad\text{(5)}
```

For the parity arc, replace $`B^2`$ inside the last theta factor by $`4B^2`$
and replace the denominator by $`1+e^{-t}\cos L_{\max}`$.
The program applies the theta upper bounds, evaluates each resulting
expression in ball arithmetic, and sums the rectangles.

These are individual monotonicity bounds for the factors. No monotonicity
assumption about their product, quadrature convergence rate, or numerical
derivative is needed.

## Minor arcs and the remaining expressions

The minor-arc contribution is evaluated from the explicit formula

```math
\overline R_{\mathrm{minor}}
=
\frac{e^{-tK}C^{d/2}}{1-e^{-t}}.
```

The proof bounds $`C`$ by the maximum of two endpoint values of a convex
scalar function. The program encloses both endpoints and their maximum,
and verifies $`C<1`$. It does not numerically sample minor arcs.

It then evaluates, with the same theta upper expressions,

```math
\begin{aligned}
D_0&=
e^{-tK}\left(\frac\alpha\beta\right)^{d/2}
\frac{1+\eta_\beta}{1-\eta_\alpha},\\
\overline R&=
\overline R_{\mathrm{zero}}+
\overline R_{\mathrm{parity}}+
\overline R_{\mathrm{minor}},\\
\overline Q_0^2&=
\vartheta(\varepsilon A)^d
\left[\vartheta((2-\varepsilon)A/B^2)^d-1\right],\\
V&=\frac{(\overline R+D_0\overline Q_0)^2}{(1-\eta_\alpha)^2},\\
\chi^2(\nu\|U)&\le
\frac{(\overline Q_0+\overline R)^2}{(1-D_0)^2}.
\end{aligned}
```

Here $`A=\pi^2/\alpha`$ and $`\varepsilon=1/100`$ in the expression for
$`\overline Q_0`$. The cap extension uses equations (25)–(27) of
[norm_tail_smoothing.md](norm_tail_smoothing.md).

### Parameter and domain checks

A successful run also establishes all of the following:

- The supplied $`\sigma`$ interval contains the exact Falcon specification
  value $`B\sqrt{\log(4n(1+\sqrt{2^{64}\lambda}))/(2\pi^2)}`$, with
  $`\lambda=128`$ or $`256`$ as appropriate.
- The unrounded specification value $`1.21d\sigma_{\rm spec}^2`$ lies in
  $`[T,T+1)`$.
- Every integer $`1\le b\le512`$ is coprime to $`12289`$, so all Dirichlet
  denominators are invertible modulo the quotient order $`12289^n`$.
- The tail contour has $`t>0`$, the integration extension covers both major
  arcs, and $`L_{\max}<\pi`$.
- $`\eta_\alpha<1`$, both major-arc denominators are positive, and the
  uniform tail bounds are below $`1`$.
- Both theta corrections under square roots are positive.
- The rectangle count is exactly ten times the number of pieces per
  block, and every reported output ball is finite.
- The final bounds meet every power-of-two contract in the first table.

These checks concern the analytic parameter ranges and the evaluated
expressions. A concrete public key must separately satisfy the lattice and
Gram–Schmidt hypotheses; the certificate does not inspect a public key.

## Independent identity checks

The standard-library program
[norm_circle_identity_checks.py](../verification/norm_circle_identity_checks.py)
provides a different kind of verification:

~~~sh
python verification/norm_circle_identity_checks.py
~~~

It checks the twisted quadratic Gauss expansion for all relatively prime
$`a,b`$ with $`b\le32`$, including periodic and antiperiodic phases. It checks
the scaled-dual merger on a two-dimensional quotient of order 17, with
both zero and half-integer shifts. It also evaluates a noncoprime example
where the kernel factor in the general merger formula is necessary.

Finally, it compares the upper-tail contour with a direct finite Gaussian
sum on the same small quotient. These calculations use ordinary floating
point and finite summation ranges. They are intended to detect phase,
normalization, and missing-hypothesis errors. The general identities are
proved in the analytic document; the high-dimensional inequalities are
certified by the separate Arb program.

The standard-library checks and the Arb certificate have no access to
secret keys, signing-oracle transcripts, or network services during
execution.

## References

The arithmetic design is described by Johansson2017Arb in
[bibliography.bib](../references/bibliography.bib):

- Fredrik Johansson, [*Arb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic*](https://doi.org/10.1109/TC.2017.2690633),
  IEEE Transactions on Computers 66(8), 1281–1292, 2017.
- [python-flint Arb interface](https://python-flint.readthedocs.io/en/stable/arb.html).
- [FLINT real-ball arithmetic contract](https://flintlib.org/doc/arb.html).
