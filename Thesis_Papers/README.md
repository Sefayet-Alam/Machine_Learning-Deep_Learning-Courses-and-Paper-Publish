# Intensive 7-Day Dual-Paper Plan

**Goal for this week:** make serious progress on **both papers**:

1. **Thesis paper:** multimodal sarcasm detection based on cue learning / CLIP-style multimodal modeling, with proper model development and updated experiments.
2. **Second paper:** Bangla cyberbullying detection with strong ML/DL baselines and a submission-ready first draft.

By the end of 7 days, the target is:

- working **ML/DL models** for both papers
- **first submissionable drafts** for both papers (not final, but serious)
- solid understanding of the **required topics only**

---

## Final strategy

Because your thesis teacher wants a **proper sarcasm-detection model like the one in the paper, with improvements**, this week should be split into **two active tracks every day**:

### Track A — Thesis paper (highest priority)
**Topic:** Multimodal sarcasm detection based on cue learning / CLIP-style multimodal modeling

### Track B — Second paper
**Topic:** Bangla cyberbullying detection using strong classical + transformer baselines

This is an **intensive** plan, not a light one. It assumes you can give the week fully.

---

# What success looks like by Day 7

## Paper 1 — Thesis sarcasm paper
You should have:
- a working multimodal pipeline
- at least 2-3 baselines
- one improved model direction over a simple baseline
- ablation/error analysis
- first full draft of the paper
- clear understanding of CLIP, multimodal fusion, cue learning, prompt tuning, and evaluation

## Paper 2 — Cyberbullying paper
You should have:
- cleaned Bangla dataset
- classical ML baselines
- transformer baseline
- comparison table
- error analysis
- first full draft of the paper
- clear understanding of text classification workflow for Bangla

---

# Tools / stack to use

## For sarcasm paper
- Python
- PyTorch
- Hugging Face Transformers
- CLIP / OpenCLIP
- scikit-learn
- pandas, numpy, matplotlib

## For cyberbullying paper
- Python
- scikit-learn
- Hugging Face Transformers
- pandas, numpy, matplotlib

---

# Main paper ideas

## Paper 1 (thesis)
**Working title:**
**Multimodal Sarcasm Detection with Cue Learning: Reproduction, Adaptation, and Low-Resource Extensions**

Possible contribution this week:
- reproduce a simplified version of the cue-learning idea
- compare text-only vs image-only vs multimodal
- compare simple CLIP fusion vs prompt/cue-enhanced version
- provide error analysis and limitations
- optionally add small Bangla/Banglish pilot ideas in the discussion section

## Paper 2
**Working title:**
**Bangla Cyberbullying Detection using Classical ML and Transformer Baselines**

Possible contribution this week:
- benchmark strong baselines on Bangla data
- compare classical vs transformer models
- analyze failure cases and label ambiguity

---

# 7-Day Intensive Plan

## Day 01 — Build foundations for both papers

### To read

#### For thesis sarcasm paper
1. Reference paper:
   - [A multi-modal sarcasm detection model based on cue learning](https://www.nature.com/articles/s41598-025-94266-w.pdf)
2. Multimodal sarcasm dataset quality / benchmark awareness:
   - [MMSD2.0 paper](https://aclanthology.org/2023.findings-acl.689/)
   - [MMSD2.0 repository](https://github.com/joeying1019/mmsd2.0)
   - [MMSD3.0](https://arxiv.org/abs/2510.23299)
3. CLIP basics:
   - [OpenAI CLIP repository](https://github.com/openai/CLIP)

#### For cyberbullying paper
1. Bangla cyberbullying dataset paper:
   - [Bengali cyberbullying detection dataset](https://www.sciencedirect.com/science/article/pii/S2352340925009266)
2. Dataset sources:
   - [Mendeley dataset](https://data.mendeley.com/datasets/sz5558wrd4/2)
   - [Kaggle Bangla cyberbullying dataset](https://www.kaggle.com/datasets/moshiurrahmanfaisal/bangla-cyber-bullying-dataset)

#### For both papers
1. Transformer basics:
   - [Hugging Face NLP course](https://huggingface.co/learn/llm-course/en/chapter1/2)
   - [How transformers work](https://huggingface.co/learn/llm-course/en/chapter1/4)
2. Classification metrics:
   - [Google ML Crash Course - Classification](https://developers.google.com/machine-learning/crash-course/classification)
   - [Accuracy, Precision, Recall](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)

### To watch
1. [NLP intro](https://youtu.be/fLvJ8VdHLA0?si=QgK5-wWPDIvVBS9o)
2. [Tokenization](https://youtu.be/YdreZtH8oWk?si=XnwgJUBV9BCRomva)
3. [Vector Embedding short](https://youtube.com/shorts/FJtFZwbvkI4?si=_9O9ZUEK5bF_9eHE)
4. [Vector Embedding explained](https://youtu.be/dN0lsF2cvm4?si=f9oNtbwSHmsMJLSN)

### To do
1. Make two project folders:
   - `sarcasm_thesis/`
   - `bangla_cyberbullying/`
2. Create note files for both papers with these headings:
   - problem
   - dataset
   - model
   - baselines
   - evaluation
   - limitations
   - possible contributions
3. Decide the exact target of each paper.
4. Set up Python environment and install core libraries.

### Code to implement
- Create starter notebooks/scripts for both projects.
- Implement a common evaluation function for:
  - accuracy
  - precision
  - recall
  - macro F1
  - weighted F1
  - confusion matrix

### Expected outcomes
- clear problem statements for both papers
- environment ready
- starter codebase for both
- solid understanding of the main concepts

---

## Day 02 — Data pipeline and baseline setup

### To read

#### Thesis sarcasm paper
1. Read the experiment section of the cue-learning paper carefully.
2. Read CLIP usage examples:
   - [OpenAI CLIP repository](https://github.com/openai/CLIP)
3. Read prompt tuning basics:
   - [Hugging Face PEFT Prompt Tuning](https://huggingface.co/docs/peft/main/en/package_reference/prompt_tuning)
   - [Prompting / soft prompt concepts](https://huggingface.co/docs/peft/main/en/conceptual_guides/prompting)

#### Cyberbullying paper
1. Inspect the chosen Bangla dataset paper and label structure.

### To watch
1. [CampusX 100 Days ML playlist](https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH)
   - watch only relevant videos for:
     - train/test split
     - text preprocessing
     - metrics
     - model evaluation
2. [FreeCodeCamp Data Science video](https://www.youtube.com/watch?v=r-uOLxNrNk8)
   - only the practical parts relevant to preprocessing / workflow

### To do

#### Thesis sarcasm paper
1. Download and inspect the sarcasm dataset you will use first.
   - Prefer a benchmark like MMSD2.0 or a reliable multimodal sarcasm dataset.
2. Understand the format:
   - text field
   - image path / image id
   - label
3. Decide your first baselines:
   - text-only baseline
   - image-only baseline
   - simple multimodal baseline

#### Cyberbullying paper
1. Choose the Bangla cyberbullying dataset.
2. Clean the dataset:
   - remove duplicates
   - remove missing rows
   - inspect label balance
3. Decide binary vs multiclass setup.
   - Recommended: start with **binary**, then extend if time remains.

### Code to implement

#### Thesis sarcasm paper
- dataset loader for text + image
- sample visualization / inspection script
- train/validation/test split

#### Cyberbullying paper
- dataset loader
- preprocessing pipeline
- train/validation/test split
- save processed CSV files

### Expected outcomes
- usable datasets ready for both projects
- clear baseline plan for both
- no ambiguity about data format

---

## Day 03 — Strong classical baselines + simple multimodal baseline

### To read
1. Revisit metrics and error analysis notes:
   - [Google Classification module](https://developers.google.com/machine-learning/crash-course/classification)

### To watch
#### For cyberbullying paper
1. [Naive Bayes](https://youtu.be/8vv9julkQEA?si=yE7_boraLqzaWoZH)
2. [Decision Tree Implementation](https://youtu.be/PHxYNGo8NcI?si=lldNKJKZaZGZQx6D)
3. [Random Forest Basics](https://youtu.be/gkXX4h3qYm4?si=bkULumqFr7zUQObx)
4. [Random Forest Implementation](https://youtu.be/ok2s1vV9XW0?si=XjXDX7PjKUW_M_ex)
5. [SVM Basics](https://youtu.be/NDqACjz5j8g?si=niJ3vNsVK_PaUnhL)
6. [SVM Implementation](https://youtu.be/FB5EdxAGxQg?si=Tye3KLmUG99Em5tF)

### To do

#### Cyberbullying paper
Train and compare:
- TF-IDF + Logistic Regression
- TF-IDF + Naive Bayes
- TF-IDF + SVM
- TF-IDF + Random Forest

#### Thesis sarcasm paper
Build the first simple multimodal baseline:
- text embedding + image embedding
- concatenate features
- small classifier on top

Also create two weaker baselines:
- text-only
- image-only

### Code to implement

#### Cyberbullying paper
- full classical baseline training loop
- metric table export
- confusion matrix plotting

#### Thesis sarcasm paper
- CLIP embedding extraction for text and image
- feature concatenation
- MLP / logistic regression classifier on top
- evaluation script

### Expected outcomes
- strong classical baseline for cyberbullying
- first working multimodal sarcasm baseline
- text-only / image-only comparison started

---

## Day 04 — Deep learning day for both papers

### To read
1. [Transformers - what can they do?](https://huggingface.co/learn/llm-course/chapter1/3)
2. [How transformers work](https://huggingface.co/learn/llm-course/en/chapter1/4)
3. For multimodal understanding:
   - [A multimodal world](https://huggingface.co/learn/computer-vision-course/en/unit4/multimodal-models/a_multimodal_world)

### To watch
1. [RNN explained](https://youtu.be/AsNTP8Kwu80?si=HSkM9MOoSNQlpbNT)
2. [RNN implementation](https://youtu.be/0_PgWWmauHk?si=xC67ecbKAze2FD13)
3. [LSTM](https://youtu.be/b61DPVFX03I?si=2R83brFKALCbcBLZ)

Watch these lightly for background only. Do **not** spend the whole day here.

### To do

#### Cyberbullying paper
Train at least one transformer model:
- multilingual BERT, XLM-R, or Bangla-specific transformer if quickly available

#### Thesis sarcasm paper
Train at least one better multimodal model:
- CLIP-based classifier with trainable top layer
- compare frozen CLIP features vs partially trainable classifier head

Also document:
- training settings
- learning rate
- batch size
- epoch count
- early stopping / validation strategy

### Code to implement

#### Cyberbullying paper
- tokenizer
- transformer fine-tuning pipeline
- validation loop
- checkpoint saving

#### Thesis sarcasm paper
- CLIP feature pipeline
- training script for multimodal classifier head
- evaluation across text-only, image-only, multimodal

### Expected outcomes
- transformer baseline for cyberbullying
- stronger multimodal sarcasm model than Day 3 baseline
- model comparison tables growing for both papers

---

## Day 05 — Cue learning / prompt-inspired improvement + paper drafting starts seriously

### To read
1. Re-read the cue-learning paper carefully:
   - [Cue learning paper PDF](https://www.nature.com/articles/s41598-025-94266-w.pdf)
2. Prompt tuning docs:
   - [Prompt tuning](https://huggingface.co/docs/peft/main/en/package_reference/prompt_tuning)
   - [Soft prompting concepts](https://huggingface.co/docs/peft/main/en/conceptual_guides/prompting)

### To watch
1. [Interested in something like this](https://youtu.be/JgnbwKnHMZQ?si=VGkSGGG79Fq4R88F)
2. [Video 1](https://youtu.be/5HQCNAsSO-s?si=pzWjxyfnoiplFPse)
3. [Video 2](https://youtu.be/4YGkfAd2iXM?si=_RFMwVQvnLreFPbg)

### To do

#### Thesis sarcasm paper
This is the key day.

Implement an **improved model** inspired by the paper. It does not need to be a perfect replica, but it must be a real upgrade over the simple baseline.

Possible realistic improvements:
- prompt-like textual cues for sarcasm / non-sarcasm classes
- handcrafted sarcasm cue templates
- similarity-based selection of prompt candidates
- multiple text prompts and ensemble scores
- class-specific learned vectors on top of CLIP text embeddings

Minimum target:
- simple baseline
- improved cue/prompt-inspired version
- comparison table

#### Cyberbullying paper
Start writing the paper seriously:
- Abstract
- Introduction
- Related Work
- Dataset
- Methods

Also finalize the best model shortlist:
- best classical
- best transformer

### Code to implement

#### Thesis sarcasm paper
- prompt / cue template code
- class prompt generation
- cosine similarity-based scoring or selection
- comparison with the previous baseline

#### Cyberbullying paper
- final training rerun for best models if needed
- export predictions
- save result tables

### Expected outcomes
- thesis work now has a **proper improved model direction**
- cyberbullying paper draft is half written
- both projects now have real experiments, not just ideas

---

## Day 06 — Ablations, error analysis, and full drafts

### To read
1. [ACL reproducibility / reporting checklist](https://aclanthology.org/attachments/2025.findings-emnlp.1404.checklist.pdf)
2. [Weights & Biases quickstart](https://docs.wandb.ai/get-started)

### To do

#### Thesis sarcasm paper
Run ablations such as:
- text-only vs image-only vs multimodal
- simple CLIP fusion vs cue/prompt-enhanced version
- different numbers of prompt templates if possible
- frozen features vs trainable classifier head

Perform error analysis:
- where image helps
- where text alone is enough
- where sarcasm is culturally dependent
- label ambiguity cases

Start writing full draft:
- Abstract
- Introduction
- Related Work
- Method
- Dataset
- Experiments
- Initial Results

#### Cyberbullying paper
Run final analysis:
- best classical vs best transformer
- preprocessing vs no preprocessing
- class weighting if relevant
- binary vs multiclass if feasible

Write remaining sections:
- Results
- Error Analysis
- Limitations
- Conclusion

### Code to implement

#### Thesis sarcasm paper
- ablation experiment loop
- error analysis export
- result table generation

#### Cyberbullying paper
- final comparison table
- confusion matrix figure
- misclassification export

### Expected outcomes
- thesis paper has real ablation results
- cyberbullying paper has a nearly complete draft
- both have serious result sections

---

## Day 07 — Finalize both first-submission drafts and package deliverables

### To read
1. Re-read your own drafts.
2. Re-check the reproducibility checklist:
   - [ACL checklist](https://aclanthology.org/attachments/2025.findings-emnlp.1404.checklist.pdf)

### To do

#### Thesis sarcasm paper
Finalize the first submissionable draft in this order:
1. Title
2. Abstract
3. Introduction
4. Related Work
5. Methodology
6. Experimental Setup
7. Results
8. Ablation Study
9. Error Analysis
10. Limitations
11. Conclusion

Also prepare:
- final result tables
- model comparison chart
- architecture diagram if possible
- future work note for Bangla/Banglish extension

#### Cyberbullying paper
Finalize the first submissionable draft:
1. Title
2. Abstract
3. Introduction
4. Related Work
5. Dataset
6. Methods
7. Experiments
8. Results
9. Error Analysis
10. Limitations
11. Conclusion

Also package the repo / folder:
- `README.md`
- `requirements.txt`
- cleaned notebooks
- trained model checkpoints
- figures
- results CSV files

### Code to implement
- final rerun if any key result is missing
- save best models
- save plots
- save prediction files
- clean training scripts

### Expected outcomes
By the end of Day 7, you should have:

#### Thesis sarcasm paper
- working multimodal model
- improved cue/prompt-inspired version
- multiple baseline comparisons
- ablation and error analysis
- first submissionable draft
- strong conceptual understanding of the paper and related topics

#### Cyberbullying paper
- cleaned dataset and full pipeline
- classical ML baselines
- transformer baseline
- comparison tables
- error analysis
- first submissionable draft
- strong conceptual understanding of Bangla text classification workflow

---

# Topic checklist — what you must understand this week

## For sarcasm thesis paper
- sarcasm as incongruity
- multimodal learning basics
- CLIP
- text/image shared embedding space
- feature fusion
- prompt tuning / cue learning intuition
- cosine similarity
- few-shot / low-resource thinking
- ablations and error analysis

## For cyberbullying paper
- text classification pipeline
- Bangla text preprocessing
- TF-IDF
- logistic regression / SVM / Naive Bayes / Random Forest
- transformer fine-tuning
- class imbalance
- precision / recall / F1
- confusion matrix
- error analysis

---

# Minimum model targets by the end of the week

## Thesis sarcasm paper
You should aim to have at least:
1. text-only baseline
2. image-only baseline
3. simple multimodal baseline
4. improved cue/prompt-inspired multimodal model

## Cyberbullying paper
You should aim to have at least:
1. TF-IDF + Logistic Regression
2. TF-IDF + SVM
3. TF-IDF + Naive Bayes
4. one transformer model

---

# Writing targets by the end of the week

## Thesis sarcasm paper
Draft must include:
- motivation
- paper summary vs your extension
- method details
- dataset description
- experiment settings
- results and ablations
- error analysis
- limitations and future work

## Cyberbullying paper
Draft must include:
- motivation for Bangla cyberbullying detection
- dataset description
- baseline comparison
- transformer model results
- error analysis
- limitations

---

# What not to do this week

Do **not** waste time on:
- completing all ML playlists end-to-end
- advanced theory not needed for implementation
- building a huge new Bangla sarcasm dataset from scratch
- trying too many models without documenting results
- rewriting code repeatedly without saving experiments

---

# Final note

This revised plan is intentionally aggressive because you said you can fully use the week. The best use of that time is:

- **morning / first half:** thesis sarcasm model and reading
- **second half:** cyberbullying model and writing
- **night / final block:** documentation, tables, figures, and paper drafting

The thesis paper now gets **full implementation priority**, not just background reading.

