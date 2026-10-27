#!/usr/bin/env python3
"""Rigorous arithmetic for the CoreFalcon security-transfer bounds.

Requires python-flint==0.8.0. All transcendental calculations use Arb balls.
No binary floating-point constants enter the mathematical expressions.

The norm-tail contracts are proved in science/norm_tail_smoothing.md and
checked independently by verification/norm_circle_interval.py. This program
imports those two explicit contracts, derives accepted-image and FFO moments,
and checks the numerical claims in science/security_transfer.md. Printed balls
enclose *upper-bound expressions*, not the unknown distribution's divergence.
"""

from __future__ import annotations

import argparse
from math import isqrt

import flint
from flint import arb, ctx


def require(condition: bool, message: str) -> None:
    """Keep certificate checks enabled even when Python is invoked with -O."""
    if not condition:
        raise ArithmeticError(message)


def log2(value: arb) -> arb:
    return value.log() / arb(2).log()


def theta_excess_upper(argument: arb) -> arb:
    """An analytic upper bound on theta(argument)-1 for argument > 1.

    The omitted terms start at k=12. Their successive squared exponents
    differ by at least 25, giving the displayed geometric-series remainder.
    Arb encloses the finite expression rigorously; its upper endpoint is
    therefore also an upper bound on the infinite theta excess.
    """
    require(argument > 1, "theta-series argument must be greater than one")
    partial = arb(2) * sum(
        ((-argument * k * k).exp() for k in range(1, 12)), arb(0)
    )
    remainder = arb(2) * (-144 * argument).exp() / (
        -(-25 * argument).expm1()
    )
    return partial + remainder


def theta_power_excess_upper(argument: arb, dimension: int) -> arb:
    excess = theta_excess_upper(argument)
    return (dimension * excess.log1p()).expm1()


def print_ball(label: str, value: arb) -> None:
    require(value.is_finite(), f"nonfinite output: {label}")
    print(f"{label}: {value.str(28, more=True)}")


def parameters(n: int) -> dict[str, arb | int]:
    require(n in (512, 1024), "unsupported parameter set")
    d = 2 * n
    target = 34_034_726 if n == 512 else 70_265_242
    k_tail = target + 1
    reference_queries = arb(2) ** 64
    spec_level = 128 if n == 512 else 256
    epsilon = 1 / (reference_queries * spec_level).sqrt()
    gs_bound = arb("117/100") * arb(12_289).sqrt()
    sigma = gs_bound * (
        (4 * n * (1 + 1 / epsilon)).log() / (2 * arb.pi() ** 2)
    ).sqrt()

    # Gaussian exponent coefficient is tau, distinct from Renyi order rho.
    tau = 1 / (2 * sigma * sigma)
    beta = arb(d) / (2 * k_tail)
    tilt = tau - beta
    require(tilt > 0, "upper-tail tilt must be positive")
    eta = theta_power_excess_upper(arb.pi() ** 2 / (tau * gs_bound**2), d)
    eta_beta = theta_power_excess_upper(
        arb.pi() ** 2 / (beta * gs_bound**2), d
    )
    require(eta < 1, "Gaussian flatness denominator must be positive")
    rejection = (
        -tilt * k_tail
        + n * (tau / beta).log()
        + eta_beta.log1p()
        - (-eta).log1p()
    ).exp()

    split = arb("1/100")
    poisson_argument = arb.pi() ** 2 / tau
    first_factor = (
        d * theta_excess_upper(split * poisson_argument).log1p()
    ).exp()
    second_factor = theta_power_excess_upper(
        (2 - split) * poisson_argument / gs_bound**2, d
    )
    base_l2_upper = (first_factor * second_factor).sqrt()

    # These are deliberately rounded outward from the independent circle
    # certificate. That script explicitly verifies these same inequalities.
    tail_log2 = arb("-4559/100") if n == 512 else arb("-6041/100")
    tail_l2_upper = (arb(2).log() * tail_log2).exp()
    chi2_expression = (base_l2_upper + tail_l2_upper) ** 2 / (1 - rejection) ** 2
    chi2_bits = 81 if n == 512 else 83
    chi2_contract = arb(2) ** (-chi2_bits)
    require(
        chi2_expression < chi2_contract,
        "accepted-image chi-square contract was not certified",
    )
    lower_density = (1 - eta) * (1 - rejection)
    require(lower_density > 0, "accepted-image lower density must be positive")

    # FFO's pointwise profile: Fouque et al., Lemma 20's normalization
    # argument (p.41), transported by FFO Lemma 22 / Appendix F.3.
    # This does not identify FFO's output law with ordinary Klein.
    leaf_error = epsilon / d
    log_b = d * (leaf_error.log1p() - (-leaf_error).log1p())
    b = log_b.exp()
    require(b * rejection < 1, "actual sampler's acceptance bound must be positive")

    return {
        "n": n,
        "d": d,
        "T": target,
        "K": k_tail,
        "sigma": sigma,
        "eta": eta,
        "D0": rejection,
        "Q0_upper": base_l2_upper,
        "R_upper": tail_l2_upper,
        "chi2_expression": chi2_expression,
        "chi2_contract": chi2_contract,
        "lower_density": lower_density,
        "log_b": log_b,
        "b": b,
    }


def transfer_case(
    parameter_set: dict[str, arb | int],
    simulator_exponent: int,
    order: int,
    claimed_ceiling: str,
) -> None:
    n = int(parameter_set["n"])
    rejection = parameter_set["D0"]
    log_b = parameter_set["log_b"]
    b = parameter_set["b"]
    rho = arb(order)
    queries = arb(2) ** 64

    variance_bound = log_b.expm1() * (-(-log_b).expm1())
    sampler_excess = rho * (rho - 1) / 2 * (
        (rho - 2) * log_b
    ).exp() * variance_bound
    log_conditioning = (rho - 1) * (-rejection).log1p() - rho * (
        -b * rejection
    ).log1p()
    conditioning = log_conditioning.exp()
    image_excess = rho * (rho - 1) / 2 * (
        (-rho - 1) * parameter_set["lower_density"].log()
    ).exp() * parameter_set["chi2_contract"]

    log_sampler_moment = (conditioning * sampler_excess).log1p()
    log_image_moment = image_excess.log1p()
    scale = queries / rho / arb(2).log()
    sampler_cost = scale * log_sampler_moment
    image_cost = scale * log_image_moment
    conditioning_increment = scale * (
        log_conditioning.expm1() * sampler_excess / (1 + sampler_excess)
    ).log1p()
    transfer_loss = arb(simulator_exponent) / rho + sampler_cost + image_cost
    require(transfer_loss < arb(claimed_ceiling), "claimed transfer loss not certified")

    print(f"\nTRANSFER n={n} q_S=2^64 lambda_sim={simulator_exponent} rho={order}")
    print_ball("conditioned_sampler_excess_multiplier", conditioning)
    print_ball("image_transfer_loss_bits", image_cost)
    print_ball("sampler_transfer_loss_bits", sampler_cost)
    print_ball("sampler_conditioning_increment_bits", conditioning_increment)
    print_ball("total_transfer_loss_bits", transfer_loss)
    print(f"CERTIFIED transfer_loss < {claimed_ceiling} bits")


def runtime_and_format_checks(parameter_set: dict[str, arb | int]) -> None:
    n = int(parameter_set["n"])
    target = int(parameter_set["T"])
    rejection = parameter_set["D0"]
    b = parameter_set["b"]
    queries_int = 2**64
    extra_pool = 2**50 if n == 512 else 2**36
    pool_size = queries_int + extra_pool
    first_bad_count = extra_pool + 1
    frequency = arb(first_bad_count) / pool_size
    require(frequency > rejection, "binomial threshold must exceed its mean")
    relative_entropy = frequency * (frequency / rejection).log() + (
        1 - frequency
    ) * ((1 - frequency) / (1 - rejection)).log()
    pool_failure_bits = pool_size * relative_entropy / arb(2).log()
    require(pool_failure_bits > 1000, "pool-failure target was not certified")

    real_attempt_limit = 32 if n == 512 else 16
    real_cap_failure_bits = -(
        arb(64) + real_attempt_limit * log2(b * rejection)
    )
    require(real_cap_failure_bits > 390, "real-signer cap target was not certified")

    # A norm-passing, coefficient-encodable s2 uses 9n + sum floor(|s2|/128)
    # bits. Cauchy--Schwarz proves this sufficient bound without sampling.
    quotient_bits = isqrt(n * target) // 128
    compressed_length_bound = 41 + (9 * n + quotient_bits + 7) // 8
    maximum_buffer = 752 if n == 512 else 1462
    require(compressed_length_bound <= maximum_buffer, "compressed buffer is insufficient")

    print(f"\nPARAMETERS n={n} d={2*n} T={target} K={target+1}")
    print_ball("official_sigma", parameter_set["sigma"])
    print_ball("eta_upper_expression", parameter_set["eta"])
    print_ball("log2_uniform_coset_rejection_bound", log2(rejection))
    print_ball("log2_accepted_image_chi2_bound", log2(parameter_set["chi2_expression"]))
    print(f"public_Gaussian_pool_size: 2^64 + 2^{50 if n == 512 else 36}")
    print_ball("negative_log2_pool_failure_upper_bound", pool_failure_bits)
    print("CERTIFIED pool_failure < 2^-1000")
    print(f"optional_real_attempt_limit_per_query: {real_attempt_limit}")
    print_ball("negative_log2_real_cap_failure_upper_bound", real_cap_failure_bits)
    print("CERTIFIED real_cap_failure < 2^-390")
    print(f"compressed_norm_based_length_upper_bound_bytes: {compressed_length_bound}")
    print(f"published_maximum_compressed_buffer_bytes: {maximum_buffer}")


def oracle_probability_examples() -> None:
    q_s = arb(2) ** 64
    salt_space = arb(2) ** 320
    print("\nORACLE EXAMPLES (probability terms, not overall security levels)")
    for log_q_h in (64, 128):
        q_h = arb(2) ** log_q_h
        classical = (q_s * q_h + q_s * (q_s - 1) / 2) / salt_space
        quantum = arb(3) * q_s / 2 * ((q_h + q_s + 1) / salt_space).sqrt()
        print(f"q_S=2^64 q_H=2^{log_q_h} salt_bits=320")
        print_ball("log2_ROM_reprogramming_probability_bound", log2(classical))
        print_ball("log2_QROM_reprogramming_probability_bound", log2(quantum))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=256, help="Arb precision in bits (default: 256)")
    arguments = parser.parse_args()
    require(arguments.precision >= 192, "use at least 192 bits of working precision")
    ctx.prec = arguments.precision
    print("CoreFalcon security-transfer arithmetic")
    print(f"backend: python-flint {flint.__version__} / Arb")
    print(f"precision_bits: {ctx.prec}")
    print("All printed balls enclose analytic upper-bound expressions.")
    print("Tail contracts are imported from norm_circle_interval.py.")
    parameter_sets = {n: parameters(n) for n in (512, 1024)}
    for parameter_set in parameter_sets.values():
        runtime_and_format_checks(parameter_set)
    transfer_case(parameter_sets[512], 120, 73, "3.268")
    transfer_case(parameter_sets[512], 128, 75, "3.376")
    transfer_case(parameter_sets[1024], 256, 151, "3.387")
    oracle_probability_examples()
    print("\nPASS: all stated arithmetic inequalities were certified.")


if __name__ == "__main__":
    main()
