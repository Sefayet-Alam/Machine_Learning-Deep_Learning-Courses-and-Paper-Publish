## Baseline 1: TF-IDF + Logistic Regression on Ben-Sarc Binary
- Dataset: Ben-Sarc Binary
- Features: TF-IDF (1,2)-grams
- Model: Logistic Regression
- Train/Val/Test split: fixed saved split
- Random state: 42
- Results:
  - Validation Accuracy: 0.6427
  - Validation Macro-F1: 0.6427
  - Test Accuracy: 0.6646
  - Test Macro-F1: 0.6646
- Notes:
  - First classical ML baseline completed successfully.
  - Ben-Sarc appears harder than the other Bengali datasets under TF-IDF + Logistic Regression.


## Baseline 2: TF-IDF + Logistic Regression on all binary datasets
- Datasets:
  - ben_sarc_binary
  - banglasarc_binary
  - banglasarc3_binary
- Features: TF-IDF (1,2)-grams
- Model: Logistic Regression
- Random state: 42
- Output file: 04_outputs/tables/baseline_ml_results.csv
- Results:
  - banglasarc3_binary
    - Validation Accuracy: 0.6708
    - Validation Macro-F1: 0.6705
    - Test Accuracy: 0.6708
    - Test Macro-F1: 0.6707
  - banglasarc_binary
    - Validation Accuracy: 0.8963
    - Validation Macro-F1: 0.8873
    - Test Accuracy: 0.8887
    - Test Macro-F1: 0.8806
  - ben_sarc_binary
    - Validation Accuracy: 0.6427
    - Validation Macro-F1: 0.6427
    - Test Accuracy: 0.6646
    - Test Macro-F1: 0.6646
- Notes:
  - BanglaSarc is easiest for the TF-IDF baseline.
  - Ben-Sarc is the hardest among the three in this setup.
  - These results form the classical baseline table for the thesis.


  ## Transformer Baseline 1: BanglaBERT on Ben-Sarc Binary
- Model: csebuetnlp/banglabert
- Dataset: ben_sarc_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Best model metric: macro_f1
- Output dir: 03_models/checkpoints/banglabert_ben_sarc_baseline
- Results:
  - Validation Accuracy: 0.8030
  - Validation Precision (binary): 0.8312
  - Validation Recall (binary): 0.7605
  - Validation F1 (binary): 0.7943
  - Validation Macro-F1: 0.8027
  - Test Accuracy: 0.7910
  - Test Precision (binary): 0.8336
  - Test Recall (binary): 0.7270
  - Test F1 (binary): 0.7767
  - Test Macro-F1: 0.7901
- Notes:
  - Training completed successfully.
  - Post-training `trainer.evaluate()` had a callback-state issue, so final test metrics were computed from `trainer.predict(test_ds)`.
  - BanglaBERT strongly outperformed the TF-IDF baseline on Ben-Sarc.

## Baseline Comparison: TF-IDF vs BanglaBERT on Binary Datasets
- Input files:
  - 04_outputs/tables/baseline_ml_results.csv
  - 04_outputs/tables/banglabert_binary_summary.csv
- Output files:
  - 04_outputs/tables/baseline_model_comparison_long.csv
  - 04_outputs/tables/baseline_model_comparison_macro_f1.csv
- Notes:
  - Combined classical and transformer baselines into unified comparison tables.
  - This table will be used in the thesis baseline results section.

## Transformer Baseline 4: BanglaBERT on BanglaSarc3 Ternary
- Model: csebuetnlp/banglabert
- Dataset: banglasarc3_ternary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Output dir: 03_models/checkpoints/banglabert_banglasarc3_ternary
- Results:
  - Validation Accuracy: 0.6736
  - Validation Macro-F1: 0.6729
  - Validation Weighted-F1: 0.6730
  - Test Accuracy: 0.6416
  - Test Macro-F1: 0.6413
  - Test Weighted-F1: 0.6414
- Notes:
  - Ternary classification is substantially harder than binary classification.
  - Best class performance is on Sarcastic, weakest on Non-Sarcastic.
  - This supports the ambiguity/confusion-aware direction of the thesis.

## Robustness Model 1: BanglaBERT + FGM on Ben-Sarc Binary
- Model: csebuetnlp/banglabert + FGM
- Dataset: ben_sarc_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Epsilon: 0.5
- Output dir: 03_models/checkpoints/banglabert_fgm_ben_sarc_binary
- Results:
  - Validation Accuracy: 0.8038
  - Validation Precision (binary): 0.8041
  - Validation Recall (binary): 0.8034
  - Validation F1 (binary): 0.8037
  - Validation Macro-F1: 0.8038
  - Test Accuracy: 0.8097
  - Test Precision (binary): 0.8212
  - Test Recall (binary): 0.7917
  - Test F1 (binary): 0.8062
  - Test Macro-F1: 0.8096
- Notes:
  - FGM improved over the plain BanglaBERT baseline on Ben-Sarc.
  - This supports adversarial fine-tuning as a useful robustness strategy for Bengali sarcasm detection.