# Applied Assignments

Assignments are submitted as Jupyter notebooks plus a short written conclusion.
Each notebook must run from top to bottom and must cite any dataset used.

Every assignment follows the same analysis cycle:

```text
question -> data -> method -> result -> uncertainty -> decision
```

Students should not submit notebooks that only contain code and output. Each
assignment must include short markdown explanations that justify the method,
interpret the result, and state limitations.

## Assignment 1 - Probability From Data

Alignment: probability theory, counting, conditional probability, Bayes' rule,
and random sampling.

Recommended dataset: Titanic.

Scenario: A safety analyst wants to communicate survival risk from historical
passenger data without overstating what the data can prove.

Tasks:

1. Load and inspect the data.
2. Define at least four events from the dataset.
3. Estimate marginal, joint, and conditional probabilities.
4. Compare empirical probabilities across at least two subgroups.
5. Use Bayes' rule to answer a risk-oriented question.
6. Write a decision recommendation and state its limitations.

Required outputs:

1. Event definitions written in words and implemented in code.
2. A probability table with marginal and conditional probabilities.
3. One visualization that compares subgroup probabilities.
4. A 150-250 word conclusion that explains which probability is useful for the
   decision and which causal claims are not justified.

## Assignment 2 - Distribution Modeling

Alignment: discrete random variables, continuous random variables, expected
value, and common distributions.

Recommended datasets: Bike Sharing Demand or House Prices.

Scenario: An operations or planning team needs a simple probabilistic model for
future demand or measurements. The model does not need to be perfect, but the
team must know where it works and where it fails.

Tasks:

1. Identify one count variable and one continuous variable.
2. Visualize each variable.
3. Fit or compare at least two candidate distributions.
4. Estimate expected value and variance.
5. Use simulation to explain one model assumption.
6. Decide whether the distribution is useful for a practical question.

Required outputs:

1. Histograms or count plots for selected variables.
2. Empirical summaries: mean, variance, skewness, and selected quantiles.
3. At least two model comparisons using visual or numeric evidence.
4. A model recommendation that explicitly names the assumption most likely to
   fail in practice.

## Assignment 3 - Estimation And Uncertainty

Alignment: sampling distributions, confidence intervals, standard error,
estimation for means and proportions, and sample size.

Recommended dataset: World Happiness Report or House Prices.

Scenario: A stakeholder needs an estimate, not just a sample average. The
analysis must communicate precision and explain how much data would be needed
for a more useful estimate.

Tasks:

1. Define a population question and a sample statistic.
2. Estimate the statistic with a confidence interval.
3. Use bootstrap resampling to approximate sampling variability.
4. Compare two groups with an interval estimate.
5. Compute a sample size target for a desired margin of error.
6. Write a conclusion that separates estimate, uncertainty, and decision.

Required outputs:

1. A clearly stated population quantity.
2. A point estimate and confidence interval.
3. A bootstrap distribution plot.
4. A comparison between two groups using interval reasoning.
5. A sample-size calculation tied to a practical margin of error.

## Assignment 4 - Tests And Experiments

Alignment: hypothesis testing, p-values, chi-square tests, ANOVA, and
experimental design.

Recommended dataset: A/B Testing.

Scenario: A product or process owner wants to decide whether a treatment,
design, policy, or process change should be adopted.

Tasks:

1. Define null and alternative hypotheses.
2. Check assumptions and describe threats to validity.
3. Run a test for a mean, proportion, or conversion rate.
4. Run a categorical test or ANOVA when appropriate.
5. Interpret the p-value for decision making.
6. Recommend an action and describe what evidence would change the decision.

Required outputs:

1. Null and alternative hypotheses in words and symbols.
2. Assumption check or threat-to-validity discussion.
3. Test statistic, p-value, effect size, and practical interpretation.
4. A recommendation that separates statistical significance from practical
   importance.

## Rubric

Use `rubrics/assignment_rubric.md` for grading. The summary weights are:

| Criterion | Weight |
| --- | ---: |
| Reproducible notebook execution | 15% |
| Statistical method and assumptions | 30% |
| Python data workflow quality | 20% |
| Decision-oriented interpretation | 25% |
| Citation, ethics, and limitations | 10% |
