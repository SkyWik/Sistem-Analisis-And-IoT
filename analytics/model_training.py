import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
import os

# Membuat data sintetik untuk studi kasus jika database kosong
def generate_synthetic_data():
    import numpy as np
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'temperature': np.random.normal(27, 2, n),
        'humidity': np.random.normal(65, 10, n),
        'light_level': np.random.randint(200, 800, n)
    })
    # Membuat anomali jika suhu > 29 atau kelembaban > 80
    df['target_anomaly'] = ((df['temperature'] > 29) | (df['humidity'] > 80)).astype(int)
    return df

db_path = '../backend/warehouse_data.db'

print("Tahap CRISP-DM: Data Understanding & Preparation...")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT temperature, humidity, light_level, target_anomaly FROM sensor_logs", conn)
    conn.close()
    if len(df) < 50:
        df = generate_synthetic_data()
else:
    df = generate_synthetic_data()

print(f"Total baris data: {len(df)}")

X = df[['temperature', 'humidity', 'light_level']]
y = df['target_anomaly']

# Memastikan tidak ada data leakage dengan memisahkan data latih dan uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("\nTahap CRISP-DM: Pemodelan...")
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    roc_auc = roc_auc_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\n--- {name} ---")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    # Menghindari model yang tidak layak seperti pada studi kasus PT Maju Bersama
    if roc_auc < 0.65:
        print("Peringatan: Model ini memiliki performa yang buruk dalam mendeteksi anomali.")
