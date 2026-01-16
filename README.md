# Survival Analysis in R

## Overview

This repository contains a comprehensive tutorial on **Survival Analysis in R**, covering both traditional statistical methods and modern machine learning approaches. The project is built using [Quarto](https://quarto.org/) and provides detailed, hands-on tutorials with practical examples and code implementations.

Survival analysis is a statistical method that examines the time until a specific event occurs, such as death, disease relapse, or machine failure. It is valuable for studying event timing and accounts for cases in which some individuals do not experience the event during the study period, a phenomenon known as **censoring**.

## Table of Contents

1. [Introduction](#introduction)
2. [Key Concepts](#key-concepts)
3. [Tutorial Sections](#tutorial-sections)
4. [Installation and Setup](#installation-and-setup)
5. [Data Sources](#data-sources)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [Resources](#resources)
9. [License](#license)

## Introduction

This tutorial series provides a comprehensive guide to survival analysis in R, covering:

- **Non-parametric methods** for estimating survival functions
- **Semi-parametric methods** like Cox regression
- **Parametric models** with specific distributional assumptions
- **Advanced topics** including recurrent events, competing risks, and joint modeling
- **Machine learning approaches** for survival prediction

Each tutorial includes:
- Theoretical background
- Step-by-step implementations
- Practical examples with real and simulated data
- Visualizations and interpretations
- Links to GitHub notebooks for interactive learning

## Key Concepts

### Survival Analysis Fundamentals

**Survival Time**: The time from the starting point (like diagnosis or study enrollment) to the event of interest. For individuals who don't experience the event during the study, this time is considered *censored*.

**Censoring**: Occurs when the event of interest has not happened for some subjects during the observation period. Common types include:
- **Right censoring**: Event hasn't occurred by the end of the study
- **Left censoring**: Event happened before the subject entered the study
- **Interval censoring**: Event happened within a certain interval

### Key Functions

1. **Survival Function** $S(t)$: Probability that the time to event is greater than time $t$
   - $S(t) = P(T > t)$
   - Starts at 1 and decreases over time

2. **Hazard Function** $h(t)$: Instantaneous rate at which events occur, given survival up to time $t$
   - $h(t) = \frac{f(t)}{S(t)}$
   - Measures event risk over time

3. **Cumulative Hazard Function** $H(t)$: Sum of hazard over time
   - $H(t) = \int_0^t h(u) \, du$

## Tutorial Sections

### 1. Non-Parametric Methods

Non-parametric methods make no assumptions about the underlying distribution of survival times.

- **Introduction to Non-Parametric Survival Models** (`02-07-01-00-*.qmd`)
- **Kaplan-Meier Estimator** (`02-07-01-01-*.qmd`)
  - Estimates survival function by calculating proportion of subjects surviving past each event time
  - Produces step-function survival curves
  - Handles right-censored data
- **Nelson-Aalen Estimator** (`02-07-01-02-*.qmd`)
  - Estimates cumulative hazard function
  - Alternative to Kaplan-Meier for hazard-focused analysis

### 2. Semi-Parametric Methods

Semi-parametric methods assume a specific form for the relationship between covariates and hazard but don't require a specific distribution for survival times.

- **Introduction to Semi-Parametric Survival Models** 
- **Cox Proportional Hazards Model** 
  - Models hazard as $h(t|X) = h_0(t) \exp(\beta X)$
  - Assesses effect of covariates on survival
  - Assumes proportional hazards (constant hazard ratios over time)
- **Time-Dependent Covariates** 
  - Allows covariates or hazard ratios to vary over time
- **Stratified Cox Model** 
  - Handles non-proportional hazards by stratifying on variables

### 3. Parametric Methods

Parametric methods assume a specific distribution for survival times and model both the survival/hazard function and the effect of covariates.

- **Introduction to Parametric Survival Models** 
- **Exponential Model** 
  - Assumes constant hazard rate
  - Simple but often unrealistic
- **Weibull Model** 
  - Allows hazard to increase or decrease over time
  - Flexible for modeling accelerating or decelerating risks
- **Log-Normal Model** 
  - Models survival times with skewed distribution
- **Log-Logistic Model** (`02-07-03-04-*.qmd`)
  - Alternative to log-normal for skewed survival times
- **Generalized Gamma Model** (`02-07-03-05-*.qmd`)
  - Very flexible model encompassing exponential, Weibull, and log-normal
- **Gompertz Model** (`02-07-03-06-*.qmd`)
  - Models hazards that increase exponentially with time
  - Common in aging studies

### 4. Recurrent Event Models

Models for multiple events occurring over time for the same subject.

- **Introduction to Recurrent Event Models** 
- **Andersen-Gill (AG) Model** 
  - Extends Cox model to count multiple events
  - Assumes independence between events conditional on covariates
- **Prentice-Williams-Peterson (PWP) Model** 
  - Accounts for the order of events
  - Models time to the k-th event
- **Frailty Models** 
  - Incorporates random effects for unobserved heterogeneity
- **Marginal Models** 
  - Treats each event as a separate observation
  - Adjusts for correlation within subjects

### 5. Risk Regression

Advanced methods for modeling competing risks and cause-specific hazards.

- **Introduction to Risk Regression** 
- **Cause-Specific Hazard Regression** 
  - Models hazard for each specific event type
  - Treats other events as censoring
- **Subdistribution Hazard Regression (Fine-Gray Model)** 
  - Directly models cumulative incidence function
  - Accounts for competing risks
- **Absolute Risk Regression** (`02-07-05-03-*.qmd`)
  - Direct modeling of cumulative incidence function
- **Aalen's Additive Regression Model** (`02-07-05-04-*.qmd`)
  - Flexible approach with time-varying effects
  - Models impact of risk factors on different causes

### 6. Joint Modeling in Survival Analysis

Methods for jointly modeling longitudinal and survival data.

- **Introduction to Joint Modeling** 
- **Standard Joint Model** 
  - Shared random effects model
  - Links longitudinal trajectories to survival outcomes
- **Baseline Hazard Function** 
  - Estimation and specification of baseline hazard in joint models
- **Causal Effects** 
  - Causal inference from joint models
- **Competing Risks** 
  - Joint models with competing risks
- **Dynamic Joint Model** 
  - Time-varying predictions using longitudinal data
- **Joint Frailty Models** 
  - For recurrent and terminal events

### 7. Machine Learning Based Survival Models

Modern ML approaches for survival prediction with high-dimensional and complex data.

- **Introduction to Machine Learning Based Survival Models** 
- **Survival Trees (CART)** 
  - Decision trees adapted for survival data
- **Random Survival Forest** 
  - Ensemble of survival trees
  - Handles non-linear relationships and high-dimensional data
- **Gradient Boosted Survival Model** 
  - Excellent predictive performance
- **Support Vector Machine (SVM) Survival Model** 
  - Ranking-based approach for survival
- **DeepSurv - Deep Survival Model (CPU)** 
- **DeepSurv - Deep Survival Model (GPU)** 
  - Neural network adaptation of Cox model
  - Captures complex non-linear relationships
- **DeepHit**
  - Deep learning for competing risks
  - Discrete-time survival model
- **NNet-Survival** 
  - Discrete-time survival model with neural networks
- **CoxNNet** 
  - Neural network extension of Cox model
- **CoxNNet for Omics Data** 
  - High-throughput transcriptomics applications
- **LSTMCox Model**
  - Deep learning for recurrent events
  - Time-series survival analysis
- **Ensemble Survival Models with Stacking** 
  - Meta-learning approach combining multiple models
- **Super Learner Survival Prediction** 
  - Ensemble-based prediction with cross-validation

## Installation and Setup

### Prerequisites

- **R** (version 4.0 or higher recommended)
- **RStudio** (recommended IDE)
- **Quarto** (for rendering the website)

### Required R Packages

The tutorials use various R packages. Key packages include:

```{r}
# Core survival analysis packages
install.packages(c(
  "survival",      # Core survival analysis functions
  "survminer",     # Beautiful Kaplan-Meier plots
  "flexsurv",      # Parametric survival models
  "riskRegression", # Risk regression models
  "prodlim",       # Product-limit estimation
  "cmprsk",        # Competing risks
  "timereg",       # Time-dependent regression
  "JM",            # Joint modeling
  "JMbayes2",      # Bayesian joint models
  "joineRML"       # Joint models with ML
))

# Machine learning packages
install.packages(c(
  "randomForestSRC", # Random survival forests
  "gbm",             # Gradient boosting
  "xgboost",         # Extreme gradient boosting
  "rpart",           # Survival trees
  "survival",        # Base survival functions
  "survivalsvm",     # Survival SVM
  "keras",           # Deep learning (CPU)
  "tensorflow",      # Deep learning (GPU)
  "torch"            # PyTorch for R
))

# Visualization and utilities
install.packages(c(
  "ggplot2",         # Graphics
  "dplyr",           # Data manipulation
  "tidyr",           # Data tidying
  "knitr",           # Dynamic report generation
  "rmarkdown"        # Markdown rendering
))
```

## Data Sources

The tutorials use various datasets located in the `Data/` directory:

- **Melanoma_data.csv**: Melanoma survival data
- **support2.csv**: SUPPORT study data
- **lung_dataset.csv**: Lung cancer survival data
- **synthetic_comprisk.csv**: Synthetic competing risks data
- And many more datasets for specific analyses


## Applications

Survival analysis has wide applications:

1. **Medical Research**
   - Time until patient death or relapse after treatment
   - Assessing impact of treatments or risk factors

2. **Reliability Engineering**
   - Time until failure for mechanical systems
   - Predicting lifespans of components

3. **Customer Retention**
   - Time until customer churn
   - Understanding customer lifetime value

4. **Economics**
   - Time until unemployment, bankruptcy, or loan default
   - Duration analysis in econometrics

## Resources

### Textbooks

1. **Klein & Moeschberger** — *Survival Analysis: Techniques for Censored and Truncated Data*
   - Comprehensive classic covering Kaplan-Meier, Cox model, parametric models, competing risks

2. **Collett** — *Modelling Survival Data in Medical Research*
   - Practical guide with strong R examples for medical applications

3. **Therneau & Grambsch** — *Modeling Survival Data: Extending the Cox Model*
   - Advanced Cox model details, time-varying covariates, frailty, diagnostics
   - Author of the R `survival` package

4. **Hosmer, Lemeshow, May** — *Applied Survival Analysis*
   - Beginner-friendly with strong theory and applied examples

5. **Andersen, Geskus, de Witte, & Putter** — *Competing Risks and Multi-State Models*
   - Best resource for competing risks and multi-state modeling

### Online Resources

- **UCLA Institute for Digital Research & Education (IDRE)**: Clear applied tutorials
- **Penn State STAT 507**: Full lecture notes and exercises
- **Imperial College London**: Concise introductory notes
- **Johns Hopkins Biostat**: Advanced course material

### R Package Documentation

- **`survival` package**: Primary reference for Kaplan-Meier, Cox PH, time-varying covariates
- **`survminer`**: Publication-quality survival plots
- **`flexsurv`**: Parametric survival models
- **`riskRegression`**, **`prodlim`**, **`cmprsk`**: Competing risks and prediction models
- **`JM`**, **`JMbayes2`**, **`joineRML`**: Joint models

## Contributing

Contributions are welcome! If you find errors, have suggestions, or want to add new tutorials:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under CC-BY (Creative Commons Attribution). See the footer in `_quarto.yml` for details.

## Author

**Zia Ahmed**  
University at Buffalo  
Email: zia207@gmail.com  
GitHub: [@zia207](https://github.com/zia207)  
LinkedIn: [Zia Ahmed](https://www.linkedin.com/in/zia-ahmed207)

## Acknowledgments

- RENEW Institute, University at Buffalo
- R Community and package developers
- All contributors and users of this tutorial


