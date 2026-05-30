# Model Comparison

## Applied Filters

The filtered executions apply the following dataset cleaning rules:

* Remove ambiguous words using the concreteness standard deviation (`Conc.SD < 1.5`)

---

# Results Without Filters

| Embeddings             | ML Model     | MAE    | R²     | Accuracy | Precision | Recall | F1 Score |
| ---------------------- | ------------ | ------ | ------ | -------- | --------- | ------ | -------- |
| spaCy `en_core_web_md` | RandomForest | 0.5795 | 0.4826 | 0.7752   | 0.7421    | 0.7629 | 0.7523   |
| spaCy `en_core_web_md` | XGBoost      | 0.5623 | 0.5162 | 0.7772   | 0.7443    | 0.8016 | 0.7719   |
| FastText               | XGBoost      | 0.3631 | 0.7849 | 0.8656   | 0.8374    | 0.8602 | 0.8487   |
| MPNet                  | XGBoost      | 0.4045 | 0.7383 | 0.8473   | 0.7990    | 0.8803 | 0.8377   |

---

# Results with Training Filter (Conc.SD < 1.5)

| Embeddings | ML Model | MAE | R² | Accuracy | Precision | Recall | F1 Score |
|------------|----------|------|------|----------|-----------|--------|----------|
| spaCy `en_core_web_md` | RandomForest | 0.5792 | 0.4738 | 0.7767 | 0.7422 | 0.7679 | 0.7548 |
| spaCy `en_core_web_md` | XGBoost | 0.5621 | 0.5081 | 0.7772 | 0.7431 | 0.8042 | 0.7725 |
| FastText | XGBoost | 0.3621 | 0.7850 | 0.8661 | 0.8380 | 0.8606 | 0.8491 |
| MPNet | XGBoost | 0.4044 | 0.7363 | 0.8457 | 0.7940 | 0.8848 | 0.8369 |

---