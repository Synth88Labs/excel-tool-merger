"""
merge_excel.py — Merge a folder of Excel/CSV files into one clean workbook.

Combines every .csv / .xlsx / .xls file in a folder into a single output file.
Handles mismatched columns (keeps the union), tags each row with its source
file, and can optionally drop duplicate rows.

Usage:
    python merge_excel.py <input_folder> [-o output.xlsx] [options]

Examples:
    python merge_excel.py ./sample_data
    python merge_excel.py ./reports -o combined.xlsx --dedupe
    python merge_excel.py ./data --recursive --sheet "Sheet1"

Author: Synth88Labs
License: MIT
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def find_files(folder: Path, recursive: bool) -> list[Path]:
    """Return a sorted list of supported spreadsheet files in *folder*."""
    pattern = "**/*" if recursive else "*"
    files = [
        p
        for p in folder.glob(pattern)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        # skip Excel lock/temp files like ~$report.xlsx
        and not p.name.startswith("~$")
    ]
    return sorted(files)


def read_one(path: Path, sheet: str | None) -> pd.DataFrame:
    """Read a single CSV/Excel file into a DataFrame, as strings where safe."""
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    # Excel: sheet=None would return a dict, so default to the first sheet.
    sheet_arg = sheet if sheet is not None else 0
    return pd.read_excel(path, sheet_name=sheet_arg, dtype=str, na_filter=False)


def merge_files(
    files: list[Path],
    sheet: str | None,
    add_source: bool,
) -> pd.DataFrame:
    """Read and vertically concatenate *files*, aligning columns by name."""
    frames: list[pd.DataFrame] = []
    for path in files:
        try:
            df = read_one(path, sheet)
        except Exception as exc:  # noqa: BLE001 - report and skip bad files
            print(f"  ! Skipped {path.name}: {exc}", file=sys.stderr)
            continue

        if df.empty:
            print(f"  - {path.name}: no rows, skipped")
            continue

        if add_source:
            df.insert(0, "source_file", path.name)

        frames.append(df)
        print(f"  + {path.name}: {len(df)} rows, {df.shape[1]} columns")

    if not frames:
        raise SystemExit("No readable data found. Nothing to merge.")

    # sort=False keeps column order stable; union of all columns is preserved.
    return pd.concat(frames, ignore_index=True, sort=False)


def write_output(df: pd.DataFrame, out_path: Path) -> None:
    """Write the merged DataFrame to CSV or Excel based on the extension."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.suffix.lower() == ".csv":
        df.to_csv(out_path, index=False)
    else:
        df.to_excel(out_path, index=False, sheet_name="Merged")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge a folder of Excel/CSV files into one clean file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("folder", type=Path, help="Folder containing the files to merge.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("merged_output.xlsx"),
        help="Output file path (.xlsx or .csv). Default: merged_output.xlsx",
    )
    parser.add_argument(
        "--dedupe",
        action="store_true",
        help="Drop fully duplicate rows after merging.",
    )
    parser.add_argument(
        "--no-source",
        action="store_true",
        help="Do not add a 'source_file' column.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Also search sub-folders.",
    )
    parser.add_argument(
        "--sheet",
        default=None,
        help="For Excel files: the sheet name to read (default: first sheet).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    folder: Path = args.folder
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a folder.", file=sys.stderr)
        return 1

    files = find_files(folder, args.recursive)
    if not files:
        exts = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        print(f"No supported files ({exts}) found in '{folder}'.", file=sys.stderr)
        return 1

    print(f"Found {len(files)} file(s) in '{folder}':")
    merged = merge_files(files, sheet=args.sheet, add_source=not args.no_source)

    before = len(merged)
    if args.dedupe:
        merged = merged.drop_duplicates(ignore_index=True)
        print(f"Deduped: removed {before - len(merged)} duplicate row(s).")

    write_output(merged, args.output)
    print(
        f"\nDone. Merged {len(files)} file(s) -> {len(merged)} rows, "
        f"{merged.shape[1]} columns."
    )
    print(f"Saved: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
