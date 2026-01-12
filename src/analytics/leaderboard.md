# 🏆 Anomaly Detection Leaderboard

![Model Comparison](model_comparison_f1.png)

| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇 | **GradientBoosting** | supervised | 0.8344 | 0.8366 | 63 | 65 | 6 | 19 | `archive/GradientBoosting.bin` |
| 🥈 | **DecisionTree** | supervised | 0.8228 | 0.8170 | 65 | 60 | 11 | 17 | `archive/DecisionTree.bin` |
| 🥉 | **RandomForest** | supervised | 0.8138 | 0.8235 | 59 | 67 | 4 | 23 | `archive/RandomForest.bin` |
| 4 | **SVM_RBF** | supervised | 0.7626 | 0.7843 | 53 | 67 | 4 | 29 | `archive/SVM_RBF.bin` |
| 5 | **KNN** | supervised | 0.7556 | 0.7843 | 51 | 69 | 2 | 31 | `archive/KNN.bin` |
| 6 | **NeuralNetwork** | supervised | 0.7465 | 0.7647 | 53 | 64 | 7 | 29 | `archive/NeuralNetwork.bin` |
| 7 | **LDA** | supervised | 0.7338 | 0.7582 | 51 | 65 | 6 | 31 | `archive/LDA.bin` |
| 8 | **NaiveBayes** | supervised | 0.7059 | 0.7386 | 48 | 65 | 6 | 34 | `archive/NaiveBayes.bin` |
| 9 | **SVM_Linear** | supervised | 0.6950 | 0.7190 | 49 | 61 | 10 | 33 | `archive/SVM_Linear.bin` |
| 10 | **LogisticRegression** | supervised | 0.6667 | 0.7059 | 45 | 63 | 8 | 37 | `archive/LogisticRegression.bin` |
| 11 | **IsolationForest** | unsupervised | 0.5500 | 0.6471 | 33 | 66 | 5 | 49 | `archive/IsolationForest.bin` |
| 12 | **OneClassSVM** | unsupervised | 0.5470 | 0.6536 | 32 | 68 | 3 | 50 | `archive/OneClassSVM.bin` |
| 13 | **LocalOutlierFactor** | unsupervised | 0.0471 | 0.4706 | 2 | 70 | 1 | 80 | `archive/LocalOutlierFactor.bin` |


### Metrics Breakdown
![Top 6 Confusion Matrices](confusion_matrices_top6.png)

### Training Behavior
![NN Loss Curve](neural_network_loss.png)
