import json
from pathlib import Path


COMMON_SETUP = """
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

rng = np.random.default_rng(1001)
sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", 20)
"""


LESSONS = [
    {
        "file": "01_python_jupyter_pandas.ipynb",
        "title": "Python, Jupyter, And Pandas For Statistical Work",
        "alignment": "Course objective: structured databases, technological tools, written communication.",
        "scenario": "A program coordinator has student activity data and needs an early warning summary. The decision is not only which group has the lowest average, but which group needs support and what evidence justifies that support.",
        "concept": "A notebook is a statistical argument, not a scratchpad. The reader should see the question, the data, the calculation, and the conclusion. pandas gives us a way to represent rows as observations and columns as variables. Good analysis starts by checking what each row means, which variables are measured, and whether the data can answer the question.",
        "math": "For a numeric variable x, the sample mean is xbar = (x1 + ... + xn) / n. This is a summary of the observed sample, not a guarantee about a population.",
        "data_note": "This first notebook uses a small simulated class dataset so everyone can run the workflow before configuring Kaggle.",
        "code_cells": [
            COMMON_SETUP,
            """
student_activity = pd.DataFrame({
    "section": np.repeat(["A", "B", "C"], 40),
    "hours_practice": rng.normal(6.5, 1.8, 120).clip(0),
    "notebook_score": rng.normal(78, 10, 120).clip(40, 100),
    "submitted_on_time": rng.choice([True, False], 120, p=[0.82, 0.18]),
})

student_activity.head()
""",
            """
student_activity.info()
""",
            """
summary = (
    student_activity
    .groupby("section")
    .agg(
        students=("notebook_score", "size"),
        mean_score=("notebook_score", "mean"),
        score_sd=("notebook_score", "std"),
        mean_hours=("hours_practice", "mean"),
        on_time_rate=("submitted_on_time", "mean"),
    )
    .round(2)
)
summary
""",
            """
ax = sns.scatterplot(
    data=student_activity,
    x="hours_practice",
    y="notebook_score",
    hue="section",
)
ax.set_title("Practice time and notebook score by section")
ax.set_xlabel("Hours of practice")
ax.set_ylabel("Notebook score")
plt.show()
""",
        ],
        "checkpoint": "Which section appears to need the most support? Use at least two columns from the summary, and name one reason the evidence may be incomplete.",
        "mistakes": [
            "Treating a notebook as a list of commands without explaining the question.",
            "Reporting a mean without checking sample size or variability.",
            "Making a causal claim from an observational table.",
        ],
        "practice": "Create a new variable called `high_score` for scores of 85 or more. Compare the high-score rate by section and write a three-sentence recommendation.",
        "exit": "What makes a notebook reproducible for another student or instructor?",
    },
    {
        "file": "02_probability_simulation.ipynb",
        "title": "Probability Foundations Through Simulation",
        "alignment": "1.1 set theory and probability calculation; 1.2 counting techniques.",
        "scenario": "A game designer wants to set a fair payout for an event involving two dice. Before choosing a payout, the designer needs to know how often the event happens and how simulation compares with exact counting.",
        "concept": "Probability describes long-run regularity under a model. In data science, we often estimate probability from data, but we also use probability models to reason before data are collected. Events can be represented as Boolean conditions. Unions, intersections, and complements become `or`, `and`, and `not` operations in code.",
        "math": "For equally likely outcomes, P(A) = number of outcomes in A / number of possible outcomes. For two events, P(A union B) = P(A) + P(B) - P(A intersection B).",
        "data_note": "This lesson uses simulated dice because the true sample space is known. That makes it possible to compare empirical and theoretical probability.",
        "code_cells": [
            COMMON_SETUP,
            """
rolls = pd.DataFrame({
    "die_1": rng.integers(1, 7, 20_000),
    "die_2": rng.integers(1, 7, 20_000),
})
rolls["total"] = rolls["die_1"] + rolls["die_2"]
rolls.head()
""",
            """
event_total_7 = rolls["total"].eq(7)
event_double = rolls["die_1"].eq(rolls["die_2"])

probability_summary = pd.Series({
    "P(total = 7)": event_total_7.mean(),
    "P(double)": event_double.mean(),
    "P(total = 7 and double)": (event_total_7 & event_double).mean(),
    "P(total = 7 or double)": (event_total_7 | event_double).mean(),
})
probability_summary.round(4)
""",
            """
exact_outcomes = pd.MultiIndex.from_product(
    [range(1, 7), range(1, 7)],
    names=["die_1", "die_2"],
).to_frame(index=False)
exact_outcomes["total"] = exact_outcomes["die_1"] + exact_outcomes["die_2"]

exact_total_7 = exact_outcomes["total"].eq(7)
exact_double = exact_outcomes["die_1"].eq(exact_outcomes["die_2"])

pd.Series({
    "Exact P(total = 7)": exact_total_7.mean(),
    "Exact P(double)": exact_double.mean(),
    "Exact P(total = 7 or double)": (exact_total_7 | exact_double).mean(),
})
""",
            """
sample_sizes = [50, 100, 500, 1000, 5000, 20_000]
convergence = []
for n in sample_sizes:
    sample = rolls.head(n)
    convergence.append({
        "n": n,
        "estimated_P_total_7": sample["total"].eq(7).mean(),
    })

pd.DataFrame(convergence)
""",
        ],
        "checkpoint": "Explain why the simulated estimate changes with sample size but the exact probability does not.",
        "mistakes": [
            "Confusing an empirical estimate with the exact probability.",
            "Adding P(A) and P(B) for overlapping events without subtracting the intersection.",
            "Ignoring the model assumption that the dice are fair and independent.",
        ],
        "practice": "Define a new event, such as `total >= 10`. Estimate it by simulation, compute it exactly, and compare the two values.",
        "exit": "When would simulation be more useful than exact counting?",
    },
    {
        "file": "03_conditional_probability_bayes.ipynb",
        "title": "Conditional Probability, Bayes Rule, And Sampling",
        "alignment": "1.3 conditional probability and Bayes' rule; 1.4 random sampling.",
        "scenario": "A safety analyst is asked to communicate risk from passenger data. The analyst must distinguish P(survived | group) from P(group | survived), because they answer different questions.",
        "concept": "Conditional probability restricts the reference group. P(A | B) means the probability of A among cases where B is true. Bayes' rule lets us reverse a conditional probability when we also know the base rates. In data science, many communication errors come from switching the condition and the outcome.",
        "math": "P(A | B) = P(A intersection B) / P(B). Bayes' rule: P(A | B) = P(B | A) P(A) / P(B).",
        "data_note": "Uses Titanic if `data/raw/titanic/train.csv` exists; otherwise uses a simulated table with the same kind of variables.",
        "code_cells": [
            COMMON_SETUP,
            """
path = Path("data/raw/titanic/train.csv")
if path.exists():
    passengers = pd.read_csv(path).rename(
        columns={"Survived": "survived", "Sex": "sex", "Pclass": "pclass"}
    )
else:
    print(f"Missing {path}. Download Titanic from https://www.kaggle.com/c/titanic")
    passengers = pd.DataFrame({
        "survived": rng.binomial(1, 0.38, 891),
        "sex": rng.choice(["female", "male"], 891, p=[0.36, 0.64]),
        "pclass": rng.choice([1, 2, 3], 891, p=[0.24, 0.21, 0.55]),
    })

passengers[["survived", "sex", "pclass"]].head()
""",
            """
survived = passengers["survived"].eq(1)
female = passengers["sex"].eq("female")

pd.Series({
    "P(survived)": survived.mean(),
    "P(female)": female.mean(),
    "P(survived | female)": survived[female].mean(),
    "P(female | survived)": female[survived].mean(),
}).round(3)
""",
            """
conditional_table = (
    passengers
    .groupby(["sex", "pclass"])["survived"]
    .agg(["count", "mean"])
    .rename(columns={"mean": "survival_rate"})
    .sort_values("survival_rate", ascending=False)
)
conditional_table
""",
            """
sample_estimates = []
for seed in range(30):
    sampled = passengers.sample(120, random_state=seed)
    sample_estimates.append(sampled.loc[sampled["sex"].eq("female"), "survived"].mean())

pd.Series(sample_estimates).describe()
""",
        ],
        "checkpoint": "Write two sentences: one using P(survived | female) correctly and one using P(female | survived) correctly.",
        "mistakes": [
            "Reversing the condition and the outcome.",
            "Ignoring base rates when interpreting Bayes' rule.",
            "Treating historical associations as proof of a causal survival mechanism.",
        ],
        "practice": "Choose another subgroup, estimate its survival probability, and compare the full-data estimate with repeated samples of size 120.",
        "exit": "What information is lost when a probability is reported without its conditioning group?",
    },
    {
        "file": "04_discrete_random_variables.ipynb",
        "title": "Discrete Random Variables And Binomial Models",
        "alignment": "2.1 discrete distributions; 2.2 Bernoulli and binomial; 2.3 multinomial.",
        "scenario": "A product team expects a conversion probability near 0.35. If 20 users see a new flow, how many conversions would be ordinary and how many would be concerning?",
        "concept": "A random variable converts outcomes into numbers. For Bernoulli trials, each observation is success or failure. A binomial random variable counts successes in a fixed number of independent trials with the same success probability.",
        "math": "If X follows Binomial(n, p), then P(X = k) = C(n, k) p^k (1-p)^(n-k), E[X] = np, and Var(X) = np(1-p).",
        "data_note": "Uses simulation to isolate the binomial assumptions before applying the idea to real event data.",
        "code_cells": [
            COMMON_SETUP,
            """
n_trials = 20
p_success = 0.35
successes = rng.binomial(n=n_trials, p=p_success, size=5000)
successes_series = pd.Series(successes, name="successes")
successes_series.describe()
""",
            """
x = np.arange(0, n_trials + 1)
binomial_pmf = pd.DataFrame({
    "successes": x,
    "theoretical_probability": stats.binom.pmf(x, n_trials, p_success),
    "empirical_probability": successes_series.value_counts(normalize=True).reindex(x, fill_value=0).values,
})
binomial_pmf.head(12)
""",
            """
ax = sns.barplot(data=binomial_pmf, x="successes", y="theoretical_probability", color="steelblue")
ax.set_title("Binomial probability model for 20 trials")
ax.set_xlabel("Number of successes")
ax.set_ylabel("Probability")
plt.show()
""",
            """
pd.Series({
    "expected_successes": n_trials * p_success,
    "standard_deviation": np.sqrt(n_trials * p_success * (1 - p_success)),
    "P(5 or fewer successes)": stats.binom.cdf(5, n_trials, p_success),
    "P(10 or more successes)": stats.binom.sf(9, n_trials, p_success),
}).round(3)
""",
        ],
        "checkpoint": "Why is `10 or more successes` different from `exactly 10 successes` for a decision?",
        "mistakes": [
            "Using a binomial model when the success probability changes across trials.",
            "Forgetting that the model counts successes, not the order of successes.",
            "Calling an outcome unusual without defining a probability threshold.",
        ],
        "practice": "Change p_success to 0.20 and then 0.50. Explain how the expected value and tail probabilities change.",
        "exit": "Name one real situation where the binomial independence assumption is doubtful.",
    },
    {
        "file": "05_count_models.ipynb",
        "title": "Count Models: Geometric, Hypergeometric, And Poisson",
        "alignment": "2.4 geometric and negative binomial; 2.5 hypergeometric; 2.6 Poisson; 2.7 data science links.",
        "scenario": "A mobility planner wants to model hourly bike demand. A simple count model may help, but only if its assumptions are reasonable.",
        "concept": "Count models describe nonnegative integer outcomes. A Poisson model is useful for counts in a fixed interval when events occur independently at a roughly constant rate. Real data often violate that constant-rate assumption because time, weather, and context change demand.",
        "math": "If X follows Poisson(lambda), then P(X = k) = exp(-lambda) lambda^k / k!, and E[X] = Var(X) = lambda.",
        "data_note": "Uses Bike Sharing Demand if available; otherwise simulates counts with daily variation.",
        "code_cells": [
            COMMON_SETUP,
            """
path = Path("data/raw/bike-sharing/train.csv")
if path.exists():
    bike = pd.read_csv(path)
    counts = bike["count"].dropna()
else:
    print(f"Missing {path}. Download Bike Sharing Demand from https://www.kaggle.com/c/bike-sharing-demand")
    hour = np.tile(np.arange(24), 60)
    rate = 40 + 90 * ((hour >= 7) & (hour <= 9)) + 80 * ((hour >= 17) & (hour <= 19))
    counts = pd.Series(rng.poisson(rate), name="count")

counts.describe()
""",
            """
pd.Series({
    "mean": counts.mean(),
    "variance": counts.var(ddof=1),
    "variance_to_mean_ratio": counts.var(ddof=1) / counts.mean(),
}).round(2)
""",
            """
ax = sns.histplot(counts, bins=30)
ax.set_title("Observed count distribution")
ax.set_xlabel("Count")
plt.show()
""",
            """
lambda_hat = counts.mean()
threshold = counts.quantile(0.90)
pd.Series({
    "lambda_hat": lambda_hat,
    "observed_P_above_90th_percentile": (counts >= threshold).mean(),
    "poisson_P_above_same_threshold": stats.poisson.sf(threshold - 1, lambda_hat),
}).round(3)
""",
        ],
        "checkpoint": "Use the variance-to-mean ratio to decide whether a single Poisson model is plausible.",
        "mistakes": [
            "Assuming all count data are automatically Poisson.",
            "Ignoring time segmentation when the rate clearly changes.",
            "Comparing only means without checking variability.",
        ],
        "practice": "Create two segments, such as high-demand and low-demand hours. Compare the mean, variance, and Poisson tail probability for each segment.",
        "exit": "What does overdispersion mean in practical planning language?",
    },
    {
        "file": "06_continuous_random_variables.ipynb",
        "title": "Continuous Random Variables And Expected Value",
        "alignment": "3.1 density functions; 3.2 expected value; 3.3 uniform and normal distributions.",
        "scenario": "A pricing analyst needs to summarize sale prices. A mean alone is easy to report, but it may hide skewness, outliers, and uncertainty.",
        "concept": "Continuous variables describe measurements rather than counts. A density curve does not give probability by height alone; probability is area over an interval. Expected value is a long-run center of mass for a distribution, but it can be sensitive to skewed values.",
        "math": "For a continuous random variable, P(a <= X <= b) is the area under the density from a to b. The expected value is an integral, but in data we estimate it with the sample mean.",
        "data_note": "Uses House Prices if available; otherwise simulates a skewed positive variable.",
        "code_cells": [
            COMMON_SETUP,
            """
path = Path("data/raw/house-prices/train.csv")
if path.exists():
    homes = pd.read_csv(path)
    values = homes["SalePrice"].dropna()
else:
    print(f"Missing {path}. Download House Prices from https://www.kaggle.com/c/house-prices-advanced-regression-techniques")
    values = pd.Series(rng.lognormal(mean=12.0, sigma=0.35, size=1200), name="SalePrice")

values.describe()
""",
            """
summary = pd.Series({
    "mean": values.mean(),
    "median": values.median(),
    "std": values.std(ddof=1),
    "q10": values.quantile(0.10),
    "q90": values.quantile(0.90),
    "skew": stats.skew(values),
})
summary.round(2)
""",
            """
ax = sns.histplot(values, kde=True)
ax.axvline(values.mean(), color="red", linestyle="--", label="mean")
ax.axvline(values.median(), color="black", linestyle=":", label="median")
ax.set_title("Continuous measurement with density estimate")
ax.legend()
plt.show()
""",
            """
z_score = (values - values.mean()) / values.std(ddof=1)
pd.Series({
    "share_within_1_sd": z_score.between(-1, 1).mean(),
    "normal_reference_within_1_sd": stats.norm.cdf(1) - stats.norm.cdf(-1),
}).round(3)
""",
        ],
        "checkpoint": "When mean and median differ, which one would you report to a nontechnical stakeholder and why?",
        "mistakes": [
            "Interpreting density height as probability.",
            "Using a normal model without checking skewness.",
            "Reporting a center without describing spread.",
        ],
        "practice": "Choose another continuous variable or transform `values` with log. Compare the mean, median, skewness, and plot shape.",
        "exit": "What does it mean to say probability is area under a density curve?",
    },
    {
        "file": "07_distribution_fitting.ipynb",
        "title": "Distribution Fitting, Transformations, And Moment Ideas",
        "alignment": "3.3 normal distribution; 3.3 gamma-type distributions; 3.4 moment-generating function.",
        "scenario": "An analyst must decide whether to model a positive measurement on its original scale or after a log transformation. The choice affects forecasts and intervals.",
        "concept": "Distribution fitting is not about forcing data to match a named curve. It is about deciding whether a model captures the features that matter for the decision. Transformations can make skewed positive data easier to model, but conclusions must be translated back carefully.",
        "math": "Moments summarize distribution shape. The first moment relates to center, the second to spread, and higher moments to skewness or tail behavior.",
        "data_note": "Uses a skewed positive measurement so students can compare original and log scales.",
        "code_cells": [
            COMMON_SETUP,
            """
values = pd.Series(rng.lognormal(mean=11.9, sigma=0.45, size=1000), name="positive_value")
log_values = np.log(values)

comparison = pd.DataFrame({
    "scale": ["original", "log"],
    "mean": [values.mean(), log_values.mean()],
    "std": [values.std(ddof=1), log_values.std(ddof=1)],
    "skew": [stats.skew(values), stats.skew(log_values)],
})
comparison.round(3)
""",
            """
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(values, kde=True, ax=axes[0])
axes[0].set_title("Original scale")
sns.histplot(log_values, kde=True, ax=axes[1])
axes[1].set_title("Log scale")
plt.show()
""",
            """
normal_fit_log = stats.norm.fit(log_values)
gamma_fit_original = stats.gamma.fit(values, floc=0)

pd.Series({
    "normal_log_mean": normal_fit_log[0],
    "normal_log_sd": normal_fit_log[1],
    "gamma_shape": gamma_fit_original[0],
    "gamma_scale": gamma_fit_original[2],
}).round(3)
""",
            """
prob_large_original = (values > values.quantile(0.90)).mean()
normal_reference = stats.norm.sf(
    np.log(values.quantile(0.90)),
    loc=normal_fit_log[0],
    scale=normal_fit_log[1],
)

pd.Series({
    "empirical_tail_probability": prob_large_original,
    "lognormal_model_tail_probability": normal_reference,
}).round(3)
""",
        ],
        "checkpoint": "Why might the log scale be better for modeling but the original scale better for communication?",
        "mistakes": [
            "Choosing a distribution only because a histogram looks similar.",
            "Forgetting to translate log-scale conclusions back to the original units.",
            "Treating fitted parameters as exact truths rather than estimates.",
        ],
        "practice": "Compare tail probabilities under two candidate models and decide which model is more useful for a risk-oriented question.",
        "exit": "What feature of a distribution is captured by skewness?",
    },
    {
        "file": "08_sampling_distributions_bootstrap.ipynb",
        "title": "Sampling Distributions And Bootstrap Intuition",
        "alignment": "4.1 transformations; 4.2 functions of random variables; 4.3 sampling distribution of the mean.",
        "scenario": "A public-policy analyst has one sample and one average score. The stakeholder wants to know how much that average would vary if a different sample had been collected.",
        "concept": "A statistic is a number computed from a sample, but it varies from sample to sample. A sampling distribution describes that variation. The bootstrap approximates sampling variation by repeatedly resampling from the observed data.",
        "math": "For independent observations with standard deviation sigma, the standard error of the mean is approximately sigma / sqrt(n). In practice sigma is often estimated by the sample standard deviation.",
        "data_note": "Uses simulated score data to make repeated sampling visible.",
        "code_cells": [
            COMMON_SETUP,
            """
population = pd.Series(rng.normal(loc=6.2, scale=1.1, size=50_000), name="score").clip(0, 10)
sample = population.sample(120, random_state=1001)

pd.Series({
    "sample_mean": sample.mean(),
    "sample_sd": sample.std(ddof=1),
    "estimated_standard_error": sample.std(ddof=1) / np.sqrt(len(sample)),
}).round(3)
""",
            """
repeated_means = []
for seed in range(1000):
    repeated_sample = population.sample(120, random_state=seed)
    repeated_means.append(repeated_sample.mean())

pd.Series(repeated_means).describe().round(3)
""",
            """
bootstrap_means = [
    sample.sample(len(sample), replace=True, random_state=seed).mean()
    for seed in range(1000)
]
pd.Series(bootstrap_means).quantile([0.025, 0.5, 0.975]).round(3)
""",
            """
ax = sns.histplot(bootstrap_means, kde=True)
ax.axvline(sample.mean(), color="red", linestyle="--", label="sample mean")
ax.set_title("Bootstrap distribution of the sample mean")
ax.legend()
plt.show()
""",
        ],
        "checkpoint": "Explain the difference between the distribution of individual scores and the distribution of sample means.",
        "mistakes": [
            "Thinking the bootstrap creates new information from nothing.",
            "Confusing standard deviation of observations with standard error of a statistic.",
            "Ignoring whether the original sample is representative.",
        ],
        "practice": "Repeat the bootstrap with sample sizes 40 and 300. Explain how the interval width changes.",
        "exit": "Why does uncertainty usually shrink as sample size increases?",
    },
    {
        "file": "09_inferential_distributions.ipynb",
        "title": "Chi-square, t, And F Distributions For Inference",
        "alignment": "4.4 chi-square; 4.5 t; 4.6 F; 4.7 data science links.",
        "scenario": "A quality analyst must decide whether a process mean differs from a target when the population variance is unknown.",
        "concept": "Inferential distributions appear when statistics are standardized. The t distribution accounts for uncertainty from estimating the standard deviation. Chi-square distributions arise in variance and categorical-count settings. F distributions arise in variance ratios and ANOVA.",
        "math": "For a one-sample mean with unknown variance, t = (xbar - mu0) / (s / sqrt(n)), with n - 1 degrees of freedom.",
        "data_note": "Uses a simulated process measurement so the role of the reference distribution is clear.",
        "code_cells": [
            COMMON_SETUP,
            """
target = 9.0
measurements = pd.Series(rng.normal(loc=10.0, scale=2.5, size=25), name="measurement")

xbar = measurements.mean()
s = measurements.std(ddof=1)
t_stat = (xbar - target) / (s / np.sqrt(len(measurements)))
p_value = 2 * stats.t.sf(abs(t_stat), df=len(measurements) - 1)

pd.Series({
    "sample_mean": xbar,
    "sample_sd": s,
    "t_statistic": t_stat,
    "p_value": p_value,
}).round(4)
""",
            """
reference = pd.DataFrame({
    "distribution": ["t", "chi-square", "F"],
    "typical_question": [
        "How far is a sample mean from a target?",
        "Is variability larger than expected or are counts independent?",
        "Do group means explain more variation than residual noise?",
    ],
    "example_95_percent_quantile": [
        stats.t.ppf(0.95, df=24),
        stats.chi2.ppf(0.95, df=24),
        stats.f.ppf(0.95, dfn=3, dfd=24),
    ],
})
reference
""",
            """
ci = stats.t.interval(
    confidence=0.95,
    df=len(measurements) - 1,
    loc=xbar,
    scale=s / np.sqrt(len(measurements)),
)
pd.Series({"ci_low": ci[0], "ci_high": ci[1], "target": target}).round(3)
""",
            """
ax = sns.histplot(measurements, bins=10)
ax.axvline(target, color="red", linestyle="--", label="target")
ax.axvline(xbar, color="black", linestyle=":", label="sample mean")
ax.legend()
plt.show()
""",
        ],
        "checkpoint": "Why do we use a t distribution instead of a normal distribution in this example?",
        "mistakes": [
            "Using the wrong reference distribution for the statistic.",
            "Treating degrees of freedom as a decorative parameter.",
            "Reporting a p-value without the estimate and interval.",
        ],
        "practice": "Change the sample size to 10 and 100. Compare the t interval width and p-value.",
        "exit": "What role does the estimated standard error play in the t statistic?",
    },
    {
        "file": "10_estimation_confidence_intervals.ipynb",
        "title": "Point Estimation And Confidence Intervals",
        "alignment": "5.1 point estimation; 5.2 intervals; 5.3 means; 5.4 standard error; 5.5 proportions.",
        "scenario": "A survey team needs to estimate average satisfaction and support for a policy. A point estimate alone is too precise for decision making.",
        "concept": "Estimation separates what the sample says from what we infer about the population. A confidence interval is a procedure that, under its assumptions, captures the true parameter at a stated long-run rate. It is not a probability statement about one fixed parameter after the interval is computed.",
        "math": "A common interval structure is estimate +/- critical value times standard error.",
        "data_note": "Uses simulated survey data with one numeric score and one binary support variable.",
        "code_cells": [
            COMMON_SETUP,
            """
survey = pd.DataFrame({
    "satisfaction": rng.normal(72, 12, 180).clip(0, 100),
    "supports_policy": rng.binomial(1, 0.58, 180),
})
survey.head()
""",
            """
mean_estimate = survey["satisfaction"].mean()
mean_se = survey["satisfaction"].std(ddof=1) / np.sqrt(len(survey))
mean_ci = stats.t.interval(
    confidence=0.95,
    df=len(survey) - 1,
    loc=mean_estimate,
    scale=mean_se,
)

pd.Series({"mean": mean_estimate, "se": mean_se, "ci_low": mean_ci[0], "ci_high": mean_ci[1]}).round(3)
""",
            """
p_hat = survey["supports_policy"].mean()
n = len(survey)
prop_se = np.sqrt(p_hat * (1 - p_hat) / n)
prop_ci = (p_hat - 1.96 * prop_se, p_hat + 1.96 * prop_se)

pd.Series({
    "support_proportion": p_hat,
    "proportion_se": prop_se,
    "ci_low": prop_ci[0],
    "ci_high": prop_ci[1],
}).round(3)
""",
            """
bootstrap_support = [
    survey.sample(n, replace=True, random_state=seed)["supports_policy"].mean()
    for seed in range(1000)
]
pd.Series(bootstrap_support).quantile([0.025, 0.5, 0.975]).round(3)
""",
        ],
        "checkpoint": "Would you claim majority support? Use the interval, not only the sample proportion.",
        "mistakes": [
            "Saying there is a 95 percent probability that this specific interval contains the parameter.",
            "Reporting an interval without the confidence level.",
            "Ignoring whether the sample was collected in a way that supports population inference.",
        ],
        "practice": "Repeat the interval calculation for sample sizes 60 and 600. Explain the change in precision.",
        "exit": "What is the difference between a point estimate and an interval estimate?",
    },
    {
        "file": "11_sample_size_variance.ipynb",
        "title": "Variance Estimation And Sample Size Planning",
        "alignment": "5.6 variance and ratio of variances; 5.7 sample size estimation.",
        "scenario": "An operations manager wants a precise estimate of cycle time. More precision requires more observations, which costs time and money.",
        "concept": "Variance describes variability, not error. Sample size planning connects statistical precision to operational cost. Before collecting data, analysts should decide what margin of error is useful enough for the decision.",
        "math": "For estimating a mean, a planning approximation is n = (z* sigma / E)^2, where E is the target margin of error.",
        "data_note": "Uses simulated process data for two production lines.",
        "code_cells": [
            COMMON_SETUP,
            """
process = pd.DataFrame({
    "line": np.repeat(["A", "B"], 90),
    "cycle_time": np.r_[rng.normal(10.0, 1.1, 90), rng.normal(10.4, 1.8, 90)],
})
process.groupby("line")["cycle_time"].agg(["count", "mean", "std", "var"]).round(3)
""",
            """
line_a = process.loc[process["line"].eq("A"), "cycle_time"]
line_b = process.loc[process["line"].eq("B"), "cycle_time"]
variance_ratio = line_b.var(ddof=1) / line_a.var(ddof=1)

pd.Series({
    "variance_A": line_a.var(ddof=1),
    "variance_B": line_b.var(ddof=1),
    "variance_ratio_B_to_A": variance_ratio,
}).round(3)
""",
            """
estimated_sigma = process["cycle_time"].std(ddof=1)
planning = pd.DataFrame({"target_margin": [0.50, 0.25, 0.10]})
planning["required_n"] = np.ceil((1.96 * estimated_sigma / planning["target_margin"]) ** 2).astype(int)
planning
""",
            """
ax = sns.boxplot(data=process, x="line", y="cycle_time")
ax.set_title("Cycle-time variability by line")
plt.show()
""",
        ],
        "checkpoint": "Why does cutting the margin of error in half require much more than twice the sample size?",
        "mistakes": [
            "Treating sample size as only a statistical issue and ignoring collection cost.",
            "Comparing means while ignoring very different variances.",
            "Using a planning sigma with no justification.",
        ],
        "practice": "Choose a margin of error that would be useful for an operations decision. Compute the required sample size and justify whether it is realistic.",
        "exit": "What practical question should be answered before choosing a target margin of error?",
    },
    {
        "file": "12_hypothesis_testing.ipynb",
        "title": "Hypothesis Testing For Decision Making",
        "alignment": "6.1 elements; 6.2 intervals and tests; 6.3 p-values; 6.4-6.7 tests for means, proportions, and variances.",
        "scenario": "A product owner wants to know whether a treatment page should replace a control page. The analysis must separate statistical evidence from practical business value.",
        "concept": "A hypothesis test asks whether the observed data would be surprising if a null claim were true. The p-value is not the probability that the null is true. It is a probability of data at least as extreme as what was observed, calculated under the null model.",
        "math": "For two proportions, the practical effect is p_treatment - p_control. A test can evaluate evidence against equal conversion rates, but the decision should also consider effect size.",
        "data_note": "Uses a simulated A/B test unless Kaggle A/B testing files are later connected.",
        "code_cells": [
            COMMON_SETUP,
            """
ab = pd.DataFrame({
    "group": np.repeat(["control", "treatment"], 1000),
    "converted": np.r_[rng.binomial(1, 0.10, 1000), rng.binomial(1, 0.125, 1000)],
})
conversion = ab.groupby("group")["converted"].mean()
conversion
""",
            """
table = pd.crosstab(ab["group"], ab["converted"])
chi2, p_value, dof, expected = stats.chi2_contingency(table)

effect = conversion.loc["treatment"] - conversion.loc["control"]
pd.Series({
    "control_conversion": conversion.loc["control"],
    "treatment_conversion": conversion.loc["treatment"],
    "absolute_lift": effect,
    "p_value": p_value,
}).round(4)
""",
            """
control = ab.loc[ab["group"].eq("control"), "converted"]
treatment = ab.loc[ab["group"].eq("treatment"), "converted"]

bootstrap_lifts = []
for seed in range(1000):
    c = control.sample(len(control), replace=True, random_state=seed).mean()
    t = treatment.sample(len(treatment), replace=True, random_state=seed + 10_000).mean()
    bootstrap_lifts.append(t - c)

pd.Series(bootstrap_lifts).quantile([0.025, 0.5, 0.975]).round(4)
""",
            """
minimum_practical_lift = 0.02
pd.Series({
    "observed_lift": effect,
    "meets_practical_threshold": effect >= minimum_practical_lift,
    "statistically_detectable_at_0.05": p_value < 0.05,
})
""",
        ],
        "checkpoint": "Would you launch the treatment if the p-value is below 0.05 but the lift is smaller than the practical threshold?",
        "mistakes": [
            "Interpreting p < 0.05 as proof that the treatment is important.",
            "Ignoring effect size.",
            "Changing the hypothesis after seeing the result without saying so.",
        ],
        "practice": "Change the treatment conversion rate in the simulation. Find a case with a small p-value but weak practical value, or strong practical value but high uncertainty.",
        "exit": "What is one sentence you should never write about a p-value?",
    },
    {
        "file": "13_categorical_inference.ipynb",
        "title": "Goodness Of Fit, Independence, And Homogeneity",
        "alignment": "6.8 goodness of fit; 6.9 independence; 6.10 homogeneity; 6.11 several proportions.",
        "scenario": "A regional manager wants to know whether customer preferences differ by region. If preferences are independent of region, a single strategy may be enough; otherwise segmentation may be needed.",
        "concept": "Categorical inference compares observed counts with expected counts under a null structure. Tests of independence ask whether two categorical variables are associated in one population. Tests of homogeneity compare distributions across groups.",
        "math": "The chi-square statistic sums (observed - expected)^2 / expected across cells. Larger values indicate stronger disagreement with the null model.",
        "data_note": "Uses simulated region-choice data with a contingency table.",
        "code_cells": [
            COMMON_SETUP,
            """
regions = rng.choice(["North", "Center", "South"], 900, p=[0.35, 0.40, 0.25])
choice_probs = {
    "North": [0.52, 0.30, 0.18],
    "Center": [0.42, 0.38, 0.20],
    "South": [0.34, 0.42, 0.24],
}
choices = [rng.choice(["A", "B", "C"], p=choice_probs[r]) for r in regions]
survey = pd.DataFrame({"region": regions, "choice": choices})
table = pd.crosstab(survey["region"], survey["choice"])
table
""",
            """
row_percentages = table.div(table.sum(axis=1), axis=0)
row_percentages.round(3)
""",
            """
chi2, p_value, dof, expected = stats.chi2_contingency(table)
pd.Series({
    "chi_square": chi2,
    "degrees_of_freedom": dof,
    "p_value": p_value,
}).round(4)
""",
            """
expected_table = pd.DataFrame(expected, index=table.index, columns=table.columns)
(table - expected_table).round(1)
""",
        ],
        "checkpoint": "Which cells contribute most to the disagreement between observed and expected counts?",
        "mistakes": [
            "Using percentages only and never checking counts.",
            "Ignoring small expected counts.",
            "Saying the test proves why the categories are associated.",
        ],
        "practice": "Write a segmentation recommendation using both row percentages and the chi-square result.",
        "exit": "What does expected count mean in a chi-square test?",
    },
    {
        "file": "14_experimental_design_anova.ipynb",
        "title": "Experimental Design, A/B Testing, ANOVA, And Residuals",
        "alignment": "7.1 experimental strategies; 7.2 ANOVA; 7.3 fixed effects; 7.4 residual analysis.",
        "scenario": "A team compares three interface designs. The decision should use group differences, residual variation, and the quality of the experimental design.",
        "concept": "Experimental design is about creating credible comparisons. Random assignment protects against systematic differences between treatment groups. ANOVA compares between-group variability with within-group variability. Residual analysis checks whether the model leaves structure unexplained.",
        "math": "ANOVA uses an F statistic: variation explained by groups divided by residual variation, adjusted by degrees of freedom.",
        "data_note": "Uses a simulated single-factor experiment with three designs.",
        "code_cells": [
            COMMON_SETUP,
            """
experiment = pd.DataFrame({
    "design": np.repeat(["A", "B", "C"], 70),
    "response": np.r_[rng.normal(50, 7, 70), rng.normal(54, 7, 70), rng.normal(58, 7, 70)],
})
experiment.groupby("design")["response"].agg(["count", "mean", "std"]).round(2)
""",
            """
groups = [group["response"].to_numpy() for _, group in experiment.groupby("design")]
f_stat, p_value = stats.f_oneway(*groups)

pd.Series({
    "f_statistic": f_stat,
    "p_value": p_value,
}).round(4)
""",
            """
overall_mean = experiment["response"].mean()
group_means = experiment.groupby("design")["response"].transform("mean")
experiment["residual"] = experiment["response"] - group_means
experiment[["design", "response", "residual"]].head()
""",
            """
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.boxplot(data=experiment, x="design", y="response", ax=axes[0])
axes[0].set_title("Response by design")
sns.histplot(experiment["residual"], kde=True, ax=axes[1])
axes[1].set_title("Residual distribution")
plt.show()
""",
        ],
        "checkpoint": "What does a significant ANOVA result tell us, and what does it not tell us?",
        "mistakes": [
            "Treating observational group differences as experimental effects.",
            "Stopping at the ANOVA p-value without estimating the size of differences.",
            "Ignoring residual patterns or unequal variability.",
        ],
        "practice": "Estimate pairwise mean differences between designs and decide which design you would recommend.",
        "exit": "Why is random assignment central to experimental evidence?",
    },
    {
        "file": "15_capstone_workshop.ipynb",
        "title": "Capstone Workshop: Real Data, Model Justification, And Communication",
        "alignment": "7.5 randomized blocks, Latin and Graeco-Latin squares; 7.6 factorial designs; challenge outcomes.",
        "scenario": "Your team must turn a dataset into a defensible recommendation. The strongest capstones are not the most complicated; they are the clearest about question, evidence, uncertainty, and limitations.",
        "concept": "A capstone is a complete statistical argument. The data must be relevant to a decision, the method must match the question, and the conclusion must reflect uncertainty. Design ideas such as blocking and factorial structure help students notice whether comparisons are fair.",
        "math": "The capstone can use intervals, tests, ANOVA, bootstrap, or model comparison. The common structure is always estimate, uncertainty, assumptions, and decision.",
        "data_note": "Uses student-selected Kaggle or approved public data. This notebook provides planning tables and quality checks.",
        "code_cells": [
            COMMON_SETUP,
            """
capstone_checklist = pd.DataFrame({
    "section": [
        "decision question",
        "stakeholder",
        "data source citation",
        "data dictionary",
        "cleaning log",
        "exploratory analysis",
        "uncertainty quantification",
        "test or model comparison",
        "assumptions",
        "limitations and ethics",
        "recommendation",
    ],
    "status": ["not started"] * 11,
})
capstone_checklist
""",
            """
question_quality = pd.DataFrame({
    "weak_question": [
        "What is in the dataset?",
        "Can we predict prices?",
        "Which variables are interesting?",
    ],
    "stronger_question": [
        "Which segment has the highest uncertainty for a pricing decision?",
        "Which features support a useful price estimate for a specific stakeholder?",
        "Which variables materially change the recommendation under uncertainty?",
    ],
})
question_quality
""",
            """
methods_map = pd.DataFrame({
    "decision_need": [
        "estimate a population mean",
        "compare two groups",
        "compare several groups",
        "test association between categories",
        "evaluate an intervention",
    ],
    "possible_method": [
        "confidence interval or bootstrap interval",
        "two-sample interval or test",
        "ANOVA and follow-up comparisons",
        "chi-square test",
        "A/B test or experimental analysis",
    ],
})
methods_map
""",
            """
risk_register = pd.DataFrame({
    "risk": ["missing data", "sampling bias", "weak effect size", "assumption violation"],
    "mitigation": [
        "document cleaning and run sensitivity checks",
        "limit the population claim",
        "report practical significance",
        "choose a better method or qualify the conclusion",
    ],
})
risk_register
""",
        ],
        "checkpoint": "Write your capstone decision question in one sentence. Then name the stakeholder and the action the stakeholder could take.",
        "mistakes": [
            "Choosing a dataset first and never forming a decision question.",
            "Using a complex model without explaining why it answers the question.",
            "Writing a report that describes charts but never makes a recommendation.",
        ],
        "practice": "Complete the checklist for your project. Mark every item as not started, in progress, or complete, and add the next concrete task.",
        "exit": "What evidence would make you change your capstone recommendation?",
    },
]


def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().splitlines()],
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().splitlines()],
    }


def make_notebook(lesson):
    cells = [
        md(f"# {lesson['title']}\n\nOfficial MA1001B alignment: {lesson['alignment']}"),
        md(
            "## How To Use This Lesson\n\n"
            "Read the explanation cells before running the code. Run each code cell in order. "
            "When a checkpoint appears, stop and write your answer before continuing. "
            "The goal is not only to obtain output; the goal is to justify a decision from data."
        ),
        md("## Learning Goals\n\n"
           "- Explain the statistical idea in words.\n"
           "- Implement the idea in Python with readable code.\n"
           "- Interpret the result as evidence for a decision.\n"
           "- State at least one assumption or limitation."),
        md(f"## Decision Scenario\n\n{lesson['scenario']}"),
        md(f"## Conceptual Explanation\n\n{lesson['concept']}"),
        md(f"## Mathematical Anchor\n\n{lesson['math']}"),
        md(f"## Data And Workflow Notes\n\n{lesson['data_note']}"),
    ]

    for index, source in enumerate(lesson["code_cells"], start=1):
        if index == 1:
            cells.append(md("## Python Setup"))
        elif index == 2:
            cells.append(md("## Worked Example"))
        elif index == 4:
            cells.append(md("## From Calculation To Evidence"))
        cells.append(code(source))

    cells.extend(
        [
            md(f"## Guided Checkpoint\n\n{lesson['checkpoint']}"),
            md(
                "## Common Mistakes\n\n"
                + "\n".join(f"- {item}" for item in lesson["mistakes"])
            ),
            md(f"## Independent Practice\n\n{lesson['practice']}"),
            md(
                "## Interpretation Template\n\n"
                "Use this structure for your written answer:\n\n"
                "1. The decision question is ...\n"
                "2. The statistical evidence is ...\n"
                "3. The uncertainty or limitation is ...\n"
                "4. Therefore, I recommend ... because ..."
            ),
            md(f"## Exit Ticket\n\n{lesson['exit']}"),
        ]
    )

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    lessons_dir = Path("lessons")
    lessons_dir.mkdir(exist_ok=True)
    for lesson in LESSONS:
        target = lessons_dir / lesson["file"]
        target.write_text(
            json.dumps(make_notebook(lesson), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
