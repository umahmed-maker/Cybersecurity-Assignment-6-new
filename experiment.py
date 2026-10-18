"""Assignment 6: baseline and tuned phishing classifiers. Run after installing requirements."""
from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

path = Path('data/phishing.csv')
if not path.exists():
    raise SystemExit('Missing data/phishing.csv. Copy the CSV from Assignment 5 into the data folder.')
df = pd.read_csv(path)
if 'CLASS_LABEL' not in df.columns:
    raise SystemExit('Dataset must contain CLASS_LABEL.')
# Match Assignment 5 duplicate treatment: ignore identifier column(s) if present.
id_cols = [c for c in df.columns if c.lower() in ('id', 'index')]
df = df.drop_duplicates(subset=[c for c in df.columns if c not in id_cols])
y = df['CLASS_LABEL']
X = df.drop(columns=['CLASS_LABEL'] + id_cols).select_dtypes(include='number')
if X.isnull().any().any() or y.isnull().any():
    raise SystemExit('Missing values found; document and implement a train-only imputation strategy.')
if y.nunique() != 2:
    raise SystemExit('Expected binary classification target.')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, stratify=y, random_state=42)
models = {
 'Logistic Regression baseline': Pipeline([('scale', StandardScaler()), ('model', LogisticRegression(max_iter=2000, random_state=42))]),
 'Random Forest baseline': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
}
# Feature selection and parameter tuning happen inside cross-validation, never on test data.
pipe = Pipeline([('select', SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1), threshold='median')),
                 ('model', RandomForestClassifier(random_state=42, n_jobs=-1))])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = GridSearchCV(pipe, {'model__n_estimators':[100,200], 'model__max_depth':[None,12], 'model__min_samples_leaf':[1,2]},
                      scoring='f1', cv=cv, n_jobs=-1, refit=True)
models['Tuned Random Forest + feature selection'] = search
results=[]
for name,model in models.items():
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    row={'model':name, 'accuracy':accuracy_score(y_test,pred), 'precision':precision_score(y_test,pred,zero_division=0),
         'recall':recall_score(y_test,pred,zero_division=0), 'f1':f1_score(y_test,pred,zero_division=0),
         'confusion_matrix':confusion_matrix(y_test,pred).tolist()}
    if hasattr(model,'predict_proba'):
        row['roc_auc']=roc_auc_score(y_test,model.predict_proba(X_test)[:,1])
    if hasattr(model,'best_params_'):
        row['best_params']=model.best_params_
        row['best_cv_f1']=model.best_score_
    results.append(row)
Path('results').mkdir(exist_ok=True)
pd.DataFrame([{k:v for k,v in row.items() if k not in ('confusion_matrix','best_params')} for row in results]).to_csv('results/model_comparison.csv',index=False)
Path('results/model_comparison.json').write_text(json.dumps(results,indent=2))
print(pd.DataFrame(results).drop(columns=['confusion_matrix','best_params'],errors='ignore').to_string(index=False))
print('Saved results/model_comparison.csv and .json')
