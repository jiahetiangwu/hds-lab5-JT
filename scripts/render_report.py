"""Generate a Markdown report from workflow summary outputs."""

import argparse
import os
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", required=True, type=Path)
    parser.add_argument("--figure", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    metrics = pd.read_csv(args.metrics, sep="\t")
    if metrics.duplicated(["dataset", "metric"]).any():
        raise ValueError("Duplicate dataset-metric pairs")
    if not args.figure.is_file():
        raise FileNotFoundError(args.figure)

    values = metrics.set_index(["dataset", "metric"])["value"]

    def get(dataset, metric):
        return float(values.loc[(dataset, metric)])

    sample_count = int(get("clinical_samples", "sample_count"))
    patient_count = int(get("patient_features", "patient_count"))
    mean_glucose = get("clinical_samples", "glucose_mean_mg_dl")
    median_glucose = get("clinical_samples", "glucose_median_mg_dl")
    min_glucose = get("clinical_samples", "glucose_min_mg_dl")
    max_glucose = get("clinical_samples", "glucose_max_mg_dl")

    gene_rows = []
    for gene in ["TP53", "KRAS", "EGFR", "STK11", "KEAP1"]:
        count = int(get(
            "patient_features",
            f"{gene}_non_silent_mutation_records",
        ))
        gene_rows.append(f"| {gene} | {count} |")

    missing_rows = []
    for column in ["sex", "age_at_diagnosis", "stage"]:
        count = int(get("patient_features", f"missing_{column}"))
        missing_rows.append(f"| {column} | {count} |")

    figure_link = Path(os.path.relpath(
        args.figure.resolve(),
        start=args.output.parent.resolve(),
    )).as_posix()

    report = f"""# Lab 5 Analysis Summary

## Data Sources and Scope

The clinical sample dataset contains {sample_count} records from Lab 3.
The patient feature table contains {patient_count} patients from the Lab 4
cohort database.

These datasets describe independent cohorts. Clinical sample identifiers
use the S0001 format, whereas the database uses TCGA identifiers. No shared
identifier or mapping table is available, so the datasets are summarized
separately without a row-level join.

## Clinical Sample Summary

| Metric | Glucose (mg/dL) |
| --- | ---: |
| Mean | {mean_glucose:.2f} |
| Median | {median_glucose:.2f} |
| Minimum | {min_glucose:.2f} |
| Maximum | {max_glucose:.2f} |

Cleaning follows the Lab 3 rules for identifiers, dates, sex, enrollment
sites, and glucose units. Values recorded in mmol/L are multiplied by 18.

Some source measurements have questionable unit labels. Literal conversion
produces extreme glucose values, which are retained rather than silently
corrected. These measurements require source verification before further
analysis. The mean and histogram are sensitive to these extreme values.

## Patient Feature Summary

All {patient_count} patients are retained. Clinical missing values remain
missing and are not replaced with zero.

| Clinical field | Missing patients |
| --- | ---: |
{chr(10).join(missing_rows)}

The following totals count mutation records classified as non-Silent.
They do not represent counts of distinct patients with mutations.

| Gene | Non-Silent mutation records |
| --- | ---: |
{chr(10).join(gene_rows)}

A zero gene count means no qualifying mutation record was found in the
database. It does not establish biological absence or adequate sequencing
coverage.

## Summary Figure

![Independent clinical and patient cohort summaries]({figure_link})

## Workflow

The workflow cleans clinical samples and queries the cohort database in
independent branches. Their outputs feed the summary stage, which produces
metrics and a figure. This report is generated from those summary outputs.
"""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Saved report: {args.output}")


if __name__ == "__main__":
    main()