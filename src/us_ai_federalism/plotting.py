from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

LABELS = {
    "current": "Current state system",
    "broad_ceiling": "Broad federal ceiling",
    "eo14365_carveouts": "Ceiling with EO carve-outs",
    "federal_floor": "Federal floor",
}

DOMAIN_LABELS = {
    "impact_assessment": "Impact assessment",
    "model_evaluation": "Model evaluation",
    "human_oversight": "Human oversight",
    "consumer_notice": "Consumer notice",
    "explanation_appeal": "Explanation or appeal",
    "antidiscrimination": "Antidiscrimination",
    "incident_reporting": "Incident reporting",
    "frontier_safety": "Frontier-model safety",
    "child_safety": "Child safety",
    "health_restriction": "Health restrictions",
    "infrastructure": "AI infrastructure",
    "government_use": "Government use",
    "enforcement_authority": "Public enforcement",
    "private_right": "Private right of action",
    "penalty": "Specified penalties",
    "exemption": "Exemptions",
}


def plot_coverage(estimates: pd.DataFrame, output: str | Path) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    order = (
        estimates[estimates["scenario"] == "current"]
        .sort_values("coverage", ascending=True)["domain"]
        .tolist()
    )
    scenarios = ["current", "eo14365_carveouts", "federal_floor"]
    pivot = (
        estimates[estimates["scenario"].isin(scenarios)]
        .pivot(index="domain", columns="scenario", values="coverage")
        .reindex(order)
    )
    pivot.index = [
        DOMAIN_LABELS.get(domain, domain.replace("_", " ").title()) for domain in pivot.index
    ]
    colors = ["#26324B", "#C74634", "#2F7D68"]
    ax = pivot.plot(
        kind="barh", figsize=(11, max(5.5, len(order) * 0.42)), color=colors, width=0.78
    )
    ax.set_title(
        "Public-protection coverage under alternative federal AI frameworks",
        loc="left",
        weight="bold",
        fontsize=15,
        pad=14,
    )
    ax.text(
        0,
        1.015,
        "Share of the analysis population covered by a verified obligation",
        transform=ax.transAxes,
        color="#687083",
        fontsize=10,
    )
    ax.set_xlabel("Coverage")
    ax.set_ylabel("")
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(axis="x", alpha=0.2)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend([LABELS[column] for column in pivot.columns], frameon=False, loc="lower right")
    ax.figure.text(
        0.01,
        0.01,
        "Source: coded primary state statutes. Simulations are not legal predictions.",
        fontsize=8,
        color="#687083",
    )
    ax.figure.tight_layout(rect=(0, 0.035, 1, 1))
    ax.figure.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(ax.figure)
    return path
