from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "experiment.csv"
OUT = ROOT / "docs" / "generated"
CACHE = ROOT / ".cache" / "experiment.json"


def git_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "working-tree"


def main() -> None:
    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    if CACHE.exists() and OUT.exists():
        state = json.loads(CACHE.read_text(encoding="utf-8"))
        if state.get("data_sha256") == digest:
            print("Experiment cache hit")
            return

    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(DATA)
    slope, intercept = np.polyfit(frame["x"], frame["y"], 1)
    predicted = slope * frame["x"] + intercept
    r2 = 1 - ((frame["y"] - predicted) ** 2).sum() / (
        (frame["y"] - frame["y"].mean()) ** 2
    ).sum()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(frame["x"], frame["y"], label="Наблюдения")
    ax.plot(frame["x"], predicted, color="crimson", label="Регрессия")
    ax.set(xlabel="x", ylabel="y", title="Линейная регрессия")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "regression.png", dpi=160)
    plt.close(fig)

    interactive = px.scatter(frame, x="x", y="y", trendline=None)
    interactive.add_scatter(x=frame["x"], y=predicted, mode="lines", name="Регрессия")
    interactive.write_html(OUT / "regression.html", include_plotlyjs=True, full_html=False)

    built_at = datetime.now(timezone.utc).isoformat()
    (OUT / "results.md").write_text(
        f"| Показатель | Значение |\n|---|---:|\n"
        f"| Наклон | {slope:.4f} |\n| Свободный член | {intercept:.4f} |\n"
        f"| $R^2$ | {r2:.4f} |\n\n"
        f"Версия кода: `{git_hash()}` · данные SHA-256: `{digest[:12]}` · сборка: `{built_at}`\n",
        encoding="utf-8",
    )
    CACHE.write_text(json.dumps({"data_sha256": digest}), encoding="utf-8")
    print("Experiment rebuilt")


if __name__ == "__main__":
    main()
