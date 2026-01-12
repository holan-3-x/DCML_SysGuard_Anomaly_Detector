# 🏆 Anomaly Detection Leaderboard

![Model Comparison](model_comparison_f1.png)

| Rank | Model | Type | F1-Score | Accuracy | TP | TN | FP | FN | File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇 | **RandomForest** | supervised | 0.8571 | 0.8609 | 63 | 67 | 12 | 9 | `archive/RandomForest.bin` |
| 🥈 | **GradientBoosting** | supervised | 0.8252 | 0.8344 | 59 | 67 | 12 | 13 | `archive/GradientBoosting.bin` |
| 🥉 | **SVM_RBF** | supervised | 0.7500 | 0.7748 | 51 | 66 | 13 | 21 | `archive/SVM_RBF.bin` |
| 4 | **KNN** | supervised | 0.7402 | 0.7815 | 47 | 71 | 8 | 25 | `archive/KNN.bin` |
| 5 | **NeuralNetwork** | supervised | 0.7200 | 0.7219 | 54 | 55 | 24 | 18 | `archive/NeuralNetwork.bin` |
| 6 | **SVM_Linear** | supervised | 0.6957 | 0.7219 | 48 | 61 | 18 | 24 | `archive/SVM_Linear.bin` |
| 7 | **LogisticRegression** | supervised | 0.6906 | 0.7152 | 48 | 60 | 19 | 24 | `archive/LogisticRegression.bin` |
| 8 | **LDA** | supervised | 0.6718 | 0.7152 | 44 | 64 | 15 | 28 | `archive/LDA.bin` |
| 9 | **DecisionTree** | supervised | 0.6525 | 0.6755 | 46 | 56 | 23 | 26 | `archive/DecisionTree.bin` |
| 10 | **NaiveBayes** | supervised | 0.6387 | 0.7152 | 38 | 70 | 9 | 34 | `archive/NaiveBayes.bin` |
| 11 | **OneClassSVM** | unsupervised | 0.5517 | 0.6556 | 32 | 67 | 12 | 40 | `archive/OneClassSVM.bin` |
| 12 | **IsolationForest** | unsupervised | 0.5091 | 0.6424 | 28 | 69 | 10 | 44 | `archive/IsolationForest.bin` |
| 13 | **LocalOutlierFactor** | unsupervised | 0.2326 | 0.5629 | 10 | 75 | 4 | 62 | `archive/LocalOutlierFactor.bin` |


### Metrics Breakdown
![Top 6 Confusion Matrices](confusion_matrices_top6.png)

### Training Behavior
![NN Loss Curve](neural_network_loss.png)
