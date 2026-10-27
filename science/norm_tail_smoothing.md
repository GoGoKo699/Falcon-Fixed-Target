# Smoothing a discrete Gaussian after a squared-norm cutoff

## Result and scope

This document bounds how much the probability of passing a squared-norm
test varies between lattice cosets. It also bounds the image, modulo the
lattice, of an ambient discrete Gaussian conditioned on passing that test.
The result holds for every lattice satisfying the stated basis and index
conditions. It concerns exact discrete Gaussians. Applying it to a
finite-precision sampler requires an independently established sampler
profile meeting the contract in [security_transfer.md](security_transfer.md).

Let $`n\in\{512,1024\}`$, $`d=2n`$, $`q=12289`$, and
$`B=1.17\sqrt q`$. Let $`\Lambda\subset\mathbb Z^d`$ be a full-rank lattice of
index $`q^n`$ that has a basis with every Gram–Schmidt length at most $`B`$.
Use one of the following parameter sets. The endpoints of the intervals
are exact decimal numbers.

| $`n`$ | $`d`$ | Admissible Gaussian width $`\sigma`$ | Accepted squared norm $`T`$ |
|---:|---:|---|---:|
| 512 | 1024 | $`[165.736617182977,\ 165.736617182979]`$ | 34034726 |
| 1024 | 2048 | $`[168.388571446543,\ 168.388571446545]`$ | 70265242 |

Write $`X\sim D_{\mathbb Z^d,\sigma}`$ for the distribution with mass
proportional to $`\exp(-\|x\|^2/(2\sigma^2))`$. For a coset $`y`$, let

```math
a_y=\Pr[\|X\|^2\le T\mid X\bmod\Lambda=y].
```

**Theorem.** For every such lattice and every $`\sigma`$ in the indicated
interval, with the coset $`y`$ distributed uniformly,

```math
\begin{array}{c|cc}
n&512&1024\\\hline
\mathrm{Var}(a_y)&<2^{-90}&<2^{-120}.
\end{array}
```

Let $`\nu`$ be the distribution of $`X\bmod\Lambda`$ conditional on
$`\|X\|^2\le T`$, and let $`U`$ be the uniform distribution on the quotient.
Then

```math
\begin{array}{c|cc}
n&512&1024\\\hline
\chi^2(\nu\|U)&<2^{-81}&<2^{-83}.
\end{array}
```

Both pairs of inequalities remain valid when acceptance additionally
requires $`|X_j|\le2047`$ on any fixed set of $`n`$ coordinates. This extension
does not impose a bound on the sum of encoded coordinate lengths.

The parameter intervals contain the exact values specified by Falcon v1.2,
equations (2.13)–(2.14). The relation between Falcon key generation and the
basis hypothesis is discussed in [falcon_parameters.md](falcon_parameters.md).
The numeric inequalities follow from the explicit bounds proved below and
the Arb certificate in [numerical_certificate.md](numerical_certificate.md).

## Notation and the two image distributions

Put

```math
\alpha=\frac1{2\sigma^2},\qquad K=T+1,\qquad
G=\mathbb Z^d/\Lambda,\qquad N=|G|.
```

The rejection event is exactly $`\|X\|^2\ge K`$, since $`\|X\|^2`$ is an
integer. Define densities relative to the uniform probability measure on
$`G`$ by

```math
\begin{aligned}
p(y)&=N\Pr[X\bmod\Lambda=y],\\
r(y)&=N\Pr[X\bmod\Lambda=y,\ \|X\|^2\ge K],\\
\delta&=\mathbb E_U r=\Pr[\|X\|^2\ge K].
\end{aligned}
```

In particular $`\mathbb E_U p=1`$. Set

```math
Q_0=\|p-1\|_{L^2(U)},\qquad
R=\|r-\delta\|_{L^2(U)},\qquad
\delta_y=\frac{r(y)}{p(y)},\qquad a_y=1-\delta_y.
```

All coset Gaussian masses are positive. The density of $`\nu`$ relative to
$`U`$ is

```math
\frac{d\nu}{dU}(y)=\frac{p(y)-r(y)}{1-\delta}.
\tag{1}
```

This is the image of an **ambient** Gaussian after acceptance. It is
different from the joint law obtained by first selecting a uniform coset
and then sampling an accepted preimage of that coset. The signing laws
and their comparison are defined in
[signing_model.md](signing_model.md) and
[security_transfer.md](security_transfer.md).

For $`c>0`$, use

```math
\rho_c(S)=\sum_{x\in S}e^{-c\|x\|^2},\qquad
\vartheta(c)=\rho_c(\mathbb Z).
```

The dual lattice is $`\Lambda^*=\{w:\langle w,\Lambda\rangle\subseteq \mathbb Z\}`$. Characters of $`G`$ are indexed by
$`\widehat G=\Lambda^*/\mathbb Z^d`$. Parseval's identity, with the uniform
probability normalization, gives

```math
R^2=\sum_{w\in\widehat G\setminus\{0\}}
\left|
\mathbb E\left[e^{2\pi i\langle w,X\rangle}
\mathbf1_{\{\|X\|^2\ge K\}}\right]
\right|^2.
\tag{2}
```

Signs of character representatives do not affect any bound below.

## Gaussian estimates from the basis hypothesis

### Dual mass and translated mass

The dual basis, in reverse order, has Gram–Schmidt lengths equal to the
reciprocals of the original lengths. These lengths are therefore at least
$`1/B`$. Successive summation over its integer coefficients, using
$`\rho_c(\mathbb Z+u)\le\rho_c(\mathbb Z)`$, proves

```math
\rho_c(\Lambda^*)\le\vartheta(c/B^2)^d.
\tag{3}
```

To justify the translated-mass inequality used here and later, Poisson
summation for any full-rank lattice $`L`$ gives

```math
\rho_c(L+z)=\frac{(\pi/c)^{d/2}}{\det L}
\sum_{w\in L^*}e^{-\pi^2\|w\|^2/c}
e^{2\pi i\langle w,z\rangle}.
```

The absolute value is at most the same sum with every phase replaced by
$`1`$, which is $`\rho_c(L)`$. Thus the maximum Gaussian mass of a translate
occurs at an unshifted lattice. The one-dimensional integral comparison
also gives

```math
\vartheta(c)\le1+\sqrt{\pi/c}.
\tag{4}
```

Define

```math
\eta_c=\vartheta\!\left(\frac{\pi^2}{cB^2}\right)^d-1.
```

Poisson summation and (3) imply, for every real translate $`z`$,

```math
\frac{(\pi/c)^{d/2}}{N}(1-\eta_c)
\le\rho_c(\Lambda+z)
\le\frac{(\pi/c)^{d/2}}{N}(1+\eta_c).
\tag{5}
```

The lower bound is useful when $`\eta_c<1`$, as it is at the parameters
used here.

### Unconditioned quotient image

For an integral coset representative $`y`$, Poisson summation expresses
$`p(y)`$ as

```math
p(y)=
\frac{\sum_{w\in\Lambda^*}e^{-A\|w\|^2}
e^{2\pi i\langle w,y\rangle}}
{\rho_A(\mathbb Z^d)},\qquad A=\frac{\pi^2}{\alpha}.
```

All integer dual vectors contribute phase $`1`$. Subtracting the
denominator before taking absolute values yields

```math
|p(y)-1|
\le\frac{\rho_A(\Lambda^*)-\rho_A(\mathbb Z^d)}
{\rho_A(\mathbb Z^d)}
\le\eta_\alpha.
\tag{6}
```

This cancellation is why no additional ambient-normalization error is
needed in (6).

For $`0<\varepsilon<2`$, weighted Cauchy–Schwarz gives

```math
\rho_A(C)^2\le
\rho_{\varepsilon A}(C)\rho_{(2-\varepsilon)A}(C).
\tag{7}
```

The Fourier coefficient of the unconditioned quotient image at $`w`$ is
$`\rho_A(\mathbb Z^d-w)/\rho_A(\mathbb Z^d)`$. Apply (7), bound its first
factor by the unshifted mass, sum the second over all nontrivial
characters, and drop a denominator that is at least $`1`$. The result is

```math
Q_0^2\le
\vartheta(\varepsilon A)^d
\left[
\vartheta\!\left(\frac{(2-\varepsilon)A}{B^2}\right)^d-1
\right].
\tag{8}
```

The numerical certificate uses $`\varepsilon=1/100`$ in (8).

## An exact contour for the rejected tail

Choose

```math
\beta=\frac{d}{2K},\qquad t=\alpha-\beta>0,
```

and define

```math
\Theta(z,u)=\sum_{x\in\mathbb Z}e^{-zx^2+2\pi iux},
\qquad Z_\alpha=\Theta(\alpha,0).
```

For each character $`w`$, the tail Fourier coefficient is exactly

```math
\begin{aligned}
&\mathbb E\left[e^{2\pi i\langle w,X\rangle}
\mathbf1_{\{\|X\|^2\ge K\}}\right]\\
&\quad=
\frac{e^{-tK}}{2\pi Z_\alpha^d}
\int_{-\pi}^{\pi}
\frac{\prod_{j=1}^d\Theta(\beta-i\theta,w_j)
e^{-iK\theta}}
{1-e^{-t-i\theta}}\,d\theta.
\end{aligned}
\tag{9}
```

Indeed, expand the denominator as
$`\sum_{j\ge0}e^{-tj-ij\theta}`$. For a lattice vector of squared norm
$`m`$, the integral selects $`m-K-j=0`$. Such a $`j`$ exists exactly when
$`m\ge K`$, and the remaining weight is
$`e^{-tK}e^{-\beta m}e^{-t(m-K)}=e^{-\alpha m}`$.
The exchanges of sums and integrals are justified by
$`\beta>0`$, $`t>0`$, and absolute convergence.

Apply Minkowski's integral inequality to the finite vector of nontrivial
Fourier coefficients in (9). It remains to bound its Euclidean norm at
each angle $`\theta`$. The following rational-arc calculation supplies this
bound without a factor depending on $`N`$.

## Rational angles and the finite-quotient identity

### Twisted quadratic Gauss sums

Write

```math
\theta=\frac{\pi a}{b}+v,\qquad
b\ge1,\quad \gcd(a,b)=1,
```

and put $`\eta=0`$ if $`ab`$ is even and $`\eta=1/2`$ otherwise. The quadratic
phase $`f(x)=e^{i\pi ax^2/b}`$ satisfies
$`f(x+b)=(-1)^{ab}f(x)`$. Consequently

```math
f(x)=\sum_{\ell=0}^{b-1}c_\ell
e^{2\pi i(\ell+\eta)x/b},\qquad |c_\ell|=b^{-1/2}.
\tag{10}
```

Here is a direct proof of the magnitude. The sequence
$`g(x)=f(x)e^{-2\pi i\eta x/b}`$ is $`b`$-periodic. Its autocorrelation at
shift $`h`$ is a constant of absolute value $`1`$ times
$`\sum_{x=0}^{b-1}e^{2\pi iahx/b}`$. Coprimality makes this sum zero for
$`h\not\equiv0\pmod b`$ and equal to $`b`$ for $`h\equiv0\pmod b`$.
Taking its discrete Fourier transform shows
$`|c_\ell|^2=b/b^2=1/b`$ for every $`\ell`$.

Set

```math
z=\beta-iv,\qquad h=|z|,\qquad
A_v=\frac{\pi^2\beta}{h^2}.
```

Complex Poisson summation is valid since $`\Re z>0`$. Combining it with
(10), then using the triangle inequality in each coordinate, gives

```math
\left|\prod_{j=1}^d\Theta(\beta-i\theta,w_j)\right|
\le
\left(\frac\pi{bh}\right)^{d/2}
\rho_{A_v}\!\left(b^{-1}(\mathbb Z^d+\eta\mathbf1)-w\right).
\tag{11}
```

In one dimension the sums over the $`b`$ frequency shifts and the Poisson
integer combine into $`b^{-1}(\mathbb Z+\eta)`$. The sign of $`\eta`$ is
irrelevant because $`\mathbb Z-\eta=\mathbb Z+\eta`$ for these two choices.

### Merging the character sum

If $`\gcd(b,N)=1`$, multiplication by $`b`$ permutes
$`\Lambda^*/\mathbb Z^d`$. For any $`c>0`$,

```math
\sum_{w\in\Lambda^*/\mathbb Z^d}
\rho_c\!\left(b^{-1}(\mathbb Z^d+\eta\mathbf1)-w\right)
=
\rho_{c/b^2}(\Lambda^*+\eta\mathbf1).
\tag{12}
```

To see this, multiply each vector inside the mass by $`b`$. The resulting
sets are $`\mathbb Z^d+\eta\mathbf1-bw`$. They form a disjoint coset
decomposition of $`\Lambda^*+\eta\mathbf1`$ because $`w\mapsto bw`$ is a
permutation of the quotient. The squared norms acquire the factor
$`1/b^2`$.

The coprimality hypothesis is substantive. For a general $`b`$, the same
calculation instead gives

```math
|\ker(b:\widehat G\to\widehat G)|\,
\rho_{c/b^2}(\mathbb Z^d+b\Lambda^*+\eta\mathbf1).
\tag{13}
```

Thus (12) cannot be used unchanged at a denominator sharing a prime
factor with the quotient order.

Apply (7) to the mass in (11). Its first factor is at most
$`\vartheta(\varepsilon A_v/b^2)^d`$. Sum the second factor using (12),
bound a translate by its unshifted mass, and then use (3). Finally,
$`Z_\alpha\ge\sqrt{\pi/\alpha}`$. The Euclidean norm over **all** characters
of the product in (9), normalized by $`Z_\alpha^d`$, is at most

```math
\left[
\frac\alpha{bh}
\vartheta\!\left(\frac{\varepsilon A_v}{b^2}\right)
\vartheta\!\left(\frac{(2-\varepsilon)A_v}{b^2B^2}\right)
\right]^{d/2}.
\tag{14}
```

It is also an upper bound after the trivial character is omitted.

## Minor arcs

Set $`Q=512`$ and $`L=\pi/Q`$. Dirichlet approximation supplies, for every
$`\theta\in[-\pi,\pi]`$, relatively prime integers $`a,b`$ such that

```math
1\le b\le Q,\qquad
\left|\theta-\frac{\pi a}{b}\right|\le\frac\pi{bQ}.
```

Because $`N=12289^n`$, every denominator in this range is coprime to $`N`$.
Outside the intervals at distance at most $`L`$ from $`0`$ and from the
identified endpoints $`\pm\pi`$, the selected denominator must satisfy
$`b\ge2`$.

Use $`\varepsilon=1/2`$ in (14). For $`r=bh`$, define

```math
\begin{aligned}
r_{\min}&=2\beta,&
r_{\max}&=\sqrt{(Q\beta)^2+(\pi/Q)^2},\\
u&=\sqrt{\frac2{\pi\beta}},&
v_0&=B\sqrt{\frac2{3\pi\beta}},\\
F(r)&=\frac\alpha r+\alpha(u+v_0)+\alpha u v_0r,&
C&=\max\{F(r_{\min}),F(r_{\max})\}.
\end{aligned}
```

The Dirichlet bound gives $`r_{\min}\le r\le r_{\max}`$. Applying (4) to
the two theta factors in (14) bounds the expression inside the brackets
by $`F(r)`$. Since $`F''(r)=2\alpha/r^3>0`$, it is at most $`C`$ throughout
this interval.

The contour denominator has modulus at least $`1-e^{-t}`$. Bounding the
total minor-arc length by $`2\pi`$ therefore gives

```math
\overline R_{\mathrm{minor}}
=\frac{e^{-tK}C^{d/2}}{1-e^{-t}}.
\tag{15}
```

This argument does not require an enumeration or a disjoint partition of
all rational arcs.

## The zero and parity arcs

The all-character estimate (14) would retain an unnecessarily large
trivial term near $`\theta=0`$. Near $`\theta=\pm\pi`$, a different
arithmetic term needs to be removed.

### Removing the zero term at the origin

For $`b=1`$, $`a=0`$, and $`\eta=0`$,

```math
\sum_{w\ne0}\rho_c(\mathbb Z^d-w)
=\rho_c(\Lambda^*)-\rho_c(\mathbb Z^d)
\le\vartheta(c/B^2)^d-1.
\tag{16}
```

This is the character sum arising after weighted Cauchy–Schwarz.

### The half-character at the parity angle

At $`\theta=\pi`$, the identity

```math
(-1)^{\|x\|^2}=(-1)^{\sum_jx_j}
```

turns the quadratic phase into the character $`\mathbf1/2`$. This is a
discrete arithmetic contribution; replacing the integer Gaussian by a
continuous radial approximation would omit it.

Since $`N`$ is odd, $`\mathbf1/2\notin\Lambda^*`$: its class would otherwise
have order $`2`$ in $`\Lambda^*/\mathbb Z^d`$. Multiplication by $`2`$ injects
$`\Lambda^*+\mathbf1/2`$ into $`\Lambda^*\setminus\{0\}`$. Therefore

```math
\rho_c(\Lambda^*+\mathbf1/2)
\le\rho_{c/4}(\Lambda^*)-1
\le\vartheta\!\left(\frac{c}{4B^2}\right)^d-1.
\tag{17}
```

For an even-index quotient this removal of the zero term need not be
valid. The odd-index condition and the denominator coprimality condition
have distinct roles in the proof.

### Major-arc integrals

For $`v\ge0`$, write

```math
h(v)=\sqrt{\beta^2+v^2},\qquad
A(v)=\frac{\pi^2\beta}{\beta^2+v^2},
```

and, for $`s\in\{1,4\}`$ and $`0<\varepsilon<2`$, define

```math
H_s(v;\varepsilon)=
\left(\frac\alpha{h(v)}\right)^{d/2}
\vartheta(\varepsilon A(v))^{d/2}
\sqrt{
\vartheta\!\left(\frac{(2-\varepsilon)A(v)}{sB^2}\right)^d-1
}.
```

Equations (16)–(17), inserted into the derivation of (14), yield

```math
\overline R_{\mathrm{zero}}
=\frac{e^{-tK}}\pi
\int_0^L
\frac{H_1(v;\varepsilon(v))}
{\sqrt{(1-e^{-t})^2+4e^{-t}\sin^2(v/2)}}\,dv,
\tag{18}
```

and

```math
\overline R_{\mathrm{parity}}
=\frac{e^{-tK}}{\pi(1+e^{-t}\cos L)}
\int_0^L H_4(v;\varepsilon(v))\,dv.
\tag{19}
```

For (19), $`|1+e^{-t-iv}|\ge1+e^{-t}\cos L`$ when $`|v|\le L`$.
The two pieces adjoining $`\pi`$ and $`-\pi`$ together account for a full
interval of length $`2L`$, which explains the factor $`1/\pi`$ in (19).
Each pointwise estimate holds for every $`\varepsilon\in(0,2)`$, so
$`\varepsilon(v)`$ may be selected separately on different intervals.

Combining the three angular regions with Minkowski's inequality gives

```math
R\le\overline R:=
\overline R_{\mathrm{zero}}+
\overline R_{\mathrm{parity}}+
\overline R_{\mathrm{minor}}.
\tag{20}
```

The certificate enlarges both major-arc integrals to
$`L_{\max}=512\beta\ge L`$, replaces the denominator in (19) by
$`1+e^{-t}\cos L_{\max}`$, and uses proved upper rectangles. It checks
$`L_{\max}<\pi`$, which ensures the required denominator monotonicity.
These changes only enlarge the bounds. The complete quadrature argument
and the explicit theta-series remainder appear in
[numerical_certificate.md](numerical_certificate.md).

## From tail smoothing to acceptance variance

### A uniform coset tail bound

Markov's inequality and (5) give, for every coset $`y`$,

```math
\begin{aligned}
\delta_y
&\le e^{-tK}
\frac{\rho_\beta(\Lambda+y)}{\rho_\alpha(\Lambda+y)}\\
&\le
D_0:=e^{-tK}\left(\frac\alpha\beta\right)^{d/2}
\frac{1+\eta_\beta}{1-\eta_\alpha}.
\end{aligned}
\tag{21}
```

In particular $`\delta\le D_0`$ and $`a_y\ge1-D_0`$.

### Variance across uniformly selected cosets

The ambient rejection mean $`\delta`$ need not equal
$`\mathbb E_U\delta_y`$. Nevertheless,

```math
\delta_y-\delta=\frac{r(y)-\delta p(y)}{p(y)}.
```

Use $`p(y)\ge1-\eta_\alpha`$ from (6), the $`L^2`$ triangle inequality,
and $`\delta\le D_0`$ to obtain

```math
\begin{aligned}
\mathrm{Var}_U(a_y)
&=\mathrm{Var}_U(\delta_y)\\
&\le\|\delta_y-\delta\|_{L^2(U)}^2\\
&\le\frac{(R+D_0Q_0)^2}{(1-\eta_\alpha)^2}
\le V,
\end{aligned}
\tag{22}
```

where $`V`$ is the last expression with the certified upper bounds for
$`R`$ and $`Q_0`$ substituted. The second line uses the elementary fact that
variance is the smallest mean squared error around a constant; it does
not equate the two rejection means.

### Image of the accepted ambient Gaussian

From (1),

```math
\frac{d\nu}{dU}-1
=\frac{(p-1)-(r-\delta)}{1-\delta}.
```

Consequently

```math
\chi^2(\nu\|U)
\le\frac{(Q_0+R)^2}{(1-D_0)^2}.
\tag{23}
```

The following are conservative upper bounds on the base-two logarithms
of the computed upper-bound expressions. Every displayed decimal has
been rounded upward; the complete enclosing balls are saved with the
certificate.

| Bound | $`n=512`$ | $`n=1024`$ |
|---|---:|---:|
| Uniform coset rejection $`D_0`$ | $`-14.31496`$ | $`-28.62992`$ |
| Zero-arc contribution $`\overline R_{\mathrm{zero}}`$ | $`-68.25478`$ | $`-84.41017`$ |
| Parity-arc contribution $`\overline R_{\mathrm{parity}}`$ | $`-45.60045`$ | $`-60.41745`$ |
| Minor-arc contribution $`\overline R_{\mathrm{minor}}`$ | $`-222.19277`$ | $`-470.14170`$ |
| Total tail norm upper bound $`\overline R`$ | $`-45.60045`$ | $`-60.41745`$ |
| Unconditioned image norm upper bound for $`Q_0`$ | $`-40.76750`$ | $`-41.76000`$ |
| Acceptance variance upper bound $`V`$ | $`-91.19687`$ | $`-120.83204`$ |
| Accepted-image $`\chi^2`$ upper bound | $`-81.43535`$ | $`-83.51999`$ |

In particular, the certificate proves the slightly looser tail contracts
$`R<2^{-45.59}`$ and $`R<2^{-60.41}`$. Those exact rational exponents are
used as the interface to the separate security-transfer calculation.

## Optional individual coordinate cap

Let $`I\subseteq\{1,\ldots,d\}`$ be a fixed set of $`m`$ coordinates. For any
real $`s`$, completing the square and applying (5) to the shifted coset
shows

```math
\mathbb E[e^{sX_j}\mid X\bmod\Lambda=y]
\le
\frac{1+\eta_\alpha}{1-\eta_\alpha}
e^{\sigma^2s^2/2}.
\tag{24}
```

Chernoff's inequality, optimized at $`s=L_0/\sigma^2`$, and a union bound
therefore give

```math
\Pr[\exists j\in I:\ |X_j|\ge L_0\mid X\bmod\Lambda=y]
\le
C_{\mathrm{cap}}:=
2m\frac{1+\eta_\alpha}{1-\eta_\alpha}
e^{-L_0^2/(2\sigma^2)}.
\tag{25}
```

For $`m=n`$ and $`L_0=2048`$, this is below $`2^{-100.14568}`$ for $`n=512`$
and below $`2^{-95.70363}`$ for $`n=1024`$.

Define

```math
b_y=\Pr[\|X\|^2\le T\text{ and the cap fails}\mid X\bmod\Lambda=y].
```

Then $`0\le b_y\le C_{\mathrm{cap}}`$ and the new acceptance probability
is $`a'_y=a_y-b_y`$. Popoviciu's inequality and the triangle inequality for
centered $`L^2`$ norms imply

```math
\mathrm{Var}_U(a'_y)
\le\left(\sqrt V+\frac{C_{\mathrm{cap}}}{2}\right)^2,
\qquad
a'_y\ge1-D_0-C_{\mathrm{cap}}.
\tag{26}
```

For completeness, the ambient rejected-tail density grows by
$`e(y)=p(y)b_y`$. By (6),
$`0\le e(y)\le(1+\eta_\alpha)C_{\mathrm{cap}}`$. Thus its centered
$`L^2`$ norm is at most $`(1+\eta_\alpha)C_{\mathrm{cap}}/2`$, and its mean
is at most $`C_{\mathrm{cap}}`$, since $`\mathbb E_U p=1`$. If $`\nu'`$ is
the ambient image conditioned on both tests, then

```math
\chi^2(\nu'\|U)
\le
\frac{\left(Q_0+R+(1+\eta_\alpha)C_{\mathrm{cap}}/2\right)^2}
{(1-D_0-C_{\mathrm{cap}})^2}.
\tag{27}
```

The certificate checks (26)–(27). Their additions are small enough that
the theorem's stated powers of two remain valid. This treatment of the
cap is through variance and density bounds; it does not require charging
every cap overflow as a separate failure event.

## Boundaries and relation to earlier analysis

The proof uses the integer squared norm, the quotient's arithmetic, and a
uniform bound on Gram–Schmidt lengths. It does not prove an analogous
result for an arbitrary acceptance predicate. In particular, a summed
padded-encoding budget is an additional predicate outside this theorem.
It also does not establish an implementation's precision error,
deterministic signing policy, or chosen-target security by itself.

The Gaussian contour, rational arcs, Poisson summation, and quadratic
Gauss sums are classical tools. Magyar's analysis of discrete spheres is
a direct methodological reference. Continuous lattice smoothing and
code-smoothing results provide related Fourier techniques, but their
stated distributions and hypotheses differ from this integer norm-tail
calculation. The comparison with these works and with recent Falcon
analyses is given in [related_work.md](../references/related_work.md).

References used here are Falcon2020Spec, Magyar1997,
DebrisAlazardEtAl2023, and JiaEtAl2026 in
[bibliography.bib](../references/bibliography.bib). Canonical entry points:

- [Falcon v1.2 specification](https://falcon-sign.info/falcon.pdf),
  equations (2.13)–(2.14).
- [Magyar, *L^p-bounds for spherical maximal operators on Z^n*](https://doi.org/10.4171/RMI/222).
- [Debris-Alazard, Ducas, Resch and Tillich, *Smoothing Codes and Lattices*](https://arxiv.org/abs/2205.10552).
- [Jia et al., *Revisiting the Concrete Security of Falcon-Type Signatures*](https://eprint.iacr.org/2026/096).
