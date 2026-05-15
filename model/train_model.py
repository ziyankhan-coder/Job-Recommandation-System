import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('Job_Dataset.csv')
X = df[['User_Skills','Job_Requirements','Match_Score']]
y = df['Recommended']
df['combined_skills'] = df['User_Skills'] + " " + df['Job_Requirements']
print(df['combined_skills'])

vectorizer = CountVectorizer()

X_text = vectorizer.fit_transform(df['combined_skills'])
X = hstack((X_text, df[['Match_Score']].values))


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

joblib.dump(model,"job_model.pkl")
joblib.dump(vectorizer,"vectorizer.pkl")