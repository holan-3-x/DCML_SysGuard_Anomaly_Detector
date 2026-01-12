# 🏆 Anomaly Detection Leaderboard

![Model Comparison](model_comparison_f1.png)

| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇 | **GradientBoosting** | supervised | 0.8704 | 0.8906 | 47 | 67 | 8 | 6 | `archive/GradientBoosting.pkl` |
| 🥈 | **RandomForest** | supervised | 0.8571 | 0.8828 | 45 | 68 | 7 | 8 | `archive/RandomForest.pkl` |
| 🥉 | **LogisticRegression** | supervised | 0.8039 | 0.8438 | 41 | 67 | 8 | 12 | `archive/LogisticRegression.pkl` |
| 4 | **NeuralNetwork** | supervised | 0.7928 | 0.8203 | 44 | 61 | 14 | 9 | `archive/NeuralNetwork.pkl` |
| 5 | **SVM_RBF** | supervised | 0.7917 | 0.8438 | 38 | 70 | 5 | 15 | `archive/SVM_RBF.pkl` |
| 6 | **DecisionTree** | supervised | 0.7885 | 0.8281 | 41 | 65 | 10 | 12 | `archive/DecisionTree.pkl` |
| 7 | **SVM_Linear** | supervised | 0.7843 | 0.8281 | 40 | 66 | 9 | 13 | `archive/SVM_Linear.pkl` |
| 8 | **NaiveBayes** | supervised | 0.7556 | 0.8281 | 34 | 72 | 3 | 19 | `archive/NaiveBayes.pkl` |
| 9 | **LDA** | supervised | 0.7500 | 0.7812 | 42 | 58 | 17 | 11 | `archive/LDA.pkl` |
| 10 | **LocalOutlierFactor** | unsupervised | 0.6809 | 0.7656 | 32 | 66 | 9 | 21 | `archive/LocalOutlierFactor.pkl` |
| 11 | **KNN** | supervised | 0.5909 | 0.7188 | 26 | 66 | 9 | 27 | `archive/KNN.pkl` |
| 12 | **OneClassSVM** | unsupervised | 0.5366 | 0.7031 | 22 | 68 | 7 | 31 | `archive/OneClassSVM.pkl` |
| 13 | **IsolationForest** | unsupervised | 0.3824 | 0.6719 | 13 | 73 | 2 | 40 | `archive/IsolationForest.pkl` |


### Metrics Breakdown
![Top 6 Confusion Matrices](confusion_matrices_top6.png)

### Training Behavior
![NN Loss Curve](neural_network_loss.png)
