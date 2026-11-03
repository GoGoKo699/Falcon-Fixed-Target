#!/usr/bin/env python3
"""Generate and verify the analytic fixed-target distribution-transfer plot.

From the repository root, install verification/requirements.txt and run::

    python3 verification/Graph/generate_plots.py
    python3 verification/Graph/generate_plots.py --check

The default PDF, SVG preview and data outputs are beside this script. The
canonical numerical module is ../core_transfer_bounds.py. Check mode
regenerates all three assets in a temporary directory and compares exact
bytes without changing the committed files.

Arb at 256 bits encloses analytic upper-bound expressions. Curve coordinates
are floating-point midpoints used only for drawing, not empirical divergences
or end-to-end security levels. Markers identify the three stated orders,
without an optimization claim.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

import flint
from flint import arb, ctx

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


HERE = Path(__file__).resolve().parent
CANONICAL = HERE.parent / "core_transfer_bounds.py"
CASES = (
    {"n": 512, "lambda_sim": 120, "selected_order": 73, "ceiling": "3.268",
     "image_ceiling": "0.000398", "conditioning_increment_ceiling": "0.000080"},
    {"n": 512, "lambda_sim": 128, "selected_order": 75, "ceiling": "3.376",
     "image_ceiling": "0.000409", "conditioning_increment_ceiling": "0.000082"},
    {"n": 1024, "lambda_sim": 256, "selected_order": 151, "ceiling": "3.387",
     "image_ceiling": "0.000207", "conditioning_increment_ceiling": "0.000000005"},
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def load_canonical():
    spec = importlib.util.spec_from_file_location("canonical_transfer", CANONICAL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import canonical module: {CANONICAL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ball_text(value: arb) -> str:
    require(value.is_finite(), "Nonfinite upper-bound-expression enclosure")
    return value.str(50, more=True)


def transfer_values(parameter_set, simulator_exponent: int, order: int):
    """Exactly the canonical transfer_case expressions, without printing.

    M_* = (1+C_rho e_p(rho))(1+e_u(rho)); the image term uses the
    independently certified chi-square contract, as in the published rows.
    """
    rho = arb(order)
    require(rho >= 2, "This sampler-profile expression requires rho>=2")
    queries = arb(2) ** 64
    rejection = parameter_set["D0"]
    log_b = parameter_set["log_b"]
    b = parameter_set["b"]
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
    holder_cost = arb(simulator_exponent) / rho
    return {
        "total_loss_bits": holder_cost + sampler_cost + image_cost,
        "holder_exponent_cost_bits": holder_cost,
        "sampler_cost_bits": sampler_cost,
        "image_cost_bits": image_cost,
        "sampler_conditioning_increment_bits": conditioning_increment,
        "conditioning_excess_multiplier": conditioning,
        "log_M_star_upper_expression": log_sampler_moment + log_image_moment,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "transfer.pdf")
    parser.add_argument("--data", type=Path, default=HERE / "transfer_data.json")
    parser.add_argument("--svg", type=Path, default=HERE / "transfer.svg")
    parser.add_argument("--check", action="store_true",
                        help="Regenerate and compare all committed assets without modifying them")
    args = parser.parse_args()
    if args.check:
        expected = {"PDF": args.output, "SVG": args.svg, "data": args.data}
        temporary = tempfile.TemporaryDirectory(prefix="falcon-transfer-check-")
        args.output = Path(temporary.name) / "transfer.pdf"
        args.svg = Path(temporary.name) / "transfer.svg"
        args.data = Path(temporary.name) / "transfer_data.json"
    require(flint.__version__ == "0.8.0", "Use the pinned python-flint==0.8.0")
    ctx.prec = 256
    canonical = load_canonical()
    parameter_sets = {n: canonical.parameters(n) for n in (512, 1024)}

    data = {
        "figure": "Analytic distribution-transfer loss versus Renyi order",
        "formula": "L(rho)=lambda_sim/rho+q_S/rho*log2(M_star)",
        "q_S": "2^64",
        "flint_version": flint.__version__,
        "precision_bits": ctx.prec,
        "canonical_module": "verification/core_transfer_bounds.py",
        "canonical_module_sha256": hashlib.sha256(CANONICAL.read_bytes()).hexdigest(),
        "data_orders_inclusive": [20, 240],
        "plotted_orders_inclusive": [40, 220],
        "order_step": 1,
        "semantics": {
            "enclosures": "Arb balls enclose analytic upper-bound expressions; not empirical divergences.",
            "curve_coordinates": "IEEE double approximations of Arb-ball midpoints, for drawing only.",
            "rigorous_checks": "Strict Arb comparisons certify the three exact published row ceilings.",
            "markers": "Published orders only; no claim of globally optimal Renyi orders.",
            "scope": "Distribution-transfer loss only; oracle errors, hardness work factors, extraction and simulation costs are separate.",
        },
        "parameters": {
            str(n): {key: ball_text(value) if isinstance(value, arb) else value
                     for key, value in parameters.items()}
            for n, parameters in parameter_sets.items()
        },
        "cases": [],
    }

    for case in CASES:
        parameter_set = parameter_sets[case["n"]]
        selected = transfer_values(parameter_set, case["lambda_sim"], case["selected_order"])
        require(selected["total_loss_bits"] < arb(case["ceiling"]),
                f"Published ceiling failed: {case}")
        require(selected["image_cost_bits"] < arb(case["image_ceiling"]),
                f"Published image contribution ceiling failed: {case}")
        require(selected["sampler_conditioning_increment_bits"]
                < arb(case["conditioning_increment_ceiling"]),
                f"Published conditioning increment ceiling failed: {case}")
        # Also invoke the unchanged canonical row check, tying the generator
        # to the independently executable repository certificate.
        canonical.transfer_case(parameter_set, case["lambda_sim"],
                                case["selected_order"], case["ceiling"])
        record = dict(case)
        record["selected_ceiling_certified"] = True
        record["selected_upper_expression_balls"] = {
            key: ball_text(value) for key, value in selected.items()
        }
        record["points"] = []
        for order in range(20, 241):
            values = transfer_values(parameter_set, case["lambda_sim"], order)
            record["points"].append({
                "rho": order,
                "upper_expression_balls": {
                    key: ball_text(value) for key, value in values.items()
                },
                "plot_y_midpoint_float": float(values["total_loss_bits"].mid()),
            })
        data["cases"].append(record)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.2,
        "axes.labelsize": 9.2,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "mathtext.fontset": "dejavusans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.hashsalt": "falcon-fixed-target-transfer-v1",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.7,
        "savefig.transparent": False,
    })
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    colors = ("#1768AC", "#D17B16", "#7B4DA6")
    line_styles = ("-", "--", "-.")
    markers = ("o", "s", "D")
    handles = []
    for case, color, style, marker in zip(data["cases"], colors, line_styles, markers):
        visible = [point for point in case["points"] if 40 <= point["rho"] <= 220]
        ax.plot([point["rho"] for point in visible],
                [point["plot_y_midpoint_float"] for point in visible],
                color=color, linestyle=style, linewidth=1.65, zorder=2)
        point = next(p for p in visible if p["rho"] == case["selected_order"])
        ax.plot(point["rho"], point["plot_y_midpoint_float"],
                marker=marker, color=color, markersize=5.5,
                markerfacecolor="white", markeredgewidth=1.2, zorder=4)
        label = (rf"$n={case['n']},\ \lambda_{{\rm sim}}={case['lambda_sim']}$"
                 + rf"; marked $\rho={case['selected_order']}$")
        handles.append(Line2D([0], [0], color=color, linestyle=style,
                              marker=marker, markerfacecolor="white",
                              markeredgewidth=1.1, linewidth=1.65,
                              markersize=4.8, label=label))

    ax.set_xlim(40, 220)
    ax.set_ylim(2.95, 7.05)
    ax.set_xticks([40, 60, 80, 100, 120, 140, 160, 180, 200, 220])
    ax.set_yticks([3, 4, 5, 6, 7])
    ax.set_xlabel("Rényi order $\\rho$", labelpad=5)
    ax.set_ylabel(r"Transfer loss bound $\mathcal{L}(\rho)$ (bits)", labelpad=7)
    ax.grid(axis="y", color="#D9DFE5", linewidth=0.6, zorder=0)
    ax.tick_params(direction="out", length=3, width=0.7)
    ax.legend(handles=handles, loc="upper right", frameon=False,
              handlelength=2.7, handletextpad=0.7, labelspacing=0.7,
              borderaxespad=0.6)
    ax.text(0.025, 0.95, r"$q_S=2^{64}$", transform=ax.transAxes,
            ha="left", va="top", fontsize=9.2)
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.97)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.data.parent.mkdir(parents=True, exist_ok=True)
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, format="pdf", metadata={
        "Title": "Analytic fixed-target distribution-transfer loss",
        "Subject": "Upper-bound expressions at q_S=2^64; marked published orders, not optimized minima",
        "Creator": "generate_transfer_figure.py",
        "CreationDate": None, "ModDate": None,
    })
    fig.savefig(args.svg, format="svg", metadata={
        "Title": "Analytic fixed-target distribution-transfer loss",
        "Description": "Upper-bound expressions at q_S=2^64; markers identify stated orders",
        "Creator": "generate_plots.py",
        "Date": None,
    })
    args.svg.write_text(
        "\n".join(line.rstrip() for line in args.svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)
    args.data.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.check:
        generated = {"PDF": args.output, "SVG": args.svg, "data": args.data}
        for kind, path in generated.items():
            committed = expected[kind]
            require(committed.is_file(), f"Missing committed plot {kind}: {committed}")
            require(path.read_bytes() == committed.read_bytes(),
                    f"Plot {kind} differs from regeneration; inspect the inputs and pinned dependencies")
            print(f"PASS plot {kind}: {hashlib.sha256(committed.read_bytes()).hexdigest()}")
        temporary.cleanup()
    else:
        print(f"Wrote {args.output}")
        print(f"Wrote {args.svg}")
        print(f"Wrote {args.data}")


if __name__ == "__main__":
    main()
