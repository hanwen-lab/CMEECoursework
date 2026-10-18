#!/usr/bin/env python3
"""Validate and clean the synthetic Silwood tree survey."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "silwood_trees_raw.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

INPUT_FIELDS = [
    "record_id",
    "location",
    "genus",
    "species",
    "distance_m",
    "angle_degrees",
]
ISSUE_FIELDS = ["source_row", "record_id", "reasons"]
OAK_COUNT_FIELDS = ["species", "count"]


def load_records(path: Path = INPUT_PATH) -> list[dict[str, str]]:
    """Read the survey and check its column names."""
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != INPUT_FIELDS:
            raise ValueError(
                f"Expected columns {INPUT_FIELDS}, found {reader.fieldnames}"
            )
        return list(reader)


def validate_record(
    row: dict[str, str],
    source_row: int,
    accepted_ids: set[str],
) -> tuple[dict[str, str] | None, list[str]]:
    """Clean one record, or return the reasons it cannot be used."""
    reasons = []

    record_id = row["record_id"].strip()
    location = row["location"].strip()
    genus = row["genus"].strip()
    species = row["species"].strip()
    distance = row["distance_m"].strip()
    angle = row["angle_degrees"].strip()

    if not record_id:
        reasons.append("missing record_id")
    elif len(record_id) != 5 or not record_id.startswith("ST") or not record_id[2:].isdigit():
        reasons.append("invalid record_id")
    elif record_id in accepted_ids:
        reasons.append("duplicate record_id")

    locations = [
        "Silwood Bottom",
        "Nash's Field",
        "Manor House",
        "Reactor Wood"
    ]

    canonical_location = next(
        (x for x in locations if x.lower() == location.lower()),
        None
    )

    if not location:
        reasons.append("missing location")
    elif canonical_location is None:
        reasons.append("invalid location")

    valid_pairs = {
        ("Quercus", "robur"),
        ("Quercus", "petraea"),
        ("Acer", "pseudoplatanus"),
        ("Betula", "pendula"),
        ("Fagus", "sylvatica"),
        ("Fraxinus", "excelsior")
    }

    genera = {g for g, s in valid_pairs}
    canonical_genus = next(
        (g for g in genera if g.lower() == genus.lower()),
        None
    )

    if not genus:
        reasons.append("missing genus")
    elif canonical_genus is None:
        reasons.append("invalid genus")

    species_options = {
        "Quercus": ["robur", "petraea"],
        "Acer": ["pseudoplatanus"],
        "Betula": ["pendula"],
        "Fagus": ["sylvatica"],
        "Fraxinus": ["excelsior"]
    }

    canonical_species = None
    if canonical_genus is not None:
        canonical_species = next(
            (
                s for s in species_options[canonical_genus]
                if s.lower() == species.lower()
            ),
            None
        )

    if not species:
        reasons.append("missing species")
    elif canonical_genus is not None and canonical_species is None:
        all_species = [
            s for options in species_options.values()
            for s in options
        ]
        if not any(s.lower() == species.lower() for s in all_species):
            reasons.append("invalid species")
        else:
            reasons.append("invalid genus/species combination")
    elif canonical_genus is None and species:
        if species.lower() not in [
            s.lower()
            for options in species_options.values()
            for s in options
        ]:
            reasons.append("invalid species")

    def parse_number(value, field):
        if not value:
            reasons.append(f"missing {field}")
            return None
        try:
            number = float(value)
        except ValueError:
            reasons.append(f"invalid {field}")
            return None
        import math
        if not math.isfinite(number):
            reasons.append(f"invalid {field}")
            return None
        return number

    distance_value = parse_number(distance, "distance_m")
    if distance_value is not None and not (0 < distance_value <= 100):
        reasons.append("distance_m out of range")

    angle_value = parse_number(angle, "angle_degrees")
    if angle_value is not None and not (0 < angle_value < 90):
        reasons.append("angle_degrees out of range")

    if reasons:
        return None, reasons

    cleaned = {
        "record_id": record_id,
        "location": canonical_location,
        "genus": canonical_genus,
        "species": canonical_species,
        "distance_m": str(distance_value),
        "angle_degrees": str(angle_value)
    }

    return cleaned, []


def process_records(
    rows: Iterable[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Sort records into accepted rows and issue reports."""
    clean_records = []
    issues = []
    accepted_ids = set()

    for source_row, row in enumerate(rows, start=2):
        cleaned, reasons = validate_record(
            row, source_row, accepted_ids
        )

        if reasons:
            issues.append({
                "source_row": str(source_row),
                "record_id": row["record_id"].strip(),
                "reasons": "; ".join(reasons)
            })
        else:
            clean_records.append(cleaned)
            accepted_ids.add(cleaned["record_id"])

    clean_records.sort(key=lambda row: row["record_id"])

    return clean_records, issues


def summarise_oaks(clean_records: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Count accepted oak records by species."""
    counts = {}

    for row in clean_records:
        if row["genus"] == "Quercus":
            species = row["species"]
            counts[species] = counts.get(species, 0) + 1

    return [
        {"species": species, "count": str(counts[species])}
        for species in sorted(counts)
    ]


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, str]],
) -> None:
    """Write rows to a CSV file, replacing an older copy."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Clean the survey and write the three result files."""
    clean_records, issues = process_records(load_records())
    oak_counts = summarise_oaks(clean_records)

    write_csv(
        RESULTS_DIR / "silwood_trees_clean.csv",
        INPUT_FIELDS,
        clean_records,
    )
    write_csv(
        RESULTS_DIR / "silwood_tree_issues.csv",
        ISSUE_FIELDS,
        issues,
    )
    write_csv(
        RESULTS_DIR / "oak_species_counts.csv",
        OAK_COUNT_FIELDS,
        oak_counts,
    )


if __name__ == "__main__":
    main()

print("OK.")
