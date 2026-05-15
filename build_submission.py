"""
ML Assignment Submission Builder
---------------------------------
Run this from the ROOT folder that contains all 01-XX subfolders.
It will:
  1. Scan every subfolder for .py/.ipynb files
  2. Extract code content
  3. Generate a professional README.md report
  4. Zip everything (code + README) into submission.zip
"""

import os
import json
import zipfile
from pathlib import Path
from datetime import date

# ─────────────────────────────────────────────
# CONFIG — edit these
# ─────────────────────────────────────────────
STUDENT_NAME = "Balram Meena"
ROLL_NUMBER  = "2023BTCSE006"          # seen on your paper
SUBJECT      = "Machine Learning Lab"
ROOT_DIR     = "."                    # run from the folder containing 01-xx folders
OUTPUT_ZIP   = "submission.zip"
README_FILE  = "README.md"

# ─────────────────────────────────────────────
# ALGORITHM + DATASET metadata per folder
# (edit dataset names/descriptions as needed)
# ─────────────────────────────────────────────
FOLDER_META = {
    "01-Linear-Regression":   {"algo": "Linear Regression",        "dataset": "Boston Housing / Custom CSV"},
    "02-Gradient-Descent":    {"algo": "Gradient Descent",         "dataset": "Synthetic function f(x,y) = x² + xy + y²"},
    "03-Logistic-Regression": {"algo": "Logistic Regression",      "dataset": "Breast Cancer (sklearn)"},
    "04-Naive-Bayes":         {"algo": "Naive Bayes",              "dataset": "Iris / Text Classification"},
    "05-KNN":                 {"algo": "K-Nearest Neighbors",      "dataset": "Iris Dataset"},
    "06-Regularization":      {"algo": "Lasso & Ridge Regression", "dataset": "Boston Housing"},
    "07-Decision-Tree":       {"algo": "Decision Tree",            "dataset": "Iris / Wine Dataset"},
    "08-Random-Forest":       {"algo": "Random Forest",            "dataset": "Breast Cancer / Iris"},
    "09-Ensemble-Learning":   {"algo": "Bagging & Stacking",       "dataset": "Iris / Custom"},
    "10-Boosting":            {"algo": "AdaBoost / XGBoost",       "dataset": "Breast Cancer"},
    "11-Neural-Network":      {"algo": "Feedforward Neural Net",   "dataset": "MNIST / Custom"},
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_py_files(folder_path):
    """Return all .py and .ipynb files in a folder."""
    p = Path(folder_path)
    files = list(p.rglob("*.py")) + list(p.rglob("*.ipynb"))
    return sorted(files)

def extract_notebook_code(nb_path):
    """Pull code cells out of a .ipynb file."""
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        code_lines = []
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "code":
                code_lines.append("# --- code cell ---")
                code_lines.extend(cell.get("source", []))
                code_lines.append("\n")
        return "".join(code_lines)
    except Exception as e:
        return f"# Could not parse notebook: {e}"

def read_file_content(file_path):
    if file_path.suffix == ".ipynb":
        return extract_notebook_code(file_path)
    try:
        return file_path.read_text(encoding="utf-8")
    except:
        return "# Could not read file (encoding issue)"

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def build_readme(root, folder_data):
    lines = []
    lines.append(f"# Machine Learning Lab — Assignment Submission\n")
    lines.append(f"**Student:** {STUDENT_NAME}  ")
    lines.append(f"**Roll No:** {ROLL_NUMBER}  ")
    lines.append(f"**Subject:** {SUBJECT}  ")
    lines.append(f"**Date:** {date.today().strftime('%B %d, %Y')}  \n")
    lines.append("---\n")
    lines.append("## Table of Contents\n")
    for folder_name in folder_data:
        anchor = folder_name.lower().replace(" ", "-")
        lines.append(f"- [{folder_name}](#{anchor})")
    lines.append("\n---\n")

    for folder_name, data in folder_data.items():
        meta   = FOLDER_META.get(folder_name, {"algo": "N/A", "dataset": "N/A"})
        files  = data["files"]

        lines.append(f"## {folder_name}\n")
        lines.append(f"| Field | Details |")
        lines.append(f"|-------|---------|")
        lines.append(f"| **Algorithm** | {meta['algo']} |")
        lines.append(f"| **Dataset** | {meta['dataset']} |")
        lines.append(f"| **Files** | {', '.join([f['name'] for f in files]) or 'None found'} |")
        lines.append("")

        for file_info in files:
            lines.append(f"### `{file_info['name']}`\n")
            lines.append("```python")
            # Truncate very long files in README (full code still in zip)
            code = file_info["content"]
            if len(code.splitlines()) > 120:
                truncated = "\n".join(code.splitlines()[:120])
                lines.append(truncated)
                lines.append(f"\n# ... (truncated for report, full code in zip)")
            else:
                lines.append(code)
            lines.append("```\n")

        lines.append("---\n")

    return "\n".join(lines)


def main():
    root = Path(ROOT_DIR).resolve()
    print(f"📁 Scanning: {root}\n")

    folder_data = {}

    for folder_name in sorted(FOLDER_META.keys()):
        folder_path = root / folder_name
        if not folder_path.exists():
            print(f"  ⚠️  Skipping (not found): {folder_name}")
            continue

        print(f"  ✅ Processing: {folder_name}")
        py_files = get_py_files(folder_path)

        files = []
        for f in py_files:
            files.append({
                "name":    f.name,
                "path":    f,
                "content": read_file_content(f)
            })

        folder_data[folder_name] = {"files": files}

    # Generate README
    print("\n📝 Generating README.md ...")
    readme_content = build_readme(root, folder_data)
    readme_path = root / README_FILE
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  ✅ README saved: {readme_path}")

    # Build ZIP
    print("\n📦 Creating submission.zip ...")
    zip_path = root / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add README
        zf.write(readme_path, README_FILE)

        # Add all code files
        for folder_name, data in folder_data.items():
            for file_info in data["files"]:
                arcname = f"{folder_name}/{file_info['name']}"
                zf.write(file_info["path"], arcname)
                print(f"  + {arcname}")

    print(f"\n✅ Done! Zip created: {zip_path}")
    print(f"   Size: {zip_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()