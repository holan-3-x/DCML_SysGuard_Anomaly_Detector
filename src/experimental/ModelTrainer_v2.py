"""
ModelTrainer_v2.py: Industrial-grade ML training for V2 Datasets.
Optimized for strictly rate-based telemetry (no cumulative counters).
"""
import pandas as pd
import numpy as np
import pathlib
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import dump
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
# Metrics
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from sklearn.preprocessing import StandardScaler

def main_v2():
    base_path = pathlib.Path(__file__).parent.resolve()
    # Explicitly looking for V2 data
    csv_path = base_path / 'output_folder/monitored_data_v2.csv'
    archive_path = base_path / 'archive_v2'
    analytics_path = base_path / 'analytics_v2'
    
    archive_path.mkdir(exist_ok=True)
    analytics_path.mkdir(exist_ok=True)
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found. Please run 'DataCollector_v2_v2.py' first.")
        return

    print(f"🚀 (V2) Starting Industrial Model Training...")
    dataset = pd.read_csv(csv_path)
    
    # Preprocessing (V2 is cleaner, so less dropping needed)
    cols_to_drop = ['Timestamp', 'UserReadTime', 'net_connections']
    X = dataset.drop(columns=[c for c in cols_to_drop if c in dataset.columns], errors='ignore')
    
    # If injector column exists, use it for labels
    if 'injector' in dataset.columns:
        X = X.drop(columns='injector')
        y_true = np.array([0 if i == 'rest' else 1 for i in dataset['injector']])
    else:
        print("Error: No 'injector' column found in V2 data.")
        return
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)
    
    # Save V2 Scaler
    dump(scaler, base_path.parent / 'standard_scaler_v2.bin')
    print(f"Saved scaler to ../standard_scaler_v2.bin")
    
    results = []
    
    # V2 Selection: Focused on High Performance Models
    models = {
        "RandomForest_V2": RandomForestClassifier(n_estimators=100, random_state=42),
        "NeuralNetwork_V2": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
        "GradientBoosting_V2": GradientBoostingClassifier(random_state=42),
        "IsolationForest_V2": IsolationForest(contamination='auto', random_state=42),
    }

    for name, model in models.items():
        print(f"Training {name}...")
        try:
            if "IsolationForest" in name:
                model.fit(X_train_std)
                raw_pred = model.predict(X_test_std)
                y_pred = [1 if i == -1 else 0 for i in raw_pred]
            else:
                model.fit(X_train_std, y_train)
                y_pred = model.predict(X_test_std)

            f1 = f1_score(y_test, y_pred)
            acc = accuracy_score(y_test, y_pred)
            
            # Save V2 Model per model file
            model_file = f"archive_v2/{name}.bin"
            dump(model, base_path.parent / model_file)
            
            results.append({
                "name": name,
                "f1": f1,
                "accuracy": acc,
                "path": model_file
            })
        except Exception as e:
            print(f"Failed {name}: {e}")

    # Rank and Pick Champion
    results.sort(key=lambda x: x['f1'], reverse=True)
    champion = results[0]
    
    # Save Best V2 Model
    import shutil
    shutil.copy(base_path.parent / champion['path'], base_path.parent / 'best_model_v2.bin')
    
    print(f"\n🏆 V2 Training Complete. Champion: {champion['name']} (F1: {champion['f1']:.4f})")
    print(f"Saved champion to: src/best_model_v2.bin")

if __name__ == '__main__':
    main_v2()
