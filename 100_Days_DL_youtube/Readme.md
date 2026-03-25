# 100 Days of Deep Learning (CampusX)
This README is designed to be *revision-friendly* and *interview-ready*.

**How to use (best method)**
1. Revise **3–5 videos/day**.
2. After each video section, answer both questions **out loud**.
3. If you can’t answer confidently, write a 2–3 line “gap note” and move on.
4. Before interviews: revise **losses, backprop intuition, optimization, regularization, initialization, normalization**.

---

## Notes by video (1–84)

### Video 1 — Course Announcement
**What to remember**
- Course map: ANN → CNN → RNN/LSTM/GRU → Seq2Seq/Attention → Transformers.
- What you should build along the way: small ANN projects, CNN classifier, sequence model, transformer intuition.

**Interview Questions (with answers)**
**Q1. How would you structure a deep learning learning-plan to avoid “tutorial hell”?**  
Use a cycle: (1) concept video → (2) implement minimal version → (3) debug shape/metric issues → (4) small project → (5) write learnings. The key is *tight feedback loops*: every concept must translate to a runnable model and a measurable metric.

**Q2. What’s the fastest way to detect whether you truly understood a DL topic?**  
Try to explain it as: inputs/outputs, the equation (or core operation), where gradients flow, and one failure mode. If you can’t state the failure mode (e.g., vanishing gradients for sigmoid stacks), understanding is shallow.

---

### Video 2 — What is Deep Learning? DL vs ML
**What to remember**
- DL = representation learning with neural networks (often many layers).
- DL shines on unstructured data (images/audio/text) + large data + compute.
- Classical ML still wins often on small/medium tabular problems.

**Interview Questions (with answers)**
**Q1. What does “representation learning” mean in deep learning?**  
Instead of manually crafting features, the model learns intermediate features automatically (edges → textures → parts in vision, or subword → syntax/semantics in NLP). These representations make downstream prediction easier.

**Q2. What’s a practical rule-of-thumb for choosing DL vs classical ML?**  
If the data is mostly tabular with limited samples, start with boosted trees/logistic regression. If inputs are high-dimensional and unstructured, or you can leverage pretraining/transfer learning, DL is usually the better path.

---

### Video 3 — Types of Neural Networks + History + Applications
**What to remember**
- ANN/MLP: general-purpose function approximators.
- CNN: locality + translation invariance for grid-like data.
- RNN/LSTM/GRU: sequence modeling with temporal dependencies.
- Transformers: attention-based sequence modeling, parallelizable.

**Interview Questions (with answers)**
**Q1. Why did CNNs become dominant for vision compared to plain MLPs?**  
CNNs exploit spatial structure via convolution (local receptive fields) and parameter sharing, reducing parameters and improving generalization. MLPs ignore spatial locality and become huge for images.

**Q2. Name one “fit-for-purpose” reason to pick RNNs over Transformers (today).**  
For very small models on strict latency/memory constraints, a compact GRU/LSTM can be cheaper. Transformers often need more memory due to attention (especially for long sequences).

---

### Video 4 — Perceptron: Intuition + Geometry
**What to remember**
- Perceptron = linear classifier: sign(w·x + b).
- Decision boundary is a hyperplane; works only for linearly separable data.
- Geometric view: w is normal to the separating hyperplane.

**Interview Questions (with answers)**
**Q1. What is the geometric meaning of the weights vector `w` in a perceptron?**  
`w` defines the direction perpendicular (normal) to the decision boundary. Moving along `w` increases the score `w·x + b`, so classification depends on which side of the hyperplane the point lies.

**Q2. Why does perceptron fail on XOR even though it’s “simple”?**  
XOR is not linearly separable: no single line/hyperplane can separate the classes. You need at least one hidden layer (nonlinear feature transformation) to make it separable.

---

### Video 5 — Perceptron Trick + Training
**What to remember**
- Update rule intuition: move boundary toward misclassified points.
- If y ∈ {+1, −1}: when misclassified, w ← w + yx, b ← b + y.
- Converges only if data is linearly separable (classic perceptron convergence).

**Interview Questions (with answers)**
**Q1. What does a perceptron update do to the margin of a misclassified example?**  
It increases the score for the true class by nudging `w` toward `y*x`. This shifts/rotates the hyperplane so that the misclassified point moves closer to the correct side.

**Q2. What’s the key assumption behind perceptron convergence guarantees?**  
Linear separability with a positive margin. If classes overlap or are noisy, perceptron may oscillate and not converge to a stable separator.

---

### Video 6 — Perceptron Loss: Hinge, BCE, Sigmoid
**What to remember**
- Perceptron uses hard threshold; modern training uses smooth losses.
- Hinge loss (SVM-like): max(0, 1 − y·score).
- BCE with sigmoid for probabilistic binary classification.

**Interview Questions (with answers)**
**Q1. Why is sigmoid + BCE preferred over a hard threshold loss?**  
Hard threshold is non-differentiable (no useful gradient). Sigmoid+BCE provides smooth gradients that enable gradient descent, and outputs interpretable probabilities.

**Q2. When does hinge loss behave differently from BCE in practice?**  
Hinge focuses on *margin*: once correctly classified with enough margin, loss becomes zero. BCE keeps penalizing based on probability calibration, pushing confident predictions closer to 0/1.

---

### Video 7 — Problem with Perceptron
**What to remember**
- Linearity limitation + non-differentiability issues with step activation.
- Single-layer can’t model complex decision boundaries.
- Leads to multi-layer networks + differentiable activations.

**Interview Questions (with answers)**
**Q1. What specifically breaks gradient-based learning in the original perceptron?**  
The step function has zero gradient almost everywhere and is undefined at the threshold. Backprop can’t propagate meaningful gradients through it.

**Q2. If data is almost linearly separable, why still prefer logistic regression over perceptron?**  
Logistic regression gives probabilities, is trained with a convex loss (BCE), is more stable with noise, and supports calibrated decisions and threshold tuning.

---

### Video 8 — MLP Notation
**What to remember**
- Layers, neurons, weights matrices, bias vectors, activations.
- Shapes matter: (batch, features) → (batch, hidden) → (batch, output).
- Clear naming prevents implementation bugs.

**Interview Questions (with answers)**
**Q1. In matrix form, why do we prefer `Z = XW + b` instead of looping samples?**  
Vectorization is faster (BLAS/GPU), simpler to reason about shapes, and aligns with autodiff frameworks. It also reduces code-level bugs from indexing mistakes.

**Q2. What’s the most common shape bug in beginner MLP implementations?**  
Bias broadcasting mismatch and transposed weight matrices (confusing whether `W` is (in, out) or (out, in)). Fix by writing shapes next to every tensor in notes.

---

### Video 9 — Multi Layer Perceptron (MLP) Intuition
**What to remember**
- Hidden layers learn nonlinear features via activations.
- Universal approximation (in theory) but depth helps efficiency.
- Capacity vs generalization trade-off.

**Interview Questions (with answers)**
**Q1. Why does adding a hidden layer increase expressive power?**  
Because non-linear activation composes linear transforms into non-linear functions, enabling curved decision boundaries and feature interactions that a single hyperplane can’t capture.

**Q2. “Universal approximation” doesn’t mean “easy to train”—why?**  
It’s an existence claim, not an optimization guarantee. Training depends on gradients, initialization, conditioning, and data; the network may still get stuck or generalize poorly.

---

### Video 10 — Forward Propagation
**What to remember**
- Forward pass: compute activations layer by layer.
- Store intermediate values (Z, A) for backprop.
- Output layer depends on task: sigmoid (binary), softmax (multi-class), linear (regression).

**Interview Questions (with answers)**
**Q1. Why do we store intermediate activations during forward pass?**  
Backprop needs them to compute gradients using the chain rule. Without cached `A`/`Z`, you’d recompute forward repeatedly or lose information needed for derivatives.

**Q2. What’s a clean way to decide the final-layer activation?**  
Match it to the target distribution: probabilities → sigmoid/softmax; real-valued unbounded → linear; bounded regression → scaled sigmoid/tanh.

---

### Video 11 — Customer Churn Prediction using ANN (Keras)
**What to remember**
- Typical pipeline: preprocessing → train/val split → baseline → ANN.
- Handle categorical vars (one-hot/embeddings), scaling numeric features.
- Watch class imbalance; pick appropriate metrics.

**Interview Questions (with answers)**
**Q1. In churn (imbalanced) classification, why can accuracy be misleading?**  
If 90% are non-churn, predicting “non-churn” always gives 90% accuracy but zero business value. Use PR-AUC/F1/recall at a chosen precision, plus cost-based thresholds.

**Q2. What’s a strong baseline before building an ANN for churn?**  
Logistic regression or gradient boosting with proper preprocessing and calibration. If ANN can’t beat a tuned baseline, complexity isn’t justified.

---

### Video 12 — MNIST Digit Classification using ANN
**What to remember**
- Flattened pixels + MLP works but ignores spatial structure.
- Overfitting risk; need regularization (dropout/L2) and good validation.
- CNNs typically outperform MLPs on images.

**Interview Questions (with answers)**
**Q1. Why does an ANN on flattened MNIST underperform a CNN?**  
Flattening destroys locality: nearby pixels that form edges/strokes aren’t treated specially. CNN kernels explicitly learn local patterns and reuse them across the image.

**Q2. If you must use an MLP for MNIST, what’s the first improvement you try?**  
Normalize inputs, add dropout/L2, use ReLU, and tune width/depth modestly. Also ensure learning rate scheduling and early stopping.

---

### Video 13 — Graduate Admission Prediction using ANN
**What to remember**
- Tabular regression/classification style problem; scaling crucial.
- Small data → overfitting risk; simpler models often competitive.
- Evaluate with MAE/RMSE (regression) and calibration if probabilistic.

**Interview Questions (with answers)**
**Q1. Why is feature scaling especially important in neural nets on tabular data?**  
Unscaled features create uneven gradient magnitudes, slowing training and making optimization unstable. Scaling improves conditioning and helps the optimizer take consistent steps.

**Q2. When is a neural net a poor choice for admissions prediction?**  
When data is small and interpretability is required. Linear/GBM models can be more stable, easier to explain, and may generalize better with limited samples.

---

### Video 14 — Loss Functions in Deep Learning
**What to remember**
- Loss = training objective; must match task and output activation.
- Classification: BCE/CE; regression: MSE/MAE/Huber.
- Add regularization terms (L2) or task-specific losses.

**Interview Questions (with answers)**
**Q1. Why can MAE be harder to optimize than MSE with gradient descent?**  
MAE has a constant-magnitude gradient (and non-differentiable at zero), which can make convergence less smooth. MSE provides gradients proportional to error, giving stronger signal for large mistakes.

**Q2. When is Huber loss a good compromise?**  
When you want MSE-like sensitivity near zero but robustness to outliers. Huber is quadratic for small errors and linear for large errors.

---

### Video 15 — Backpropagation Part 1 (The What)
**What to remember**
- Backprop = efficient gradient computation using chain rule.
- Computes ∂Loss/∂params for all layers in O(number of edges).
- Enables gradient-based optimization of deep nets.

**Interview Questions (with answers)**
**Q1. What problem does backprop solve compared to naive differentiation?**  
Naive differentiation recomputes shared sub-expressions repeatedly. Backprop reuses intermediate derivatives (dynamic programming), making gradient computation efficient and scalable.

**Q2. What does it mean that backprop is “not an optimizer”?**  
Backprop only computes gradients. The optimizer (SGD/Adam) uses those gradients to update parameters. Confusing these leads to wrong explanations in interviews.

---

### Video 16 — Backprop Part 2 (The How)
**What to remember**
- Local gradients multiply along paths (chain rule).
- For each layer: compute dZ, dW, db using cached activations.
- Correct shape handling is critical.

**Interview Questions (with answers)**
**Q1. In a dense layer, why is `dW = A_prev^T · dZ`?**  
Because Z = A_prev W + b. Each weight connects an input activation to an output pre-activation. Matrix calculus yields the outer-product accumulation across the batch.

**Q2. What’s a practical debugging trick for backprop implementations?**  
Gradient checking: compare analytical gradients with numerical finite-difference approximations on a tiny model/batch. Large mismatch usually indicates sign/shape errors.

---

### Video 17 — Backprop Part 3 (The Why)
**What to remember**
- Why gradients can vanish/explode: repeated multiplication by small/large Jacobians.
- Activation choice + initialization affects gradient flow.
- Depth increases optimization difficulty without good design.

**Interview Questions (with answers)**
**Q1. Why do sigmoids often cause vanishing gradients in deep networks?**  
Sigmoid saturates for large |x|, making derivative near 0. Multiplying many near-zero derivatives across layers collapses gradients, so early layers learn extremely slowly.

**Q2. Why did ReLU help deep learning “take off” historically?**  
ReLU avoids saturation for positive inputs (derivative ~1), improving gradient flow and enabling deeper nets to train faster with simpler initialization strategies.

---

### Video 18 — MLP Memoization
**What to remember**
- Store forward-pass intermediates to reuse in backward pass.
- Trades memory for speed (common in deep learning).
- Frameworks use computation graphs + autograd caches.

**Interview Questions (with answers)**
**Q1. What’s the memory–compute trade-off in training deep nets?**  
Caching activations speeds backprop but uses memory. To reduce memory, you can recompute some activations (checkpointing) at the cost of extra compute.

**Q2. Why is this especially relevant on GPUs?**  
GPU memory is limited; large batch sizes or big models can OOM. Smart caching/checkpointing lets you train larger models without changing the math.

---

### Video 19 — Gradient Descent in Neural Nets (Batch vs SGD vs Mini-batch)
**What to remember**
- Batch GD: stable but slow per step.
- SGD: noisy but can escape shallow minima; high variance.
- Mini-batch: best practical trade-off; leverages GPU parallelism.

**Interview Questions (with answers)**
**Q1. Why can SGD generalize better than full-batch GD sometimes?**  
Noise acts like implicit regularization, preventing sharp minima and improving robustness. Mini-batch noise helps explore parameter space more than deterministic full-batch updates.

**Q2. How do you choose batch size pragmatically?**  
Pick the largest that fits GPU memory while keeping good throughput, then tune learning rate accordingly. Extremely large batches may need LR scaling/warmup and can hurt generalization.

---

### Video 20 — Vanishing & Exploding Gradients (Code Example)
**What to remember**
- Deep chains of multiplications can shrink/blow up gradients.
- Fixes: ReLU-family, better initialization (Xavier/He), normalization, residuals, gradient clipping.

**Interview Questions (with answers)**
**Q1. Why does poor initialization contribute to exploding gradients?**  
If weights are too large, activations and derivatives grow layer by layer. The gradient magnitude then increases exponentially with depth, causing unstable updates and divergence.

**Q2. When is gradient clipping the right tool?**  
Mostly for sequence models (RNN/LSTM) where occasional large gradients occur. Clipping prevents rare spikes from destabilizing training while still allowing learning.

---

### Video 21 — How to Improve Neural Network Performance
**What to remember**
- Levers: data quality/quantity, architecture, regularization, optimization, and evaluation protocol.
- Biggest wins often come from data + correct splits + baseline comparisons.
- Monitor training curves to diagnose bias vs variance.

**Interview Questions (with answers)**
**Q1. If your model underfits, what are the first two fixes you try?**  
Increase capacity (more units/layers) and reduce regularization. Also ensure features/inputs are sufficient; underfitting can be caused by overly aggressive dropout/L2.

**Q2. If your model overfits, what’s the most reliable improvement?**  
More data (or augmentation), plus regularization (dropout/L2) and early stopping. Also simplify architecture and ensure validation is truly representative.

---

### Video 22 — Early Stopping
**What to remember**
- Stop training when validation loss stops improving (patience).
- Prevents overfitting and saves compute.
- Works best with a clean validation set.

**Interview Questions (with answers)**
**Q1. Why is early stopping considered a form of regularization?**  
It limits effective model complexity by preventing weights from fully fitting noise. It’s similar to restricting how far optimization travels toward a potentially overfit solution.

**Q2. What’s a common mistake when using early stopping?**  
Tuning hyperparameters repeatedly on the same validation set without a final test set, causing validation leakage (overfitting to the val split itself).

---

### Video 23 — Data Scaling in Neural Networks
**What to remember**
- Scaling improves optimization conditioning and training stability.
- Standardization (zero mean, unit variance) is common for MLPs.
- Fit scaler on train only; apply to val/test.

**Interview Questions (with answers)**
**Q1. Why does scaling change the “shape” of the loss landscape?**  
It reduces anisotropy: gradients aren’t dominated by large-scale features. This makes level sets more circular, letting gradient descent move efficiently toward minima.

**Q2. When might you avoid standardization?**  
If features are already in meaningful bounded ranges or model expects raw scales (rare). More common: you still normalize but choose robust scaling for heavy-tailed distributions.

---

### Video 24 — Dropout Layer (Concept)
**What to remember**
- Dropout randomly zeroes activations during training → reduces co-adaptation.
- Acts like training an ensemble of subnetworks.
- Typically disabled at inference (use full network).

**Interview Questions (with answers)**
**Q1. Why does dropout often help generalization?**  
It forces redundancy: neurons can’t rely on specific other neurons always being present. This reduces brittle feature dependencies and improves robustness to noise.

**Q2. Where is dropout usually a bad idea?**  
Right before the output in regression can destabilize predictions; also in some modern CNN/Transformer setups where normalization + residuals + data augmentation already regularize well.

---

### Video 25 — Dropout (Code Example: Regression & Classification)
**What to remember**
- Dropout rate controls strength (e.g., 0.1–0.5 common).
- Too much dropout → underfitting.
- Monitor train-vs-val gap to set dropout.

**Interview Questions (with answers)**
**Q1. How do you detect “too much dropout” from learning curves?**  
Training loss stays high and doesn’t decrease much; validation loss is similar (small gap) but also high. That indicates regularization is preventing the model from fitting even the training signal.

**Q2. Why must dropout behavior differ between training and inference?**  
During training, randomness regularizes. During inference, you want deterministic predictions using the expected activations (either via scaling during training or equivalent at inference).

---

### Video 26 — Regularization (L1, L2, Weight Decay)
**What to remember**
- L2 penalizes large weights → smoother solutions, better generalization.
- L1 encourages sparsity (feature selection-like behavior).
- Weight decay in optimizers is often the practical way to apply L2.

**Interview Questions (with answers)**
**Q1. How does L2 regularization reduce overfitting intuitively?**  
It discourages complex, high-magnitude parameter configurations that can fit noise. Smaller weights generally produce smoother functions with less sensitivity to small input changes.

**Q2. Why is “weight decay” sometimes not identical to “L2 regularization” in Adam?**  
In adaptive optimizers, naive L2 added to gradients interacts with per-parameter learning rates. Decoupled weight decay (AdamW) applies decay directly to weights, matching the intended regularization behavior.

---

### Video 27 — Activation Functions (Sigmoid, Tanh, ReLU)
**What to remember**
- Sigmoid: probabilities but saturates → vanishing gradients.
- Tanh: zero-centered but can still saturate.
- ReLU: sparse activations, better gradient flow; risk of dead neurons.

**Interview Questions (with answers)**
**Q1. Why is tanh often preferred over sigmoid in hidden layers (historically)?**  
Tanh is zero-centered, which makes optimization easier because gradients don’t push biases in one direction as strongly as sigmoid (which outputs strictly positive values).

**Q2. What causes “dying ReLU,” and how do you mitigate it?**  
If many pre-activations become negative, gradient becomes zero and neuron stops updating. Mitigate with smaller learning rates, better initialization (He), and ReLU variants like Leaky ReLU.

---

### Video 28 — ReLU Variants (Leaky, PReLU, ELU, SELU)
**What to remember**
- Leaky ReLU: small slope for negative region → fewer dead neurons.
- PReLU: learnable negative slope.
- ELU/SELU: smoother negative region; SELU supports self-normalizing networks (with constraints).

**Interview Questions (with answers)**
**Q1. When would you choose Leaky ReLU over standard ReLU?**  
When training is unstable or you observe many dead activations (lots of zeros). Leaky ReLU keeps gradient alive for negative inputs, improving learning in early stages.

**Q2. What’s the key idea behind SELU being “self-normalizing”?**  
Under specific conditions (activation + initialization + architecture constraints), activations tend to maintain mean ~0 and variance ~1 across layers, reducing the need for explicit normalization—though it’s not universally applicable.

---

# Readme_part2 — 100 Days of Deep Learning (CampusX)
Covers Videos **29 → 56** (Initialization → BatchNorm → Optimizers → CNN Core → CNN Backprop → Augmentation/Pretraining/Transfer → Functional API → RNN Intro)

---

## Video 29 — Weight Initialization Techniques | What not to do?
**What to remember**
- Bad init (all zeros / same constant) ⇒ symmetry problem: neurons learn identical features.
- Very large weights ⇒ exploding activations/gradients; very small ⇒ vanishing.
- Goal: keep activation variance and gradient variance stable across layers.

**Interview Questions (with answers)**
**Q1. Why is initializing all weights to zero a problem in a multilayer network but not in linear regression?**  
In multi-layer nets, zero initialization makes all neurons in a layer identical (same outputs, same gradients), so they keep learning the same feature forever (symmetry never breaks). Linear regression has no hidden units needing diverse features, so symmetry isn’t an issue.

**Q2. What’s a practical “sanity check” to detect bad initialization early?**  
Look at the first few forward passes: if activations are all near 0 (dead) or extremely large (blowing up), training loss won’t decrease properly. Also inspect gradient norms—if they’re ~0 or huge from step 1, initialization is likely wrong.

---

## Video 30 — Xavier/Glorot and He Weight Initialization
**What to remember**
- Xavier/Glorot: good for tanh/sigmoid-ish activations (keeps variance stable).
- He init: designed for ReLU-family (accounts for half activations zeroed).
- Key idea: scale weights based on fan_in (and sometimes fan_out).

**Interview Questions (with answers)**
**Q1. Why does He initialization typically use a larger variance than Xavier?**  
ReLU zeros out roughly half the inputs (negative side), reducing activation variance. He compensates by using a larger scaling so the remaining active units maintain stable variance through depth.

**Q2. If you switch from ReLU to tanh but keep He init, what can happen?**  
Tanh saturates more easily if activations become too large, so He’s larger variance may push tanh into saturation → smaller gradients → slower learning. Using Xavier reduces that risk.

---

## Video 31 — Batch Normalization in Deep Learning | Batch Layer in Keras
**What to remember**
- BN normalizes activations using batch mean/variance, then applies learnable scale (γ) and shift (β).
- Helps optimization: smoother loss landscape, allows higher learning rate, improves stability.
- During inference, BN uses running (moving) averages, not batch statistics.

**Interview Questions (with answers)**
**Q1. Why do BN layers behave differently in training vs inference?**  
Training uses current mini-batch mean/variance (stochastic). Inference must be deterministic and stable, so it uses running estimates accumulated during training to normalize inputs consistently.

**Q2. Where do you usually place BatchNorm relative to activation (and why)?**  
Common pattern: Linear/Conv → BatchNorm → Activation. BN normalizes pre-activation signals, then activation applies nonlinearity to a more controlled distribution, improving gradient flow.

---

## Video 32 — Optimizers in Deep Learning | Part 1
**What to remember**
- Optimizer = rule to update parameters using gradients.
- Plain SGD: θ ← θ − η∇L
- Practical concerns: learning rate choice dominates; scheduling often necessary.

**Interview Questions (with answers)**
**Q1. What’s the single most important hyperparameter across most optimizers?**  
Learning rate. Even advanced optimizers fail with a bad LR; a well-chosen LR + schedule can make simple SGD competitive.

**Q2. Why can an optimizer converge to a “bad” solution even if training loss decreases smoothly?**  
It might settle into sharp minima or exploit shortcuts that don’t generalize. Also, data leakage or metric mismatch can make loss reduction irrelevant to the real objective.

---

## Video 33 — Exponentially Weighted Moving Average (EWMA)
**What to remember**
- EWMA tracks a smoothed estimate: v_t = βv_{t−1} + (1−β)g_t
- β close to 1 ⇒ smoother but slower to react.
- Used in momentum/Adam to reduce gradient noise.

**Interview Questions (with answers)**
**Q1. What does β control in EWMA and how do you interpret it intuitively?**  
β controls “memory.” Higher β means the estimate remembers older gradients longer (strong smoothing), while lower β reacts quickly but is noisier.

**Q2. Why does EWMA help on mini-batch training?**  
Mini-batch gradients are noisy. EWMA dampens noise, providing a more consistent direction for updates and improving convergence stability.

---

## Video 34 — SGD with Momentum
**What to remember**
- Momentum accumulates velocity: v ← βv + (1−β)g ; θ ← θ − ηv
- Speeds up in consistent directions, damps oscillations.
- Especially helpful in ravines / ill-conditioned surfaces.

**Interview Questions (with answers)**
**Q1. In what geometry does momentum help the most?**  
In narrow valleys (steep curvature in one direction, shallow in another). Momentum reduces zig-zag across steep walls and accelerates along the shallow direction.

**Q2. How would you explain momentum to a non-technical interviewer?**  
It’s like pushing a heavy ball downhill: it gains speed in the correct direction and doesn’t get thrown off course by small bumps (noisy gradients).

---

## Video 35 — Nesterov Accelerated Gradient (NAG)
**What to remember**
- NAG “looks ahead” using the momentum step before computing gradient.
- Often more responsive than classic momentum.
- Intuition: corrects course sooner by evaluating gradient at anticipated position.

**Interview Questions (with answers)**
**Q1. What is the key difference between classical momentum and Nesterov momentum?**  
Classical momentum uses gradient at current parameters. Nesterov computes gradient after a tentative look-ahead step, which can reduce overshooting and improve stability.

**Q2. When might NAG be preferable in practice?**  
When momentum overshoots minima or oscillates near optimum. NAG’s look-ahead can provide earlier correction and slightly faster convergence.

---

## Video 36 — AdaGrad
**What to remember**
- Adapts learning rate per parameter using accumulated squared gradients.
- Good for sparse features (rarely-updated parameters get larger steps).
- Downside: learning rates can decay too much over time (stalling).

**Interview Questions (with answers)**
**Q1. Why is AdaGrad often good for sparse problems (like bag-of-words)?**  
Parameters that receive gradients infrequently don’t accumulate large squared gradients, so their effective learning rate stays higher—helping rare but informative features learn.

**Q2. What’s the main failure mode of AdaGrad in long training runs?**  
The accumulator keeps growing, making effective learning rates shrink toward zero. Eventually updates become tiny and learning slows dramatically.

---

## Video 37 — RMSProp
**What to remember**
- Fixes AdaGrad by using EWMA of squared gradients instead of full sum.
- Keeps adaptive learning rates from decaying forever.
- Commonly used for non-stationary objectives (and was popular for RNNs).

**Interview Questions (with answers)**
**Q1. How does RMSProp address AdaGrad’s “learning rate goes to zero” problem?**  
It replaces the cumulative sum with an exponentially decayed average, so old gradients fade out. This keeps the denominator bounded and maintains usable step sizes.

**Q2. Why do adaptive methods help when gradient scales vary across parameters?**  
They normalize updates by recent gradient magnitude per parameter, preventing some weights from changing too fast while others barely move.

---

## Video 38 — Adam Optimizer
**What to remember**
- Adam = momentum (1st moment) + RMSProp (2nd moment) + bias correction.
- Typically fast “out of the box,” but can generalize worse than SGD in some cases.
- AdamW (decoupled weight decay) is often preferred for proper regularization.

**Interview Questions (with answers)**
**Q1. What problem do Adam’s bias-correction terms solve?**  
At early steps, moment estimates start at zero and are biased low. Bias correction rescales them so updates aren’t artificially small in the beginning.

**Q2. If Adam trains fast but generalizes worse than SGD, what’s a common fix?**  
Try SGD+momentum after a warm-up phase, or adjust regularization (weight decay), use better data augmentation, or use AdamW with a tuned decay and LR schedule.

---

## Video 39 — Keras Tuner | Hyperparameter Tuning a Neural Network
**What to remember**
- Tune: layers, units, dropout, LR, batch size, optimizers.
- Use validation properly; avoid overfitting to validation by repeated tuning.
- Choose search strategy: random search, Bayesian optimization, Hyperband.

**Interview Questions (with answers)**
**Q1. What’s the biggest “evaluation mistake” in hyperparameter tuning?**  
Leaking information from validation by repeatedly tuning until it looks best—effectively overfitting to the validation split. Best practice: keep a final untouched test set.

**Q2. How do you decide what to tune first for maximum gain?**  
Start with learning rate + model capacity (depth/width), then regularization (dropout/weight decay), then batch size and optimizer choice. LR often gives the largest immediate improvement.

---

## Video 40 — What is CNN? CNN Intuition
**What to remember**
- Convolution learns local patterns; kernels slide across the image.
- Parameter sharing ⇒ fewer parameters than fully connected layers.
- Feature hierarchy: edges → textures → parts → objects.

**Interview Questions (with answers)**
**Q1. Why is parameter sharing crucial in CNNs?**  
The same pattern (e.g., an edge) can appear anywhere. Sharing weights lets the model detect it regardless of location and dramatically reduces the number of parameters.

**Q2. What inductive bias does a CNN add compared to an MLP?**  
Locality and translation equivariance: nearby pixels are related, and a feature detector should work across positions. This bias improves sample efficiency for images.

---

## Video 41 — CNN vs Visual Cortex | Cat Experiment | History of CNN
**What to remember**
- Biological inspiration: receptive fields and hierarchical processing.
- “Cat neuron” story motivates learned feature hierarchy (conceptually).
- CNN success: ImageNet era + compute + better training tricks.

**Interview Questions (with answers)**
**Q1. How is a receptive field conceptually related to convolution kernels?**  
A kernel focuses on a local neighborhood (receptive field). Deeper layers effectively see larger regions because receptive fields expand through stacking.

**Q2. Why is “biology inspiration” not the same as “biology equivalence”?**  
CNNs borrow high-level ideas (locality, hierarchy) but do not replicate brain mechanisms. Training, representations, and dynamics differ; inspiration guided design, not proof of equivalence.

---

## Video 42 — Convolution Operation
**What to remember**
- Convolution = weighted sum of local patch + bias → feature map.
- Multiple filters learn multiple feature maps.
- Channels: kernels span depth (e.g., 3 channels for RGB).

**Interview Questions (with answers)**
**Q1. In Conv2D, why does each filter have depth equal to input channels?**  
Because it must combine information across all input channels to produce one output feature map. For RGB, a filter is (k×k×3).

**Q2. What is the difference between convolution and cross-correlation in practice?**  
Many DL libraries implement cross-correlation (no kernel flip). It behaves similarly for learning because weights are learned; the model can learn the flipped pattern if needed.

---

## Video 43 — Padding & Strides in CNN
**What to remember**
- Padding controls spatial size and border information retention.
- Stride controls downsampling and receptive field progression.
- “Same” padding preserves spatial dimensions (approx).

**Interview Questions (with answers)**
**Q1. Why does padding often improve performance in CNNs?**  
Without padding, border pixels contribute to fewer outputs, losing information and shrinking feature maps too quickly. Padding preserves spatial context and allows deeper stacks without excessive shrinkage.

**Q2. What’s the trade-off between stride and pooling for downsampling?**  
Strided conv learns downsampling while extracting features; pooling is fixed and cheaper. Strided conv can be more expressive but adds parameters and compute.

---

## Video 44 — Pooling Layer | MaxPooling
**What to remember**
- Pooling reduces spatial size and adds some translation robustness.
- MaxPool keeps strongest activation; AvgPool averages activations.
- Too much pooling can discard fine details (hurts localization tasks).

**Interview Questions (with answers)**
**Q1. When might average pooling be preferable to max pooling?**  
When you want smoother, more global statistics (e.g., some classification heads) or when max is too sensitive to noise spikes. AvgPool preserves overall activation magnitude.

**Q2. Why is pooling sometimes removed in modern CNNs?**  
Strided convolutions and global average pooling can replace intermediate pooling while keeping learnable downsampling and maintaining gradient flow more smoothly.

---

## Video 45 — CNN Architecture | LeNet-5
**What to remember**
- LeNet-5: conv → pooling → conv → pooling → FC → output.
- Demonstrates hierarchical feature extraction and early practical CNN design.
- Great reference for “classic CNN pipeline”.

**Interview Questions (with answers)**
**Q1. What design lesson does LeNet-5 still teach today?**  
Stacking conv layers with periodic downsampling builds hierarchical features. Early layers capture local patterns; deeper layers represent more abstract concepts.

**Q2. Why were fully connected layers heavily used at the end in older CNNs?**  
They acted as generic classifiers on extracted features. Modern designs often reduce FC size using global average pooling to cut parameters and overfitting.

---

## Video 46 — Comparing CNN vs ANN
**What to remember**
- CNN: fewer parameters, exploits spatial structure.
- ANN on images: huge parameters, ignores locality; often overfits.
- CNN improves sample efficiency and generalization on vision tasks.

**Interview Questions (with answers)**
**Q1. If you must use an ANN for an image task, what is the biggest risk?**  
Parameter explosion: too many weights relative to data → overfitting, slow training, and poor generalization. Also it fails to leverage spatial priors.

**Q2. What scenario could make an ANN competitive on vision-like data?**  
If features are already compact and meaningful (e.g., embeddings or handcrafted descriptors) and spatial structure is removed/irrelevant, an MLP can work well.

---

## Video 47 — Backpropagation in CNN | Part 1
**What to remember**
- Gradients flow through conv kernels similar to dense layers but with weight sharing.
- Each kernel weight receives gradient contributions from many spatial positions.
- Understanding “how gradients accumulate” is key.

**Interview Questions (with answers)**
**Q1. Why do convolution weights receive gradients summed over many locations?**  
Because the same kernel weight is used at every sliding window position. The total gradient is the sum of contributions from each position where that weight influenced the output.

**Q2. What’s a common intuition error about conv backprop?**  
Thinking each output pixel has its own independent weights. Actually weights are shared, so updates reflect global evidence across the entire feature map.

---

## Video 48 — CNN Backprop Part 2 | Conv, MaxPool, Flatten
**What to remember**
- Backprop through maxpool routes gradient only to argmax positions.
- Flatten just reshapes; gradients reshape back.
- Conv gradients involve sliding correlations with upstream gradients.

**Interview Questions (with answers)**
**Q1. Why does max pooling create sparse gradients?**  
Only the max element in each pooling window influenced the output, so only it receives non-zero gradient; the rest get zero for that window.

**Q2. What’s the practical effect of sparse gradients from maxpool?**  
It can make learning focus on strongest features but may slow learning for weaker-but-useful activations. Sometimes avg pooling or strided conv provides smoother gradient flow.

---

## Video 49 — Cat vs Dog Image Classification Project (CNN Project)
**What to remember**
- Pipeline: dataset → preprocessing → CNN model → training curves → evaluation.
- Prevent leakage: separate train/val/test; ensure label correctness.
- Monitor: accuracy + loss + confusion matrix (esp. class imbalance).

**Interview Questions (with answers)**
**Q1. What’s the most common data leakage in image classification projects?**  
Near-duplicate images across train and validation/test (same photos resized/cropped). This inflates metrics because the model effectively “sees” the same content during training.

**Q2. If val accuracy is high but real-world performance is poor, what do you suspect?**  
Domain shift: lighting/background/camera distribution differs. Fix with better augmentation, collecting representative data, or fine-tuning with target-domain samples.

---

## Video 50 — Data Augmentation in Deep Learning
**What to remember**
- Augmentation increases effective dataset size and robustness.
- Use realistic transforms: flips, crops, color jitter, rotation (task-dependent).
- Avoid label-destroying transforms (e.g., flipping digits 6↔9).

**Interview Questions (with answers)**
**Q1. How do you decide whether an augmentation is “valid”?**  
Ask: does it preserve the label semantics for the task? For example, horizontal flip is valid for cats/dogs, but not for text recognition where direction matters.

**Q2. Why can augmentation act like regularization?**  
It forces the model to learn invariant features rather than memorizing exact pixels. Training distribution becomes broader, reducing overfitting to specific appearances.

---

## Video 51 — Pretrained Models | ImageNet | ILSVRC | Keras Code
**What to remember**
- ImageNet pretraining provides general visual features.
- Use pretrained backbones (ResNet/VGG/MobileNet etc.) for faster convergence.
- Correct preprocessing (input scaling/normalization) must match the pretrained model.

**Interview Questions (with answers)**
**Q1. Why does ImageNet pretraining transfer well to many vision tasks?**  
Early layers learn generic primitives (edges, textures) and mid-level patterns that appear across many domains. Fine-tuning adapts higher layers to the target task.

**Q2. What preprocessing mismatch can silently ruin transfer learning?**  
Using the wrong input normalization (mean/std, scaling range, channel order). The backbone expects a specific input distribution; mismatch shifts activations and harms performance.

---

## Video 52 — What does a CNN see? | Visualizing Filters & Feature Maps
**What to remember**
- Visualizations show what layers respond to: edges → textures → object parts.
- Helps debug: whether model focuses on background vs object.
- Techniques: activation maps, filter visualization, (optionally) Grad-CAM style attention.

**Interview Questions (with answers)**
**Q1. How can feature map visualization help diagnose dataset bias?**  
If activations highlight backgrounds (e.g., grass for dogs) more than the object, the model may be using spurious correlations. You can then adjust data, augmentation, or cropping.

**Q2. Why do deeper layer feature maps look “more abstract”?**  
They combine many earlier features and represent higher-level concepts (compositions). Spatial resolution also decreases, so maps emphasize semantics over precise location.

---

## Video 53 — Transfer Learning | Fine-tuning vs Feature Extraction
**What to remember**
- Feature extraction: freeze backbone, train new head.
- Fine-tuning: unfreeze some layers and train with small LR.
- Start frozen, then gradually unfreeze if needed.

**Interview Questions (with answers)**
**Q1. When should you prefer feature extraction over full fine-tuning?**  
When dataset is small or close to ImageNet-like domain; freezing reduces overfitting and training time. You fine-tune only if you need more task-specific adaptation.

**Q2. What is a safe fine-tuning strategy to avoid destroying pretrained features?**  
Unfreeze last block(s) first, use a much smaller LR for backbone than head, and possibly use LR warmup. Monitor validation carefully for overfitting.

---

## Video 54 — Keras Functional Model | Non-linear Neural Networks
**What to remember**
- Functional API supports multi-input, multi-output, skip connections, shared layers.
- Essential for complex architectures (ResNets, Siamese nets, attention models).
- Graph-style model definition improves clarity for non-sequential flows.

**Interview Questions (with answers)**
**Q1. Give an example where Sequential API is insufficient.**  
Any architecture with branches/merges: residual connections, two-tower (Siamese) networks, multi-modal inputs (image + text), or multi-head outputs.

**Q2. Why are shared layers useful (e.g., Siamese networks)?**  
They enforce the same transformation on different inputs, making embeddings comparable and reducing parameters. This improves consistency for similarity/verification tasks.

---

## Video 55 — Why RNNs are needed | RNNs vs ANNs
**What to remember**
- Sequences have order + context; MLP assumes independent fixed-size inputs.
- RNN introduces hidden state to carry information across time steps.
- Useful for time series, text, audio—where past affects future.

**Interview Questions (with answers)**
**Q1. Why can’t a standard feedforward ANN naturally model variable-length sequences?**  
It expects fixed-size input vectors and lacks a state mechanism to carry history. You can pad/aggregate, but the network still doesn’t explicitly model temporal dependency across positions.

**Q2. What is the hidden state in an RNN, conceptually?**  
A learned summary of past inputs. It’s a compact memory vector updated each step, allowing the model to condition current predictions on previous context.

---

## Video 56 — RNN Forward Propagation | Architecture
**What to remember**
- Same cell (shared weights) unrolled over time.
- h_t = f(W_x x_t + W_h h_{t−1} + b)
- Output can be produced at each step or only at final step (task dependent).

**Interview Questions (with answers)**
**Q1. Why are RNN weights shared across time steps?**  
It enforces consistent processing for each position in the sequence and keeps parameter count independent of sequence length. This enables generalization to variable-length sequences.

**Q2. What’s the difference between “many-to-one” and “many-to-many” RNN setups?**  
Many-to-one outputs a single prediction for the full sequence (e.g., sentiment). Many-to-many outputs a prediction per timestep (e.g., tagging) or sequence-to-sequence with alignment (later extended with encoder-decoder).
---

# Readme_part3 — 100 Days of Deep Learning (CampusX)
Covers Videos **57 → 84** (RNN → LSTM/GRU → Seq2Seq/Attention → Transformers)

---

## Video 57 — RNN Sentiment Analysis | RNN Code Example in Keras
**What to remember**
- Text pipeline: tokenize → sequences → padding → embeddings → RNN → sigmoid/softmax.
- Embedding layer converts token IDs to dense vectors.
- Watch overfitting: small text datasets need regularization + validation discipline.

**Interview Questions (with answers)**
**Q1. Why do we usually use an Embedding layer instead of one-hot vectors for text?**  
One-hot is high-dimensional and sparse, making models heavy and less generalizable. Embeddings learn dense semantic representations where similar words end up close, improving learning efficiency and performance.

**Q2. In sentiment analysis, why is padding + masking important?**  
Sequences have different lengths; padding standardizes batch shapes. Masking prevents padded zeros from influencing hidden states and gradients, so the model learns from real tokens only.

---

## Video 58 — Types of RNN | Many-to-Many | One-to-Many | Many-to-One
**What to remember**
- Many-to-one: sequence → single label (sentiment).
- One-to-many: single input → sequence output (image captioning).
- Many-to-many: sequence labeling (POS tagging) or seq2seq (translation).

**Interview Questions (with answers)**
**Q1. Give an example where many-to-many outputs are aligned with inputs (same length).**  
Sequence labeling like POS tagging or NER: each input token maps to a tag, so output length equals input length and aligns position-wise.

**Q2. What changes in training when outputs are produced at every timestep?**  
Loss is computed per timestep and aggregated (sum/mean). Backprop must account for gradient contributions at each step, increasing dependence on stable gradient flow through time.

---

## Video 59 — Backpropagation works in RNN | Backpropagation Through Time (BPTT)
**What to remember**
- Unroll RNN across time; treat as deep network with shared weights.
- Gradients accumulate across all timesteps due to weight sharing.
- Truncated BPTT limits unroll length to manage compute and stability.

**Interview Questions (with answers)**
**Q1. Why do gradients in RNNs often vanish/explode more severely than in feedforward nets?**  
Because you multiply Jacobians across many timesteps (sometimes hundreds). Repeated multiplication by values <1 shrinks gradients; >1 grows them, making long-range dependency learning hard.

**Q2. What is truncated BPTT and what trade-off does it make?**  
It backprops only through a fixed window of timesteps (e.g., last 50). This reduces compute/memory and stabilizes training, but limits how far back the model can assign credit/blame.

---

## Video 60 — Problems with RNN
**What to remember**
- Vanishing gradients → weak long-term memory.
- Sequential computation → slow training/inference vs parallel models.
- Exposure bias in generation if trained with teacher forcing only (context for later seq2seq).

**Interview Questions (with answers)**
**Q1. Why are vanilla RNNs poor at long-term dependencies?**  
Their hidden state update repeatedly compresses history; small gradient signals fade over many steps. The model tends to rely on recent context because it’s easier to optimize.

**Q2. What is a non-gradient reason RNNs are less popular than Transformers now?**  
They’re inherently sequential: you can’t fully parallelize across timesteps. Transformers process tokens in parallel, enabling much faster training on modern hardware.

---

## Video 61 — LSTM | Part 1 | The What?
**What to remember**
- LSTM introduces a cell state (long-term memory) plus gates.
- Gates control information flow: forget, input, output.
- Designed to keep gradients flowing via additive memory path.

**Interview Questions (with answers)**
**Q1. What’s the key innovation of the LSTM cell state compared to vanilla RNN hidden state?**  
The cell state provides an (approximately) linear, additive path for information over time, making it easier for gradients to flow without repeatedly shrinking, which helps retain long-term information.

**Q2. Intuitively, what does the “forget gate” decide?**  
How much of the previous memory to keep vs discard. It allows the model to reset irrelevant past context and avoid cluttering memory with outdated information.

---

## Video 62 — LSTM Architecture | Part 2 | The How?
**What to remember**
- LSTM equations combine gates with sigmoid/tanh.
- Forget gate scales previous cell state; input gate writes new content.
- Output gate decides what part of cell state becomes visible as hidden state.

**Interview Questions (with answers)**
**Q1. Why are sigmoids used in gates but tanh used in candidate updates?**  
Sigmoid outputs (0–1) act like soft switches for gating. Tanh outputs (−1 to 1) provide a bounded candidate signal to write into memory, preventing uncontrolled growth.

**Q2. How do LSTMs reduce vanishing gradients conceptually?**  
The cell state update is largely additive (c_t = f_t ⊙ c_{t−1} + i_t ⊙ g_t). Additive paths preserve gradient magnitude better than repeated multiplicative transforms in vanilla RNNs.

---

## Video 63 — LSTM Part 3 | Next Word Predictor
**What to remember**
- Language modeling: predict next token given previous tokens.
- Use embeddings + LSTM + softmax over vocabulary.
- Use sampling strategies at inference (greedy, temperature, top-k/top-p in general).

**Interview Questions (with answers)**
**Q1. Why does next-word prediction typically use softmax at the output?**  
Because the target is a categorical distribution over vocabulary tokens. Softmax converts logits into normalized probabilities, enabling cross-entropy training and probabilistic sampling.

**Q2. What is “temperature” in sampling and what effect does it have?**  
Temperature scales logits before softmax. Lower temperature makes distribution sharper (more conservative, repetitive); higher temperature makes it flatter (more diverse but riskier/less coherent).

---

## Video 64 — GRU | Gated Recurrent Unit
**What to remember**
- GRU simplifies LSTM: fewer gates, no separate cell state (often).
- Update and reset gates manage memory and new input mixing.
- Often similar performance to LSTM with fewer parameters.

**Interview Questions (with answers)**
**Q1. Why might you choose GRU over LSTM in a production system?**  
GRUs are lighter (fewer parameters) and often train faster while achieving comparable performance, especially when you need efficiency and the task doesn’t demand very long dependencies.

**Q2. What does the reset gate control in a GRU?**  
How much past information to ignore when computing the candidate hidden state. It allows the model to “forget” history selectively when new context is more relevant.

---

## Video 65 — Deep RNNs | Stacked RNNs/LSTMs/GRUs
**What to remember**
- Stacking adds depth in representation (layer-wise abstraction).
- Risks: overfitting, harder optimization, slower training.
- Use dropout (recurrent dropout carefully), normalization, and good regularization.

**Interview Questions (with answers)**
**Q1. What benefit do stacked RNN layers provide over a single layer?**  
Lower layers capture local/short patterns; upper layers combine them into higher-level temporal features. This hierarchical temporal representation can improve accuracy on complex sequences.

**Q2. What’s a common failure mode of deep RNN stacks and a mitigation?**  
Overfitting and unstable training. Mitigate with dropout between layers, smaller hidden sizes, early stopping, and sometimes replacing deeper recurrence with attention mechanisms.

---

## Video 66 — Bidirectional RNN | BiLSTM | Bidirectional GRU
**What to remember**
- BiRNN processes sequence forward and backward.
- Useful when full context is available (e.g., tagging in offline setting).
- Not suitable for strict real-time streaming where future tokens aren’t known.

**Interview Questions (with answers)**
**Q1. Why do BiLSTMs often outperform unidirectional LSTMs in sequence labeling?**  
Because labeling a token often depends on both left and right context. BiLSTMs incorporate future context (backward pass), improving disambiguation.

**Q2. Why is BiRNN problematic for online prediction tasks?**  
It requires access to future timesteps to compute backward states. In streaming/real-time, future inputs are unavailable, so you can’t compute backward context.

---

## Video 67 — History of Large Language Models | From LSTMs to ChatGPT
**What to remember**
- Progression: word embeddings → RNN/LSTM seq models → attention → Transformers → scaling + pretraining.
- Key shifts: parallelism, self-attention, large-scale data/compute, instruction tuning (high-level).
- This video is conceptual history, not just math.

**Interview Questions (with answers)**
**Q1. What “engineering constraint” pushed the shift from LSTMs to Transformers?**  
Parallelism. Transformers remove strict sequential dependency in computation, enabling massive GPU/TPU parallel training, which made scaling feasible.

**Q2. What is the fundamental modeling advantage of self-attention over recurrence?**  
Direct interactions between any pair of tokens in one step (path length 1). This makes it easier to model long-range dependencies compared to passing information step-by-step through many recurrent transitions.

---

## Video 68 — Encoder–Decoder | Sequence-to-Sequence Architecture
**What to remember**
- Encoder converts input sequence into a context representation; decoder generates output sequence.
- Works for translation, summarization, etc.
- Without attention, fixed context vector can bottleneck performance on long sequences.

**Interview Questions (with answers)**
**Q1. Why does a fixed-size context vector become a bottleneck in vanilla seq2seq?**  
All information must be compressed into one vector regardless of input length. As sequences get longer, compression loses details, making decoding harder and degrading quality.

**Q2. What is “teacher forcing” in a decoder and why used?**  
Feeding the ground-truth previous token during training (instead of the model’s prediction). It stabilizes and speeds learning because the model sees correct context, but can create mismatch at inference.

---

## Video 69 — Attention Mechanism in 1 video | Seq2Seq + Attention
**What to remember**
- Attention lets decoder focus on relevant encoder states at each step.
- Computes alignment scores → softmax weights → weighted sum context.
- Improves long sequence performance and interpretability.

**Interview Questions (with answers)**
**Q1. What problem does attention solve in encoder-decoder models?**  
It removes the fixed-vector bottleneck by allowing the decoder to dynamically retrieve relevant parts of the input at each output step, improving information access and long-range handling.

**Q2. Why is attention described as “soft alignment”?**  
Because it assigns continuous weights across all input positions rather than choosing a single hard position. The model can attend to multiple tokens with varying importance.

---

## Video 70 — Bahdanau Attention vs Luong Attention
**What to remember**
- Bahdanau (additive) attention: uses a feedforward network to compute scores.
- Luong (multiplicative/dot-product family): score via dot/general dot between states.
- Trade-off: additive can be more flexible; dot-product can be faster.

**Interview Questions (with answers)**
**Q1. Why might dot-product attention be computationally faster than additive attention?**  
Dot-product relies on matrix multiplications (highly optimized on GPUs) and avoids extra feedforward layers per alignment score, so it scales efficiently.

**Q2. When might additive attention be preferred?**  
When hidden sizes differ or when you want a more expressive scoring function that can learn complex alignments beyond similarity via dot products.

---

## Video 71 — Introduction to Transformers | Transformers Part 1
**What to remember**
- Transformer replaces recurrence with attention + feedforward blocks.
- Core blocks: self-attention, multi-head, positional encoding, residual + norm.
- Big win: parallelism + strong long-range dependency modeling.

**Interview Questions (with answers)**
**Q1. What is the role of the position-wise feedforward network in a Transformer block?**  
After attention mixes information across tokens, the feedforward network applies non-linear transformation independently to each token representation, increasing model capacity and enabling richer feature extraction.

**Q2. Why are residual connections essential in Transformers?**  
They stabilize training of deep stacks by preserving gradient flow and allowing layers to learn refinements over an identity mapping rather than relearning entire representations.

---

## Video 72 — What is Self Attention | Transformers Part 2
**What to remember**
- Self-attention computes token-to-token relevance within the same sequence.
- Q, K, V projections; attention weights from similarity(Q, K).
- Output is weighted sum of V based on attention weights.

**Interview Questions (with answers)**
**Q1. In self-attention, why do we project into Q, K, and V instead of using embeddings directly?**  
Projections let the model learn task-specific subspaces: queries represent what a token seeks, keys represent what it offers, and values represent information to pass. This flexibility improves expressiveness over raw embeddings.

**Q2. What is the computational complexity of full self-attention and why does it matter?**  
It’s O(n²) in sequence length due to all-pairs interactions. For long sequences, memory/compute grow quickly, motivating sparse/linear attention variants.

---

## Video 73 — Self Attention with Code (Simple Explanation)
**What to remember**
- Implement attention via matrix multiplications + softmax.
- Shapes: (batch, seq, d_model) → Q,K,V → attention scores (seq×seq).
- Numerical stability: softmax on logits; careful scaling and masking.

**Interview Questions (with answers)**
**Q1. Why is numerical stability important in attention implementations?**  
Attention scores can become large; softmax on large logits can overflow and produce NaNs. Stability practices (scaling, subtracting max inside softmax) prevent training collapse.

**Q2. What is a quick way to verify your attention code is correct?**  
Check tensor shapes at every step and test on a tiny synthetic input where you can manually compute expected weights (e.g., identical tokens should yield symmetric attention patterns).

---

## Video 74 — Scaled Dot Product Attention | Why scale?
**What to remember**
- Attention score = (Q·Kᵀ) / √d_k
- Scaling prevents dot products from growing too large with dimension.
- Helps keep softmax in a healthy gradient region.

**Interview Questions (with answers)**
**Q1. Why do dot products grow with vector dimension, and how does scaling help?**  
If components are roughly zero-mean with similar variance, dot product variance increases with d_k. Dividing by √d_k normalizes score magnitude, preventing softmax saturation.

**Q2. What happens if softmax saturates in attention?**  
Weights become near one-hot; gradients through softmax shrink, making learning unstable or slow. Scaling reduces saturation and improves training dynamics.

---

## Video 75 — Self Attention Geometric Intuition | Visualization
**What to remember**
- Attention as “soft retrieval”: query pulls relevant keys.
- Similarity measures alignment of token roles/meaning.
- Geometric view: Q and K define comparison space; V defines content space.

**Interview Questions (with answers)**
**Q1. Explain attention as a retrieval system in one minute.**  
Each token forms a query; all tokens provide keys and values. The query compares to keys to compute weights, then combines values accordingly—like retrieving and blending information from a memory bank.

**Q2. Why might Q/K and V be different subspaces?**  
The model may need one representation to decide relevance (comparison) and another to carry the content to be transferred. Decoupling lets it optimize “matching” and “information payload” separately.

---

## Video 76 — Why is it called “Self” Attention? | Self vs Luong Attention
**What to remember**
- “Self” = attention within the same sequence (tokens attend to tokens).
- Cross-attention = attention from one sequence to another (decoder→encoder).
- Luong attention historically refers to attention in seq2seq (often cross-attn).

**Interview Questions (with answers)**
**Q1. What is the key difference between self-attention and cross-attention?**  
Self-attention uses Q,K,V from the same sequence (intra-sequence mixing). Cross-attention uses queries from one sequence (e.g., decoder) and keys/values from another (e.g., encoder outputs).

**Q2. Why is self-attention useful even without an encoder-decoder setup?**  
It contextualizes representations by letting each token incorporate information from other tokens, enabling richer features for tasks like classification, tagging, and language modeling.

---

## Video 77 — Multi-head Attention
**What to remember**
- Multiple heads learn different relation patterns in parallel.
- Each head has its own Q,K,V projections; outputs are concatenated then projected.
- Increases expressiveness without huge compute blowup.

**Interview Questions (with answers)**
**Q1. Why is multi-head attention better than a single head with large dimension?**  
Different heads can focus on different types of relationships (syntax, coreference, local vs global). A single head might mix them into one space, reducing interpretability and flexibility.

**Q2. What’s a common sign that too many heads is wasteful?**  
Heads become redundant: many attend similarly or contribute little. Empirically you see minimal performance gain but higher compute/memory and sometimes worse training stability.

---

## Video 78 — Positional Encoding in Transformers
**What to remember**
- Attention alone is permutation-invariant; we must inject order information.
- Positional encodings (sinusoidal or learned) add/merge position signals.
- Enables model to distinguish token order and relative distances.

**Interview Questions (with answers)**
**Q1. Why can’t a vanilla Transformer know word order without positional encoding?**  
Self-attention treats tokens as a set; it computes pairwise interactions without inherent sequence indices. Without position signals, “dog bites man” and “man bites dog” could look identical.

**Q2. What’s one advantage of sinusoidal positional encodings?**  
They can extrapolate to longer sequence lengths than seen in training (in principle) because positions are computed by a deterministic function, not limited to learned embeddings for fixed positions.

---

## Video 79 — Layer Normalization | Layer Norm vs Batch Norm
**What to remember**
- LayerNorm normalizes across feature dimension per token (per example).
- Works well for variable-length sequences and small batch sizes.
- In Transformers, LN stabilizes training within each token representation.

**Interview Questions (with answers)**
**Q1. Why is LayerNorm preferred over BatchNorm in Transformers?**  
BatchNorm depends on batch statistics and is less stable with varying batch sizes/sequence lengths. LayerNorm is computed per sample/token, making it consistent for NLP workloads and autoregressive inference.

**Q2. What training symptom suggests normalization is misconfigured in a Transformer?**  
Loss becomes unstable (spikes/NaNs) or gradients explode. Correct LN placement (pre-norm vs post-norm) and proper epsilon values often stabilize training.

---

## Video 80 — Transformer Architecture | Encoder Architecture
**What to remember**
- Encoder block: (Self-attention → Add&Norm) + (FFN → Add&Norm).
- Produces contextualized representations for all tokens.
- Used for understanding tasks (classification, retrieval) or as encoder in seq2seq.

**Interview Questions (with answers)**
**Q1. What does the Transformer encoder output represent?**  
A contextual embedding for each input token where each token vector includes information from other tokens via attention, enabling downstream tasks to use rich representations.

**Q2. Why do we stack multiple encoder layers?**  
Each layer refines representations—early layers capture local/syntactic relations, deeper layers capture higher-level semantics and global dependencies (in practice).

---

## Video 81 — Masked Self Attention | Transformer Decoder
**What to remember**
- Decoder self-attention uses a causal mask to prevent peeking at future tokens.
- Ensures autoregressive property for generation.
- Decoder block typically: masked self-attn → cross-attn → FFN (with residual+norm).

**Interview Questions (with answers)**
**Q1. What exactly does the causal mask enforce mathematically?**  
It sets attention logits for future positions to −∞ (or very negative), making their softmax weights ~0. Thus token t can only attend to tokens ≤ t.

**Q2. Why is masking necessary even during training when ground-truth is known?**  
Without masking, the model can use future tokens to predict the current token, creating an unrealistic shortcut. Masking matches the inference condition where future tokens are unknown.

---

## Video 82 — Cross Attention in Transformers
**What to remember**
- Cross-attention connects decoder queries to encoder keys/values.
- Lets decoder selectively read source information for each generated token.
- Central to translation/summarization and many seq2seq tasks.

**Interview Questions (with answers)**
**Q1. In cross-attention, why are Q and (K,V) from different places?**  
Because the decoder asks: “What do I need from the source to generate next token?” So queries come from decoder state, while keys/values come from encoder outputs (the source memory).

**Q2. What failure mode occurs if cross-attention is weak or mislearned?**  
The decoder may ignore the source and become a generic language model, producing fluent but unfaithful outputs (hallucination-like behavior in seq2seq).

---

## Video 83 — Transformer Decoder Architecture
**What to remember**
- Decoder has three sublayers: masked self-attn, cross-attn, FFN.
- Residual connections + normalization around each sublayer.
- Used for autoregressive generation and seq2seq decoding.

**Interview Questions (with answers)**
**Q1. Why does the decoder need both masked self-attn and cross-attn?**  
Masked self-attn models dependencies within the generated prefix (target-side language modeling). Cross-attn injects information from the source sequence to ensure conditioned generation.

**Q2. How is a decoder-only Transformer different from encoder-decoder?**  
Decoder-only uses causal self-attention only (no encoder, no cross-attn) and is trained to predict next token on a single sequence. Encoder-decoder separates source understanding and target generation.

---

## Video 84 — Transformer Inference | How inference is done in Transformer?
**What to remember**
- Autoregressive generation: produce tokens one by one.
- Use decoding strategies: greedy, beam search, sampling.
- KV caching speeds up inference by reusing past attention computations.

**Interview Questions (with answers)**
**Q1. What is KV caching and why does it speed up decoding?**  
Instead of recomputing keys/values for all previous tokens every step, cache them once. Each new token only computes its own K,V and attends to cached history, reducing repeated computation.

**Q2. Greedy vs Beam Search: when does beam search help, and what’s a downside?**  
Beam search helps when you need high-likelihood, structured outputs (e.g., translation) by exploring multiple hypotheses. Downside: slower inference and can reduce diversity, sometimes producing generic outputs.
---