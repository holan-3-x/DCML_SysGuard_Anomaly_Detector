"""
ModelTrainer.py: Extreme benchmarking script.
Trains and evaluates 13+ ML models, archives them as .bin, and generates a visual leaderboard.
"""
import pandas as pd
import numpy as np
import pathlib
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import dump

# Models
from sklearn.ensemble import RandomForestClassifier, IsolationForest, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, OneClassSVM
from sklearn.neighbors import KNeighborsClassifier, LocalOutlierFactor
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, confusion_matrix

def main():
    base_path = pathlib.Path(__file__).parent.resolve()
    csv_path = base_path / 'output_folder/monitored_data.csv'
    archive_path = base_path / 'archive'
    analytics_path = base_path / 'analytics'
    archive_path.mkdir(exist_ok=True)
    analytics_path.mkdir(exist_ok=True)
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        return

    print(f"🚀 Starting Extreme Benchmarking & Visualization on monitored_data.csv...")
    dataset = pd.read_csv(csv_path)
    
    # Preprocessing
    suffixes_to_drop = ['irq', 'steal', 'guest', 'guest_nice', 'iowait', 'min', 'max']
    cols_to_drop = [c for c in dataset.columns if any(s in c for s in suffixes_to_drop)]
    cols_to_drop += ['time_s', 'Timestamp', 'UserReadTime', 'virtual_total']
    dataset = dataset.drop(columns=[c for c in cols_to_drop if c in dataset.columns])
    
    X = dataset.drop(columns='injector')
    y_true = np.array([0 if i == 'rest' else 1 for i in dataset['injector']])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)
    dump(scaler, base_path / 'standard_scaler.bin')
    
    results = []
    loss_curves = {}

    # Model Definitions
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "NeuralNetwork": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(random_state=42),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "NaiveBayes": GaussianNB(),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "SVM_Linear": SVC(kernel='linear', probability=True, random_state=42),
        "SVM_RBF": SVC(kernel='rbf', probability=True, random_state=42),
        "LDA": LinearDiscriminantAnalysis(),
        "IsolationForest": IsolationForest(contamination='auto', random_state=42),
        "OneClassSVM": OneClassSVM(nu=0.1, kernel='rbf'),
        "LocalOutlierFactor": LocalOutlierFactor(n_neighbors=20, novelty=True)
    }

    for name, model in models.items():
        print(f"Training {name}...")
        start_t = time.time()
        
        is_unsupervised = name in ["IsolationForest", "OneClassSVM", "LocalOutlierFactor"]
        
        try:
            if is_unsupervised:
                model.fit(X_train_std)
                raw_pred = model.predict(X_test_std)
                y_pred = [1 if i == -1 else 0 for i in raw_pred]
            else:
                model.fit(X_train_std, y_train)
                y_pred = model.predict(X_test_std)
                if name == "NeuralNetwork":
                    loss_curves[name] = model.loss_curve_

            train_time = time.time() - start_t
            
            # Metrics
            f1 = f1_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            acc = accuracy_score(y_test, y_pred)
            
            cm = confusion_matrix(y_test, y_pred)
            tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (cm[0][0], 0, 0, 0)
            
            model_file = f"archive/{name}.bin"
            dump(model, base_path / model_file)
            
            results.append({
                "rank": 0, # Placeholder
                "name": name,
                "type": "unsupervised" if is_unsupervised else "supervised",
                "f1": float(f1),
                "precision": float(prec),
                "recall": float(rec),
                "accuracy": float(acc),
                "tp": int(tp), "tn": int(tn), "fp": int(fp), "fn": int(fn),
                "path": model_file
            })
        except Exception as e:
            print(f"Failed to train {name}: {e}")

    # --- VISUALIZATION ---
    plt.style.use('ggplot')
    
    # 1. Leaderboard Bar Chart
    results_df = pd.DataFrame(results).sort_values(by='f1', ascending=False)
    plt.figure(figsize=(14, 7))
    sns.barplot(x='name', y='f1', data=results_df, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('Anomaly Detection Performance: Model Comparison (F1-Score)')
    plt.ylabel('F1 Score')
    plt.tight_layout()
    plt.savefig(analytics_path / 'model_comparison_f1.png')
    plt.close()

    # 2. Confusion Matrices Heatmap (Top 6 Models)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    top_6 = results_df.head(6)['name'].tolist()
    for i, name in enumerate(top_6):
        row, col = i // 3, i % 3
        r = [res for res in results if res['name'] == name][0]
        cm_data = [[r['tn'], r['fp']], [r['fn'], r['tp']]]
        sns.heatmap(cm_data, annot=True, fmt='d', cmap='Blues', ax=axes[row, col], cbar=False)
        axes[row, col].set_title(f"{name} (F1: {r['f1']:.2f})")
        axes[row, col].set_xlabel('Predicted')
        axes[row, col].set_ylabel('Actual')
    plt.suptitle('Confusion Matrices: Top 6 Performers', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(analytics_path / 'confusion_matrices_top6.png')
    plt.close()

    # 3. Training Loss Curve (Neural Network)
    if "NeuralNetwork" in loss_curves:
        plt.figure(figsize=(10, 6))
        plt.plot(loss_curves["NeuralNetwork"], color='tab:red', linewidth=2)
        plt.title('Neural Network Training Loss Curve')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(analytics_path / 'neural_network_loss.png')
        plt.close()

    # 4. Comprehensive Metrics Plot (Precision vs Recall)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='recall', y='precision', hue='name', size='accuracy', data=results_df, palette='Set2', sizes=(100, 400))
    plt.title('Model Precision vs Recall Trade-off')
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(analytics_path / 'precision_recall_scatter.png')
    plt.close()

    # Save Leaderboard to Markdown
    results.sort(key=lambda x: x['f1'], reverse=True)
    md_table = "| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |\n"
    md_table += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(results):
        rank = medals[i] if i < 3 else str(i + 1)
        md_table += f"| {rank} | **{r['name']}** | {r['type']} | {r['f1']:.4f} | {r['accuracy']:.4f} | {r['tp']} | {r['tn']} | {r['fp']} | {r['fn']} | `{r['path']}` |\n"

    with open(analytics_path / 'leaderboard.md', 'w') as f:
        f.write("# 🏆 Anomaly Detection Leaderboard\n\n")
        f.write("![Model Comparison](model_comparison_f1.png)\n\n")
        f.write(md_table)
        f.write("\n\n### Metrics Breakdown\n")
        f.write("![Top 6 Confusion Matrices](confusion_matrices_top6.png)\n")
        if "NeuralNetwork" in loss_curves:
            f.write("\n### Training Behavior\n")
            f.write("![NN Loss Curve](neural_network_loss.png)\n")

    # Save JSON Leaderboard with ranks
    for i, r in enumerate(results):
        r['rank'] = i + 1
    
    with open(analytics_path / 'leaderboard.json', 'w') as f:
        json.dump({"models": results, "generated_at": time.ctime()}, f, indent=4)

    # Save Best Model to best_model.bin
    best_model_path = base_path / results[0]['path']
    import shutil
    shutil.copy(best_model_path, base_path / 'best_model.bin')
    
    print(f"\n✅ Benchmarking & Visualization complete! Best model: {results[0]['name']}")
    print(f"Find all plots in src/analytics/")

if __name__ == '__main__':
    main()
