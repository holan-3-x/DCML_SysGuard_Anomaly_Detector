# 🏆 Anomaly Detection Leaderboard

![Model Comparison](model_comparison_f1.png)

| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇 | **RandomForest** | supervised | 0.8712 | 0.8600 | 71 | 58 | 11 | 10 | `archive/RandomForest.bin` |
| 🥈 | **GradientBoosting** | supervised | 0.8679 | 0.8600 | 69 | 60 | 9 | 12 | `archive/GradientBoosting.bin` |
| 🥉 | **LDA** | supervised | 0.8182 | 0.8133 | 63 | 59 | 10 | 18 | `archive/LDA.bin` |
| 4 | **LogisticRegression** | supervised | 0.8158 | 0.8133 | 62 | 60 | 9 | 19 | `archive/LogisticRegression.bin` |
| 5 | **NeuralNetwork** | supervised | 0.8077 | 0.8000 | 63 | 57 | 12 | 18 | `archive/NeuralNetwork.bin` |
| 6 | **SVM_RBF** | supervised | 0.7973 | 0.8000 | 59 | 61 | 8 | 22 | `archive/SVM_RBF.bin` |
| 7 | **DecisionTree** | supervised | 0.7901 | 0.7733 | 64 | 52 | 17 | 17 | `archive/DecisionTree.bin` |
| 8 | **KNN** | supervised | 0.7838 | 0.7867 | 58 | 60 | 9 | 23 | `archive/KNN.bin` |
| 9 | **SVM_Linear** | supervised | 0.7755 | 0.7800 | 57 | 60 | 9 | 24 | `archive/SVM_Linear.bin` |
| 10 | **NaiveBayes** | supervised | 0.6667 | 0.7067 | 44 | 62 | 7 | 37 | `archive/NaiveBayes.bin` |
| 11 | **IsolationForest** | unsupervised | 0.5299 | 0.6333 | 31 | 64 | 5 | 50 | `archive/IsolationForest.bin` |
| 12 | **OneClassSVM** | unsupervised | 0.5079 | 0.5867 | 32 | 56 | 13 | 49 | `archive/OneClassSVM.bin` |
| 13 | **LocalOutlierFactor** | unsupervised | 0.3269 | 0.5333 | 17 | 63 | 6 | 64 | `archive/LocalOutlierFactor.bin` |


### Metrics Breakdown
![Top 6 Confusion Matrices](confusion_matrices_top6.png)

### Training Behavior
![NN Loss Curve](neural_network_loss.png)
