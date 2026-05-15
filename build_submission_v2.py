"""
ML Assignment Submission Builder v2
-------------------------------------
Generates a CLEAN 5-page report (no code) + zips everything.
Report contains: Algorithm, Dataset, How it works, Final Output/Metrics.

HOW TO USE:
  1. Place this script in the ROOT folder (same level as 01-xx folders)
  2. Edit CONFIG section below
  3. Run: python build_submission_v2.py
"""

import os
import json
import zipfile
import subprocess
import sys
import io
from pathlib import Path
from datetime import date
from contextlib import redirect_stdout

# ─────────────────────────────────────────────
# CONFIG — EDIT THESE
# ─────────────────────────────────────────────
STUDENT_NAME  = "Balram Meena"
ROLL_NUMBER   = "2023BTCSE006"
SUBJECT       = "Machine Learning Lab"
COURSE_CODE   = "CSE-XXX"
ROOT_DIR      = "."
OUTPUT_ZIP    = "submission.zip"
README_FILE   = "REPORT.md"

# ─────────────────────────────────────────────
# REPORT CONTENT — Algorithm + Dataset + What it does + Expected Output
# Edit "actual_output" fields with YOUR real results after running your code
# ─────────────────────────────────────────────
EXPERIMENTS = [
    {
        "id": "01",
        "title": "Linear Regression",
        "folder": "01-Linear-Regression",
        "algorithm": "Linear Regression",
        "how_it_works": (
            "Fits a straight line (y = mx + b) to the data by minimizing the "
            "Mean Squared Error (MSE) between predicted and actual values using "
            "the Ordinary Least Squares method."
        ),
        "dataset": "Boston Housing Dataset (sklearn) — 506 samples, 13 features, target: house price",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Mean Squared Error (MSE) | 24.29 |
| R² Score | 0.67 |

> Model converged successfully. Predicted vs Actual scatter plot shows strong positive correlation.
""",
    },
    {
        "id": "02",
        "title": "Gradient Descent",
        "folder": "02-Gradient-Descent",
        "algorithm": "Batch Gradient Descent",
        "how_it_works": (
            "Iteratively updates parameters by moving in the direction of the "
            "negative gradient of the loss function. Learning rate controls step size. "
            "Applied to f(x,y) = x² + xy + y² to find the global minimum."
        ),
        "dataset": "Synthetic — f(x,y) = x² + xy + y², starting point: (3.0, 4.0)",
        "actual_output": """
| Iteration | Loss | x | y |
|-----------|------|---|---|
| 0 | 37.00 | 2.30 | 3.00 |
| 10 | 3.21 | 0.68 | 0.89 |
| 20 | 0.28 | 0.20 | 0.26 |
| 30 | 0.024 | 0.06 | 0.08 |
| 49 | ~0.000 | ~0.00 | ~0.00 |

> **Final x ≈ 0.0, y ≈ 0.0** (Global minimum reached ✓)  
> Loss plot shows smooth exponential decay over 50 iterations.
""",
    },
    {
        "id": "03",
        "title": "Logistic Regression",
        "folder": "03-Logistic-Regression",
        "algorithm": "Logistic Regression (Binary Classification)",
        "how_it_works": (
            "Uses the sigmoid function to squash linear output into [0,1] probability. "
            "Decision boundary at 0.5. Trained using maximum likelihood estimation "
            "with L2 regularization."
        ),
        "dataset": "Breast Cancer Dataset (sklearn) — 569 samples, 30 features, binary: malignant/benign",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy | 0.9737 |
| Precision | 0.9726 |
| Recall | 0.9863 |
| F1-Score | 0.9794 |

> Model correctly classified 97.37% of tumors. High recall means very few missed malignancies.
""",
    },
    {
        "id": "04",
        "title": "Naive Bayes",
        "folder": "04-Naive-Bayes",
        "algorithm": "Gaussian Naive Bayes",
        "how_it_works": (
            "Applies Bayes' theorem with a strong independence assumption between features. "
            "Computes the probability of each class given the input features and "
            "picks the class with the highest posterior probability."
        ),
        "dataset": "Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy | 0.9333 |
| Precision (macro) | 0.9375 |
| Recall (macro) | 0.9333 |
| F1-Score (macro) | 0.9329 |

> Confusion matrix shows near-perfect separation. Minor overlap between Versicolor and Virginica.
""",
    },
    {
        "id": "05",
        "title": "K-Nearest Neighbors (KNN)",
        "folder": "05-KNN",
        "algorithm": "K-Nearest Neighbors (k=5)",
        "how_it_works": (
            "Non-parametric lazy learner. For a new point, finds the k closest training "
            "examples using Euclidean distance and assigns the majority class. "
            "No training phase — all computation happens at prediction time."
        ),
        "dataset": "Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy (k=5) | 0.9667 |
| Best k | 5 |

> Accuracy vs K plot shows k=5 as optimal. Performance degrades for k > 15.
""",
    },
    {
        "id": "06",
        "title": "Regularization (Lasso & Ridge)",
        "folder": "06-Regularization",
        "algorithm": "Ridge (L2) and Lasso (L1) Regression",
        "how_it_works": (
            "Ridge adds L2 penalty (sum of squared weights) to shrink all coefficients. "
            "Lasso adds L1 penalty (sum of absolute weights) which can zero out irrelevant features. "
            "Both prevent overfitting."
        ),
        "dataset": "Boston Housing Dataset — 506 samples, 13 features",
        "actual_output": """
| Model | MSE | R² Score |
|-------|-----|----------|
| Linear Regression | 24.29 | 0.669 |
| Ridge (α=1.0) | 22.83 | 0.683 |
| Lasso (α=0.1) | 23.91 | 0.671 |

> Ridge outperforms plain regression. Lasso zeroed out 3 low-importance features.
""",
    },
    {
        "id": "07",
        "title": "Decision Tree",
        "folder": "07-Decision-Tree",
        "algorithm": "Decision Tree Classifier (Gini Impurity)",
        "how_it_works": (
            "Recursively splits the dataset on the feature that gives the highest "
            "information gain (lowest Gini impurity). Creates a binary tree of "
            "if-else rules. Prone to overfitting without depth limit."
        ),
        "dataset": "Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy | 0.9333 |
| Max Depth Used | 4 |
| Feature Importance (top) | petal length (0.43), petal width (0.41) |

> Tree visualization shows clean splits. Petal dimensions dominate decision boundary.
""",
    },
    {
        "id": "08",
        "title": "Random Forest",
        "folder": "08-Random-Forest",
        "algorithm": "Random Forest (100 trees, Bootstrap Aggregation)",
        "how_it_works": (
            "Ensemble of decision trees trained on random subsets of data and features. "
            "Final prediction is majority vote across all trees. Reduces variance "
            "and overfitting compared to a single decision tree."
        ),
        "dataset": "Breast Cancer Dataset — 569 samples, 30 features, binary classification",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy | 0.9649 |
| Precision | 0.9589 |
| Recall | 0.9863 |
| F1-Score | 0.9724 |
| OOB Score | 0.9578 |

> Top 5 features: worst radius, worst concave points, mean concave points, worst perimeter, mean radius.
""",
    },
    {
        "id": "09",
        "title": "Ensemble Learning",
        "folder": "09-Ensemble-Learning",
        "algorithm": "Bagging + Voting Classifier",
        "how_it_works": (
            "Bagging trains multiple base learners on bootstrapped samples and averages results. "
            "Voting Classifier combines predictions from different model types (hard/soft voting) "
            "to reduce variance and improve generalization."
        ),
        "dataset": "Iris Dataset — 150 samples, 4 features, 3 classes",
        "actual_output": """
| Model | Accuracy |
|-------|----------|
| Decision Tree (base) | 0.9333 |
| Bagging Classifier | 0.9333 |
| Voting Classifier | 0.9667 |

> Ensemble consistently outperforms single models. Soft voting gave best results.
""",
    },
    {
        "id": "10",
        "title": "Boosting",
        "folder": "10-Boosting",
        "algorithm": "AdaBoost + Gradient Boosting",
        "how_it_works": (
            "Boosting sequentially trains weak learners, where each new model focuses "
            "on the errors of the previous one. AdaBoost reweights misclassified samples. "
            "Gradient Boosting fits residuals using gradient descent in function space."
        ),
        "dataset": "Breast Cancer Dataset — 569 samples, 30 features",
        "actual_output": """
| Model | Accuracy | F1-Score |
|-------|----------|----------|
| AdaBoost | 0.9649 | 0.9726 |
| Gradient Boosting | 0.9737 | 0.9794 |

> Gradient Boosting matches Logistic Regression performance. AdaBoost slightly weaker on this dataset.
""",
    },
    {
        "id": "11",
        "title": "Neural Network",
        "folder": "11-Neural-Network",
        "algorithm": "Feedforward Neural Network (MLP)",
        "how_it_works": (
            "Multi-layer perceptron with input, hidden, and output layers. "
            "Each neuron applies a weighted sum + activation function (ReLU/Sigmoid). "
            "Trained via backpropagation using cross-entropy loss and Adam optimizer."
        ),
        "dataset": "Breast Cancer Dataset — 569 samples, 30 features, binary classification",
        "actual_output": """
| Metric | Value |
|--------|-------|
| Accuracy | 0.9825 |
| Precision | 0.9863 |
| Recall | 0.9863 |
| F1-Score | 0.9863 |
| Epochs | 100 |
| Final Loss | 0.0821 |

> Neural network achieves highest accuracy across all experiments. Loss curve shows smooth convergence.
""",
    },
]

# ─────────────────────────────────────────────
# BUILD REPORT
# ─────────────────────────────────────────────

def build_report():
    lines = []

    # Cover
    lines.append("# Machine Learning Lab — Practical Submission Report\n")
    lines.append(f"| | |")
    lines.append(f"|---|---|")
    lines.append(f"| **Student Name** | {STUDENT_NAME} |")
    lines.append(f"| **Roll Number** | {ROLL_NUMBER} |")
    lines.append(f"| **Subject** | {SUBJECT} |")
    lines.append(f"| **Course Code** | {COURSE_CODE} |")
    lines.append(f"| **Submission Date** | {date.today().strftime('%B %d, %Y')} |")
    lines.append(f"| **Total Experiments** | {len(EXPERIMENTS)} |\n")
    lines.append("---\n")

    # Summary Table
    lines.append("## Summary of All Experiments\n")
    lines.append("| # | Experiment | Algorithm | Dataset |")
    lines.append("|---|-----------|-----------|---------|")
    for exp in EXPERIMENTS:
        lines.append(f"| {exp['id']} | {exp['title']} | {exp['algorithm']} | {exp['dataset'].split('—')[0].strip()} |")
    lines.append("\n---\n")

    # Each experiment
    for exp in EXPERIMENTS:
        lines.append(f"## Experiment {exp['id']}: {exp['title']}\n")
        lines.append(f"**Algorithm:** {exp['algorithm']}  ")
        lines.append(f"**Dataset:** {exp['dataset']}  \n")
        lines.append(f"**How it works:**  \n{exp['how_it_works']}\n")
        lines.append(f"**Results & Final Output:**")
        lines.append(exp['actual_output'])
        lines.append("---\n")

    return "\n".join(lines)


def main():
    root = Path(ROOT_DIR).resolve()

    print("📝 Building clean report...")
    report = build_report()
    report_path = root / README_FILE
    report_path.write_text(report, encoding="utf-8")
    print(f"  ✅ Report saved: {report_path}")

    print("\n📦 Creating submission.zip...")
    zip_path = root / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add report
        zf.write(report_path, README_FILE)

        # Add all code files from each folder
        for exp in EXPERIMENTS:
            folder_path = root / exp["folder"]
            if not folder_path.exists():
                print(f"  ⚠️  Folder not found: {exp['folder']}")
                continue

            for ext in ("*.py", "*.ipynb"):
                for f in sorted(folder_path.rglob(ext)):
                    arcname = f"{exp['folder']}/{f.name}"
                    zf.write(f, arcname)
                    print(f"  + {arcname}")

    print(f"\n✅ Done!")
    print(f"   Report : {report_path}")
    print(f"   Zip    : {zip_path} ({zip_path.stat().st_size / 1024:.1f} KB)")
    print(f"\n⚠️  IMPORTANT: Update the 'actual_output' fields in EXPERIMENTS[]")
    print(f"   with your real results before final submission!")


if __name__ == "__main__":
    main()
