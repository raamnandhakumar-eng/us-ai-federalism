"""Run an end-to-end plumbing test with invented data. Produces no research finding."""

import matplotlib.pyplot as plt
import pandas as pd

from us_ai_federalism.metrics import prepare_state_domain, scenario_effects, simulate_all
from us_ai_federalism.plotting import plot_coverage
from us_ai_federalism.settings import PROJECT_ROOT


def main() -> None:
    source = PROJECT_ROOT / "data" / "synthetic"
    output = PROJECT_ROOT / "data" / "processed" / "synthetic_demo"
    output.mkdir(parents=True, exist_ok=True)
    codings = pd.read_csv(source / "codings_reviewed.csv")
    states = pd.read_csv(source / "states.csv")
    grid = prepare_state_domain(codings, states)
    estimates = simulate_all(grid)
    effects = scenario_effects(estimates)
    estimates.to_csv(output / "scenario_estimates.csv", index=False)
    effects.to_csv(output / "scenario_effects.csv", index=False)
    figure = plot_coverage(estimates, output / "coverage_scenarios_SYNTHETIC.png")
    image = plt.imread(figure)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.imshow(image)
    ax.axis("off")
    ax.text(
        0.5,
        0.5,
        "SYNTHETIC • NOT A FINDING",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=28,
        color="#C74634",
        alpha=0.35,
        rotation=22,
        weight="bold",
    )
    fig.savefig(figure, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Synthetic demo written to {output}")


if __name__ == "__main__":
    main()
