"""Prepare local, Git-ignored input/output directories for an authorized rerun."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = (
    "spectra",
    "results/ResultadosCLASS",
    "results/ResultadosCO",
    "results/ResultadosHNC",
    "results/ResultadosSCCs",
)

def main() -> None:
    for relative in DIRECTORIES:
        path = PROJECT_ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        print(f"Ready: {path}")

if __name__ == "__main__":
    main()
