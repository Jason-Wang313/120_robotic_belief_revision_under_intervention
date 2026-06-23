from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS = Path.home() / "Downloads"
DESKTOP = Path.home() / "Desktop"
PDF_NAME = "120.pdf"
CANONICAL_PDF = DOWNLOADS / PDF_NAME


CSV_BY_COUNT = {
    "dataset_summary": "dataset_summary.csv",
    "main_cell": "cell_metrics.csv",
    "main_group": "main_group_metrics.csv",
    "seed_metric": "seed_metrics.csv",
    "metric": "metrics.csv",
    "hard_seed": "hard_seed_metrics.csv",
    "hard_metric": "hard_aggregate_metrics.csv",
    "hard_pairwise": "hard_pairwise_stats.csv",
    "ablation_cell": "ablation_cell_metrics.csv",
    "ablation_seed": "ablation_seed_metrics.csv",
    "ablation_metric": "ablation_metrics.csv",
    "stress_cell": "stress_sweep_cell_metrics.csv",
    "stress_seed": "stress_sweep_seed_metrics.csv",
    "stress_metric": "stress_sweep.csv",
    "fixed_risk_cell": "fixed_risk_cell_metrics.csv",
    "fixed_risk_seed": "fixed_risk_seed_metrics.csv",
    "fixed_risk_metric": "fixed_risk_metrics.csv",
    "fixed_risk_pairwise": "fixed_risk_pairwise_stats.csv",
    "failure_cases": "failure_cases.csv",
}


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def validate_numeric_csv(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=2):
            for key, value in row.items():
                if value is None or value == "":
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                if not math.isfinite(number):
                    raise AssertionError(f"{path.name}:{index}:{key} is not finite")


def pdf_pages(path: Path) -> int:
    result = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
    if not match:
        raise AssertionError(f"could not read page count for {path}")
    return int(match.group(1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def assert_no_numbered_pdf_copies() -> None:
    forbidden = [
        DESKTOP / PDF_NAME,
        ROOT.parent / PDF_NAME,
        ROOT / PDF_NAME,
    ]
    for path in forbidden:
        if path.exists():
            raise AssertionError(f"forbidden numbered PDF copy exists: {path}")


def main() -> None:
    summary_path = RESULTS / "summary.json"
    if not summary_path.exists():
        raise AssertionError("missing results/summary.json")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("version") != "v5_expanded":
        raise AssertionError("summary version is not v5_expanded")
    if summary.get("terminal_decision") not in {"STRONG_REVISE", "KILL_ARCHIVE"}:
        raise AssertionError("invalid terminal decision")
    if not summary.get("local_gates_pass"):
        raise AssertionError("local gates did not pass")
    if summary.get("iclr_main_ready"):
        raise AssertionError("summary incorrectly marks ICLR main ready")

    row_counts = summary["row_counts"]
    for key, csv_name in CSV_BY_COUNT.items():
        path = RESULTS / csv_name
        if not path.exists():
            raise AssertionError(f"missing required CSV: {csv_name}")
        observed = count_rows(path)
        expected = int(row_counts[key])
        if observed != expected:
            raise AssertionError(f"{csv_name} row count {observed} != summary {expected}")
        validate_numeric_csv(path)

    paper_pdf = PAPER / "main.pdf"
    if not paper_pdf.exists():
        raise AssertionError("missing paper/main.pdf")
    if not CANONICAL_PDF.exists():
        raise AssertionError(f"missing canonical PDF: {CANONICAL_PDF}")
    if sha256(paper_pdf) != sha256(CANONICAL_PDF):
        raise AssertionError("paper/main.pdf and Downloads/120.pdf differ")
    pages = pdf_pages(CANONICAL_PDF)
    if pages < 25:
        raise AssertionError(f"PDF has only {pages} pages")
    assert_no_numbered_pdf_copies()
    print(f"Paper 120 validation passed. SHA256={sha256(CANONICAL_PDF)} pages={pages}")


if __name__ == "__main__":
    main()
