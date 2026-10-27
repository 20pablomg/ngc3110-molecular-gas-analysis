"""Convert CLASS integrated intensities (K km/s) to Jy km/s.

Uses the line-specific conversion factors adopted in the thesis. The
fit and moment tables must have matching keys (fuente, linea).
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

DENSE = 5.9 * 0.8 / 0.95
S_PER_TMB = {
    "densegas": DENSE, "12CO10_6": 5 * 0.78 / 0.94,
    "12CO21_5": 7.5 * 0.59 / 0.92,
    "HCN": DENSE, "HCO": DENSE, "HNC": DENSE,
}
DATASETS = ["CO10", "CO21", "HCN", "HCO", "HNC"]


def convert_pair(fit_path: Path, moment_path: Path, output_path: Path) -> pd.DataFrame:
    fit = pd.read_csv(fit_path, sep=r"\s+")
    moment = pd.read_csv(moment_path, sep=r"\s+")
    keys = ["fuente", "linea"]
    for field in keys + ["I_fit", "err_I"]:
        if field not in fit: raise ValueError(f"Missing {field} in {fit_path}")
    for field in keys + ["I_manual", "SigmaI"]:
        if field not in moment: raise ValueError(f"Missing {field} in {moment_path}")
    if fit.duplicated(keys).any() or moment.duplicated(keys).any():
        raise ValueError("Duplicate (fuente, linea) keys; cannot perform a safe join")
    joined = fit.merge(moment[keys+["I_manual", "SigmaI"] + (["I_moment"] if "I_moment" in moment.columns else [])], on=keys, validate="one_to_one", how="outer", indicator=True)
    if not (joined["_merge"] == "both").all():
        raise ValueError("Fit and moment tables have unmatched (fuente, linea) rows")
    factors = joined["linea"].map(S_PER_TMB)
    if factors.isna().any():
        raise ValueError(f"Unknown line names: {joined.loc[factors.isna(), 'linea'].unique().tolist()}")
    result = joined[keys].copy()
    for src, dest in [("I_fit", "I_fit_Jy"), ("err_I", "err_I_fit_Jy"),
                      ("I_manual", "I_manual_Jy"), ("SigmaI", "err_I_manual_Jy")]:
        result[dest] = (joined[src] * factors).round(4)
    if "I_moment" in joined.columns:
        result["I_moment_Jy"] = (joined["I_moment"] * factors).round(4)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, sep="\t", index=False)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=Path(__file__).resolve().parents[1] / "results" / "ResultadosCLASS")
    args = parser.parse_args()
    for name in DATASETS:
        if not (args.results_dir / f"W_{name}_fit_results.dat").exists() or not (args.results_dir / f"W_{name}_moment_results.dat").exists():
            print(f"Skipping {name}: matching CLASS tables not available")
            continue
        prefix = f"W_{name}"
        convert_pair(args.results_dir / f"{prefix}_fit_results.dat",
                     args.results_dir / f"{prefix}_moment_results.dat",
                     args.results_dir / f"{prefix}_Jy_results.dat")
        print(f"Converted {name}")


if __name__ == "__main__":
    main()
