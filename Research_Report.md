# Assignment 6 — XSS Security and AI Research Methods

## 1. Research topic and problem statement
**Topic:** Improving phishing website detection with machine learning. Phishing websites can imitate trusted services to steal personal information. Automated classifiers can help flag suspicious websites, but they can make false-positive and false-negative predictions. This project investigates whether feature selection and model tuning improve detection beyond baseline methods.

## 2. Research question and objectives
**Research question:** Can feature selection and hyperparameter tuning improve phishing website detection compared with baseline Logistic Regression and Random Forest models?

**Objective:** Evaluate the effect of feature selection and tuning on accuracy, precision, recall, F1-score and ROC-AUC, while identifying any tradeoffs in missed phishing sites and false alarms.

## 3. Dataset
Source: https://www.kaggle.com/datasets/shashwatwork/phishing-dataset-for-machine-learning

Assignment 5's repository describes the original dataset as 10,000 rows, 48 features, and a `CLASS_LABEL` target. Its previous analysis reported 9,581 records after removing 419 duplicates while ignoring the ID column, with no missing values. Reuse `data/phishing.csv` from that repository. The new script selects numeric predictors, excludes identifier columns and the target, and performs an 80/20 stratified split with random state 42. Confirm the dataset license and attribution when publishing.

## 4. Method selection
Traditional supervised machine learning is appropriate because the features are tabular and the target is a binary classification label. Logistic Regression provides a simple baseline; Random Forest captures nonlinear feature relationships. The improved method uses feature selection and cross-validated hyperparameter tuning of Random Forest. A deep learning or LLM model is not necessary to answer this narrower experimental question.

## 5. Baseline implementation
Assignment 5 reported **95.20% accuracy for Logistic Regression** and **98.38% accuracy for Random Forest**. These are historical results from Assignment 5, **not new Assignment 6 experimental results**. The provided experiment script reruns both baselines under a consistent data split and compares them against the proposed method. Any differences from the historical figures must be discussed.

## 6. Proposed improvement
The proposed approach selects features using a Random Forest importance model and then tunes the number of trees, maximum tree depth, and minimum leaf size. This could remove less useful inputs and reduce overfitting. It might not improve performance; that is an empirical question. Feature selection occurs inside the cross-validation pipeline to avoid leakage.

## 7. Experimental design and results
The script uses an 80/20 stratified training/test split and five-fold stratified cross-validation on training data for tuning. The test set is used once to compare final models. It produces `results/model_comparison.csv` and `results/model_comparison.json` with accuracy, precision, recall, F1-score, ROC-AUC and confusion matrices. The improved model is selected using cross-validation F1-score.

**Results status: Pending execution with the original CSV.** Do not report the improved method as successful until the experiment is run.

After running, insert the actual comparison table here, discuss which model had the best F1 and recall, and note whether any accuracy gain came at the cost of more false positives. Do not substitute Assignment 5's accuracy values for the new results.

## 8. Discussion and limitations
Potential limitations include one dataset, possible collection bias, features that may not generalize to modern phishing sites, and reliance on a single holdout split. Hyperparameter search adds computation. A future study could evaluate on a second dataset and test stability across multiple seeds. High accuracy alone is insufficient when missing a malicious website has meaningful consequences.

## 9. XSS security problem, control, mitigation and improvement
**Security problem:** When a page interprets untrusted user input as HTML, malicious markup or scripts may execute in the browser.

**Security control:** Use context-appropriate output encoding and safe DOM APIs such as `textContent`; avoid rendering user input with `innerHTML`. Validate inputs for expected structure, but do not rely on validation alone for XSS prevention.

**Mitigation:** The included local demonstration displays a harmless HTML-like string as literal text, rather than interpreting it as markup. No attack is executed and no external service is targeted.

**Security improvement:** User-entered text cannot create new HTML elements through this display path. This demonstrates one defense, not proof that the entire application is XSS-free.

## 10. Code and reproducibility
1. Download the project package and copy the original Assignment 5 `data/phishing.csv` into `data/`.
2. Install Python 3.10+ and run `pip install -r requirements.txt`.
3. Run `python experiment.py` from the project root.
4. Inspect the generated `results/model_comparison.csv` and `.json`.
5. Open `xss_demo.html` in a browser and test the safe rendering of untrusted text.
6. Insert actual model metrics and interpretation into this report before submission.

**Previous project:** https://github.com/umahmed-maker/Cybersecurity-Assignment-5

**AI assistance disclosure:** ChatGPT assisted with the draft, Python experiment structure, and XSS demonstration. The student should run the code, inspect outputs, verify claims, and document any revisions before submitting.
