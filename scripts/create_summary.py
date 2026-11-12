"""Summarize the independent clinical and patient feature datasets."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


GENES = ["TP53", "KRAS", "EGFR", "STK11", "KEAP1"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", required=True, type=Path)
    parser.add_argument("--features", required=True, type=Path)
    parser.add_argument("--metrics", required=True, type=Path)
    parser.add_argument("--figure", required=True, type=Path)
    args = parser.parse_args()

    samples = pd.read_csv(args.samples)
    patients = pd.read_csv(args.features, sep="\t")

    if samples["sample_id"].duplicated().any():
        raise ValueError("Duplicate clinical sample IDs")
    if patients["patient_id"].duplicated().any():
        raise ValueError("Duplicate patient IDs")

    glucose = pd.to_numeric(samples["glucose_value"], errors="raise")
    gene_counts = patients[GENES].apply(pd.to_numeric, errors="raise")

    if glucose.isna().any():
        raise ValueError("Missing glucose measurements")
    if gene_counts.isna().any().any() or (gene_counts < 0).any().any():
        raise ValueError("Missing or negative mutation counts")

    # Keep the two unrelated cohorts separate in all summaries.
    records = [
        ("clinical_samples", "sample_count", len(samples)),
        ("clinical_samples", "glucose_mean_mg_dl", glucose.mean()),
        ("clinical_samples", "glucose_median_mg_dl", glucose.median()),
        ("clinical_samples", "glucose_min_mg_dl", glucose.min()),
        ("clinical_samples", "glucose_max_mg_dl", glucose.max()),
        ("patient_features", "patient_count", len(patients)),
    ]

    for column in ["sex", "age_at_diagnosis", "stage"]:
        records.append((
            "patient_features",
            f"missing_{column}",
            int(patients[column].isna().sum()),
        ))

    for gene in GENES:
        records.append((
            "patient_features",
            f"{gene}_non_silent_mutation_records",
            int(gene_counts[gene].sum()),
        ))

    metrics = pd.DataFrame(records, columns=["dataset", "metric", "value"])
    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(args.metrics, sep="\t", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].hist(glucose, bins=15, color="#307A9E", edgecolor="white")
    axes[0].set_title(f"Clinical samples (n = {len(samples)})")
    axes[0].set_xlabel("Glucose (mg/dL; recorded units converted)")
    axes[0].set_ylabel("Number of samples")

    totals = gene_counts.sum()
    axes[1].bar(totals.index, totals.values, color="#43856A")
    axes[1].set_title(f"Patient cohort (n = {len(patients)})")
    axes[1].set_xlabel("Gene")
    axes[1].set_ylabel("Non-Silent mutation records")

    fig.suptitle("Independent dataset summaries")
    fig.tight_layout()
    args.figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.figure, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Clinical samples: {len(samples)}")
    print(f"Patient cohort: {len(patients)}")
    print(f"Saved metrics: {args.metrics}")
    print(f"Saved figure: {args.figure}")


if __name__ == "__main__":
    main()