# Experiment Log — Bengali Sarcasm Detection Thesis

Project: **Robust Bengali Sarcasm Detection**  
Owner: **Sefayet Alam**  
Repo root: `Thesis_Papers/Sarcasm_detection`  

This log follows the notebook workflow used in the thesis and records the main experimental decisions, outputs, and takeaways. The thesis is organized around three evidence blocks:

1. **Strong binary baselines**
2. **Robustness via adversarial fine-tuning (FGM)**
3. **Ambiguity-aware ternary modeling + cross-dataset evaluation**

---

## Dataset setup and common protocol

### Datasets used
- **Ben-Sarc** — binary sarcasm detection, 25,636 rows
- **BanglaSarc** — binary sarcasm detection, 5,112 rows
- **BanglaSarc3** — binary + ternary sarcasm detection, 12,072 cleaned rows  
  - 17 missing-text rows dropped during cleaning

### Common transformer setup
Unless otherwise stated:
- Model backbone: `csebuetnlp/banglabert`
- Max length: `128`
- Epochs: `2`
- Batch size: `8`
- Learning rate: `2e-5`

### General interpretation preserved across experiments
- BanglaBERT is the correct transformer backbone baseline for this thesis.
- FGM helps **in-domain robustness and calibration**, but is **not** a universal cross-domain generalization fix.
- Weighted/confusion-aware ternary training is useful for BanglaSarc3.
- Cross-dataset evaluation is one of the strongest contributions of the thesis.
- Ben-Sarc is the harder target domain; BanglaSarc is the easiest binary dataset in this setup.

---

# Notebook-aligned experiment history

## 00_dataset_audit.ipynb
### Purpose
- Inspect raw files
- Verify schemas
- Confirm label columns and row counts

### Outcome
- Established the usable raw datasets for binary and ternary sarcasm detection
- Confirmed that BanglaSarc3 required cleaning before modeling

### Decision
- Proceed to a standardized cleaned representation for all datasets

---

## 01_clean_and_standardize.ipynb
### Purpose
- Create standardized clean dataset copies
- Normalize column structure for later experiments

### Outcome
- BanglaSarc3 cleaned to **12,072 rows**
- **17 missing-text rows dropped**

### Decision
- Use standardized cleaned files as the source for split generation and all downstream modeling

---

## 03_build_splits.ipynb
### Purpose
- Build fixed train/validation/test splits for the experiments

### Outcome
- Established reproducible saved splits used by the baseline and transformer pipelines

### Decision
- Keep split definitions fixed across model families to ensure fair comparison

---

## 04_baseline_ml.ipynb

### EXP-B1 — TF-IDF + Logistic Regression on Ben-Sarc Binary
- Dataset: `Ben-Sarc Binary`
- Features: `TF-IDF (1,2)-grams`
- Model: `Logistic Regression`
- Train/Val/Test: fixed saved split
- Random state: `42`

#### Results
- Validation Accuracy: **0.6427**
- Validation Macro-F1: **0.6427**
- Test Accuracy: **0.6646**
- Test Macro-F1: **0.6646**

#### Takeaway
- First classical baseline completed successfully
- Ben-Sarc appears relatively hard under sparse lexical features

---

### EXP-B2 — TF-IDF + Logistic Regression on all binary datasets
- Datasets:
  - `ben_sarc_binary`
  - `banglasarc_binary`
  - `banglasarc3_binary`
- Features: `TF-IDF (1,2)-grams`
- Model: `Logistic Regression`
- Random state: `42`
- Output file: `04_outputs/tables/baseline_ml_results.csv`

#### Results
- **BanglaSarc3-binary**
  - Validation Accuracy: **0.6708**
  - Validation Macro-F1: **0.6705**
  - Test Accuracy: **0.6708**
  - Test Macro-F1: **0.6707**

- **BanglaSarc**
  - Validation Accuracy: **0.8963**
  - Validation Macro-F1: **0.8873**
  - Test Accuracy: **0.8887**
  - Test Macro-F1: **0.8806**

- **Ben-Sarc**
  - Validation Accuracy: **0.6427**
  - Validation Macro-F1: **0.6427**
  - Test Accuracy: **0.6646**
  - Test Macro-F1: **0.6646**

#### Takeaway
- BanglaSarc is the easiest binary dataset for the classical baseline
- Ben-Sarc is the hardest binary dataset in this setup
- These results form the classical baseline table for the thesis

### Next decision
- Move to contextual transformer modeling because TF-IDF performance is clearly limited, especially on the harder datasets

---

## 05_transformer_baseline.ipynb / 05_transformer_baseline_upd.ipynb

### EXP-T1 — BanglaBERT on Ben-Sarc Binary
- Model: `csebuetnlp/banglabert`
- Dataset: `ben_sarc_binary`
- Best model metric: `macro_f1`
- Output dir: `03_models/checkpoints/banglabert_ben_sarc_baseline`

#### Results
- Validation Accuracy: **0.8030**
- Validation Precision (binary): **0.8312**
- Validation Recall (binary): **0.7605**
- Validation F1 (binary): **0.7943**
- Validation Macro-F1: **0.8027**
- Test Accuracy: **0.7910**
- Test Precision (binary): **0.8336**
- Test Recall (binary): **0.7270**
- Test F1 (binary): **0.7767**
- Test Macro-F1: **0.7901**

#### Notes
- Training completed successfully
- Post-training `trainer.evaluate()` had a callback-state issue, so final test metrics were computed using `trainer.predict(test_ds)`

#### Comparison vs TF-IDF
- Ben-Sarc Macro-F1 improvement over TF-IDF: **+0.1255** using the notebook-specific values above
- Thesis master comparison rounds this to the broader summary result where BanglaBERT clearly beats TF-IDF on Ben-Sarc

#### Takeaway
- BanglaBERT strongly outperforms the classical baseline on Ben-Sarc
- Transformer modeling is the correct main baseline direction

---

### EXP-T2 — BanglaBERT binary baselines across all binary datasets
- Output summary file: `04_outputs/tables/banglabert_binary_summary.csv`

#### Test summary used in thesis master comparison
- **Ben-Sarc**
  - Accuracy: **0.7964**
  - Macro-F1: **0.7957**
  - Binary F1: **0.7839**

- **BanglaSarc**
  - Accuracy: **0.9766**
  - Macro-F1: **0.9751**
  - Binary F1: **0.9689**

- **BanglaSarc3-binary**
  - Accuracy: **0.7357**
  - Macro-F1: **0.7353**
  - Binary F1: **0.7452**

#### Takeaway
- BanglaBERT beats TF-IDF on all tested binary datasets
- BanglaSarc remains easiest
- Ben-Sarc remains hardest
- BanglaSarc3-binary is clearly harder than BanglaSarc and supports the need for robustness/ambiguity analysis

---

## 05b_baseline_comparison.ipynb

### EXP-C1 — TF-IDF vs BanglaBERT comparison table
- Input files:
  - `04_outputs/tables/baseline_ml_results.csv`
  - `04_outputs/tables/banglabert_binary_summary.csv`
- Output files:
  - `04_outputs/tables/baseline_model_comparison_long.csv`
  - `04_outputs/tables/baseline_model_comparison_macro_f1.csv`

#### Main binary gains that matter
- **Ben-Sarc: BanglaBERT vs TF-IDF**
  - Macro-F1 gain: **+0.1311**
- **BanglaSarc: BanglaBERT vs TF-IDF**
  - Macro-F1 gain: **+0.0944**
- **BanglaSarc3-binary: BanglaBERT vs TF-IDF**
  - Macro-F1 gain: **+0.0646**

#### Takeaway
- The baseline comparison is complete and supports BanglaBERT as the correct backbone for the rest of the thesis

### Next decision
- Move beyond binary classification and test ambiguity-aware ternary modeling on BanglaSarc3

---

## 05c_ternary_transformer_baseline.ipynb

### EXP-T3 — BanglaBERT on BanglaSarc3 Ternary
- Model: `csebuetnlp/banglabert`
- Dataset: `banglasarc3_ternary`
- Output dir: `03_models/checkpoints/banglabert_banglasarc3_ternary`

#### Results
- Validation Accuracy: **0.6736**
- Validation Macro-F1: **0.6729**
- Validation Weighted-F1: **0.6730**
- Test Accuracy: **0.6416**
- Test Macro-F1: **0.6413**
- Test Weighted-F1: **0.6414**

#### Notes
- Ternary classification is substantially harder than binary classification
- Best class performance is on **Sarcastic**
- Weakest class performance is on **Non-Sarcastic**

#### Takeaway
- BanglaSarc3 ternary confirms the ambiguity challenge and motivates confusion-aware training

---

## 06_fgm_training.ipynb / 06b / 06c

### EXP-R1 — BanglaBERT + FGM on Ben-Sarc Binary
- Model: `csebuetnlp/banglabert + FGM`
- Dataset: `ben_sarc_binary`
- Epsilon: `0.5`
- Output dir: `03_models/checkpoints/banglabert_fgm_ben_sarc_binary`

#### Results
- Validation Accuracy: **0.8038**
- Validation Precision (binary): **0.8041**
- Validation Recall (binary): **0.8034**
- Validation F1 (binary): **0.8037**
- Validation Macro-F1: **0.8038**
- Test Accuracy: **0.8097**
- Test Precision (binary): **0.8212**
- Test Recall (binary): **0.7917**
- Test F1 (binary): **0.8062**
- Test Macro-F1: **0.8096**

#### Comparison vs plain BanglaBERT
- Macro-F1 gain on Ben-Sarc: **+0.0139**

#### Takeaway
- FGM improves in-domain performance on Ben-Sarc
- Adversarial fine-tuning is a useful robustness method in-domain

---

### EXP-R2 — BanglaBERT + FGM on BanglaSarc3 Binary
- Model: `csebuetnlp/banglabert + FGM`
- Dataset: `banglasarc3_binary`
- Epsilon: `0.5`
- Output dir: `03_models/checkpoints/banglabert_fgm_banglasarc3_binary`

#### Results
- Validation Accuracy: **0.7731**
- Validation Precision (binary): **0.7639**
- Validation Recall (binary): **0.7905**
- Validation F1 (binary): **0.7770**
- Validation Macro-F1: **0.7730**
- Test Accuracy: **0.7456**
- Test Precision (binary): **0.7329**
- Test Recall (binary): **0.7731**
- Test F1 (binary): **0.7524**
- Test Macro-F1: **0.7454**

#### Comparison vs plain BanglaBERT
- Macro-F1 gain on BanglaSarc3-binary: **+0.0102**

#### Takeaway
- FGM also improves in-domain performance on BanglaSarc3-binary
- This strengthens the in-domain robustness story

---

## 07_confusion_aware_training.ipynb / 07a

### EXP-A1 — Weighted BanglaBERT on BanglaSarc3 Ternary
- Model: `csebuetnlp/banglabert + weighted loss`
- Dataset: `banglasarc3_ternary`
- Class weights: `[1.15, 1.00, 1.00]`
- Output dir: `03_models/checkpoints/banglabert_weighted_banglasarc3_ternary`

#### Results
- Validation Accuracy: **0.6562**
- Validation Macro-F1: **0.6577**
- Validation Weighted-F1: **0.6578**
- Test Accuracy: **0.6523**
- Test Macro-F1: **0.6529**
- Test Weighted-F1: **0.6530**

#### Comparison vs plain ternary BanglaBERT
- Test Macro-F1 gain: **+0.0116**

#### Notes
- Weighted confusion-aware training improves over the plain ternary baseline
- **Non-Sarcastic** remains the hardest class

#### Takeaway
- Ambiguity-aware training improves ternary BanglaSarc3 performance and should be retained in the thesis narrative

---

## 08_cross_dataset_eval.ipynb / reverse / 08a / 08b

### EXP-X1 — Cross-dataset: train on Ben-Sarc, test on BanglaSarc3-binary
- Model: `csebuetnlp/banglabert`
- Source dataset: `ben_sarc_binary`
- Target dataset: `banglasarc3_binary`
- Output dir: `03_models/checkpoints/cross_ben_sarc_binary_to_banglasarc3_binary`

#### Results
- Test Accuracy: **0.6696**
- Test Precision (binary): **0.6954**
- Test Recall (binary): **0.6035**
- Test F1 (binary): **0.6462**
- Test Macro-F1: **0.6681**

#### Comparison vs target in-domain score
- BanglaSarc3-binary in-domain Macro-F1: **0.7353**
- Cross-domain gap: **0.0672**

#### Takeaway
- Cross-dataset performance is meaningfully lower than in-dataset performance
- There is clear domain / annotation / style shift across Bengali sarcasm datasets

---

### EXP-X2 — Cross-dataset: train on BanglaSarc3-binary, test on Ben-Sarc
- Model: `csebuetnlp/banglabert`
- Source dataset: `banglasarc3_binary`
- Target dataset: `ben_sarc_binary`
- Output dir: `03_models/checkpoints/cross_banglasarc3_binary_to_ben_sarc_binary`

#### Results
- Test Accuracy: **0.6853**
- Test Precision (binary): **0.6745**
- Test Recall (binary): **0.7161**
- Test F1 (binary): **0.6947**
- Test Macro-F1: **0.6850**

#### Comparison vs target in-domain score
- Ben-Sarc in-domain Macro-F1: **0.7957**
- Cross-domain gap: **0.1108**

#### Takeaway
- Reverse transfer also drops sharply
- Ben-Sarc is the harder target domain

---

### EXP-X3 — Cross-dataset FGM: train on BanglaSarc3-binary, test on Ben-Sarc
- Model: `csebuetnlp/banglabert + FGM`
- Source dataset: `banglasarc3_binary`
- Target dataset: `ben_sarc_binary`
- Epsilon: `0.5`
- Output dir: `03_models/checkpoints/cross_fgm_banglasarc3_binary_to_ben_sarc_binary`

#### Results
- Validation Accuracy: **0.7743**
- Validation Macro-F1: **0.7743**
- Test Accuracy: **0.6591**
- Test Precision (binary): **0.6340**
- Test Recall (binary): **0.7527**
- Test F1 (binary): **0.6883**
- Test Macro-F1: **0.6561**

#### Comparison vs plain cross-dataset model
- Plain BS3 -> Ben-Sarc Macro-F1: **0.6850**
- FGM BS3 -> Ben-Sarc Macro-F1: **0.6561**
- Effect: **-0.0288**

#### Takeaway
- FGM improves in-domain robustness but does **not** improve the harder cross-dataset transfer direction
- This negative result is important and should be kept

---

## 09_calibration_and_ablation.ipynb / 09b_calibration_binary.ipynb

### EXP-K1 — Binary calibration analysis
#### Calibration results
- **Ben-Sarc**
  - BanglaBERT
    - Brier: **0.1687**
    - ECE: **0.1352**
  - BanglaBERT + FGM
    - Brier: **0.1381**
    - ECE: **0.0464**

- **BanglaSarc3-binary**
  - BanglaBERT
    - Brier: **0.1906**
    - ECE: **0.1319**
  - BanglaBERT + FGM
    - Brier: **0.1694**
    - ECE: **0.0524**

#### Takeaway
- FGM improves not only in-domain classification, but also **confidence quality**
- This is one of the strongest thesis contributions because it moves beyond raw accuracy/F1

### Decision
- Preserve calibration as a core thesis result, not a side note

---

## 10a_binary_error_analysis.ipynb

### EXP-E1 — Binary error analysis
#### Error reductions
- **Ben-Sarc**
  - Plain errors: **522**
  - FGM errors: **488**
  - Reduction: **34 fewer errors**

- **BanglaSarc3-binary**
  - Plain errors: **208**
  - FGM errors: **204**
  - Reduction: **4 fewer errors**

#### Takeaway
- In-domain FGM reduces actual prediction errors, not just metrics on paper

---

## 10b_ternary_error_analysis.ipynb

### EXP-E2 — Ternary error analysis
#### Error comparison
- **BanglaSarc3 ternary**
  - Plain baseline errors: **433**
  - Weighted-model errors: **420**
  - Effect: **13 fewer errors**

#### Takeaway
- The weighted/confusion-aware model reduces ternary errors and supports the ambiguity-aware modeling claim

---

## 10c_cross_dataset_error_analysis.ipynb

### EXP-E3 — Cross-dataset error analysis
#### Error comparison
- **Cross-dataset BS3 -> Ben-Sarc**
  - Plain baseline errors: **807**
  - Cross-dataset FGM errors: **874**
  - Effect: **67 more errors**

#### Takeaway
- Cross-dataset FGM can worsen generalization errors
- This reinforces the conclusion that adversarial robustness and cross-domain generalization are not the same

---

# Final thesis-level findings

## Binary in-domain
- BanglaBERT consistently outperforms TF-IDF across all tested binary datasets
- BanglaSarc is easiest
- Ben-Sarc is hardest
- FGM improves in-domain binary Macro-F1 on both tested binary datasets

## Ternary ambiguity-aware modeling
- BanglaSarc3 ternary is clearly harder than binary classification
- Weighted/confusion-aware training improves ternary Macro-F1 over the plain BanglaBERT baseline

## Cross-dataset generalization
- Cross-dataset performance is substantially weaker than in-dataset performance
- Ben-Sarc is the harder target domain
- FGM does not improve the harder cross-dataset transfer direction

## Calibration
- FGM improves Brier score and ECE on both tested binary datasets
- Robustness should therefore be framed in terms of both classification quality and confidence quality

---

# Final interpretation to preserve in the paper/thesis

This thesis studies **robust Bengali sarcasm detection** under both in-domain and cross-domain settings. Across binary datasets, contextual transformer models consistently outperform sparse lexical baselines. Adversarial fine-tuning with FGM further improves in-domain Macro-F1 and substantially improves calibration, indicating stronger confidence quality. For ambiguity-aware sarcasm detection, weighted/confusion-aware ternary training on BanglaSarc3 improves over a plain ternary BanglaBERT baseline. However, cross-dataset transfer remains substantially weaker than in-dataset testing, showing that dataset shift is a major challenge in Bengali sarcasm detection.

A key conclusion is that **robustness is multi-dimensional**: a method may improve in-domain performance and calibration while still failing to improve cross-domain generalization. Future Bengali sarcasm detection work should therefore evaluate not only within-dataset accuracy, but also confidence quality and cross-dataset transfer.

---

# Suggested repo follow-up

Before finalizing the repo:
- keep this log synchronized with final output CSVs in `04_outputs/tables`
- add experiment IDs to any thesis tables for easier cross-reference
- make sure notebook names and this log use the same final filenames
- preserve the negative cross-dataset FGM result rather than hiding it