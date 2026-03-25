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

## Robustness Model 2: BanglaBERT + FGM on BanglaSarc3 Binary
- Model: csebuetnlp/banglabert + FGM
- Dataset: banglasarc3_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Epsilon: 0.5
- Output dir: 03_models/checkpoints/banglabert_fgm_banglasarc3_binary
- Results:
  - Validation Accuracy: 0.7731
  - Validation Precision (binary): 0.7639
  - Validation Recall (binary): 0.7905
  - Validation F1 (binary): 0.7770
  - Validation Macro-F1: 0.7730
  - Test Accuracy: 0.7456
  - Test Precision (binary): 0.7329
  - Test Recall (binary): 0.7731
  - Test F1 (binary): 0.7524
  - Test Macro-F1: 0.7454
- Notes:
  - FGM improved over the plain BanglaBERT baseline on BanglaSarc3-binary.
  - This supports adversarial fine-tuning as a generally useful robustness method across Bengali sarcasm datasets.


## Confusion-Aware Model 1: Weighted BanglaBERT on BanglaSarc3 Ternary
- Model: csebuetnlp/banglabert + weighted loss
- Dataset: banglasarc3_ternary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Class weights: [1.15, 1.00, 1.00]
- Output dir: 03_models/checkpoints/banglabert_weighted_banglasarc3_ternary
- Results:
  - Validation Accuracy: 0.6562
  - Validation Macro-F1: 0.6577
  - Validation Weighted-F1: 0.6578
  - Test Accuracy: 0.6523
  - Test Macro-F1: 0.6529
  - Test Weighted-F1: 0.6530
- Notes:
  - Weighted confusion-aware training improved over the plain ternary BanglaBERT baseline on test Macro-F1.
  - Non-Sarcastic remains the hardest class.


## Cross-Dataset Evaluation 1: BanglaBERT train on Ben-Sarc, test on BanglaSarc3-binary
- Model: csebuetnlp/banglabert
- Source dataset: ben_sarc_binary
- Target dataset: banglasarc3_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Output dir: 03_models/checkpoints/cross_ben_sarc_binary_to_banglasarc3_binary
- Results:
  - Test Accuracy: 0.6696
  - Test Precision (binary): 0.6954
  - Test Recall (binary): 0.6035
  - Test F1 (binary): 0.6462
  - Test Macro-F1: 0.6681
- Notes:
  - Cross-dataset performance is substantially lower than in-dataset performance on BanglaSarc3-binary.
  - This indicates nontrivial domain/annotation/style shift across Bengali sarcasm datasets.


## Cross-Dataset Evaluation 2: BanglaBERT train on BanglaSarc3-binary, test on Ben-Sarc
- Model: csebuetnlp/banglabert
- Source dataset: banglasarc3_binary
- Target dataset: ben_sarc_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Output dir: 03_models/checkpoints/cross_banglasarc3_binary_to_ben_sarc_binary
- Results:
  - Test Accuracy: 0.6853
  - Test Precision (binary): 0.6745
  - Test Recall (binary): 0.7161
  - Test F1 (binary): 0.6947
  - Test Macro-F1: 0.6850
- Notes:
  - Reverse cross-dataset transfer also shows a substantial generalization drop compared with in-dataset evaluation.
  - Ben-Sarc appears harder as a target domain than BanglaSarc3-binary.

  ## Cross-Dataset Evaluation 3: BanglaBERT + FGM train on BanglaSarc3-binary, test on Ben-Sarc
- Model: csebuetnlp/banglabert + FGM
- Source dataset: banglasarc3_binary
- Target dataset: ben_sarc_binary
- Max length: 128
- Epochs: 2
- Batch size: 8
- Learning rate: 2e-5
- Epsilon: 0.5
- Output dir: 03_models/checkpoints/cross_fgm_banglasarc3_binary_to_ben_sarc_binary
- Results:
  - Validation Accuracy: 0.7743
  - Validation Macro-F1: 0.7743
  - Test Accuracy: 0.6591
  - Test Precision (binary): 0.6340
  - Test Recall (binary): 0.7527
  - Test F1 (binary): 0.6883
  - Test Macro-F1: 0.6561
- Notes:
  - FGM improved in-domain validation on the source dataset but reduced cross-dataset performance on the harder transfer direction.
  - This suggests adversarial robustness and cross-domain generalization are not the same.