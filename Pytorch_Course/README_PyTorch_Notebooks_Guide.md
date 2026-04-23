# PyTorch Course README — Beginner-Friendly Guide + Interview Prep

This README explains **what each notebook is teaching**, **why it matters**, and **what you should be able to say in an interview** after studying it.

It is written for someone who already knows **basic Machine Learning** and is now trying to understand **PyTorch and Deep Learning workflows**.

---

## How to Use This README

Use this file in 3 passes:

1. **First pass:** read the “big picture” and notebook summaries.
2. **Second pass:** open each notebook and match the code with the explanation here.
3. **Third pass:** revise the **interview questions**, **common mistakes**, and **key terms** at the end.

---

## Big Picture: What These Notebooks Teach Together

These notebooks collectively walk through the full PyTorch workflow:

- **Tensors** → the basic data structure in PyTorch
- **Autograd** → automatic differentiation for backpropagation
- **Models** → how to define neural networks using `nn.Module`
- **Dataset + DataLoader** → how data is loaded in batches
- **Training Loop** → forward pass, loss, backward pass, optimizer step
- **TensorBoard** → visualize training and debugging signals
- **Captum** → understand *why* a model made a prediction

So the journey is:

**data -> tensors -> model -> loss -> gradients -> optimizer -> metrics -> visualization -> interpretation**

That is the standard deep learning pipeline.

---

## Suggested Order to Study

Some notebooks overlap. This order is the smoothest for a beginner:

1. `1 - PyTorch Tensors.ipynb`
2. `Video+2+-+Tensors.ipynb`
3. `Video+3+-+Autograd.ipynb`
4. `2 - A Simple PyTorch model(1).ipynb`
5. `Video+4+-+Building+Models+in+PyTorch.ipynb`
6. `3 - Dataset and DataLoader(1).ipynb`
7. `4 - A Simple PyTorch Training Loop.ipynb`
8. `Video+5+-+Tensorboard+Support+in+PyTorch.ipynb`
9. `Video+6+-+Model+Training+with+PyTorch.ipynb`
10. `Getting-Started-with-Captum.ipynb`

---

# 1) `1 - PyTorch Tensors.ipynb`

## What this notebook is about
This is your **first introduction to tensors**.

A tensor is the PyTorch version of a multi-dimensional array. If you know NumPy arrays, tensors are very similar, but PyTorch tensors are designed to work well with **autograd** and **GPUs**.

## What happens in the notebook
The notebook shows:

- how to create tensors with zeros, ones, and random values
- how to control tensor **data types** (`dtype`)
- how random seeds work using `torch.manual_seed()`
- basic elementwise math like addition and multiplication
- common mathematical operations like absolute value, trigonometric functions, determinant, SVD, max, and summary statistics

## Why it matters
Everything in PyTorch is built on tensors:

- input data is a tensor
- model weights are tensors
- gradients are tensors
- outputs and losses are tensors

If tensors feel natural, PyTorch becomes much easier.

## Beginner-friendly mental model
Think of a tensor as:

- a **number** (0D tensor)
- a **list** (1D tensor)
- a **table / matrix** (2D tensor)
- a **stack of matrices** (3D+ tensor)

For images, a common shape is:

- grayscale image: `(1, height, width)`
- color image: `(3, height, width)`

## Interview-ready points
You should be able to explain:

- **What is a tensor?** A multi-dimensional array used by PyTorch for data, parameters, and gradients.
- **Why use `manual_seed`?** For reproducibility. Same seed gives the same random numbers.
- **What is `dtype`?** It tells PyTorch how data is stored, like `float32` or `int16`.
- **What is elementwise operation?** Same operation applied to corresponding tensor elements.

## Common mistakes
- confusing tensor shape with tensor values
- forgetting that many deep learning models expect floating-point tensors
- assuming random results will repeat without setting a seed

---

# 2) `Video+2+-+Tensors.ipynb`

## What this notebook is about
This is the **deeper version** of the tensor notebook.

## What happens in the notebook
It expands tensor fundamentals by covering:

- tensor creation with methods like `empty`, `zeros`, `ones`, `rand`
- shape and dimensionality
- data types
- broadcasting
- math and logic operations
- in-place operations
- copying tensors
- likely tensor views / reshape-style thinking and memory behavior

## Important concepts explained

### `torch.empty()`
Creates a tensor with allocated memory but **uninitialized values**. It is fast, but the values are garbage until you assign something.

### Broadcasting
Broadcasting lets PyTorch perform operations on tensors of different shapes **when the shapes are compatible**.

Example:
- tensor A shape: `(2, 3)`
- tensor B shape: `(1, 3)`

PyTorch can “stretch” B across the missing dimension.

### In-place operations
Operations ending with `_` modify the tensor directly, for example `sin_()`.

This saves memory, but can be dangerous if autograd needs the original tensor later.

### Copying vs sharing memory
This matters because sometimes two tensors look separate but are actually views into the same storage.

## Interview-ready points
- **What is broadcasting?** A rule that allows arithmetic on differently shaped tensors when dimensions are compatible.
- **Why can in-place operations be risky?** They may overwrite values needed to compute gradients.
- **Difference between `empty` and `zeros`?** `empty` is uninitialized; `zeros` is initialized with zeros.

## Common mistakes
- using `empty()` and forgetting it is not zero-filled
- not checking shapes before math operations
- doing in-place operations during gradient tracking

---

# 3) `Video+3+-+Autograd.ipynb`

## What this notebook is about
This notebook explains **autograd**, which is one of the most important parts of PyTorch.

Autograd automatically computes gradients so we can train neural networks using backpropagation.

## What happens in the notebook
The notebook demonstrates:

- tensors created with `requires_grad=True`
- building a computation graph automatically
- computing derivatives through `.backward()`
- turning gradient tracking off with `torch.no_grad()`
- why in-place operations can break gradient computation
- autograd profiler tools
- higher-level derivative APIs like Jacobian and vector-Jacobian products

## Beginner-friendly explanation
When you do operations on tensors that require gradients, PyTorch remembers the sequence of operations.

That remembered structure is called the **computation graph**.

Later, when you call `backward()`, PyTorch walks backward through that graph and calculates gradients using the chain rule.

## Why gradients matter
The gradient tells us:

> “If I change this parameter a little, how much will the loss change?”

The optimizer uses that information to update model weights.

## Core terms you should know

### `requires_grad=True`
Tells PyTorch to track operations on that tensor.

### `.grad`
Stores the gradient after backpropagation.

### `.backward()`
Starts backpropagation from a scalar result such as loss.

### `torch.no_grad()`
Turns off gradient tracking. Useful during evaluation or inference.

### Jacobian / VJP
Advanced derivative tools. Not needed for basic training loops, but useful for understanding deeper autograd functionality.

## Interview-ready points
- **What is autograd?** PyTorch’s automatic differentiation engine.
- **Why use `requires_grad=True`?** To track operations for gradient computation.
- **Why call `model.eval()` and `torch.no_grad()` during inference?** To disable training-specific behavior and avoid storing gradients unnecessarily.
- **Why can in-place ops be a problem?** They can overwrite tensors needed for backward computation.

## Common mistakes
- forgetting to zero gradients before the next batch
- expecting `.grad` to be populated before `backward()`
- using `no_grad()` during training by mistake

---

# 4) `2 - A Simple PyTorch model(1).ipynb`

## What this notebook is about
This notebook shows how to define a neural network in PyTorch using **`nn.Module`**.

It uses a classic CNN architecture inspired by **LeNet-5**.

## What happens in the notebook
The notebook:

- imports `torch`, `torch.nn`, and `torch.nn.functional`
- defines a `LeNet` class that inherits from `nn.Module`
- creates convolutional layers and fully connected layers
- defines the `forward()` method
- instantiates the network
- sends a dummy image through the model
- prints output shapes and model structure

## What LeNet is doing
The model takes a small image and gradually transforms it:

1. **Convolution** extracts local patterns like edges and textures.
2. **Activation** adds non-linearity.
3. **Pooling / subsampling** reduces spatial size and keeps important signals.
4. **Flattening** converts feature maps into a vector.
5. **Fully connected layers** combine learned features for final classification.

## About the LeNet-5 image
The diagram in the notebook shows the progression from:

- input image
- convolution feature maps
- subsampling
- more convolution + subsampling
- fully connected layers
- final output classes

This is one of the earliest CNN designs and is great for understanding the flow of image models.

## Beginner-friendly explanation of `forward()`
`forward()` tells PyTorch:

> “When data enters my network, what exact computations should happen?”

You do **not** manually call backpropagation inside `forward()`.
`forward()` only defines the forward pass.

## Interview-ready points
- **Why inherit from `nn.Module`?** It gives parameter tracking, helper methods, and integration with training tools.
- **What goes in `__init__()`?** Layer definitions.
- **What goes in `forward()`?** How input data flows through those layers.
- **What does a convolution layer do?** Learns local spatial patterns using kernels.
- **Why flatten before fully connected layers?** Dense layers expect vector inputs.

## Common mistakes
- defining layers inside `forward()` instead of `__init__()`
- forgetting to flatten before linear layers
- confusing feature maps with output classes

---

# 5) `Video+4+-+Building+Models+in+PyTorch.ipynb`

## What this notebook is about
This is the broader, more complete notebook on **model building**.

## What happens in the notebook
It explains:

- `torch.nn.Module`
- `torch.nn.Parameter`
- linear layers
- convolutional layers
- recurrent layers like LSTM
- other layers like max pooling, batch normalization, and dropout
- general architecture design patterns

## Why this notebook matters
This notebook teaches that PyTorch is not “just training loops.” It also gives you a **language for building architectures**.

## Key ideas

### Linear layer
Applies:

`output = input * weight^T + bias`

Used in MLPs and classification heads.

### Convolution layer
Learns local patterns in images.
Good for spatial data.

### Recurrent layers / LSTM
Used for sequence data like text and time series.
They help model information across time steps.

### MaxPool
Downsamples a feature map by keeping the strongest activation in a local region.

### BatchNorm
Normalizes activations during training to stabilize and speed up learning.

### Dropout
Randomly zeros some activations during training to reduce overfitting.

## Interview-ready points
- **What is `nn.Parameter`?** A tensor that PyTorch registers as a learnable model parameter.
- **What is the difference between a layer and an activation?** A layer transforms data with learnable or fixed logic; an activation adds non-linearity.
- **Why use dropout?** To reduce overfitting by making the network less dependent on specific neurons.
- **Why use batch norm?** To improve training stability and often convergence speed.

## Common mistakes
- using dropout during inference without switching to eval mode
- not understanding that recurrent models are for ordered data
- thinking batch norm “replaces” good preprocessing

---

# 6) `3 - Dataset and DataLoader(1).ipynb`

## What this notebook is about
This notebook teaches how PyTorch handles **data pipelines**.

## What happens in the notebook
It:

- installs/imports PyTorch and TorchVision
- defines image transforms
- downloads the **CIFAR-10** dataset
- wraps it in a `DataLoader`
- batches and shuffles the data
- visualizes a sample batch and labels

## Why it matters
Training does not happen one image at a time in practice.
We usually process data in **mini-batches**.

That is what `DataLoader` helps with.

## Key terms

### `Dataset`
A dataset knows how to return one sample at a time.

### `DataLoader`
A dataloader:

- groups samples into batches
- shuffles data
- can load in parallel with workers
- gives an iterable over batches

### `transforms.Compose`
Chains multiple preprocessing steps.

### `ToTensor()`
Converts image data to a PyTorch tensor.

### `Normalize()`
Scales data into a range that often helps training behave better.

## Interview-ready points
- **Why batch data?** Better hardware utilization and more stable gradient estimates than pure single-sample training.
- **Why shuffle training data?** To reduce order bias and improve generalization.
- **Why normalize images?** It makes optimization easier and more stable.
- **What is the role of `num_workers`?** Parallelizes data loading.

## Common mistakes
- forgetting that labels also come batched
- mixing up dataset length and number of batches
- not normalizing data consistently across train/test

---

# 7) `4 - A Simple PyTorch Training Loop.ipynb`

## What this notebook is about
This notebook connects everything into a real **training pipeline**.

## What happens in the notebook
It:

- loads CIFAR-10 training and test data
- defines a CNN model similar to LeNet
- sets a loss function: `CrossEntropyLoss`
- sets an optimizer: SGD with momentum
- loops over epochs and batches
- performs forward pass
- computes loss
- calls `loss.backward()`
- updates parameters with `optimizer.step()`
- evaluates model accuracy with `torch.no_grad()`

## This is the core training recipe
For each batch:

1. get inputs and labels
2. zero old gradients
3. run forward pass
4. compute loss
5. backpropagate gradients
6. update weights

That sequence is extremely important.

## Why `optimizer.zero_grad()` matters
By default, PyTorch **accumulates** gradients.
So if you do not clear them, gradients from previous batches keep adding up.

## Why `CrossEntropyLoss` is used
It is standard for multi-class classification.
It compares the predicted class scores with the correct labels.

## Interview-ready points
- **Why zero gradients every batch?** Because PyTorch accumulates gradients by default.
- **What does `loss.backward()` do?** Computes gradients of loss with respect to all learnable parameters.
- **What does `optimizer.step()` do?** Updates the parameters using the computed gradients.
- **Why use `torch.no_grad()` in evaluation?** To save memory and avoid unnecessary gradient tracking.
- **Difference between training and evaluation?** Training updates parameters; evaluation only measures performance.

## Common mistakes
- calling `optimizer.step()` before `backward()`
- forgetting `zero_grad()`
- using training mode during evaluation
- interpreting loss and accuracy as the same thing

---

# 8) `Video+5+-+Tensorboard+Support+in+PyTorch.ipynb`

## What this notebook is about
This notebook teaches how to use **TensorBoard** with PyTorch.

## What happens in the notebook
It:

- loads Fashion-MNIST
- visualizes image batches
- creates a `SummaryWriter`
- logs images
- trains a small CNN
- logs scalar metrics like loss
- logs the model graph
- logs embeddings for dataset visualization

## Why it matters
TensorBoard helps you **see what training is doing**.
That makes debugging and experimentation easier.

## What TensorBoard is useful for
- checking whether loss is decreasing
- comparing runs
- visualizing the model graph
- inspecting embeddings
- spotting training problems early

## Interview-ready points
- **Why use TensorBoard?** For experiment tracking and training visualization.
- **What are scalars in TensorBoard?** Single-value metrics over time, like loss or accuracy.
- **Why log images?** To confirm input preprocessing and labels look correct.
- **Why log the graph?** To inspect model structure and verify the data flow.

## Common mistakes
- only looking at final metrics and ignoring training curves
- not naming runs clearly
- forgetting to close the writer

---

# 9) `Video+6+-+Model+Training+with+PyTorch.ipynb`

## What this notebook is about
This is the more complete, polished version of a **training notebook**.

## What happens in the notebook
It covers:

- `Dataset` and `DataLoader`
- a garment classification CNN
- `CrossEntropyLoss`
- SGD optimizer
- a structured `train_one_epoch()` function
- validation after each epoch
- TensorBoard logging
- saving the best model with `torch.save()`

## Why this notebook is important
This notebook moves from “toy training loop” to **good engineering practice**.

It introduces habits that interviewers like:

- separating training and validation
- writing reusable functions
- tracking metrics per epoch
- saving the best checkpoint
- logging experiments cleanly

## Key terms

### Training loss vs validation loss
- **Training loss**: performance on the data used for learning
- **Validation loss**: performance on held-out data

If training loss falls but validation loss worsens, that may indicate **overfitting**.

### Checkpointing
Saving model state so you can reload the best-performing version later.

## Interview-ready points
- **Why validate after each epoch?** To measure generalization, not just memorization.
- **Why save the best model instead of the last model?** The last epoch is not always the best on validation data.
- **Why structure training into functions?** Better readability, reuse, and debugging.

## Common mistakes
- choosing models only by training loss
- not separating validation from test logic
- overwriting the best checkpoint carelessly

---

# 10) `Getting-Started-with-Captum.ipynb`

## What this notebook is about
This notebook is about **model interpretability** using **Captum**, a PyTorch library.

## What happens in the notebook
It:

- loads a pretrained `ResNet101`
- preprocesses an input image
- predicts a class using softmax probabilities
- applies interpretability methods including:
  - **Integrated Gradients**
  - **Occlusion**
  - **Layer GradCAM**
- visualizes attribution maps
- uses **Captum Insights** for interactive interpretation

## Why it matters
Deep learning models are often accurate but hard to explain.
Captum helps answer:

> “Which parts of the input influenced the model’s prediction?”

That is useful for debugging, trust, and analysis.

## Beginner-friendly explanation of each method

### Integrated Gradients
Measures how much each input feature contributes to the prediction by accumulating gradients from a baseline to the actual input.

Simple intuition:
> It asks how prediction changes as we move from a blank/reference input toward the real input.

### Occlusion
Covers parts of the image and checks how the prediction changes.

Simple intuition:
> If hiding one region hurts the prediction a lot, that region was important.

### Layer GradCAM
Shows which spatial regions strongly activated an internal convolutional layer for a chosen class.

Simple intuition:
> It creates a heatmap of important image regions from inside the network.

### Captum Insights
An interactive tool for exploring predictions and attribution visually.

## Interview-ready points
- **What is model interpretability?** Techniques to understand why a model made a prediction.
- **Why use Captum?** To inspect feature importance and debug model behavior.
- **Difference between Integrated Gradients and Occlusion?** Integrated Gradients is gradient-based; Occlusion is perturbation-based.
- **What does GradCAM show?** Important spatial regions in convolutional feature maps.

## Common mistakes
- assuming attribution maps are proof of causality
- treating interpretability as a replacement for evaluation metrics
- forgetting that explanations depend on the chosen baseline / method

---

# What Repeats Across the Notebooks

Some notebooks teach similar ideas in different depth.
That is useful, not a problem.

## Repeated themes

### Tensors
Covered in:
- `1 - PyTorch Tensors.ipynb`
- `Video+2+-+Tensors.ipynb`

### Model building
Covered in:
- `2 - A Simple PyTorch model(1).ipynb`
- `Video+4+-+Building+Models+in+PyTorch.ipynb`

### Training
Covered in:
- `4 - A Simple PyTorch Training Loop.ipynb`
- `Video+6+-+Model+Training+with+PyTorch.ipynb`

### Visualization / debugging
Covered in:
- `Video+5+-+Tensorboard+Support+in+PyTorch.ipynb`
- `Getting-Started-with-Captum.ipynb`

So you can think of the course as:

- **simple intro notebooks** for first understanding
- **video notebooks** for more complete explanations

---

# PyTorch Workflow You Should Be Able to Explain in an Interview

A strong simple answer is:

1. Load and preprocess data using `Dataset`, transforms, and `DataLoader`
2. Define a model by subclassing `nn.Module`
3. Write the `forward()` computation
4. Choose a loss function
5. Choose an optimizer
6. In each training batch: zero grads, forward pass, compute loss, backward pass, optimizer step
7. Evaluate on validation/test data using `model.eval()` and `torch.no_grad()`
8. Track metrics using TensorBoard
9. Save the best model checkpoint
10. Use interpretability tools like Captum to inspect predictions when needed

If you can explain that clearly, you already sound much stronger in interviews.

---

# Most Important Concepts to Memorize

## 1. Tensor
A multi-dimensional array used by PyTorch.

## 2. Gradient
Tells us how much the loss changes when a parameter changes.

## 3. Backpropagation
The process of computing gradients backward through the network.

## 4. `nn.Module`
Base class for neural network models.

## 5. `forward()`
Defines how input becomes output.

## 6. Loss function
Measures prediction error.

## 7. Optimizer
Updates model parameters using gradients.

## 8. Epoch
One full pass through the training dataset.

## 9. Batch
A small subset of training samples processed together.

## 10. Evaluation mode
Used during inference/validation to disable training-specific behavior like dropout.

---

# Common Interview Questions + Good Beginner Answers

## Q1. What is the difference between PyTorch and NumPy?
PyTorch tensors are similar to NumPy arrays, but PyTorch supports automatic differentiation and GPU acceleration more naturally for deep learning.

## Q2. What is `requires_grad`?
It tells PyTorch to track operations on a tensor so gradients can be computed later.

## Q3. Why do we use `zero_grad()`?
Because PyTorch accumulates gradients by default. We clear old gradients before computing new ones.

## Q4. What does `loss.backward()` do?
It computes gradients of the loss with respect to all learnable parameters involved in producing that loss.

## Q5. What does an optimizer do?
It updates the model’s parameters using the gradients, according to a rule like SGD or Adam.

## Q6. What is the role of `DataLoader`?
It loads data in batches, optionally shuffles it, and helps data loading happen efficiently.

## Q7. Why normalize input images?
Normalization improves optimization stability and helps the model train more effectively.

## Q8. What is the difference between training mode and evaluation mode?
Training mode enables behaviors like dropout and batch norm updates. Evaluation mode turns them into inference behavior.

## Q9. Why use convolution for images?
Convolutions learn local spatial patterns such as edges, shapes, and textures while preserving spatial structure.

## Q10. Why use TensorBoard?
To visualize training metrics, inputs, model graphs, and embeddings so experiments are easier to debug and compare.

## Q11. What is overfitting?
When the model learns the training data too specifically and performs worse on unseen data.

## Q12. Why might validation loss increase while training loss decreases?
That often suggests overfitting.

## Q13. What is Captum used for?
To interpret model predictions by highlighting which input features were important.

---

# Common Practical Bugs You Should Recognize

## Shape mismatch
Very common when moving from convolution layers to linear layers.

## Wrong label format
For `CrossEntropyLoss`, labels should usually be class indices, not one-hot vectors.

## Forgetting `model.train()` / `model.eval()`
Can change dropout and batch norm behavior.

## Forgetting `torch.no_grad()` in evaluation
Wastes memory and compute.

## Forgetting `optimizer.zero_grad()`
Causes gradient accumulation across batches.

## Wrong normalization
If train/test preprocessing differs, performance can become misleading.

## Device mismatch
Model on GPU but data on CPU, or vice versa.

---

# How to Talk About These Notebooks in an Interview

A good summary answer:

> I worked through a sequence of PyTorch notebooks that covered tensors, autograd, model building with `nn.Module`, data loading with `Dataset` and `DataLoader`, training loops, TensorBoard experiment tracking, and model interpretability with Captum. I learned how to define CNNs, train them with cross-entropy loss and SGD, evaluate them properly, and visualize both training metrics and feature attributions.

A more technical version:

> The notebooks moved from tensor fundamentals to full training workflows. I practiced building LeNet-style CNNs, using autograd for backpropagation, batching data with `DataLoader`, training with `optimizer.zero_grad()`, `loss.backward()`, and `optimizer.step()`, validating with `model.eval()` and `torch.no_grad()`, logging metrics with TensorBoard, and analyzing model decisions using Integrated Gradients, Occlusion, and GradCAM in Captum.

---

# Final Revision Checklist

Before interviews, make sure you can explain these without looking anything up:

- what a tensor is
- what `requires_grad` does
- what `forward()` does
- why `zero_grad()` is needed
- what `backward()` computes
- what an optimizer does
- how `DataLoader` helps training
- why we use train/eval modes
- what TensorBoard is used for
- what Captum is used for
- the difference between training, validation, and test sets
- why CNNs are good for image data

---

# One-Line Summary of Each Notebook

- **`1 - PyTorch Tensors.ipynb`** → basic tensor creation and math
- **`Video+2+-+Tensors.ipynb`** → deeper tensor operations, broadcasting, and memory behavior
- **`Video+3+-+Autograd.ipynb`** → automatic differentiation and gradient tracking
- **`2 - A Simple PyTorch model(1).ipynb`** → defining a CNN with `nn.Module` using LeNet
- **`Video+4+-+Building+Models+in+PyTorch.ipynb`** → broader view of layers and model architecture components
- **`3 - Dataset and DataLoader(1).ipynb`** → preparing, transforming, batching, and loading data
- **`4 - A Simple PyTorch Training Loop.ipynb`** → end-to-end CNN training and evaluation
- **`Video+5+-+Tensorboard+Support+in+PyTorch.ipynb`** → logging and visualizing experiments
- **`Video+6+-+Model+Training+with+PyTorch.ipynb`** → cleaner training design with validation and checkpointing
- **`Getting-Started-with-Captum.ipynb`** → interpreting model predictions with attribution methods

---

# Closing Advice

You do **not** need to memorize every line of code.
You should instead understand the following story:

> “PyTorch uses tensors as the core data structure. Models are built with `nn.Module`. Autograd computes gradients automatically. Data is fed using `Dataset` and `DataLoader`. Training works by forward pass -> loss -> backward pass -> optimizer step. Evaluation should disable gradient tracking. TensorBoard helps monitor training, and Captum helps interpret predictions.”

If you can explain that calmly and clearly, you will already answer a large number of beginner-to-intermediate interview questions well.
