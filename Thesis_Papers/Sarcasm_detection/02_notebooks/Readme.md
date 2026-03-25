# 02_notebooks


#### Thesis name: Robust Bengali Sarcasm Detection with Confusion-Aware Adversarial Fine-Tuning and Cross-Dataset Evaluation 

This folder contains the experiment notebooks for the thesis on **robust Bengali sarcasm detection**.

The overall research direction has three main pillars:

1. **Strong binary baselines**  
   Compare classical ML and transformer models on multiple Bengali sarcasm datasets.

2. **Robustness via adversarial fine-tuning (FGM)**  
   Test whether adversarial training improves in-domain classification and confidence quality.

3. **Ambiguity-aware modeling and transfer analysis**  
   Study ternary sarcasm detection and cross-dataset generalization to understand whether high in-dataset performance really transfers.

---

## Recommended reading / execution order

1. `00_dataset_audit.ipynb`
2. `01_clean_and_standardize.ipynb`
3. `02_eda_and_bias_checks.ipynb`
4. `03_build_splits.ipynb`
5. `04_baseline_ml.ipynb`
6. `05_transformer_baseline_upd.ipynb`
7. `05b_baseline_comparison.ipynb`
8. `05c_ternary_transformer_baseline.ipynb`
9. `06_fgm_training.ipynb`
10. `06a_fgm_comparison.ipynb`
11. `06b_fgm_banglasarc3_binary.ipynb`
12. `06c_fgm_comparison.ipynb`
13. `07_confusion_aware_training.ipynb`
14. `07a_ternary_comparison.ipynb`
15. `08_cross_dataset_eval.ipynb`
16. `08_cross_dataset_eval_reverse.ipynb`
17. `08a_cross_dataset_comparison.ipynb`
18. `08b_cross_dataset_fgm.ipynb`
19. `09_calibration_and_ablation.ipynb`
20. `09b_calibration_binary.ipynb`
21. `10a_binary_error_analysis.ipynb`
22. `10b_ternary_error_analysis.ipynb`
23. `10c_cross_dataset_error_analysis.ipynb`

---

## Notebook-by-notebook summary

### `00_dataset_audit.ipynb`
**What I did in this notebook**  
Inspected the raw dataset files, checked schemas, confirmed text and label columns, and reviewed dataset sizes.

**Results (summary)**  
Verified the core datasets and their structures before any cleaning or modeling. This notebook established the starting point for all later experiments.

**What I decided to do next and why**  
Standardize the datasets into a common format so that the same downstream pipeline can be reused across datasets.

**What other options I had**  
I could have started modeling directly on the raw files, but that would have made the pipeline fragile and harder to reproduce.

---

### `01_clean_and_standardize.ipynb`
**What I did in this notebook**  
Cleaned and standardized the datasets into a consistent tabular format with unified text and label handling.

**Results (summary)**  
Created cleaned copies suitable for fixed experimental pipelines. Also handled issues such as missing text rows.

**What I decided to do next and why**  
Run EDA and bias checks to understand dataset properties before training models.

**What other options I had**  
I could have performed heavier normalization or linguistic preprocessing, but I chose a cleaner minimal pipeline compatible with transformer models.

---

### `02_eda_and_bias_checks.ipynb`
**What I did in this notebook**  
Performed exploratory analysis and basic dataset diagnostics, including class patterns and possible dataset artifacts.

**Results (summary)**  
Helped identify that the datasets differ in difficulty and likely differ in distribution, which later became important for the transfer experiments.

**What I decided to do next and why**  
Build fixed train/validation/test splits so that all models can be compared on the same evaluation protocol.

**What other options I had**  
I could have added richer lexical or stylistic analysis here, such as token overlap or sarcasm-marker frequency analysis.

---

### `03_build_splits.ipynb`
**What I did in this notebook**  
Created and saved fixed train/validation/test splits for the binary and ternary tasks.

**Results (summary)**  
Established the exact split files used in all later experiments. This made notebook-to-notebook comparisons consistent.

**What I decided to do next and why**  
Start with a classical baseline before moving to transformers, so that later gains are meaningful.

**What other options I had**  
I could have used k-fold cross-validation, but fixed splits were simpler and easier to manage across many experiments.

---

### `04_baseline_ml.ipynb`
**What I did in this notebook**  
Built TF-IDF + Logistic Regression baselines for the binary datasets.

**Results (summary)**  
Produced the classical baseline table. BanglaSarc was the easiest dataset, while Ben-Sarc was harder. These baselines became the reference point for transformer gains.

**What I decided to do next and why**  
Move to BanglaBERT because sparse lexical models were clearly limited on this task.

**What other options I had**  
I could have tested SVM, Naive Bayes, Random Forest, or character n-grams, but Logistic Regression was a strong and standard baseline.

---

### `05_transformer_baseline_upd.ipynb`
**What I did in this notebook**  
Trained and evaluated BanglaBERT on all three binary datasets in a single looped pipeline.

**Results (summary)**  
BanglaBERT outperformed TF-IDF on all tested binary datasets. The improvement was strongest on Ben-Sarc and still meaningful on BanglaSarc and BanglaSarc3-binary.

**What I decided to do next and why**  
Create a dedicated comparison notebook to summarize the baseline gains clearly.

**What other options I had**  
I could have trained each dataset in separate notebooks only, but the unified loop made the setup cleaner and more comparable.

---

### `05b_baseline_comparison.ipynb`
**What I did in this notebook**  
Compared TF-IDF and BanglaBERT across the binary datasets in one place.

**Results (summary)**  
Confirmed that BanglaBERT is the correct backbone baseline for the thesis. The transformer consistently beat the classical baseline across datasets.

**What I decided to do next and why**  
Extend the work to the ternary setting to address ambiguity and neutral cases.

**What other options I had**  
I could have stopped at binary classification, but that would miss the ambiguity challenge present in BanglaSarc3.

---

### `05c_ternary_transformer_baseline.ipynb`
**What I did in this notebook**  
Trained a 3-class BanglaBERT baseline on BanglaSarc3.

**Results (summary)**  
Built the ternary baseline and established a reference performance level before trying ambiguity-aware improvements.

**What I decided to do next and why**  
Test whether better loss design can improve ternary performance, especially around confusing classes.

**What other options I had**  
I could have reduced the task back to binary only, but the ternary setup is more realistic for ambiguous sarcasm.

---

### `06_fgm_training.ipynb`
**What I did in this notebook**  
Applied FGM-based adversarial fine-tuning to BanglaBERT for binary sarcasm detection.

**Results (summary)**  
FGM improved in-domain performance on Ben-Sarc and strengthened the robustness story beyond the plain transformer baseline.

**What I decided to do next and why**  
Create a comparison notebook so the plain-vs-FGM gains are easy to inspect and report.

**What other options I had**  
I could have used other adversarial methods such as PGD or FreeLB, but FGM was simpler and computationally cheaper.

---

### `06a_fgm_comparison.ipynb`
**What I did in this notebook**  
Compared plain BanglaBERT and BanglaBERT + FGM on the main binary setup.

**Results (summary)**  
Showed that FGM provides a measurable in-domain gain and justifies including robustness as a thesis pillar.

**What I decided to do next and why**  
Repeat the FGM test on BanglaSarc3-binary to see whether the gain is dataset-specific or more general.

**What other options I had**  
I could have focused only on a single benchmark, but validating across datasets gives a stronger claim.

---

### `06b_fgm_banglasarc3_binary.ipynb`
**What I did in this notebook**  
Applied FGM training to BanglaSarc3 in the binary setting.

**Results (summary)**  
FGM again improved the in-domain binary result, though the gain was smaller than on Ben-Sarc.

**What I decided to do next and why**  
Build a comparison notebook for BanglaSarc3-binary so the effect is easy to summarize in tables.

**What other options I had**  
I could have used different epsilon values or more extensive hyperparameter sweeps.

---

### `06c_fgm_comparison.ipynb`
**What I did in this notebook**  
Compared the plain binary BanglaBERT and FGM-enhanced BanglaBERT runs on BanglaSarc3-binary.

**Results (summary)**  
Confirmed a modest but real in-domain improvement from FGM.

**What I decided to do next and why**  
Move to ternary ambiguity-aware training, because robustness alone does not address the neutral class.

**What other options I had**  
I could have tried more adversarial variants first, but the ternary problem was more central to the thesis story.

---

### `07_confusion_aware_training.ipynb`
**What I did in this notebook**  
Trained a ternary BanglaBERT model with weighted / confusion-aware loss on BanglaSarc3.

**Results (summary)**  
Improved over the plain ternary baseline and reduced ternary classification errors, supporting the ambiguity-aware modeling claim.

**What I decided to do next and why**  
Create a direct comparison notebook to clearly show the benefit over the plain ternary model.

**What other options I had**  
I could have tried focal loss, label smoothing, or class-balanced loss instead of the chosen weighting strategy.

---

### `07a_ternary_comparison.ipynb`
**What I did in this notebook**  
Compared plain ternary BanglaBERT against the weighted/confusion-aware ternary model.

**Results (summary)**  
Showed that the weighted/confusion-aware setup performs better on BanglaSarc3, making it the preferred ternary result.

**What I decided to do next and why**  
Test cross-dataset transfer, because strong in-domain performance may still fail under dataset shift.

**What other options I had**  
I could have added more ternary baselines first, but transfer testing was the more important next question.

---

### `08_cross_dataset_eval.ipynb`
**What I did in this notebook**  
Trained on one binary dataset and tested on another to measure cross-dataset transfer.

**Results (summary)**  
Cross-dataset performance was clearly weaker than in-dataset performance. This established one of the strongest thesis findings: Bengali sarcasm models do not generalize as well as in-domain scores suggest.

**What I decided to do next and why**  
Run the reverse transfer direction to confirm that the effect is not one-sided.

**What other options I had**  
I could have stopped at a single transfer direction, but bidirectional testing provides a more credible generalization analysis.

---

### `08_cross_dataset_eval_reverse.ipynb`
**What I did in this notebook**  
Repeated the transfer experiment in the reverse direction.

**Results (summary)**  
Confirmed asymmetry in transfer difficulty and showed that Ben-Sarc is the harder target domain.

**What I decided to do next and why**  
Create a comparison notebook to summarize in-domain vs cross-domain gaps.

**What other options I had**  
I could have expanded to more source-target combinations or leave-one-dataset-out setups.

---

### `08a_cross_dataset_comparison.ipynb`
**What I did in this notebook**  
Summarized the cross-dataset results and compared them against in-domain reference scores.

**Results (summary)**  
Quantified the transfer gaps clearly, which supports the thesis claim that high in-dataset performance overestimates real robustness.

**What I decided to do next and why**  
Test whether FGM helps in the harder cross-dataset direction.

**What other options I had**  
I could have also added calibration comparisons under transfer.

---

### `08b_cross_dataset_fgm.ipynb`
**What I did in this notebook**  
Applied FGM in the harder cross-dataset transfer direction.

**Results (summary)**  
FGM did **not** improve cross-dataset generalization and actually hurt Macro-F1 in the tested harder direction. This is an important negative result.

**What I decided to do next and why**  
Preserve this result and discuss it explicitly, because it shows that in-domain robustness and cross-domain generalization are not the same thing.

**What other options I had**  
I could have tried domain adaptation, continued pretraining, or stronger regularization for transfer robustness.

---

### `09_calibration_and_ablation.ipynb`
**What I did in this notebook**  
Collected master tables / ablations and organized results for later interpretation.

**Results (summary)**  
Helped consolidate the thesis evidence and support the final narrative around robustness, ambiguity, and transfer.

**What I decided to do next and why**  
Evaluate confidence quality directly using calibration metrics.

**What other options I had**  
I could have kept all results fragmented across notebooks, but central aggregation is better for reporting.

---

### `09b_calibration_binary.ipynb`
**What I did in this notebook**  
Computed binary calibration metrics such as Brier Score and Expected Calibration Error (ECE).

**Results (summary)**  
FGM improved calibration strongly on the tested binary datasets. This is one of the most important thesis results because it shows improved confidence quality, not just improved classification scores.

**What I decided to do next and why**  
Perform qualitative error analysis to better interpret where models fail.

**What other options I had**  
I could have added calibration plots, temperature scaling, or post-hoc calibration baselines.

---

### `10a_binary_error_analysis.ipynb`
**What I did in this notebook**  
Analyzed binary mistakes made by the baseline and improved models.

**Results (summary)**  
FGM reduced the number of binary errors in-domain, especially on the harder binary setting.

**What I decided to do next and why**  
Inspect ternary errors to understand ambiguity-related failures.

**What other options I had**  
I could have produced a richer manual taxonomy of error types.

---

### `10b_ternary_error_analysis.ipynb`
**What I did in this notebook**  
Analyzed ternary errors on BanglaSarc3.

**Results (summary)**  
The improved ternary model reduced errors relative to the plain ternary baseline, supporting the ambiguity-aware modeling claim.

**What I decided to do next and why**  
Inspect transfer errors to understand why cross-dataset performance remains weak.

**What other options I had**  
I could have added class-wise qualitative examples with more annotation notes.

---

### `10c_cross_dataset_error_analysis.ipynb`
**What I did in this notebook**  
Analyzed errors in the cross-dataset setting, including the FGM transfer experiment.

**Results (summary)**  
Showed that cross-dataset FGM can increase errors, reinforcing the conclusion that robustness does not automatically transfer across domains.

**What I decided to do next and why**  
Use these findings to write the thesis discussion and final paper narrative.

**What other options I had**  
I could have expanded into deeper domain-shift analysis, such as lexical overlap and topic-shift diagnostics.

---

## Main results at a glance

### Binary in-domain
- BanglaBERT outperformed TF-IDF across all tested binary datasets.
- FGM improved in-domain Macro-F1 on the tested binary setups.
- BanglaSarc was easiest, Ben-Sarc was hardest.

### Ternary
- Plain ternary BanglaBERT established the baseline on BanglaSarc3.
- Weighted/confusion-aware training improved ternary performance.

### Cross-dataset
- Cross-dataset transfer was substantially weaker than in-domain testing.
- Ben-Sarc was the harder target domain.
- Cross-dataset FGM did not help and could hurt performance.

### Calibration
- FGM improved confidence quality as measured by Brier Score and ECE.

---

## How this folder fits the thesis

This notebook sequence supports the final thesis claim:

> Bengali sarcasm detection models can appear strong under in-dataset evaluation, but robustness is multi-dimensional.  
> A method may improve in-domain performance and calibration while still failing to improve cross-dataset generalization.

---

## Suggested future improvements

- Run multiple seeds and report mean ± std
- Add significance testing
- Compare with one or two additional transformer baselines
- Add dataset-shift diagnostics
- Expand qualitative error taxonomy
- Add a cleaner reproducibility guide for the repo

---

## Notes for reproducibility

Before re-running the notebooks:
- make sure paths are repo-relative,
- keep the split files unchanged,
- use the same random seed where intended,
- save all summary tables to `../04_outputs/tables`,
- document checkpoint names consistently in `../03_models/checkpoints`.
