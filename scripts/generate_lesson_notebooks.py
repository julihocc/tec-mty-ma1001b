import json
from pathlib import Path


COMMON_SETUP = """# Import required data science and statistical libraries
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set reproducible random seed and visual styling
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
        "goals": [
            "Use Pandas to load, inspect, and organize tabular data representing observations and variables.",
            "Calculate group-level summary statistics (mean, standard deviation, rates) to compare operational segments.",
            "Create clear, informative scatterplots and visualizations using Seaborn to communicate relationships.",
            "Formulate actionable early-warning recommendations while acknowledging observational data limitations."
        ],
        "links": {
            "conceptual": "We model student performance variability across different class sections to identify where academic risk is concentrated.",
            "computational": "We use Pandas DataFrames to organize observations (rows) and variables (columns), and grouping methods (`.groupby`) to aggregate summary metrics.",
            "decision": "The summary metrics provide objective evidence to allocate tutoring resources and academic support to the specific student sections most in need."
        },
        "code_steps": [
            {
                "title": "Environment Setup & Data Simulation",
                "explanation": "We import standard data science libraries (`numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`) and generate a simulated student activity dataset representing three course sections.",
                "code": COMMON_SETUP + """
# Generate simulated student activity data across 3 sections (40 students each)
student_activity = pd.DataFrame({
    "section": np.repeat(["A", "B", "C"], 40),
    "hours_practice": rng.normal(6.5, 1.8, 120).clip(0),  # Practice hours cannot be negative
    "notebook_score": rng.normal(78, 10, 120).clip(40, 100),  # Scores bounded between 40 and 100
    "submitted_on_time": rng.choice([True, False], 120, p=[0.82, 0.18]),  # 82% on-time submission rate
})

# Display the first 5 rows to verify structure
student_activity.head()
"""
            },
            {
                "title": "Data Structure & Type Inspection",
                "explanation": "Before computing statistics, we inspect the DataFrame structure, column data types, and check for missing values using `.info()`.",
                "code": """# Check variable types, non-null counts, and memory usage
student_activity.info()
"""
            },
            {
                "title": "Group-Level Statistical Aggregation",
                "explanation": "We aggregate data by course section to compute key operational metrics: class size, mean score, standard deviation, practice hours, and on-time submission rate.",
                "code": """# Summarize student performance and engagement by section
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
"""
            },
            {
                "title": "Visualizing Relationships Across Sections",
                "explanation": "We create a scatterplot linking practice hours to notebook scores, color-coded by section, to visually check for patterns and disparities.",
                "code": """# Plot practice time versus notebook score by section
ax = sns.scatterplot(
    data=student_activity,
    x="hours_practice",
    y="notebook_score",
    hue="section",
    alpha=0.8,
    s=60
)
ax.set_title("Practice Time and Notebook Score by Section", fontsize=14, pad=10)
ax.set_xlabel("Hours of Practice", fontsize=11)
ax.set_ylabel("Notebook Score (0-100)", fontsize=11)
plt.legend(title="Section")
plt.show()
"""
            }
        ],
        "checkpoint": "Which section appears to need the most support? Use at least two columns from the summary, and name one reason the evidence may be incomplete.",
        "mistakes": [
            "Treating a notebook as a list of commands without explaining the motivating question.",
            "Reporting a mean without checking sample size or variability (standard deviation).",
            "Making a causal claim (e.g., 'more practice causes higher scores') from an observational table.",
        ],
        "practice": "Create a new Boolean variable called `high_score` for scores of 85 or more. Compare the high-score rate by section and write a three-sentence recommendation.",
        "exit": "What makes a data science notebook reproducible for another student or instructor?",
    },
    {
        "file": "02_probability_simulation.ipynb",
        "title": "Probability Foundations Through Simulation",
        "alignment": "1.1 set theory and probability calculation; 1.2 counting techniques.",
        "scenario": "A game designer wants to set a fair payout for an event involving two dice. Before choosing a payout, the designer needs to know how often the event happens and how simulation compares with exact counting.",
        "concept": "Probability describes long-run regularity under a model. In data science, we often estimate probability from data, but we also use probability models to reason before data are collected. Events can be represented as Boolean conditions. Unions, intersections, and complements become `or`, `and`, and `not` operations in code.",
        "math": "For equally likely outcomes, P(A) = number of outcomes in A / number of possible outcomes. For two events, P(A union B) = P(A) + P(B) - P(A intersection B).",
        "data_note": "This lesson uses simulated dice because the true sample space is known. That makes it possible to compare empirical and theoretical probability.",
        "goals": [
            "Represent compound random events as Boolean conditions (`and`, `or`, `not`) in Pandas.",
            "Estimate empirical probabilities through large-scale Monte Carlo simulation.",
            "Calculate exact theoretical probabilities using combinatorial sample spaces and multi-indexing.",
            "Evaluate the long-run convergence of empirical simulation estimates to theoretical probabilities."
        ],
        "links": {
            "conceptual": "We model random outcomes under uncertainty to understand long-run event frequencies and probability rules.",
            "computational": "We use vectorized Boolean logic in Pandas to define events and compute empirical proportions across simulated trials.",
            "decision": "Accurate probability estimates allow the game designer to establish financially viable and fair payout rules."
        },
        "code_steps": [
            {
                "title": "Simulation Setup: Rolling Two Dice",
                "explanation": "We simulate 20,000 independent rolls of two fair six-sided dice using NumPy's random integer generator and store the outcomes in a DataFrame.",
                "code": COMMON_SETUP + """
# Simulate 20,000 rolls of two fair six-sided dice (integers from 1 to 6 inclusive)
rolls = pd.DataFrame({
    "die_1": rng.integers(1, 7, size=20_000),
    "die_2": rng.integers(1, 7, size=20_000),
})
# Calculate total sum of the two dice
rolls["total"] = rolls["die_1"] + rolls["die_2"]
rolls.head()
"""
            },
            {
                "title": "Empirical Probability Estimation via Boolean Logic",
                "explanation": "We define specific events (rolling a total of 7, rolling doubles) using Boolean masks and estimate their probabilities by calculating the mean of the boolean series.",
                "code": """# Define events as Boolean Series (True/False)
event_total_7 = rolls["total"].eq(7)
event_double = rolls["die_1"].eq(rolls["die_2"])

# Estimate empirical probabilities (mean of boolean series equals proportion of True values)
probability_summary = pd.Series({
    "P(total = 7)": event_total_7.mean(),
    "P(double)": event_double.mean(),
    "P(total = 7 and double)": (event_total_7 & event_double).mean(),
    "P(total = 7 or double)": (event_total_7 | event_double).mean(),
})
probability_summary.round(4)
"""
            },
            {
                "title": "Exact Theoretical Calculation via Sample Space",
                "explanation": "We construct the exact combinatorial sample space of all 36 possible outcomes using `pd.MultiIndex` to calculate the exact theoretical probabilities.",
                "code": """# Generate all 36 possible dice combinations (6 x 6 grid)
exact_outcomes = pd.MultiIndex.from_product(
    [range(1, 7), range(1, 7)],
    names=["die_1", "die_2"],
).to_frame(index=False)
exact_outcomes["total"] = exact_outcomes["die_1"] + exact_outcomes["die_2"]

# Define exact Boolean conditions on the complete sample space
exact_total_7 = exact_outcomes["total"].eq(7)
exact_double = exact_outcomes["die_1"].eq(exact_outcomes["die_2"])

# Calculate exact theoretical probabilities
pd.Series({
    "Exact P(total = 7)": exact_total_7.mean(),
    "Exact P(double)": exact_double.mean(),
    "Exact P(total = 7 or double)": (exact_total_7 | exact_double).mean(),
}).round(4)
"""
            },
            {
                "title": "Analyzing Long-Run Convergence",
                "explanation": "We demonstrate the Law of Large Numbers by tracking how the empirical probability estimate of rolling a 7 converges to the exact probability (0.1667) as sample size increases.",
                "code": """# Track probability estimation across increasing sample sizes
sample_sizes = [50, 100, 500, 1000, 5000, 20_000]
convergence = []
for n in sample_sizes:
    sample = rolls.head(n)
    convergence.append({
        "sample_size_n": n,
        "estimated_P_total_7": sample["total"].eq(7).mean(),
        "exact_probability": 6 / 36,
        "absolute_error": abs(sample["total"].eq(7).mean() - (6 / 36))
    })

pd.DataFrame(convergence).round(4)
"""
            }
        ],
        "checkpoint": "Explain why the simulated estimate changes with sample size but the exact probability does not.",
        "mistakes": [
            "Confusing an empirical simulation estimate with the exact mathematical probability.",
            "Adding P(A) and P(B) for overlapping events without subtracting the intersection P(A and B).",
            "Ignoring the underlying model assumption that the dice are fair and independent.",
        ],
        "practice": "Define a new event, such as `total >= 10`. Estimate it by simulation, compute it exactly across the 36-outcome sample space, and compare the two values.",
        "exit": "When in real-world data science would simulation be more useful or feasible than exact combinatorial counting?",
    },
    {
        "file": "03_conditional_probability_bayes.ipynb",
        "title": "Conditional Probability, Bayes Rule, And Sampling",
        "alignment": "1.3 conditional probability and Bayes' rule; 1.4 random sampling.",
        "scenario": "A safety analyst is asked to communicate risk from passenger data. The analyst must distinguish P(survived | group) from P(group | survived), because they answer different questions.",
        "concept": "Conditional probability restricts the reference group. P(A | B) means the probability of A among cases where B is true. Bayes' rule lets us reverse a conditional probability when we also know the base rates. In data science, many communication errors come from switching the condition and the outcome.",
        "math": "P(A | B) = P(A intersection B) / P(B). Bayes' rule: P(A | B) = P(B | A) P(A) / P(B).",
        "data_note": "Uses Titanic if `data/raw/titanic/train.csv` exists; otherwise uses a simulated table with the same kind of variables.",
        "goals": [
            "Distinguish between conditional probability `P(A|B)` and its reverse `P(B|A)` in practical decision contexts.",
            "Calculate marginal, joint, and conditional probabilities from tabular data using Pandas filtering and grouping.",
            "Apply Bayes' rule to invert conditional probabilities and incorporate population base rates.",
            "Evaluate sample-to-sample variability in conditional probability estimates across random sub-samples."
        ],
        "links": {
            "conceptual": "We model risk conditional on demographic and environmental factors to understand relative vulnerability and base rates.",
            "computational": "We use Pandas Boolean indexing and cross-tabulations (`pd.crosstab`, `.groupby`) to isolate conditional reference groups.",
            "decision": "Precise conditional risk communication prevents policy misallocation caused by confounding base rates with conditional risk."
        },
        "code_steps": [
            {
                "title": "Data Acquisition & Fallback Simulation",
                "explanation": "We load the Titanic passenger dataset from `data/raw/` if available; otherwise, we generate a statistically equivalent simulated dataset so the lesson remains standalone runnable.",
                "code": COMMON_SETUP + """
# Load real Titanic data if available, otherwise generate simulated passenger records
path = Path("data/raw/titanic/train.csv")
if path.exists():
    passengers = pd.read_csv(path).rename(
        columns={"Survived": "survived", "Sex": "sex", "Pclass": "pclass"}
    )
else:
    print(f"Notice: Missing {path}. Using fallback simulation. Download Titanic from Kaggle for graded work.")
    passengers = pd.DataFrame({
        "survived": rng.binomial(1, 0.38, 891),
        "sex": rng.choice(["female", "male"], 891, p=[0.36, 0.64]),
        "pclass": rng.choice([1, 2, 3], 891, p=[0.24, 0.21, 0.55]),
    })

passengers[["survived", "sex", "pclass"]].head()
"""
            },
            {
                "title": "Marginal vs. Conditional Probability",
                "explanation": "We calculate and contrast marginal survival rate P(survived), conditional survival rate given sex P(survived | female), and the reverse conditional probability P(female | survived).",
                "code": """# Define Boolean masks for survival and sex
survived = passengers["survived"].eq(1)
female = passengers["sex"].eq("female")

# Contrast marginal, conditional, and reverse conditional probabilities
pd.Series({
    "P(survived) [Marginal]": survived.mean(),
    "P(female) [Base Rate]": female.mean(),
    "P(survived | female) [Risk given group]": survived[female].mean(),
    "P(female | survived) [Group composition of survivors]": female[survived].mean(),
}).round(3)
"""
            },
            {
                "title": "Multi-Variable Conditional Risk Table",
                "explanation": "We group passengers by both sex and passenger class to analyze how conditional survival rates vary across intersecting demographic and socio-economic segments.",
                "code": """# Compute conditional survival rates across sex and passenger class
conditional_table = (
    passengers
    .groupby(["sex", "pclass"])["survived"]
    .agg(total_passengers="count", survivors="sum", survival_rate="mean")
    .sort_values("survival_rate", ascending=False)
)
conditional_table.round(3)
"""
            },
            {
                "title": "Sampling Variability in Conditional Estimates",
                "explanation": "We draw 30 random sub-samples (n=120 each) from the dataset to observe how much conditional probability estimates fluctuate due to sampling error.",
                "code": """# Simulate drawing 30 random samples of 120 passengers to check estimation stability
sample_estimates = []
for seed in range(30):
    sampled = passengers.sample(120, random_state=seed)
    sample_estimates.append(sampled.loc[sampled["sex"].eq("female"), "survived"].mean())

# Summarize the distribution of conditional survival estimates across samples
pd.Series(sample_estimates, name="estimated_P(survived|female)").describe().round(3)
"""
            }
        ],
        "checkpoint": "Write two sentences: one using P(survived | female) correctly and one using P(female | survived) correctly.",
        "mistakes": [
            "Reversing the condition and the outcome (the Prosecutor's Fallacy).",
            "Ignoring population base rates when interpreting conditional risk or Bayes' rule.",
            "Treating historical statistical associations as definitive proof of a causal survival mechanism.",
        ],
        "practice": "Choose another subgroup (e.g., `pclass == 1`), estimate its conditional survival probability, and compare the full-data estimate with repeated random samples of size 120.",
        "exit": "What critical risk information is lost when a probability is reported without explicitly naming its conditioning group?",
    },
    {
        "file": "04_discrete_random_variables.ipynb",
        "title": "Discrete Random Variables And Binomial Models",
        "alignment": "2.1 discrete distributions; 2.2 Bernoulli and binomial; 2.3 multinomial.",
        "scenario": "A product team expects a conversion probability near 0.35. If 20 users see a new flow, how many conversions would be ordinary and how many would be concerning?",
        "concept": "A random variable converts outcomes into numbers. For Bernoulli trials, each observation is success or failure. A binomial random variable counts successes in a fixed number of independent trials with the same success probability.",
        "math": "If X follows Binomial(n, p), then P(X = k) = C(n, k) p^k (1-p)^(n-k), E[X] = np, and Var(X) = np(1-p).",
        "data_note": "Uses simulation to isolate the binomial assumptions before applying the idea to real event data.",
        "goals": [
            "Model binary conversion processes using Bernoulli trials and Binomial random variables.",
            "Compare empirical simulation distributions against exact theoretical Binomial PMFs (`stats.binom.pmf`).",
            "Calculate expected value and variance for discrete count distributions.",
            "Use cumulative distribution functions (`cdf` and `sf`) to quantify tail probabilities for decision thresholds."
        ],
        "links": {
            "conceptual": "We model discrete count variability in user conversions under fixed trial numbers and constant success probabilities.",
            "computational": "We use SciPy's statistical distributions (`scipy.stats.binom`) to compute exact probability mass and cumulative tail areas.",
            "decision": "Tail probability thresholds distinguish between normal random conversion fluctuations and concerning operational anomalies."
        },
        "code_steps": [
            {
                "title": "Simulating Binomial Conversion Experiments",
                "explanation": "We simulate 5,000 independent experiments where 20 users interact with a product flow having a 35% baseline conversion probability.",
                "code": COMMON_SETUP + """
# Simulate 5,000 experiments of n=20 trials with p=0.35 conversion probability
n_trials = 20
p_success = 0.35
successes = rng.binomial(n=n_trials, p=p_success, size=5000)
successes_series = pd.Series(successes, name="conversions_per_20_users")

# Display summary statistics of simulated conversion counts
successes_series.describe().round(2)
"""
            },
            {
                "title": "Empirical vs. Theoretical PMF Comparison",
                "explanation": "We construct a side-by-side table comparing the empirical proportion of conversion counts from our simulation against the exact theoretical Binomial Probability Mass Function (PMF).",
                "code": """# Compare theoretical PMF with empirical simulation proportions across counts 0 to n_trials
x = np.arange(0, n_trials + 1)
binomial_pmf = pd.DataFrame({
    "conversions": x,
    "theoretical_probability": stats.binom.pmf(x, n_trials, p_success),
    "empirical_probability": successes_series.value_counts(normalize=True).reindex(x, fill_value=0).values,
})
binomial_pmf.head(12).round(4)
"""
            },
            {
                "title": "Visualizing the Probability Distribution",
                "explanation": "We plot the theoretical Binomial probability mass function as a bar chart to inspect the shape, center, and spread of expected conversion counts.",
                "code": """# Plot theoretical Binomial distribution
ax = sns.barplot(data=binomial_pmf, x="conversions", y="theoretical_probability", color="steelblue")
ax.set_title("Binomial Probability Model (n=20, p=0.35)", fontsize=14, pad=10)
ax.set_xlabel("Number of Conversions in 20 Trials", fontsize=11)
ax.set_ylabel("Probability Mass", fontsize=11)
plt.show()
"""
            },
            {
                "title": "Decision Thresholds & Tail Probabilities",
                "explanation": "We calculate expected successes, standard deviation, and evaluate specific decision thresholds using cumulative distribution functions (CDF and survival function SF).",
                "code": """# Compute theoretical moments and decision tail probabilities
pd.Series({
    "expected_conversions_E[X]": n_trials * p_success,
    "standard_deviation_SD(X)": np.sqrt(n_trials * p_success * (1 - p_success)),
    "P(5 or fewer conversions) [Low tail]": stats.binom.cdf(5, n_trials, p_success),
    "P(10 or more conversions) [High tail]": stats.binom.sf(9, n_trials, p_success),
}).round(4)
"""
            }
        ],
        "checkpoint": "Why is `10 or more successes` different from `exactly 10 successes` for a decision?",
        "mistakes": [
            "Using a binomial model when the success probability p changes across trials (violating constant rate).",
            "Forgetting that the binomial model counts total successes, ignoring the specific order of successes.",
            "Calling an operational outcome 'unusual' without defining a formal probability threshold beforehand.",
        ],
        "practice": "Change `p_success` to 0.20 and then 0.50. Explain in markdown how the expected value, distribution symmetry, and tail probabilities change.",
        "exit": "Name one real-world business or engineering situation where the binomial independence assumption is doubtful.",
    },
    {
        "file": "05_count_models.ipynb",
        "title": "Count Models: Geometric, Hypergeometric, And Poisson",
        "alignment": "2.4 geometric and negative binomial; 2.5 hypergeometric; 2.6 Poisson; 2.7 data science links.",
        "scenario": "A mobility planner wants to model hourly bike demand. A simple count model may help, but only if its assumptions are reasonable.",
        "concept": "Count models describe nonnegative integer outcomes. A Poisson model is useful for counts in a fixed interval when events occur independently at a roughly constant rate. Real data often violate that constant-rate assumption because time, weather, and context change demand.",
        "math": "If X follows Poisson(lambda), then P(X = k) = exp(-lambda) lambda^k / k!, and E[X] = Var(X) = lambda.",
        "data_note": "Uses Bike Sharing Demand if available; otherwise simulates counts with daily variation.",
        "goals": [
            "Model event occurrences over fixed intervals using the Poisson probability distribution.",
            "Check fundamental Poisson model assumptions by evaluating the variance-to-mean ratio (dispersion).",
            "Identify real-world overdispersion caused by time-varying rates and heterogeneous conditions.",
            "Use Poisson tail probabilities to evaluate infrastructure capacity and peak demand risks."
        ],
        "links": {
            "conceptual": "We model arrival counts per unit time while testing whether arrival rates remain constant across time intervals.",
            "computational": "We compute empirical variance-to-mean ratios in Pandas and evaluate Poisson survival functions (`stats.poisson.sf`) in SciPy.",
            "decision": "Detecting overdispersion prevents underestimating peak demand surges, guiding safer capacity and inventory planning."
        },
        "code_steps": [
            {
                "title": "Data Acquisition & Hourly Count Setup",
                "explanation": "We load the Kaggle Bike Sharing Demand dataset if available; otherwise, we simulate hourly bike counts incorporating morning and evening rush-hour peaks.",
                "code": COMMON_SETUP + """
# Load Bike Sharing Demand data or simulate time-varying hourly counts
path = Path("data/raw/bike-sharing/train.csv")
if path.exists():
    bike = pd.read_csv(path)
    counts = bike["count"].dropna()
else:
    print(f"Notice: Missing {path}. Using fallback simulation with rush-hour peaks.")
    hour = np.tile(np.arange(24), 60)
    # Rate varies significantly by hour: baseline 40, morning rush +90, evening rush +80
    rate = 40 + 90 * ((hour >= 7) & (hour <= 9)) + 80 * ((hour >= 17) & (hour <= 19))
    counts = pd.Series(rng.poisson(rate), name="hourly_bike_count")

counts.describe().round(2)
"""
            },
            {
                "title": "Checking the Poisson Dispersion Assumption",
                "explanation": "A theoretical Poisson distribution requires variance equal to mean (ratio = 1.0). We compute the empirical variance-to-mean ratio to check for overdispersion.",
                "code": """# Check Poisson assumption: Var(X) / E[X] should be approximately 1.0
mean_val = counts.mean()
var_val = counts.var(ddof=1)

pd.Series({
    "empirical_mean": mean_val,
    "empirical_variance": var_val,
    "variance_to_mean_ratio": var_val / mean_val,
    "is_overdispersed": (var_val / mean_val) > 1.5
}).round(2)
"""
            },
            {
                "title": "Visualizing Observed Count Distributions",
                "explanation": "We plot the histogram of hourly bike counts to inspect skewness, multi-modality, and extreme peak demand hours.",
                "code": """# Plot histogram of hourly demand counts
ax = sns.histplot(counts, bins=30, kde=True, color="seagreen")
ax.set_title("Observed Hourly Bike Demand Distribution", fontsize=14, pad=10)
ax.set_xlabel("Hourly Bike Rentals", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
plt.show()
"""
            },
            {
                "title": "Evaluating Capacity Risk via Tail Probabilities",
                "explanation": "We estimate the probability of exceeding the 90th percentile demand threshold under both the empirical data and a naive single-rate Poisson model.",
                "code": """# Compare empirical peak risk against naive Poisson model predictions
lambda_hat = counts.mean()
threshold = counts.quantile(0.90)

pd.Series({
    "estimated_lambda": lambda_hat,
    "90th_percentile_capacity_threshold": threshold,
    "observed_P(demand >= threshold)": (counts >= threshold).mean(),
    "naive_poisson_P(demand >= threshold)": stats.poisson.sf(threshold - 1, lambda_hat),
}).round(4)
"""
            }
        ],
        "checkpoint": "Use the variance-to-mean ratio to decide whether a single Poisson model is plausible.",
        "mistakes": [
            "Assuming all count data automatically follow a Poisson distribution without checking dispersion.",
            "Ignoring time segmentation when the underlying event rate clearly changes across hours or seasons.",
            "Comparing only averages across groups while ignoring massive differences in variance and extreme peaks.",
        ],
        "practice": "Create two time segments, such as high-demand rush hours and low-demand off-peak hours. Compare the mean, variance, and variance-to-mean ratio for each segment independently.",
        "exit": "What does 'overdispersion' mean in practical operational planning language?",
    },
    {
        "file": "06_continuous_random_variables.ipynb",
        "title": "Continuous Random Variables And Expected Value",
        "alignment": "3.1 density functions; 3.2 expected value; 3.3 uniform and normal distributions.",
        "scenario": "A pricing analyst needs to summarize sale prices. A mean alone is easy to report, but it may hide skewness, outliers, and uncertainty.",
        "concept": "Continuous variables describe measurements rather than counts. A density curve does not give probability by height alone; probability is area over an interval. Expected value is a long-run center of mass for a distribution, but it can be sensitive to skewed values.",
        "math": "For a continuous random variable, P(a <= X <= b) is the area under the density from a to b. The expected value is an integral, but in data we estimate it with the sample mean.",
        "data_note": "Uses House Prices if available; otherwise simulates a skewed positive variable.",
        "goals": [
            "Analyze continuous measurement data using probability density functions (PDFs) and empirical histograms.",
            "Calculate and contrast expected value (mean), median, standard deviation, and skewness.",
            "Interpret probability as area under a density curve across defined numerical intervals.",
            "Evaluate z-scores and compare empirical data spread against Normal distribution benchmarks."
        ],
        "links": {
            "conceptual": "We model continuous monetary or physical measurements where skewness and outliers distort simple averages.",
            "computational": "We use SciPy (`stats.skew`, `stats.norm`) and Seaborn kernel density estimates (`kde=True`) to visualize continuous distributions.",
            "decision": "Reporting medians alongside means prevents skewed outlier values from misleading pricing and valuation decisions."
        },
        "code_steps": [
            {
                "title": "Loading Continuous Measurement Data",
                "explanation": "We load the Kaggle House Prices dataset if available; otherwise, we generate a lognormal simulated dataset representing skewed positive property values.",
                "code": COMMON_SETUP + """
# Load House Prices dataset or simulate skewed property values
path = Path("data/raw/house-prices/train.csv")
if path.exists():
    homes = pd.read_csv(path)
    values = homes["SalePrice"].dropna()
else:
    print(f"Notice: Missing {path}. Using fallback lognormal simulation for property values.")
    values = pd.Series(rng.lognormal(mean=12.0, sigma=0.35, size=1200), name="SalePrice")

values.describe().round(2)
"""
            },
            {
                "title": "Comprehensive Shape & Skewness Analysis",
                "explanation": "We calculate empirical summary statistics including mean, median, standard deviation, 10th/90th quantiles, and Fisher-Pearson skewness.",
                "code": """# Compute robust summary metrics and skewness
summary = pd.Series({
    "mean_expected_value": values.mean(),
    "median_50th_percentile": values.median(),
    "standard_deviation": values.std(ddof=1),
    "10th_percentile": values.quantile(0.10),
    "90th_percentile": values.quantile(0.90),
    "skewness_index": stats.skew(values),
})
summary.round(2)
"""
            },
            {
                "title": "Visualizing Density & Center of Mass",
                "explanation": "We plot the histogram and Kernel Density Estimate (KDE), overlaying vertical reference lines for the mean and median to highlight right-skewness.",
                "code": """# Plot continuous distribution with mean and median reference lines
ax = sns.histplot(values, kde=True, color="darkslateblue", bins=35)
ax.axvline(values.mean(), color="red", linestyle="--", linewidth=2, label=f"Mean: {values.mean():,.0f}")
ax.axvline(values.median(), color="gold", linestyle=":", linewidth=2, label=f"Median: {values.median():,.0f}")
ax.set_title("Continuous Measurement Distribution with KDE Density", fontsize=14, pad=10)
ax.set_xlabel("Sale Price ($)", fontsize=11)
ax.set_ylabel("Density / Frequency", fontsize=11)
ax.legend()
plt.show()
"""
            },
            {
                "title": "Z-Scores & Normal Distribution Benchmarking",
                "explanation": "We standardize observations into z-scores and compare the proportion of data within 1 standard deviation against the theoretical Normal distribution expectation (68.27%).",
                "code": """# Standardize data into z-scores and check empirical spread vs Normal benchmark
z_score = (values - values.mean()) / values.std(ddof=1)

pd.Series({
    "empirical_share_within_1_SD": z_score.between(-1, 1).mean(),
    "normal_model_expectation_1_SD": stats.norm.cdf(1) - stats.norm.cdf(-1),
    "empirical_share_within_2_SD": z_score.between(-2, 2).mean(),
    "normal_model_expectation_2_SD": stats.norm.cdf(2) - stats.norm.cdf(-2),
}).round(4)
"""
            }
        ],
        "checkpoint": "When mean and median differ significantly, which one would you report to a nontechnical stakeholder and why?",
        "mistakes": [
            "Interpreting the vertical height of a density curve as a direct probability (probability is area over an interval).",
            "Using a Normal distribution model without checking for severe skewness or outliers.",
            "Reporting a central average without describing the spread and range of the distribution.",
        ],
        "practice": "Apply a logarithmic transformation (`np.log(values)`) to the property values. Recompute the mean, median, skewness, and plot the new density curve. Discuss how symmetry changes.",
        "exit": "What does it mean mathematically and conceptually to say that probability is area under a density curve?",
    },
    {
        "file": "07_distribution_fitting.ipynb",
        "title": "Distribution Fitting, Transformations, And Moment Ideas",
        "alignment": "3.3 normal distribution; 3.3 gamma-type distributions; 3.4 moment-generating function.",
        "scenario": "An analyst must decide whether to model a positive measurement on its original scale or after a log transformation. The choice affects forecasts and intervals.",
        "concept": "Distribution fitting is not about forcing data to match a named curve. It is about deciding whether a model captures the features that matter for the decision. Transformations can make skewed positive data easier to model, but conclusions must be translated back carefully.",
        "math": "Moments summarize distribution shape. The first moment relates to center, the second to spread, and higher moments to skewness or tail behavior.",
        "data_note": "Uses a skewed positive measurement so students can compare original and log scales.",
        "goals": [
            "Fit parametric statistical distributions (Normal, Gamma) to empirical measurement data using maximum likelihood estimation.",
            "Apply logarithmic transformations to normalize skewed positive variables for statistical modeling.",
            "Compare statistical moments (mean, variance, skewness) across original and transformed measurement scales.",
            "Translate log-scale model inferences back into original operational units for stakeholder decision making."
        ],
        "links": {
            "conceptual": "We fit parametric probability models to capture essential distributional moments and tail behaviors.",
            "computational": "We use SciPy distribution fitting (`stats.norm.fit`, `stats.gamma.fit`) and logarithmic transformations (`np.log`, `np.exp`).",
            "decision": "Selecting the appropriate parametric model ensures that tail-risk estimates and forecasting intervals are reliable."
        },
        "code_steps": [
            {
                "title": "Simulating Skewed Data & Log Transformation",
                "explanation": "We generate a skewed positive dataset and compute its natural logarithm, creating two parallel scales for modeling comparison.",
                "code": COMMON_SETUP + """
# Simulate skewed positive measurement values and create log-transformed scale
values = pd.Series(rng.lognormal(mean=11.9, sigma=0.45, size=1000), name="original_value")
log_values = np.log(values)

# Display head of both scales
pd.DataFrame({"original_scale": values, "log_scale": log_values}).head()
"""
            },
            {
                "title": "Comparing Statistical Moments Across Scales",
                "explanation": "We calculate and compare the first three statistical moments (mean, standard deviation, skewness) on both the original and logarithmic scales.",
                "code": """# Contrast moments across original and log-transformed scales
comparison = pd.DataFrame({
    "scale": ["original_positive_units", "log_transformed_units"],
    "mean_1st_moment": [values.mean(), log_values.mean()],
    "std_2nd_moment": [values.std(ddof=1), log_values.std(ddof=1)],
    "skewness_3rd_moment": [stats.skew(values), stats.skew(log_values)],
})
comparison.round(3)
"""
            },
            {
                "title": "Visualizing Scale Transformation Effects",
                "explanation": "We plot side-by-side histograms with KDE curves to visually verify how the logarithmic transformation removes right-skewness and restores symmetry.",
                "code": """# Plot side-by-side comparison of original vs log-transformed distributions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(values, kde=True, ax=axes[0], color="indianred", bins=30)
axes[0].set_title("Original Scale (Right-Skewed)", fontsize=13)
axes[0].set_xlabel("Original Units")

sns.histplot(log_values, kde=True, ax=axes[1], color="teal", bins=30)
axes[1].set_title("Logarithmic Scale (Symmetric / Normal)", fontsize=13)
axes[1].set_xlabel("Log Units")
plt.tight_layout()
plt.show()
"""
            },
            {
                "title": "Parametric Fitting & Tail Risk Evaluation",
                "explanation": "We fit a Normal distribution to the log scale and a Gamma distribution to the original scale, then compare how accurately each model predicts top 10% tail risk.",
                "code": """# Fit Normal model to log scale and Gamma model to original scale
normal_fit_log = stats.norm.fit(log_values)  # returns (loc, scale)
gamma_fit_original = stats.gamma.fit(values, floc=0)  # returns (shape, loc, scale)

# Evaluate tail probability above the empirical 90th percentile
threshold_90 = values.quantile(0.90)
prob_large_original = (values > threshold_90).mean()

# Translate threshold to log scale to check Normal model survival function
normal_model_tail_prob = stats.norm.sf(np.log(threshold_90), loc=normal_fit_log[0], scale=normal_fit_log[1])
gamma_model_tail_prob = stats.gamma.sf(threshold_90, *gamma_fit_original)

pd.Series({
    "empirical_tail_probability": prob_large_original,
    "lognormal_model_tail_prediction": normal_model_tail_prob,
    "gamma_model_tail_prediction": gamma_model_tail_prob,
}).round(4)
"""
            }
        ],
        "checkpoint": "Why might the log scale be better for statistical modeling but the original scale better for stakeholder communication?",
        "mistakes": [
            "Choosing a distribution solely because its histogram looks visually similar without checking tail behavior.",
            "Forgetting to apply the inverse transformation (`np.exp`) when reporting log-scale model conclusions back to stakeholders.",
            "Treating fitted parametric coefficients as absolute universal truths rather than sample-dependent estimates.",
        ],
        "practice": "Fit an Exponential or Weibull distribution (`stats.expon.fit`, `stats.weibull_min.fit`) to `values`. Compare its 90th percentile tail prediction against the empirical data.",
        "exit": "What essential feature of a probability distribution is measured by the third statistical moment (skewness)?",
    },
    {
        "file": "08_sampling_distributions_bootstrap.ipynb",
        "title": "Sampling Distributions And Bootstrap Intuition",
        "alignment": "4.1 transformations; 4.2 functions of random variables; 4.3 sampling distribution of the mean.",
        "scenario": "A public-policy analyst has one sample and one average score. The stakeholder wants to know how much that average would vary if a different sample had been collected.",
        "concept": "A statistic is a number computed from a sample, but it varies from sample to sample. A sampling distribution describes that variation. The bootstrap approximates sampling variation by repeatedly resampling from the observed data.",
        "math": "For independent observations with standard deviation sigma, the standard error of the mean is approximately sigma / sqrt(n). In practice sigma is often estimated by the sample standard deviation.",
        "data_note": "Uses simulated score data to make repeated sampling visible.",
        "goals": [
            "Distinguish between the distribution of individual observations and the sampling distribution of a sample statistic.",
            "Calculate the theoretical standard error of the mean (`s / sqrt(n)`) from a single observed sample.",
            "Implement non-parametric Bootstrap resampling using Pandas `.sample(replace=True)` to simulate sampling variability.",
            "Construct and interpret 95% Bootstrap confidence intervals to quantify estimation precision."
        ],
        "links": {
            "conceptual": "We model sample-to-sample variability (standard error) to understand how much a sample mean fluctuates around the true population parameter.",
            "computational": "We use list comprehensions and Pandas resampling with replacement (`replace=True`) to computationally generate bootstrap distributions.",
            "decision": "Quantifying sampling variability prevents stakeholders from overreacting to minor sample-to-sample fluctuations."
        },
        "code_steps": [
            {
                "title": "Population Setup & Single Sample Extraction",
                "explanation": "We generate a large reference population of 50,000 policy scores and extract a single operational sample of n=120 observations to compute initial sample statistics.",
                "code": COMMON_SETUP + """
# Create reference population of 50,000 scores and draw a single sample of n=120
population = pd.Series(rng.normal(loc=6.2, scale=1.1, size=50_000), name="policy_score").clip(0, 10)
sample = population.sample(n=120, random_state=1001)

# Compute single sample statistics and theoretical standard error of the mean
pd.Series({
    "sample_mean_xbar": sample.mean(),
    "sample_sd_s": sample.std(ddof=1),
    "theoretical_standard_error_(s/sqrt(n))": sample.std(ddof=1) / np.sqrt(len(sample)),
}).round(4)
"""
            },
            {
                "title": "True Sampling Distribution (Repeated Sampling)",
                "explanation": "To demonstrate what a sampling distribution is, we draw 1,000 independent samples directly from the known population and inspect the distribution of their sample means.",
                "code": """# Draw 1,000 independent samples from population to observe true sampling variability
repeated_means = []
for seed in range(1000):
    repeated_sample = population.sample(n=120, random_state=seed)
    repeated_means.append(repeated_sample.mean())

# Summarize the true sampling distribution of the mean
pd.Series(repeated_means, name="true_sampling_distribution_means").describe().round(4)
"""
            },
            {
                "title": "Bootstrap Resampling from a Single Sample",
                "explanation": "In real data science, we only have one sample. We use Bootstrap resampling (drawing n=120 with replacement from our single sample 1,000 times) to approximate the sampling distribution.",
                "code": """# Generate 1,000 bootstrap resamples from our single observed sample
bootstrap_means = [
    sample.sample(n=len(sample), replace=True, random_state=seed).mean()
    for seed in range(1000)
]

# Calculate 95% Bootstrap percentile confidence interval
pd.Series(bootstrap_means, name="bootstrap_means").quantile([0.025, 0.50, 0.975]).round(4)
"""
            },
            {
                "title": "Visualizing Bootstrap vs. Sample Mean",
                "explanation": "We plot the histogram of the 1,000 Bootstrap sample means, marking the original sample mean and the 95% confidence interval bounds.",
                "code": """# Plot Bootstrap sampling distribution with confidence bounds
ax = sns.histplot(bootstrap_means, kde=True, color="royalblue", bins=30)
ax.axvline(sample.mean(), color="red", linestyle="--", linewidth=2, label=f"Sample Mean: {sample.mean():.2f}")
ci_low, ci_high = np.quantile(bootstrap_means, [0.025, 0.975])
ax.axvline(ci_low, color="black", linestyle=":", linewidth=1.5, label=f"95% CI: [{ci_low:.2f}, {ci_high:.2f}]")
ax.axvline(ci_high, color="black", linestyle=":", linewidth=1.5)
ax.set_title("Bootstrap Sampling Distribution of the Mean (n=120)", fontsize=14, pad=10)
ax.set_xlabel("Bootstrap Sample Mean", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.legend()
plt.show()
"""
            }
        ],
        "checkpoint": "Explain in your own words the difference between the distribution of individual scores and the sampling distribution of sample means.",
        "mistakes": [
            "Thinking that Bootstrap resampling creates new independent data from nothing (it only approximates sampling variability).",
            "Confusing the standard deviation of individual observations (`s`) with the standard error of a sample statistic (`s / sqrt(n)`).",
            "Assuming Bootstrap intervals are valid when the initial sample was collected with severe selection bias.",
        ],
        "practice": "Repeat the Bootstrap resampling procedure using simulated sample sizes of `n=40` and `n=300`. Compare the width of the resulting 95% confidence intervals.",
        "exit": "Why does statistical uncertainty (standard error) shrink as the sample size `n` increases?",
    },
    {
        "file": "09_inferential_distributions.ipynb",
        "title": "Chi-square, t, And F Distributions For Inference",
        "alignment": "4.4 chi-square; 4.5 t; 4.6 F; 4.7 data science links.",
        "scenario": "A quality analyst must decide whether a process mean differs from a target when the population variance is unknown.",
        "concept": "Inferential distributions appear when statistics are standardized. The t distribution accounts for uncertainty from estimating the standard deviation. Chi-square distributions arise in variance and categorical-count settings. F distributions arise in variance ratios and ANOVA.",
        "math": "For a one-sample mean with unknown variance, t = (xbar - mu0) / (s / sqrt(n)), with n - 1 degrees of freedom.",
        "data_note": "Uses a simulated process measurement so the role of the reference distribution is clear.",
        "goals": [
            "Select the appropriate inferential reference distribution (`t`, `chi-square`, `F`) based on the statistical estimation task.",
            "Calculate one-sample t-statistics and p-values using degrees of freedom (`df = n - 1`) when population variance is unknown.",
            "Construct exact parametric t-distribution confidence intervals using SciPy (`stats.t.interval`).",
            "Interpret degrees of freedom as an adjustment for estimation uncertainty in small samples."
        ],
        "links": {
            "conceptual": "We model standardized inferential statistics under null hypotheses to quantify how surprising an observed sample metric is.",
            "computational": "We use SciPy statistical probability functions (`stats.t.sf`, `stats.t.ppf`, `stats.t.interval`) to evaluate critical values and p-values.",
            "decision": "Using exact inferential distributions prevents false-positive decisions in small samples where Normal approximations fail."
        },
        "code_steps": [
            {
                "title": "Process Measurement & T-Statistic Calculation",
                "explanation": "We simulate 25 manufacturing process measurements, define a quality target of 9.0, and manually compute the one-sample t-statistic and two-sided p-value.",
                "code": COMMON_SETUP + """
# Simulate n=25 process measurements against a target of 9.0
target = 9.0
measurements = pd.Series(rng.normal(loc=10.0, scale=2.5, size=25), name="process_measurement")

# Calculate sample mean, sample standard deviation, and standardized t-statistic
xbar = measurements.mean()
s = measurements.std(ddof=1)
n = len(measurements)
t_stat = (xbar - target) / (s / np.sqrt(n))
p_value = 2 * stats.t.sf(abs(t_stat), df=n - 1)

pd.Series({
    "sample_mean_xbar": xbar,
    "sample_sd_s": s,
    "t_statistic": t_stat,
    "degrees_of_freedom": n - 1,
    "two_sided_p_value": p_value,
}).round(4)
"""
            },
            {
                "title": "Reference Guide: When to Use t, Chi-Square, and F",
                "explanation": "We construct an architectural reference table summarizing the typical data science questions and 95th percentile critical values for key inferential distributions.",
                "code": """# Reference guide for inferential distributions
reference = pd.DataFrame({
    "distribution": ["Student's t", "Chi-Square (chi2)", "Fisher's F"],
    "primary_application": [
        "Inference for means with unknown population variance",
        "Inference for sample variance & categorical independence",
        "Comparing ratios of variances & ANOVA group comparisons",
    ],
    "example_95th_percentile_val_(df=24)": [
        stats.t.ppf(0.95, df=24),
        stats.chi2.ppf(0.95, df=24),
        stats.f.ppf(0.95, dfn=3, dfd=24),
    ],
})
reference.round(3)
"""
            },
            {
                "title": "Parametric T-Distribution Confidence Interval",
                "explanation": "We use SciPy's automated `stats.t.interval` method to calculate the exact 95% confidence interval for the process mean and compare it against the target value.",
                "code": """# Compute 95% confidence interval using Student's t-distribution
ci_low, ci_high = stats.t.interval(
    confidence=0.95,
    df=n - 1,
    loc=xbar,
    scale=s / np.sqrt(n),
)

pd.Series({
    "target_val": target,
    "sample_mean": xbar,
    "95%_CI_lower_bound": ci_low,
    "95%_CI_upper_bound": ci_high,
    "target_is_within_CI": ci_low <= target <= ci_high
}).round(4)
"""
            },
            {
                "title": "Visualizing Sample Distribution vs. Target",
                "explanation": "We plot the histogram of the 25 process measurements, highlighting the target specification line versus the observed sample mean.",
                "code": """# Plot measurement distribution against quality target
ax = sns.histplot(measurements, bins=10, kde=True, color="darkorange")
ax.axvline(target, color="red", linestyle="--", linewidth=2, label=f"Target Specification ({target})")
ax.axvline(xbar, color="black", linestyle=":", linewidth=2, label=f"Sample Mean ({xbar:.2f})")
ax.set_title("Process Measurements vs. Target Specification (n=25)", fontsize=14, pad=10)
ax.set_xlabel("Measurement Unit", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.legend()
plt.show()
"""
            }
        ],
        "checkpoint": "Why must we use a Student's t-distribution instead of a standard Normal distribution when evaluating this sample of 25 measurements?",
        "mistakes": [
            "Using the standard Normal distribution (z-scores) when population variance is unknown and sample size is small.",
            "Treating degrees of freedom as a decorative formula parameter rather than an essential adjustment for sample uncertainty.",
            "Reporting a standalone p-value without stating the point estimate, effect size, and confidence interval.",
        ],
        "practice": "Change the sample size from `n=25` to `n=10` and then `n=100` in the simulation. Observe and explain how the t-distribution critical value and CI width change.",
        "exit": "What specific role does the estimated standard error (`s / sqrt(n)`) play in the denominator of the t-statistic?",
    },
    {
        "file": "10_estimation_confidence_intervals.ipynb",
        "title": "Point Estimation And Confidence Intervals",
        "alignment": "5.1 point estimation; 5.2 intervals; 5.3 means; 5.4 standard error; 5.5 proportions.",
        "scenario": "A survey team needs to estimate average satisfaction and support for a policy. A point estimate alone is too precise for decision making.",
        "concept": "Estimation separates what the sample says from what we infer about the population. A confidence interval is a procedure that, under its assumptions, captures the true parameter at a stated long-run rate. It is not a probability statement about one fixed parameter after the interval is computed.",
        "math": "A common interval structure is estimate +/- critical value times standard error.",
        "data_note": "Uses simulated survey data with one numeric score and one binary support variable.",
        "goals": [
            "Calculate point estimates and standard errors for continuous means and binary proportions.",
            "Construct parametric 95% confidence intervals for means using the t-distribution.",
            "Construct normal-approximation 95% confidence intervals for binary proportions (`p_hat +/- z*SE`).",
            "Interpret confidence interval widths and confidence levels correctly in stakeholder communication."
        ],
        "links": {
            "conceptual": "We model estimation uncertainty to establish plausible bounds for unknown population parameters.",
            "computational": "We combine SciPy interval methods (`stats.t.interval`) with NumPy standard error formulas (`np.sqrt(p*(1-p)/n)`).",
            "decision": "Interval estimates prevent executives from making false policy commitments based on imprecise point averages."
        },
        "code_steps": [
            {
                "title": "Survey Data Simulation & Inspection",
                "explanation": "We generate a simulated survey dataset of n=180 respondents containing a continuous satisfaction score (0-100) and a binary policy support indicator (True/False).",
                "code": COMMON_SETUP + """
# Simulate survey responses for n=180 citizens
survey = pd.DataFrame({
    "satisfaction_score": rng.normal(loc=72, scale=12, size=180).clip(0, 100),
    "supports_policy": rng.binomial(n=1, p=0.58, size=180),  # 58% true population support
})
survey.head()
"""
            },
            {
                "title": "Confidence Interval for a Continuous Mean",
                "explanation": "We compute the sample mean satisfaction score, its standard error, and the exact 95% Student's t-distribution confidence interval.",
                "code": """# Estimate continuous population mean satisfaction
mean_est = survey["satisfaction_score"].mean()
mean_se = survey["satisfaction_score"].std(ddof=1) / np.sqrt(len(survey))
mean_ci = stats.t.interval(
    confidence=0.95,
    df=len(survey) - 1,
    loc=mean_est,
    scale=mean_se,
)

pd.Series({
    "point_estimate_mean": mean_est,
    "standard_error": mean_se,
    "95%_CI_lower": mean_ci[0],
    "95%_CI_upper": mean_ci[1],
    "margin_of_error": (mean_ci[1] - mean_ci[0]) / 2
}).round(3)
"""
            },
            {
                "title": "Confidence Interval for a Binary Proportion",
                "explanation": "We compute the sample proportion of policy supporters, calculate the proportion standard error `sqrt(p*(1-p)/n)`, and derive the 95% normal-approximation interval (`z=1.96`).",
                "code": """# Estimate binary population proportion supporting policy
p_hat = survey["supports_policy"].mean()
n = len(survey)
prop_se = np.sqrt(p_hat * (1 - p_hat) / n)
prop_ci = (p_hat - 1.96 * prop_se, p_hat + 1.96 * prop_se)

pd.Series({
    "point_estimate_proportion": p_hat,
    "proportion_standard_error": prop_se,
    "95%_CI_lower": prop_ci[0],
    "95%_CI_upper": prop_ci[1],
    "margin_of_error": 1.96 * prop_se
}).round(4)
"""
            },
            {
                "title": "Verifying Proportion Interval via Bootstrap",
                "explanation": "We draw 1,000 bootstrap resamples of the binary support column to check if the non-parametric bootstrap percentile interval matches our normal approximation.",
                "code": """# Verify proportion confidence bounds using 1,000 bootstrap resamples
bootstrap_support = [
    survey.sample(n=len(survey), replace=True, random_state=seed)["supports_policy"].mean()
    for seed in range(1000)
]

bootstrap_ci = pd.Series(bootstrap_support).quantile([0.025, 0.50, 0.975])
pd.DataFrame({
    "Normal_Approximation_CI": [prop_ci[0], p_hat, prop_ci[1]],
    "Bootstrap_Percentile_CI": bootstrap_ci.values
}, index=["Lower_2.5%", "Point_Estimate", "Upper_97.5%"]).round(4)
"""
            }
        ],
        "checkpoint": "Would you claim that a definitive majority of the population supports the policy? Justify your answer using the confidence interval, not just the sample proportion.",
        "mistakes": [
            "Saying 'there is a 95% probability that the true parameter lies in this specific numerical interval' (the parameter is fixed; confidence is in the long-run procedure).",
            "Reporting a numerical confidence interval without explicitly stating the confidence level (e.g., 90%, 95%, 99%).",
            "Ignoring whether the underlying survey sample was collected via random sampling versus biased convenience sampling.",
        ],
        "practice": "Recalculate the satisfaction confidence interval using simulated sample sizes of `n=60` and `n=600`. Explain how the margin of error changes as sample size scales.",
        "exit": "What is the fundamental difference between a point estimate and a confidence interval estimate?",
    },
    {
        "file": "11_sample_size_variance.ipynb",
        "title": "Variance Estimation And Sample Size Planning",
        "alignment": "5.6 variance and ratio of variances; 5.7 sample size estimation.",
        "scenario": "An operations manager wants a precise estimate of cycle time. More precision requires more observations, which costs time and money.",
        "concept": "Variance describes variability, not error. Sample size planning connects statistical precision to operational cost. Before collecting data, analysts should decide what margin of error is useful enough for the decision.",
        "math": "For estimating a mean, a planning approximation is n = (z* sigma / E)^2, where E is the target margin of error.",
        "data_note": "Uses simulated process data for two production lines.",
        "goals": [
            "Calculate and compare sample variances and standard deviations across operational segments.",
            "Compute variance ratios (`s2_B / s2_A`) to evaluate homogeneity of variance assumptions.",
            "Apply sample size planning formulas (`n = (z*sigma / E)^2`) to achieve targeted margins of error.",
            "Evaluate the quadratic cost trade-off between statistical precision and data collection expense."
        ],
        "links": {
            "conceptual": "We model process variability and planning precision to determine how much empirical evidence is required.",
            "computational": "We use Pandas aggregation (`.var`, `.std`) and vectorized NumPy power calculations (`np.ceil`) for sample size planning.",
            "decision": "Sample size planning ensures data collection budgets are spent efficiently without collecting under-powered or wasteful samples."
        },
        "code_steps": [
            {
                "title": "Production Line Data Simulation",
                "explanation": "We simulate cycle-time measurements across two manufacturing lines (Line A and Line B, n=90 each) having different underlying variances.",
                "code": COMMON_SETUP + """
# Simulate cycle times for Line A (low variance) and Line B (high variance)
process = pd.DataFrame({
    "line": np.repeat(["Line_A", "Line_B"], 90),
    "cycle_time": np.r_[rng.normal(loc=10.0, scale=1.1, size=90), rng.normal(loc=10.4, scale=1.8, size=90)],
})

# Summarize count, mean, standard deviation, and variance by line
process.groupby("line")["cycle_time"].agg(
    count="count", mean="mean", std="std", variance="var"
).round(3)
"""
            },
            {
                "title": "Evaluating Variance Ratios",
                "explanation": "We isolate the cycle times for both lines and compute the ratio of variances (`Var_B / Var_A`) to quantify operational dispersion differences.",
                "code": """# Compute sample variances and variance ratio
line_a = process.loc[process["line"].eq("Line_A"), "cycle_time"]
line_b = process.loc[process["line"].eq("Line_B"), "cycle_time"]
var_ratio = line_b.var(ddof=1) / line_a.var(ddof=1)

pd.Series({
    "variance_Line_A": line_a.var(ddof=1),
    "variance_Line_B": line_b.var(ddof=1),
    "variance_ratio_(B_to_A)": var_ratio,
    "is_variance_more_than_double": var_ratio > 2.0
}).round(3)
"""
            },
            {
                "title": "Sample Size Planning for Targeted Precision",
                "explanation": "Using the pooled standard deviation estimate, we calculate the required sample size `n` needed to achieve margins of error of 0.50, 0.25, and 0.10 units at 95% confidence (`z=1.96`).",
                "code": """# Calculate required sample size across tightening margins of error E
est_sigma = process["cycle_time"].std(ddof=1)
planning = pd.DataFrame({"target_margin_of_error_E": [0.50, 0.25, 0.10, 0.05]})

# Apply planning formula: n = ceil( (z * sigma / E)^2 )
planning["required_sample_size_n"] = np.ceil((1.96 * est_sigma / planning["target_margin_of_error_E"]) ** 2).astype(int)
planning["relative_data_cost_multiplier"] = (planning["required_sample_size_n"] / planning["required_sample_size_n"].iloc[0]).round(1)
planning
"""
            },
            {
                "title": "Visualizing Operational Variability",
                "explanation": "We plot side-by-side boxplots of cycle times by production line to visually contrast spread, interquartile ranges, and operational stability.",
                "code": """# Plot cycle time distributions across production lines
ax = sns.boxplot(data=process, x="line", y="cycle_time", palette="Set2", width=0.4)
ax.set_title("Cycle-Time Variability by Production Line", fontsize=14, pad=10)
ax.set_xlabel("Production Line", fontsize=11)
ax.set_ylabel("Cycle Time (Minutes)", fontsize=11)
plt.show()
"""
            }
        ],
        "checkpoint": "Why does cutting the target margin of error in half (e.g., from 0.50 to 0.25) require four times as many observations rather than twice as many?",
        "mistakes": [
            "Treating sample size planning as a purely statistical exercise while ignoring practical data collection costs and feasibility.",
            "Comparing group averages using standard tests while ignoring massive disparities in group variances.",
            "Using an arbitrary planning standard deviation (`sigma`) without empirical justification or pilot study data.",
        ],
        "practice": "Choose a practical margin of error that would be meaningful for an operations manager. Compute the required sample size `n` and write a brief justification of whether collecting that much data is financially realistic.",
        "exit": "What practical operational question should be answered before deciding on a target margin of error?",
    },
    {
        "file": "12_hypothesis_testing.ipynb",
        "title": "Hypothesis Testing For Decision Making",
        "alignment": "6.1 elements; 6.2 intervals and tests; 6.3 p-values; 6.4-6.7 tests for means, proportions, and variances.",
        "scenario": "A product owner wants to know whether a treatment page should replace a control page. The analysis must separate statistical evidence from practical business value.",
        "concept": "A hypothesis test asks whether the observed data would be surprising if a null claim were true. The p-value is not the probability that the null is true. It is a probability of data at least as extreme as what was observed, calculated under the null model.",
        "math": "For two proportions, the practical effect is p_treatment - p_control. A test can evaluate evidence against equal conversion rates, but the decision should also consider effect size.",
        "data_note": "Uses a simulated A/B test unless Kaggle A/B testing files are later connected.",
        "goals": [
            "Formulate null (`H0`) and alternative (`H1`) hypotheses for comparative A/B testing experiments.",
            "Execute two-sample contingency tests (`stats.chi2_contingency`) to evaluate conversion rate differences.",
            "Interpret p-values correctly as conditional probabilities under the null model, not as probabilities of the null itself.",
            "Differentiate between statistical significance ($p < 0.05$) and practical business significance (effect size lift)."
        ],
        "links": {
            "conceptual": "We model experimental conversion differences under a null hypothesis of no effect to rigorously test design changes.",
            "computational": "We use Pandas cross-tabulations (`pd.crosstab`) and SciPy chi-square tests (`stats.chi2_contingency`) to compute test statistics.",
            "decision": "Requiring both statistical significance and practical effect size lift prevents adopting costly modifications that yield trivial gains."
        },
        "code_steps": [
            {
                "title": "A/B Test Simulation & Conversion Summary",
                "explanation": "We simulate an A/B test with 1,000 users in Control (10% baseline conversion) and 1,000 users in Treatment (12.5% conversion), then compute group conversion rates.",
                "code": COMMON_SETUP + """
# Simulate A/B test records (n=1000 per group)
ab = pd.DataFrame({
    "group": np.repeat(["control", "treatment"], 1000),
    "converted": np.r_[rng.binomial(n=1, p=0.10, size=1000), rng.binomial(n=1, p=0.125, size=1000)],
})

# Calculate conversion rates by group
conversion_rates = ab.groupby("group")["converted"].agg(total_users="count", conversions="sum", rate="mean")
conversion_rates.round(4)
"""
            },
            {
                "title": "Contingency Table & Chi-Square Test of Independence",
                "explanation": "We construct a 2x2 contingency table of group versus conversion status and execute a Chi-Square test of independence to generate our test statistic and p-value.",
                "code": """# Create 2x2 contingency table and run Chi-Square test
table = pd.crosstab(ab["group"], ab["converted"])
chi2_stat, p_value, dof, expected_counts = stats.chi2_contingency(table)

effect_lift = conversion_rates.loc["treatment", "rate"] - conversion_rates.loc["control", "rate"]
pd.Series({
    "control_rate": conversion_rates.loc["control", "rate"],
    "treatment_rate": conversion_rates.loc["treatment", "rate"],
    "absolute_conversion_lift": effect_lift,
    "chi_square_statistic": chi2_stat,
    "p_value": p_value,
}).round(4)
"""
            },
            {
                "title": "Bootstrap Confidence Interval for Effect Lift",
                "explanation": "To quantify uncertainty around the conversion lift, we generate 1,000 bootstrap resamples of both control and treatment groups and compute the 95% confidence interval of the difference.",
                "code": """# Bootstrap 95% confidence interval for absolute conversion lift (Treatment - Control)
control_data = ab.loc[ab["group"].eq("control"), "converted"]
treatment_data = ab.loc[ab["group"].eq("treatment"), "converted"]

bootstrap_lifts = []
for seed in range(1000):
    c_mean = control_data.sample(n=len(control_data), replace=True, random_state=seed).mean()
    t_mean = treatment_data.sample(n=len(treatment_data), replace=True, random_state=seed + 10_000).mean()
    bootstrap_lifts.append(t_mean - c_mean)

pd.Series(bootstrap_lifts, name="bootstrap_lift_CI").quantile([0.025, 0.50, 0.975]).round(4)
"""
            },
            {
                "title": "Statistical Significance vs. Practical Importance",
                "explanation": "We evaluate our experimental results against a predefined business threshold (minimum practical lift of 2.0 percentage points) to make a definitive launch recommendation.",
                "code": """# Evaluate decision against both statistical and practical thresholds
min_practical_lift = 0.020  # Business requires at least +2.0% lift to justify redesign costs

pd.Series({
    "observed_absolute_lift": effect_lift,
    "is_statistically_significant_(p<0.05)": p_value < 0.05,
    "meets_practical_business_threshold_(>=2.0%)": effect_lift >= min_practical_lift,
    "final_recommendation": "LAUNCH TREATMENT" if (p_value < 0.05 and effect_lift >= min_practical_lift) else "DO NOT LAUNCH"
})
"""
            }
        ],
        "checkpoint": "Would you recommend launching the treatment page if the p-value was 0.01 (statistically significant) but the observed conversion lift was only 0.2 percentage points? Justify your answer.",
        "mistakes": [
            "Interpreting $p < 0.05$ as definitive proof that an experimental intervention has high practical importance.",
            "Ignoring effect size and confidence intervals when evaluating hypothesis test outcomes.",
            "Changing the hypothesis or primary success metric after seeing the experimental results (p-hacking / HARKing).",
        ],
        "practice": "Modify the simulation so `treatment` has conversion probability `0.108` (only a minor +0.8% lift) and sample size is `10,000` per group. Run the test and explain why a tiny effect can be highly statistically significant in large samples.",
        "exit": "What is one sentence or interpretation that you should never write when explaining a p-value to a stakeholder?",
    },
    {
        "file": "13_categorical_inference.ipynb",
        "title": "Goodness Of Fit, Independence, And Homogeneity",
        "alignment": "6.8 goodness of fit; 6.9 independence; 6.10 homogeneity; 6.11 several proportions.",
        "scenario": "A regional manager wants to know whether customer preferences differ by region. If preferences are independent of region, a single strategy may be enough; otherwise segmentation may be needed.",
        "concept": "Categorical inference compares observed counts with expected counts under a null structure. Tests of independence ask whether two categorical variables are associated in one population. Tests of homogeneity compare distributions across groups.",
        "math": "The chi-square statistic sums (observed - expected)^2 / expected across cells. Larger values indicate stronger disagreement with the null model.",
        "data_note": "Uses simulated region-choice data with a contingency table.",
        "goals": [
            "Construct and inspect multi-category contingency tables using Pandas (`pd.crosstab`).",
            "Calculate row and column conditional percentage distributions to explore categorical associations.",
            "Execute Chi-Square tests of independence and homogeneity (`stats.chi2_contingency`) across multi-group data.",
            "Analyze residual cell differences (`observed - expected`) to identify specific category drivers of non-independence."
        ],
        "links": {
            "conceptual": "We model categorical frequencies under null independence assumptions to determine whether consumer preferences require regional segmentation.",
            "computational": "We use Pandas cross-tabulations and SciPy chi-square contingency evaluations to extract expected cell frequencies and residuals.",
            "decision": "Residual analysis highlights exactly which regional product preferences deviate from baseline, guiding targeted marketing campaigns."
        },
        "code_steps": [
            {
                "title": "Simulating Regional Preference Contingency Data",
                "explanation": "We simulate survey records for n=900 customers across three geographic regions (North, Center, South) choosing among three product packages (A, B, C).",
                "code": COMMON_SETUP + """
# Simulate region and product choice records for n=900 customers
regions = rng.choice(["North", "Center", "South"], size=900, p=[0.35, 0.40, 0.25])
choice_probs = {
    "North": [0.52, 0.30, 0.18],  # North prefers Package A
    "Center": [0.42, 0.38, 0.20], # Center is balanced between A and B
    "South": [0.34, 0.42, 0.24],  # South prefers Package B
}
choices = [rng.choice(["Package_A", "Package_B", "Package_C"], p=choice_probs[r]) for r in regions]

survey = pd.DataFrame({"region": regions, "choice": choices})
table = pd.crosstab(survey["region"], survey["choice"], margins=True)
table
"""
            },
            {
                "title": "Row-Wise Conditional Preference Proportions",
                "explanation": "To see if product preferences differ by region, we normalize the contingency table by row totals to obtain conditional percentage distributions.",
                "code": """# Calculate row-wise percentage distributions (excluding margins table for clean division)
raw_table = pd.crosstab(survey["region"], survey["choice"])
row_percentages = raw_table.div(raw_table.sum(axis=1), axis=0)
(row_percentages * 100).round(1).astype(str) + "%"
"""
            },
            {
                "title": "Chi-Square Test of Independence",
                "explanation": "We run the Chi-Square test of independence on the raw frequency counts to determine if the regional preference variations are statistically significant.",
                "code": """# Execute Chi-Square test of independence
chi2_stat, p_value, dof, expected_matrix = stats.chi2_contingency(raw_table)

pd.Series({
    "chi_square_statistic": chi2_stat,
    "degrees_of_freedom_(r-1)*(c-1)": dof,
    "p_value": p_value,
    "reject_null_independence_(p<0.05)": p_value < 0.05
}).round(4)
"""
            },
            {
                "title": "Residual Analysis (Observed vs. Expected)",
                "explanation": "To understand *why* the test was significant, we construct a DataFrame of residual differences (`Observed - Expected`) to pinpoint which regional preferences drive the association.",
                "code": """# Compare observed counts against expected null counts
expected_table = pd.DataFrame(expected_matrix, index=raw_table.index, columns=raw_table.columns)
residuals = raw_table - expected_table

print("--- Expected Counts under Null Independence ---")
display(expected_table.round(1))
print()
print("--- Residuals (Observed - Expected Counts) ---")
display(residuals.round(1))
"""
            }
        ],
        "checkpoint": "Which specific cells in the residual table contribute most to the disagreement between observed data and expected null counts?",
        "mistakes": [
            "Conducting Chi-Square tests on percentages or proportions rather than raw integer frequency counts.",
            "Ignoring small expected cell counts (expected counts should generally be >= 5 for reliable chi-square approximations).",
            "Claiming that a significant chi-square test explains *why* categories are associated without inspecting cell residuals.",
        ],
        "practice": "Write a regional marketing segmentation recommendation using both the row percentage table and the residual analysis results.",
        "exit": "What does an 'expected count' represent conceptually in a chi-square test of independence?",
    },
    {
        "file": "14_experimental_design_anova.ipynb",
        "title": "Experimental Design, A/B Testing, ANOVA, And Residuals",
        "alignment": "7.1 experimental strategies; 7.2 ANOVA; 7.3 fixed effects; 7.4 residual analysis.",
        "scenario": "A team compares three interface designs. The decision should use group differences, residual variation, and the quality of the experimental design.",
        "concept": "Experimental design is about creating credible comparisons. Random assignment protects against systematic differences between treatment groups. ANOVA compares between-group variability with within-group variability. Residual analysis checks whether the model leaves structure unexplained.",
        "math": "ANOVA uses an F statistic: variation explained by groups divided by residual variation, adjusted by degrees of freedom.",
        "data_note": "Uses a simulated single-factor experiment with three designs.",
        "goals": [
            "Explain the foundational role of random assignment in protecting experimental comparisons from confounding variables.",
            "Execute One-Way Analysis of Variance (ANOVA) using SciPy (`stats.f_oneway`) to compare across three or more group means.",
            "Calculate experimental group means and isolate within-group residual variation (`response - group_mean`).",
            "Inspect residual distributions using histograms and boxplots to verify ANOVA model assumptions."
        ],
        "links": {
            "conceptual": "We partition total data variation into between-group treatment effects and within-group residual noise.",
            "computational": "We use Pandas group transformations (`.transform('mean')`) to compute residuals and SciPy (`stats.f_oneway`) for F-tests.",
            "decision": "ANOVA prevents inflating Type I error rates when comparing multiple interface designs, ensuring reliable design selection."
        },
        "code_steps": [
            {
                "title": "Experimental Data Simulation across 3 UI Designs",
                "explanation": "We simulate a single-factor experiment where n=210 users are randomly assigned across three interface designs (Design A, B, C) with different underlying response scores.",
                "code": COMMON_SETUP + """
# Simulate randomized experiment across 3 UI designs (n=70 per group)
experiment = pd.DataFrame({
    "design": np.repeat(["Design_A", "Design_B", "Design_C"], 70),
    "response_score": np.r_[rng.normal(50, 7, 70), rng.normal(54, 7, 70), rng.normal(58, 7, 70)],
})

# Summarize sample size, mean, and standard deviation by design
experiment.groupby("design")["response_score"].agg(
    users="count", mean_score="mean", std_dev="std"
).round(2)
"""
            },
            {
                "title": "One-Way ANOVA F-Test Execution",
                "explanation": "We extract the response score arrays for each design group and execute a One-Way ANOVA F-test to test the null hypothesis of equal group means.",
                "code": """# Extract group response arrays and execute One-Way ANOVA
group_arrays = [group["response_score"].to_numpy() for _, group in experiment.groupby("design")]
f_stat, p_value = stats.f_oneway(*group_arrays)

pd.Series({
    "anova_F_statistic": f_stat,
    "p_value": p_value,
    "null_hypothesis_equal_means": "REJECTED (Significant group differences)" if p_value < 0.05 else "NOT REJECTED"
}).round(4)
"""
            },
            {
                "title": "Decomposing Effects & Computing Residuals",
                "explanation": "We calculate group-specific mean responses and subtract them from individual user scores to isolate unexplained within-group residuals (`residual = response - group_mean`).",
                "code": """# Calculate group means and individual residual errors
group_means = experiment.groupby("design")["response_score"].transform("mean")
experiment["residual"] = experiment["response_score"] - group_means

# Display first 2 rows of each design group to verify residual decomposition
experiment.groupby("design").head(2).round(2)
"""
            },
            {
                "title": "Visualizing Treatment Effects & Residual Health",
                "explanation": "We create side-by-side plots: a boxplot comparing response scores across UI designs, and a histogram verifying that residuals follow a symmetric Normal distribution centered at zero.",
                "code": """# Plot treatment effects and check residual normality assumption
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=experiment, x="design", y="response_score", palette="Blues", ax=axes[0], width=0.4)
axes[0].set_title("Response Score by UI Design", fontsize=13)
axes[0].set_xlabel("Interface Design")
axes[0].set_ylabel("User Response Score")

sns.histplot(experiment["residual"], kde=True, ax=axes[1], color="purple", bins=25)
axes[1].axvline(0, color="black", linestyle="--", linewidth=1.5)
axes[1].set_title("Residual Error Distribution (Check Normality)", fontsize=13)
axes[1].set_xlabel("Residual (Observed - Group Mean)")
plt.tight_layout()
plt.show()
"""
            }
        ],
        "checkpoint": "What specifically does a statistically significant ANOVA F-test tell us, and what critical information does it NOT tell us?",
        "mistakes": [
            "Treating observational group differences as causal experimental effects without verifying random assignment.",
            "Stopping at the omnibus ANOVA p-value without conducting pairwise follow-up comparisons or reporting effect sizes.",
            "Ignoring residual error patterns, severe outliers, or unequal within-group variances.",
        ],
        "practice": "Estimate the pairwise mean differences between designs (`Mean_B - Mean_A`, `Mean_C - Mean_A`, `Mean_C - Mean_B`). Based on these differences and the residual spread, decide which UI design you recommend for adoption.",
        "exit": "Why is random assignment central to establishing credible causal evidence in experimental design?",
    },
    {
        "file": "15_capstone_workshop.ipynb",
        "title": "Capstone Workshop: Real Data, Model Justification, And Communication",
        "alignment": "7.5 randomized blocks, Latin and Graeco-Latin squares; 7.6 factorial designs; challenge outcomes.",
        "scenario": "Your team must turn a dataset into a defensible recommendation. The strongest capstones are not the most complicated; they are the clearest about question, evidence, uncertainty, and limitations.",
        "concept": "A capstone is a complete statistical argument. The data must be relevant to a decision, the method must match the question, and the conclusion must reflect uncertainty. Design ideas such as blocking and factorial structure help students notice whether comparisons are fair.",
        "math": "The capstone can use intervals, tests, ANOVA, bootstrap, or model comparison. The common structure is always estimate, uncertainty, assumptions, and decision.",
        "data_note": "Uses student-selected Kaggle or approved public data. This notebook provides planning tables and quality checks.",
        "goals": [
            "Synthesize the 5-step statistical reasoning cycle into an end-to-end data science capstone project.",
            "Formulate strong, decision-oriented research questions tied to concrete stakeholder actions.",
            "Map analytical decision needs to appropriate statistical modeling and uncertainty methods.",
            "Construct a comprehensive risk register to proactively mitigate data, sampling, and assumption risks."
        ],
        "links": {
            "conceptual": "We integrate probability models, sampling uncertainty, and hypothesis testing into a cohesive statistical argument.",
            "computational": "We organize reproducible Python code, data dictionaries, and cleaning logs in a structured Jupyter notebook.",
            "decision": "The final capstone report translates complex statistical evidence into an executive-level, defensible action recommendation."
        },
        "code_steps": [
            {
                "title": "Capstone Milestone Tracking Checklist",
                "explanation": "We initialize an interactive Pandas DataFrame checklist covering all 11 essential components required for a complete, defensible capstone submission.",
                "code": COMMON_SETUP + """
# Initialize Capstone Project tracking checklist across 11 required sections
capstone_checklist = pd.DataFrame({
    "project_section": [
        "1. Decision Question",
        "2. Target Stakeholder & Action",
        "3. Data Source Citation & Ethics",
        "4. Data Dictionary & Types",
        "5. Data Cleaning & Preprocessing Log",
        "6. Exploratory Data Analysis (EDA)",
        "7. Uncertainty Quantification (CI / SE)",
        "8. Statistical Test / Model Comparison",
        "9. Explicit Assumption Checking",
        "10. Limitations & Risk Analysis",
        "11. Final Actionable Recommendation",
    ],
    "status": ["not started"] * 11,
    "lead_team_member": ["unassigned"] * 11,
    "next_concrete_action": ["Define initial scope"] * 11
})
capstone_checklist
"""
            },
            {
                "title": "Formulating Strong Decision Questions",
                "explanation": "We examine a comparative table contrasting weak, exploratory questions against strong, decision-oriented research questions that drive executive action.",
                "code": """# Contrast weak exploratory questions against strong decision-oriented questions
question_quality = pd.DataFrame({
    "weak_exploratory_question": [
        "What is in the dataset?",
        "Can we predict housing or bike rental prices?",
        "Which variables are statistically significant?",
    ],
    "strong_decision_oriented_question": [
        "Which customer segment exhibits the highest uncertainty, requiring targeted pricing buffers?",
        "Which property features provide a precise enough valuation estimate to guide municipal tax assessments?",
        "Which operational variables materially change our inventory recommendation under peak demand uncertainty?",
    ],
})
pd.set_option("display.max_colwidth", 100)
question_quality
"""
            },
            {
                "title": "Mapping Decision Needs to Statistical Methods",
                "explanation": "We review an architectural mapping table linking specific analytical decision requirements to their appropriate statistical methodology and uncertainty metric.",
                "code": """# Map decision requirements to appropriate statistical modeling methods
methods_map = pd.DataFrame({
    "analytical_decision_need": [
        "Estimate a population mean or total",
        "Compare two operational groups or A/B designs",
        "Compare three or more treatment strategies",
        "Test association between categorical variables",
        "Evaluate risk or extreme tail events",
    ],
    "recommended_statistical_method": [
        "Student's t confidence interval or Bootstrap interval",
        "Two-sample t-test, Chi-Square test, or Bootstrap lift interval",
        "One-Way ANOVA F-test with post-hoc comparisons",
        "Chi-Square test of independence and residual analysis",
        "Poisson / Gamma distribution fitting or percentile survival functions",
    ],
    "primary_uncertainty_evidence": [
        "Standard error and 95% CI bounds",
        "p-value and 95% CI of difference/lift",
        "F-statistic and residual error spread",
        "Chi-square statistic and cell residuals",
        "Tail probability P(X >= threshold)",
    ]
})
methods_map
"""
            },
            {
                "title": "Statistical Risk Register & Mitigation Strategy",
                "explanation": "We construct a proactive risk register identifying the four most common statistical pitfalls in capstone projects and defining concrete mitigation actions.",
                "code": """# Construct proactive statistical risk register
risk_register = pd.DataFrame({
    "statistical_risk_area": [
        "1. Missing or corrupted data",
        "2. Sampling selection bias",
        "3. Statistically significant but trivial effect",
        "4. Severe model assumption violation",
    ],
    "potential_impact_on_decision": [
        "Biased estimates and false precision",
        "Inability to generalize claims to true population",
        "Wasting resources implementing ineffective changes",
        "Invalid p-values and misleading confidence intervals",
    ],
    "required_mitigation_action": [
        "Document cleaning log and run sensitivity analysis on imputed values",
        "Explicitly restrict population claim scope in final report",
        "Report absolute effect size and check against business practical threshold",
        "Transform scale (e.g., log), use non-parametric Bootstrap, or qualify conclusions",
    ],
})
risk_register
"""
            }
        ],
        "checkpoint": "Write your capstone decision question in one sentence. Then name the target stakeholder and the specific operational action the stakeholder could take based on your evidence.",
        "mistakes": [
            "Choosing an interesting dataset first and never formulating a concrete decision question.",
            "Using complex machine learning or statistical models without explaining why they answer the business question better than simpler methods.",
            "Writing a technical report that describes charts and p-values but never makes an actionable executive recommendation.",
        ],
        "practice": "Complete the tracking checklist for your team's project. Mark every item as not started, in progress, or complete, assign team leads, and write down the next concrete task for Week 15.",
        "exit": "What specific statistical evidence or assumption violation would force you to change or reverse your final capstone recommendation?",
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
        md(f"# {lesson['title']}\n\n**Official MA1001B Alignment:** *{lesson['alignment']}*"),
        md(
            "## How To Use This Lesson\n\n"
            "This notebook is designed as a guided teaching episode and interactive lab, not a passive code demonstration. "
            "To get the most out of this lesson:\n"
            "1. **Read the conceptual explanations and explicit links** before running any code.\n"
            "2. **Execute code cells sequentially**, paying attention to inline educational comments.\n"
            "3. **Pause at the Guided Checkpoint** to discuss with a partner and write your reasoning before checking solutions.\n"
            "4. **Complete the Independent Practice and Exit Ticket**; written justification is the primary evidence of statistical competence."
        ),
        md(
            "## Learning Goals\n\n"
            "By the end of this lesson, you will be able to:\n"
            + "\n".join(f"- {goal}" for goal in lesson["goals"])
        ),
        md(
            "## The Three Explicit Links\n\n"
            "In accordance with the MA1001B pedagogical framework, this lesson explicitly connects theory, computation, and action:\n\n"
            f"- **1. Conceptual Link (What is modeled):** {lesson['links']['conceptual']}\n"
            f"- **2. Computational Link (How Python represents it):** {lesson['links']['computational']}\n"
            f"- **3. Decision Link (How it guides action):** {lesson['links']['decision']}"
        ),
        md(f"## Decision Scenario\n\n> **The Problem:** {lesson['scenario']}"),
        md(f"## Conceptual Explanation\n\n{lesson['concept']}"),
        md(f"## Mathematical Anchor\n\n{lesson['math']}"),
        md(f"## Data And Workflow Notes\n\n{lesson['data_note']}"),
        md("## Practical Python Workflow\n\nThe following worked example demonstrates how to implement these statistical concepts in Python to generate evidence for decision making."),
    ]

    for index, step in enumerate(lesson["code_steps"], start=1):
        cells.append(md(f"### Step {index}: {step['title']}\n\n{step['explanation']}"))
        cells.append(code(step["code"]))

    cells.extend(
        [
            md(f"## Guided Checkpoint\n\n> [!IMPORTANT]\n> **Pair Discussion & Writing Prompt:**\n> {lesson['checkpoint']}\n\n*Write your reasoned response below before continuing:*"),
            md(
                "## Common Mistakes & Statistical Pitfalls\n\n"
                "Avoid these frequent errors when conducting or communicating this analysis:\n"
                + "\n".join(f"- **Warning:** {item}" for item in lesson["mistakes"])
            ),
            md(f"## Independent Practice\n\n> [!TIP]\n> **Your Task:**\n> {lesson['practice']}\n\n*Use the empty code and markdown cells below to implement your analysis and justify your recommendation.*"),
            code("# Write your independent practice code here\n# Remember to inspect your outputs and check assumptions\n"),
            md(
                "## Decision Interpretation Template\n\n"
                "Use this structured format to write your defensible conclusion and recommendation:\n\n"
                "1. **The Decision Question:** *State the practical question being answered...*\n"
                "2. **The Statistical Evidence:** *Summarize key metrics, intervals, p-values, or model comparisons...*\n"
                "3. **Uncertainty & Limitations:** *Identify what the data cannot prove and what assumptions were made...*\n"
                "4. **Actionable Recommendation:** *Therefore, I recommend [action] because [justification]...*"
            ),
            md(f"## Exit Ticket\n\n> **Reflection:** {lesson['exit']}\n\n*Write your brief conceptual reflection below:*"),
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
    print("Successfully generated 15 upgraded lesson notebooks.")


if __name__ == "__main__":
    main()
