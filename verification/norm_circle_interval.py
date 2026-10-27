#!/usr/bin/env python3
"""Certify the explicit norm-tail bounds with FLINT/Arb ball arithmetic.

Proof: science/norm_tail_smoothing.md.
Numerical method: science/numerical_certificate.md.

Dependency used for the checked output: python-flint==0.8.0 (FLINT 3.3.1).
All noninteger inputs are exact rational/decimal strings or certified balls.
Each displayed ball encloses an *upper-bound expression*, not the unknown
lattice's actual tail norm or variance.  A successful run proves the stated
inequalities conditional on the analytic hypotheses in the proof document.

Run from the repository root:
    python verification/norm_circle_interval.py

The default run evaluates both parameter sets at 256 bits using 512 upper
rectangles per dyadic interval.  The program writes only to standard output.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import flint
from flint import arb, ctx


@dataclass(frozen=True)
class Parameters:
    n: int
    sigma_low: str
    sigma_high: str
    threshold: int
    security_level: int
    variance_bits: int
    tail_contract_exponent: str
    image_chi2_bits: int


PARAMETERS = (
    Parameters(
        512,
        "165.736617182977",
        "165.736617182979",
        34034726,
        128,
        90,
        "-4559/100",
        81,
    ),
    Parameters(
        1024,
        "168.388571446543",
        "168.388571446545",
        70265242,
        256,
        120,
        "-6041/100",
        83,
    ),
)


def require(condition: bool, message: str) -> None:
    """Fail unless a condition has been established by ball comparison.

    Ordinary assertions are intentionally avoided: python -O must not disable
    any certificate gate.  Arb comparisons are true only if the inequality is
    established for every number in the supplied balls.
    """
    if not condition:
        raise ArithmeticError(message)


def theta_minus_one_upper(x: arb) -> arb:
    r"""Evaluate a proved upper expression for theta(x)-1, for x>0.

    For x>=1 use
        2 sum_{k=1}^{11} exp(-x k^2)
        + 2 exp(-144x)/(1-exp(-25x)).
    The last term bounds every term from k=12 onward.  If the whole input
    ball is below 1, Jacobi's identity maps the calculation to pi^2/x>1.

    The returned ball encloses this upper expression, rather than theta-1
    itself.  This distinction avoids treating a positive tail upper bound
    as an equality.  It is sufficient for every subsequent inequality.
    """
    require(x > 0, "theta requires a strictly positive argument")
    if x.upper() < 1:
        transformed = arb.pi() ** 2 / x
        return (arb.pi() / x).sqrt() * (
            1 + theta_minus_one_upper(transformed)
        ) - 1
    partial = 2 * sum((-(k * k) * x).exp() for k in range(1, 12))
    remainder = 2 * (-144 * x).exp() / (-(-25 * x).expm1())
    return partial + remainder


def theta_power_upper(x: arb, exponent: int) -> arb:
    """Upper expression for theta(x)**exponent, evaluated without loss at 1."""
    return (exponent * theta_minus_one_upper(x).log1p()).exp()


def theta_power_minus_one_upper(x: arb, exponent: int) -> arb:
    """Upper expression for theta(x)**exponent-1 without cancellation."""
    return (exponent * theta_minus_one_upper(x).log1p()).expm1()


def log2(x: arb) -> arb:
    return x.log() / arb(2).log()


def pow2(exponent: int | str) -> arb:
    return (arb(exponent) * arb(2).log()).exp()


def grid(pieces: int):
    """Rational endpoint numerators over pieces, in units of beta."""
    for j in range(pieces):
        yield j, j + 1, True
    scale = 1
    while scale < 512:
        for j in range(pieces):
            yield scale * (pieces + j), scale * (pieces + j + 1), False
        scale *= 2


def evaluate(parameters: Parameters, pieces: int) -> dict[str, arb]:
    """Evaluate the upper-bound formulas and verify their numerical contracts."""
    n = parameters.n
    d = 2 * n
    K = parameters.threshold + 1
    sigma_low = arb(parameters.sigma_low)
    sigma_high = arb(parameters.sigma_high)
    sigma = sigma_low.union(sigma_high)
    B = arb("117/100") * arb(12289).sqrt()
    pi = arb.pi()

    # Falcon v1.2, equations (2.13) and (2.14).  This check establishes that
    # the analytic parameter range contains the exact specification value.
    spec_sigma = B * (
        (4 * n * (1 + (arb(2) ** 64 * parameters.security_level).sqrt())).log()
        / (2 * pi**2)
    ).sqrt()
    require(spec_sigma > sigma_low, "specification sigma below input range")
    require(spec_sigma < sigma_high, "specification sigma above input range")
    spec_norm_squared = arb("121/100") * d * spec_sigma**2
    require(
        spec_norm_squared >= parameters.threshold,
        "squared-norm specification below T",
    )
    require(spec_norm_squared < K, "squared-norm specification reaches K")

    alpha = 1 / (2 * sigma**2)
    beta = arb(d) / (2 * K)
    t = alpha - beta
    Q = 512
    require(
        all(gcd(b, 12289) == 1 for b in range(1, Q + 1)),
        "a Dirichlet denominator is not invertible in the quotient",
    )
    L = pi / Q
    extended_L = 512 * beta
    require(t > 0, "the upper-tail contour requires alpha>beta")
    require(extended_L > L, "extended integration interval misses a major arc")
    require(extended_L < pi, "zero-arc denominator monotonicity requires Lmax<pi")

    eta_alpha = theta_power_minus_one_upper(pi**2 / (alpha * B**2), d)
    eta_beta = theta_power_minus_one_upper(pi**2 / (beta * B**2), d)
    require(eta_alpha < 1, "coset Gaussian lower bound is nonpositive")
    tilt = (-t * K).exp()
    exp_minus_t = (-t).exp()
    one_minus_exp_minus_t = -(-t).expm1()
    D0_bound = (
        tilt * (alpha / beta) ** n * (1 + eta_beta) / (1 - eta_alpha)
    )
    require(D0_bound < 1, "uniform tail bound does not imply acceptance")

    # All minor arcs: Dirichlet approximation, the quotient merger, and a
    # convex scalar bound.  No numerical sampling of the arcs is performed.
    r_min = 2 * beta
    r_max = ((Q * beta) ** 2 + (pi / Q) ** 2).sqrt()
    u = (2 / (pi * beta)).sqrt()
    v0 = B * (2 / (3 * pi * beta)).sqrt()

    def minor_scalar(r: arb) -> arb:
        return alpha / r + alpha * (u + v0) + alpha * u * v0 * r

    minor_per_dimension = minor_scalar(r_min).max(minor_scalar(r_max))
    require(minor_per_dimension < 1, "minor-arc bound is not contractive")
    R_minor_bound = (
        tilt * minor_per_dimension**n / one_minus_exp_minus_t
    )

    # Both major arcs use upper rectangles.  The prefactor is largest at
    # the left endpoint, the theta factors at the right endpoint, and the
    # zero-arc denominator is smallest at the left endpoint.
    R_zero_bound = arb(0)
    R_parity_bound = arb(0)
    parity_denominator = 1 + exp_minus_t * extended_L.cos()
    require(parity_denominator > 0, "parity denominator is nonpositive")
    rectangles = 0
    for left, right, central in grid(pieces):
        lo = beta * left / pieces
        hi = beta * right / pieces
        width = beta * (right - left) / pieces
        epsilon = arb("1/100") if central else arb("1/2")
        h_lo = (beta**2 + lo**2).sqrt()
        A_hi = pi**2 * beta / (beta**2 + hi**2)
        common = (
            tilt / pi * width * (alpha / h_lo) ** n
            * theta_power_upper(epsilon * A_hi, n)
        )
        zero_denominator = (
            one_minus_exp_minus_t**2
            + 4 * exp_minus_t * (lo / 2).sin() ** 2
        ).sqrt()
        dual_zero = theta_power_minus_one_upper((2 - epsilon) * A_hi / B**2, d)
        dual_parity = theta_power_minus_one_upper(
            (2 - epsilon) * A_hi / (4 * B**2), d
        )
        require(dual_zero > 0, "zero-arc theta expression is nonpositive")
        require(dual_parity > 0, "parity-arc theta expression is nonpositive")
        R_zero_bound += common * dual_zero.sqrt() / zero_denominator
        R_parity_bound += common * dual_parity.sqrt() / parity_denominator
        rectangles += 1
    require(rectangles == 10 * pieces, "upper-rectangle grid is incomplete")

    R_bound = R_zero_bound + R_parity_bound + R_minor_bound
    A = pi**2 / alpha
    epsilon = arb("1/100")
    Q0_bound = (
        theta_power_upper(epsilon * A, d)
        * theta_power_minus_one_upper((2 - epsilon) * A / B**2, d)
    ).sqrt()
    variance_bound = (R_bound + D0_bound * Q0_bound) ** 2 / (1 - eta_alpha) ** 2
    accepted_image_chi2_bound = (Q0_bound + R_bound) ** 2 / (1 - D0_bound) ** 2

    # Optional cap on a fixed set of n coordinates: |X_j|<=2047.
    cap_bound = (
        2 * n * (1 + eta_alpha) / (1 - eta_alpha)
        * (-arb(2048) ** 2 / (2 * sigma**2)).exp()
    )
    D_cap_bound = D0_bound + cap_bound
    variance_cap_bound = (variance_bound.sqrt() + cap_bound / 2) ** 2
    R_cap_bound = R_bound + (1 + eta_alpha) * cap_bound / 2
    accepted_image_cap_chi2_bound = (
        (Q0_bound + R_cap_bound) ** 2 / (1 - D_cap_bound) ** 2
    )
    require(D_cap_bound < 1, "norm-plus-cap lower acceptance is nonpositive")

    # Public contracts consumed by verification/core_transfer_bounds.py.
    require(
        R_bound < pow2(parameters.tail_contract_exponent),
        "tail L2 bound exceeds the public security-transfer contract",
    )
    require(
        variance_bound < pow2(-parameters.variance_bits),
        "norm acceptance variance exceeds the public bound",
    )
    require(
        variance_cap_bound < pow2(-parameters.variance_bits),
        "norm-plus-cap acceptance variance exceeds the public bound",
    )
    require(
        accepted_image_chi2_bound < pow2(-parameters.image_chi2_bits),
        "accepted-image chi-square bound exceeds the public bound",
    )
    require(
        accepted_image_cap_chi2_bound < pow2(-parameters.image_chi2_bits),
        "norm-plus-cap image chi-square bound exceeds the public bound",
    )

    return {
        "sigma_input_ball": sigma,
        "specification_sigma": spec_sigma,
        "specification_unrounded_norm_squared": spec_norm_squared,
        "B": B,
        "alpha": alpha,
        "beta": beta,
        "t": t,
        "extended_L": extended_L,
        "minor_per_dimension_bound": minor_per_dimension,
        "eta_alpha_bound": eta_alpha,
        "log2_D0_bound": log2(D0_bound),
        "log2_R_zero_bound": log2(R_zero_bound),
        "log2_R_parity_bound": log2(R_parity_bound),
        "log2_R_minor_bound": log2(R_minor_bound),
        "log2_R_bound": log2(R_bound),
        "log2_Q0_bound": log2(Q0_bound),
        "log2_acceptance_variance_bound": log2(variance_bound),
        "log2_accepted_image_chi2_bound": log2(accepted_image_chi2_bound),
        "log2_coordinate_cap_bound": log2(cap_bound),
        "log2_norm_plus_cap_variance_bound": log2(variance_cap_bound),
        "log2_norm_plus_cap_image_chi2_bound": log2(accepted_image_cap_chi2_bound),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, choices=(512, 1024), help="evaluate one parameter set")
    parser.add_argument("--precision-bits", type=int, default=256)
    parser.add_argument("--pieces", type=int, default=512, help="rectangles per dyadic interval")
    args = parser.parse_args()
    if args.precision_bits < 192:
        parser.error("use at least 192 bits for the stated bounds")
    if args.pieces <= 0:
        parser.error("--pieces must be positive")
    ctx.prec = args.precision_bits
    print("backend python-flint", flint.__version__)
    print("FLINT", flint.__FLINT_VERSION__)
    print("precision_bits", ctx.prec)
    print("output_semantics balls_enclose_upper_bound_expressions")
    for parameters in PARAMETERS:
        if args.n is not None and args.n != parameters.n:
            continue
        result = evaluate(parameters, args.pieces)
        print("parameter_n", parameters.n)
        print("d", 2 * parameters.n, "T", parameters.threshold, "K", parameters.threshold + 1)
        print("rectangles_per_major_arc", 10 * args.pieces)
        for label, value in result.items():
            require(value.is_finite(), "nonfinite output: " + label)
            print(label, value.str(45))
        print(
            "CERTIFIED",
            "R_lt_2pow(" + parameters.tail_contract_exponent + ")",
            "variance_with_cap_lt_2pow(-" + str(parameters.variance_bits) + ")",
            "image_chi2_with_cap_lt_2pow(-" + str(parameters.image_chi2_bits) + ")",
            flush=True,
        )


if __name__ == "__main__":
    main()
