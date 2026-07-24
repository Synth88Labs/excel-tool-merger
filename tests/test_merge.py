"""Basic tests for merge_excel. Run with:  python -m pytest"""

import sys
from pathlib import Path

import pandas as pd

# Make the top-level module importable when running from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from merge_excel import find_files, merge_files  # noqa: E402


def _write_csv(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_find_files_skips_lock_files(tmp_path: Path) -> None:
    _write_csv(tmp_path / "a.csv", "x\n1\n")
    _write_csv(tmp_path / "~$a.xlsx", "junk")  # Excel lock file
    (tmp_path / "notes.txt").write_text("ignore me")

    found = find_files(tmp_path, recursive=False)

    names = [p.name for p in found]
    assert names == ["a.csv"]


def test_merge_aligns_mismatched_columns(tmp_path: Path) -> None:
    _write_csv(tmp_path / "jan.csv", "id,amount\n1,100\n2,200\n")
    _write_csv(tmp_path / "feb.csv", "id,amount,region\n3,300,West\n")

    files = find_files(tmp_path, recursive=False)
    merged = merge_files(files, sheet=None, add_source=True)

    # 3 data rows total
    assert len(merged) == 3
    # union of columns, plus the injected source_file column
    assert "region" in merged.columns
    assert "source_file" in merged.columns
    # rows from jan have an empty region (NaN), feb has "West"
    assert merged.loc[merged["id"] == "3", "region"].iloc[0] == "West"


def test_dedupe_removes_identical_rows(tmp_path: Path) -> None:
    _write_csv(tmp_path / "one.csv", "id,val\n1,a\n1,a\n")

    files = find_files(tmp_path, recursive=False)
    merged = merge_files(files, sheet=None, add_source=False)
    deduped = merged.drop_duplicates(ignore_index=True)

    assert len(merged) == 2
    assert len(deduped) == 1
