# 🏆 Anomaly Detection Leaderboard

![Model Comparison](model_comparison_f1.png)

| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇 | **RandomForest** | supervised | 0.8919 | 0.8954 | 66 | 71 | 12 | 4 | `archive/RandomForest.bin` |
| 🥈 | **GradientBoosting** | supervised | 0.8800 | 0.8824 | 66 | 69 | 14 | 4 | `archive/GradientBoosting.bin` |
| 🥉 | **SVM_RBF** | supervised | 0.7939 | 0.8235 | 52 | 74 | 9 | 18 | `archive/SVM_RBF.bin` |
| 4 | **LDA** | supervised | 0.7887 | 0.8039 | 56 | 67 | 16 | 14 | `archive/LDA.bin` |
| 5 | **NeuralNetwork** | supervised | 0.7755 | 0.7843 | 57 | 63 | 20 | 13 | `archive/NeuralNetwork.bin` |
| 6 | **LogisticRegression** | supervised | 0.7413 | 0.7582 | 53 | 63 | 20 | 17 | `archive/LogisticRegression.bin` |
| 7 | **DecisionTree** | supervised | 0.7273 | 0.7451 | 52 | 62 | 21 | 18 | `archive/DecisionTree.bin` |
| 8 | **SVM_Linear** | supervised | 0.7246 | 0.7516 | 50 | 65 | 18 | 20 | `archive/SVM_Linear.bin` |
| 9 | **KNN** | supervised | 0.7031 | 0.7516 | 45 | 70 | 13 | 25 | `archive/KNN.bin` |
| 10 | **NaiveBayes** | supervised | 0.5385 | 0.6863 | 28 | 77 | 6 | 42 | `archive/NaiveBayes.bin` |
| 11 | **OneClassSVM** | unsupervised | 0.4314 | 0.6209 | 22 | 73 | 10 | 48 | `archive/OneClassSVM.bin` |
| 12 | **IsolationForest** | unsupervised | 0.4211 | 0.6405 | 20 | 78 | 5 | 50 | `archive/IsolationForest.bin` |
| 13 | **LocalOutlierFactor** | unsupervised | 0.0811 | 0.5556 | 3 | 82 | 1 | 67 | `archive/LocalOutlierFactor.bin` |


### Metrics Breakdown
![Top 6 Confusion Matrices](confusion_matrices_top6.png)

### Training Behavior
![NN Loss Curve](neural_network_loss.png)
