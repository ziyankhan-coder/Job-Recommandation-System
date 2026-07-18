import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer # UPGRADE 1: CountVectorizer se TF-IDF
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier       # UPGRADE 2: Logistic Regression se Random Forest
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# 1. Load Data
df = pd.read_csv('jobrecommendation/model/Job_Dataset.csv')
df['combined_skills'] = df['User_Skills'].fillna('') + " " + df['Job_Requirements'].fillna('')

y = df['Recommended']

# 2. UPGRADE 1: Text Embedding using TF-IDF
# sublinear_tf=True lagane se frequency variations balance ho jati hain
vectorizer = TfidfVectorizer(max_features=1500, stop_words='english', sublinear_tf=True)
X_text = vectorizer.fit_transform(df['combined_skills'])

# Match Score numeric column ko horizontal stack se jodein
X = hstack((X_text, df[['Match_Score']].values))

# 3. Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. UPGRADE 2: Initialize Random Forest
# n_estimators=100 se yeh 100 alag-alag trees banakar accuracy stable karega
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=12)
model.fit(X_train, y_train)

# 5. Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("====================================")
print("🚀 Upgraded Model Accuracy:", round(accuracy * 100, 2), "%")
print("====================================")

# 6. Save Artifacts securely inside model/ folder
os.makedirs('model', exist_ok=True)
joblib.dump(model, "model/job_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")
print("[SUCCESS] Upgraded pkl files saved inside model/ folder!")