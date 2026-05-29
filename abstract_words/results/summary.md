# Model Comparison

## Applied Filters

The filtered executions apply the following dataset cleaning rules:

* Remove ambiguous words using the concreteness standard deviation (`Conc.SD < 1.2`)
* Keep only highly recognized words (`Percent_known >= 0.9`)

---

# Results Without Filters

| Embeddings             | ML Model     | MAE    | R²     | Accuracy | Precision | Recall | F1 Score |
| ---------------------- | ------------ | ------ | ------ | -------- | --------- | ------ | -------- |
| spaCy `en_core_web_md` | RandomForest | 0.5795 | 0.4826 | 0.7752   | 0.7421    | 0.7629 | 0.7523   |
| spaCy `en_core_web_md` | XGBoost      | 0.5623 | 0.5162 | 0.7772   | 0.7443    | 0.8016 | 0.7719   |
| FastText               | XGBoost      | 0.3631 | 0.7849 | 0.8656   | 0.8374    | 0.8602 | 0.8487   |
| MPNet                  | XGBoost      | 0.4045 | 0.7383 | 0.8473   | 0.7990    | 0.8803 | 0.8377   |

---

# Results With Filters

| Embeddings             | ML Model     | MAE    | R²     | Accuracy | Precision | Recall | F1 Score |
| ---------------------- | ------------ | ------ | ------ | -------- | --------- | ------ | -------- |
| spaCy `en_core_web_md` | RandomForest | 0.5337 | 0.6617 | 0.8729   | 0.8559    | 0.8896 | 0.8724   |
| spaCy `en_core_web_md` | XGBoost      | 0.5037 | 0.6889 | 0.8839   | 0.8694    | 0.9107 | 0.8896   |
| FastText               | XGBoost      | 0.3087 | 0.8934 | 0.9586   | 0.9493    | 0.9609 | 0.9551   |
| MPNet                  | XGBoost      | 0.3635 | 0.8488 | 0.9319   | 0.8988    | 0.9697 | 0.9329   |

---
