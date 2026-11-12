"""Clean clinical sample data using the rules established in Lab 3."""

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd


def parse_date(value):
    """Parse supported date formats with an explicit century cutoff."""
    value = value.strip()

    if "." in value:
        month, day, year = map(int, value.split("."))
        year += 1900 if year >= 50 else 2000
        return datetime(year, month, day).strftime("%Y-%m-%d")

    for date_format in ("%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y"):
        try:
            return datetime.strptime(value, date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unsupported date: {value}")


def clean_samples(input_path, output_path):
    """Standardize clinical fields and write a validated CSV."""
    samples = pd.read_csv(input_path, dtype=str, keep_default_na=False)

    required = {
        "sample_id", "patient_name", "dob", "sex",
        "enrollment_site", "glucose_value", "glucose_unit", "notes",
    }
    if not required.issubset(samples.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(samples.columns))}")

    samples["sample_id"] = samples["sample_id"].str.replace(
        r"(?i)^s-?", "S", regex=True
    )
    samples["patient_name"] = samples["patient_name"].str.title()
    samples["dob"] = samples["dob"].map(parse_date)

    samples["sex"] = (
        samples["sex"].str.lower()
        .map({"m": "Male", "male": "Male", "f": "Female", "female": "Female"})
        .fillna("Unknown")
    )

    site_codes = (
        samples["enrollment_site"].str.lower()
        .str.replace(r"[\s_-]+", "", regex=True)
    )
    samples["enrollment_site"] = site_codes.map({
        "sitea": "Site A",
        "siteb": "Site B",
        "sitec": "Site C",
    })
    if samples["enrollment_site"].isna().any():
        raise ValueError("Unexpected enrollment site")

    glucose = pd.to_numeric(
        samples["glucose_value"].str.extract(r"(\d+(?:\.\d+)?)", expand=False),
        errors="raise",
    )
    units = samples["glucose_unit"].str.lower()
    if not units.isin(["mg/dl", "mmol/l"]).all():
        raise ValueError("Unexpected glucose unit")

    # Follow the recorded units and the Lab 3 conversion factor.
    samples["glucose_value"] = glucose.where(
        units != "mmol/l", (glucose * 18).round(1)
    )
    samples["glucose_unit"] = "mg/dL"

    if not samples["sample_id"].str.fullmatch(r"S\d{4}").all():
        raise ValueError("Invalid standardized sample ID")
    if samples["sample_id"].duplicated().any():
        raise ValueError("Duplicate standardized sample IDs")
    if samples["glucose_value"].isna().any():
        raise ValueError("Missing glucose measurement")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    samples.to_csv(output_path, index=False)
    print(f"Saved {len(samples)} rows and {len(samples.columns)} columns.")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    clean_samples(args.input, args.output)


if __name__ == "__main__":
    main()