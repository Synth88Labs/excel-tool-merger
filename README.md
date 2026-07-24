# Excel/CSV Merger

[![CI](https://github.com/Synth88Labs/excel-tool-merger/actions/workflows/ci.yml/badge.svg)](https://github.com/Synth88Labs/excel-tool-merger/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A simple, reliable command-line tool that merges a whole folder of **Excel and CSV
files into one clean file** — aligning mismatched columns, tagging each row with its
source file, and optionally removing duplicates.

Built for the most common spreadsheet chore there is: *"I have 30 files, combine them
into one."*

> 📖 **New to the tool?** Read the full step-by-step guide:
> [How to Merge Multiple Excel & CSV Files Into One](https://excelguru.io/tutorials/how-to-merge-multiple-excel-csv-files/) on ExcelGuru.io.

## Features

- 📁 Merges every `.csv`, `.xlsx`, and `.xls` in a folder in one command
- 🧩 **Aligns mismatched columns** automatically (keeps the union of all columns)
- 🏷️ Adds a `source_file` column so you always know where each row came from
- 🧹 Optional `--dedupe` to drop duplicate rows
- 🔁 Optional `--recursive` to include sub-folders
- 🛡️ Skips Excel lock/temp files (`~$…`) and reports unreadable files instead of crashing
- 📤 Outputs to `.xlsx` or `.csv` — your choice

## Installation

```bash
git clone https://github.com/Synth88Labs/excel-tool-merger.git
cd excel-tool-merger
pip install -r requirements.txt
```

Requires Python 3.9+.

## Usage

```bash
python merge_excel.py <folder> [-o output.xlsx] [options]
```

### Quick start (try it on the included sample data)

```bash
python merge_excel.py ./sample_data -o combined.xlsx
```

### Options

| Option | Description |
|---|---|
| `-o`, `--output` | Output file path (`.xlsx` or `.csv`). Default: `merged_output.xlsx` |
| `--dedupe` | Drop fully duplicate rows after merging |
| `--no-source` | Don't add the `source_file` column |
| `--recursive` | Also search sub-folders |
| `--sheet NAME` | For Excel files, read a specific sheet (default: first sheet) |

### Examples

```bash
# Merge a folder of monthly reports, remove duplicates
python merge_excel.py ./reports -o all_reports.xlsx --dedupe

# Merge recursively and output as CSV
python merge_excel.py ./data -o everything.csv --recursive

# Read the "Sheet1" tab from every Excel file
python merge_excel.py ./exports --sheet "Sheet1"
```

## Example

Given two files with **different columns**:

`january_sales.csv`
| order_id | customer | product | amount |
|---|---|---|---|
| 1001 | Acme Corp | Widget A | 250 |

`february_sales.csv` (note the extra `region` column)
| order_id | customer | product | amount | region |
|---|---|---|---|---|
| 1004 | Gamma Inc | Widget A | 410 | West |

The tool produces one combined file with the **union of columns** and a `source_file`
tag — January rows simply have a blank `region`.

## Running the tests

```bash
pip install pytest
python -m pytest
```

## 📚 Learn More — Free Excel Tutorials

📖 **Full tutorial for this tool:**
[How to Merge Multiple Excel & CSV Files Into One](https://excelguru.io/tutorials/how-to-merge-multiple-excel-csv-files/)
— a step-by-step walkthrough with examples.

Want to level up your Excel and automation skills? Check out
**[ExcelGuru.io](https://excelguru.io/category/tutorials/)** for free, high-quality
Excel tutorials covering formulas, automation, VBA, and more.

👉 **[Browse all free Excel tutorials on ExcelGuru.io »](https://excelguru.io/category/tutorials/)**

## License

MIT — see [LICENSE](LICENSE).
