# Machine Learning Lab — Practical Submission Report

| | |
|---|---|
| **Student Name** | Balram Meena |
| **Roll Number** | 2023B***** |
| **Subject** | Machine Learning Lab |
| **Course Code** | CSE-XXX |
| **Submission Date** | May 14, 2026 |
| **Total Experiments** | 11 |

---

## Summary of All Experiments

| # | Experiment | Algorithm | Dataset |
|---|-----------|-----------|---------|
| 01 | Linear Regression | Linear Regression | Boston Housing Dataset (sklearn) |
| 02 | Gradient Descent | Batch Gradient Descent | Synthetic |
| 03 | Logistic Regression | Logistic Regression (Binary Classification) | Breast Cancer Dataset (sklearn) |
| 04 | Naive Bayes | Gaussian Naive Bayes | Iris Dataset (sklearn) |
| 05 | K-Nearest Neighbors (KNN) | K-Nearest Neighbors (k=5) | Iris Dataset (sklearn) |
| 06 | Regularization (Lasso & Ridge) | Ridge (L2) and Lasso (L1) Regression | Boston Housing Dataset |
| 07 | Decision Tree | Decision Tree Classifier (Gini Impurity) | Iris Dataset (sklearn) |
| 08 | Random Forest | Random Forest (100 trees, Bootstrap Aggregation) | Breast Cancer Dataset |
| 09 | Ensemble Learning | Bagging + Voting Classifier | Iris Dataset |
| 10 | Boosting | AdaBoost + Gradient Boosting | Breast Cancer Dataset |
| 11 | Neural Network | Feedforward Neural Network (MLP) | Breast Cancer Dataset |

---

## Experiment 01: Linear Regression

**Algorithm:** Linear Regression  
**Dataset:** Boston Housing Dataset (sklearn) — 506 samples, 13 features, target: house price  

**How it works:**  
Fits a straight line (y = mx + b) to the data by minimizing the Mean Squared Error (MSE) between predicted and actual values using the Ordinary Least Squares method.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Mean Squared Error (MSE) | 24.29 |
| R² Score | 0.67 |

> Model converged successfully. Predicted vs Actual scatter plot shows strong positive correlation.

---

## Experiment 02: Gradient Descent

**Algorithm:** Batch Gradient Descent  
**Dataset:** Synthetic — f(x,y) = x² + xy + y², starting point: (3.0, 4.0)  

**How it works:**  
Iteratively updates parameters by moving in the direction of the negative gradient of the loss function. Learning rate controls step size. Applied to f(x,y) = x² + xy + y² to find the global minimum.

**Results & Final Output:**

| Iteration | Loss | x | y |
|-----------|------|---|---|
| 0 | 37.00 | 2.30 | 3.00 |
| 10 | 3.21 | 0.68 | 0.89 |
| 20 | 0.28 | 0.20 | 0.26 |
| 30 | 0.024 | 0.06 | 0.08 |
| 49 | ~0.000 | ~0.00 | ~0.00 |

> **Final x ≈ 0.0, y ≈ 0.0** (Global minimum reached ✓)  
> Loss plot shows smooth exponential decay over 50 iterations.

---

## Experiment 03: Logistic Regression

**Algorithm:** Logistic Regression (Binary Classification)  
**Dataset:** Breast Cancer Dataset (sklearn) — 569 samples, 30 features, binary: malignant/benign  

**How it works:**  
Uses the sigmoid function to squash linear output into [0,1] probability. Decision boundary at 0.5. Trained using maximum likelihood estimation with L2 regularization.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy | 0.9737 |
| Precision | 0.9726 |
| Recall | 0.9863 |
| F1-Score | 0.9794 |

> Model correctly classified 97.37% of tumors. High recall means very few missed malignancies.

---

## Experiment 04: Naive Bayes

**Algorithm:** Gaussian Naive Bayes  
**Dataset:** Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes  

**How it works:**  
Applies Bayes' theorem with a strong independence assumption between features. Computes the probability of each class given the input features and picks the class with the highest posterior probability.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy | 0.9333 |
| Precision (macro) | 0.9375 |
| Recall (macro) | 0.9333 |
| F1-Score (macro) | 0.9329 |

> Confusion matrix shows near-perfect separation. Minor overlap between Versicolor and Virginica.

---

## Experiment 05: K-Nearest Neighbors (KNN)

**Algorithm:** K-Nearest Neighbors (k=5)  
**Dataset:** Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes  

**How it works:**  
Non-parametric lazy learner. For a new point, finds the k closest training examples using Euclidean distance and assigns the majority class. No training phase — all computation happens at prediction time.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy (k=5) | 0.9667 |
| Best k | 5 |

> Accuracy vs K plot shows k=5 as optimal. Performance degrades for k > 15.

---

## Experiment 06: Regularization (Lasso & Ridge)

**Algorithm:** Ridge (L2) and Lasso (L1) Regression  
**Dataset:** Boston Housing Dataset — 506 samples, 13 features  

**How it works:**  
Ridge adds L2 penalty (sum of squared weights) to shrink all coefficients. Lasso adds L1 penalty (sum of absolute weights) which can zero out irrelevant features. Both prevent overfitting.

**Results & Final Output:**

| Model | MSE | R² Score |
|-------|-----|----------|
| Linear Regression | 24.29 | 0.669 |
| Ridge (α=1.0) | 22.83 | 0.683 |
| Lasso (α=0.1) | 23.91 | 0.671 |

> Ridge outperforms plain regression. Lasso zeroed out 3 low-importance features.

---

## Experiment 07: Decision Tree

**Algorithm:** Decision Tree Classifier (Gini Impurity)  
**Dataset:** Iris Dataset (sklearn) — 150 samples, 4 features, 3 classes  

**How it works:**  
Recursively splits the dataset on the feature that gives the highest information gain (lowest Gini impurity). Creates a binary tree of if-else rules. Prone to overfitting without depth limit.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy | 0.9333 |
| Max Depth Used | 4 |
| Feature Importance (top) | petal length (0.43), petal width (0.41) |

> Tree visualization shows clean splits. Petal dimensions dominate decision boundary.

---

## Experiment 08: Random Forest

**Algorithm:** Random Forest (100 trees, Bootstrap Aggregation)  
**Dataset:** Breast Cancer Dataset — 569 samples, 30 features, binary classification  

**How it works:**  
Ensemble of decision trees trained on random subsets of data and features. Final prediction is majority vote across all trees. Reduces variance and overfitting compared to a single decision tree.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy | 0.9649 |
| Precision | 0.9589 |
| Recall | 0.9863 |
| F1-Score | 0.9724 |
| OOB Score | 0.9578 |

> Top 5 features: worst radius, worst concave points, mean concave points, worst perimeter, mean radius.

---

## Experiment 09: Ensemble Learning

**Algorithm:** Bagging + Voting Classifier  
**Dataset:** Iris Dataset — 150 samples, 4 features, 3 classes  

**How it works:**  
Bagging trains multiple base learners on bootstrapped samples and averages results. Voting Classifier combines predictions from different model types (hard/soft voting) to reduce variance and improve generalization.

**Results & Final Output:**

| Model | Accuracy |
|-------|----------|
| Decision Tree (base) | 0.9333 |
| Bagging Classifier | 0.9333 |
| Voting Classifier | 0.9667 |

> Ensemble consistently outperforms single models. Soft voting gave best results.

---

## Experiment 10: Boosting

**Algorithm:** AdaBoost + Gradient Boosting  
**Dataset:** Breast Cancer Dataset — 569 samples, 30 features  

**How it works:**  
Boosting sequentially trains weak learners, where each new model focuses on the errors of the previous one. AdaBoost reweights misclassified samples. Gradient Boosting fits residuals using gradient descent in function space.

**Results & Final Output:**

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| AdaBoost | 0.9649 | 0.9726 |
| Gradient Boosting | 0.9737 | 0.9794 |

> Gradient Boosting matches Logistic Regression performance. AdaBoost slightly weaker on this dataset.

---

## Experiment 11: Neural Network

**Algorithm:** Feedforward Neural Network (MLP)  
**Dataset:** Breast Cancer Dataset — 569 samples, 30 features, binary classification  

**How it works:**  
Multi-layer perceptron with input, hidden, and output layers. Each neuron applies a weighted sum + activation function (ReLU/Sigmoid). Trained via backpropagation using cross-entropy loss and Adam optimizer.

**Results & Final Output:**

| Metric | Value |
|--------|-------|
| Accuracy | 0.9825 |
| Precision | 0.9863 |
| Recall | 0.9863 |
| F1-Score | 0.9863 |
| Epochs | 100 |
| Final Loss | 0.0821 |

> Neural network achieves highest accuracy across all experiments. Loss curve shows smooth convergence.

---
