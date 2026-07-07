# MA1001B Data Science With Python Syllabus

Source anchor: `docs/MA1001B - Analítico.pdf`, official course plan for
`MA1001B - Statistical Modeling for Decision Making`.

## Course Orientation

This version of MA1001B teaches statistical modeling for decision making through
Python-based data science practice. Students learn probability, random
variables, sampling distributions, estimation, hypothesis testing, and
experimental design by working in Jupyter notebooks with real structured data.

The course objective remains aligned with the official source: students make
decisions under uncertainty, build stochastic or deterministic models adapted to
a problem context, extract relevant information from structured data, and
communicate model-based conclusions with precision.

## Learning Outcomes

By the end of the course, students will be able to:

1. Use Python, pandas, and Jupyter notebooks to organize reproducible statistical work.
2. Translate uncertain decision contexts into probability and statistical modeling questions.
3. Select and evaluate discrete and continuous probability models for real data.
4. Use simulation and sampling distributions to explain uncertainty.
5. Estimate population quantities and communicate uncertainty through confidence intervals.
6. Apply hypothesis tests and interpret p-values as decision evidence.
7. Design and analyze simple experiments, including A/B tests and ANOVA settings.
8. Produce a technical report and oral presentation based on a real-data capstone.

## Weekly Schedule

| Week | Official MA1001B alignment | Data science focus | Main artifact |
| --- | --- | --- | --- |
| 1 | Course objective, technological tools | Python, Jupyter, pandas, reproducibility | `lessons/01_python_jupyter_pandas.ipynb` |
| 2 | 1.1, 1.2 probability and counting | Empirical probability and simulation | `lessons/02_probability_simulation.ipynb` |
| 3 | 1.3, 1.4 conditional probability, Bayes, sampling | Conditional probability in tabular data | `lessons/03_conditional_probability_bayes.ipynb` |
| 4 | 2.1-2.3 discrete random variables | Count/event data and binomial models | `lessons/04_discrete_random_variables.ipynb` |
| 5 | 2.4-2.7 discrete distributions and data science | Poisson, geometric, hypergeometric model checks | `lessons/05_count_models.ipynb` |
| 6 | 3.1-3.3 continuous variables | Density, expectation, uniform and normal data | `lessons/06_continuous_random_variables.ipynb` |
| 7 | 3.3-3.4 gamma-type distributions, MGFs | Distribution fitting and transformation | `lessons/07_distribution_fitting.ipynb` |
| 8 | 4.1-4.3 transformations and sampling mean | Bootstrap and sampling distribution intuition | `lessons/08_sampling_distributions_bootstrap.ipynb` |
| 9 | 4.4-4.7 chi-square, t, F, data science | Standard error and inferential distributions | `lessons/09_inferential_distributions.ipynb` |
| 10 | 5.1-5.5 estimation | Confidence intervals for means and proportions | `lessons/10_estimation_confidence_intervals.ipynb` |
| 11 | 5.6-5.7 variance and sample size | Precision, sample size, and uncertainty planning | `lessons/11_sample_size_variance.ipynb` |
| 12 | 6.1-6.7 hypothesis testing | p-values, one-sample and two-sample tests | `lessons/12_hypothesis_testing.ipynb` |
| 13 | 6.8-6.11 categorical tests | Goodness of fit, independence, homogeneity | `lessons/13_categorical_inference.ipynb` |
| 14 | 7.1-7.4 experimental design | A/B testing, ANOVA, residual analysis | `lessons/14_experimental_design_anova.ipynb` |
| 15 | 7.5-7.6 blocks, factorial designs, challenge | Capstone synthesis and presentation | `lessons/15_capstone_workshop.ipynb` |

## Assessment Model

The official assessment model assigns 75% to activities, assignments, cases,
and module exams, and 25% to the challenge process and outcomes. This course
uses the same split.

| Component | Weight | Evidence |
| --- | ---: | --- |
| Weekly notebook practice | 25% | Completed lesson notebooks and reflection prompts |
| Applied assignments | 20% | Four applied data notebooks |
| Concept checks and short quizzes | 15% | Probability, distributions, inference, design |
| Practical module checks | 15% | Timed notebook tasks or mini-cases |
| Capstone challenge | 25% | Proposal, notebooks, report, presentation |

## Recurring Lesson Pattern

Each lesson notebook follows the same structure:

1. Topic and decision context.
2. Statistical ideas and assumptions.
3. Python workflow.
4. Guided data activity.
5. Interpretation for decision making.
6. Independent practice.
7. Written reflection.

## Required Python Stack

The base stack is intentionally standard: JupyterLab, NumPy, pandas, SciPy,
statsmodels, scikit-learn, matplotlib, seaborn, kaggle, and pyarrow.

## Capstone

Students complete a final real-data project using a Kaggle dataset or another
public dataset approved by the instructor. The capstone must include a decision
question, data source citation, exploratory analysis, uncertainty
quantification, at least one hypothesis test or model comparison, assumptions,
limitations, and a recommendation.

See `capstone/capstone_brief.md` for the full specification.

## Pedagogical Commitments

This course is not organized as a sequence of disconnected formulas. Every
topic is taught through a decision problem, a data representation, a statistical
model, and a written interpretation. Students are expected to explain why a
method is appropriate before they use it in Python.

Each week should make three links explicit:

1. Conceptual link: what uncertainty or variability is being modeled.
2. Computational link: how Python represents the data and calculation.
3. Decision link: how the result supports, weakens, or qualifies an action.

Instructors should avoid treating notebooks as passive demonstrations. Each
lesson includes short pauses, checkpoints, and writing prompts so students
practice statistical reasoning, not only syntax.
