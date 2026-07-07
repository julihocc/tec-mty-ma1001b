# MA1001B Capstone Challenge

The capstone is the official 25% challenge component of MA1001B. Students use a
real dataset to answer a decision question with statistical modeling and Python.

## Goal

Produce a reproducible analysis that supports a decision under uncertainty. The
project must show that the selected model or statistical method is appropriate
for the question, data, assumptions, and limitations.

The capstone is not a machine-learning competition. Predictive models may be
used, but the graded focus is statistical reasoning: uncertainty, assumptions,
evidence, and decision justification.

## Approved Data Sources

Students may use one of the recommended Kaggle datasets in `data/README.md` or
another public dataset approved by the instructor. The dataset must be large
enough to support exploratory analysis and statistical inference.

## Required Deliverables

1. Project proposal.
2. Exploratory data analysis notebook.
3. Statistical modeling notebook.
4. Final technical report.
5. Oral presentation of findings.

## Milestones

| Week | Milestone | Evidence |
| --- | --- | --- |
| 5 | Dataset shortlist | Two possible datasets and one possible decision question for each |
| 7 | Proposal | Approved question, stakeholder, data source, and planned methods |
| 10 | EDA checkpoint | Cleaned data, data dictionary, missingness summary, initial figures |
| 12 | Inference checkpoint | Interval, test, bootstrap, or model-comparison draft |
| 14 | Draft report | Complete argument with gaps marked clearly |
| 15 | Final submission | Notebooks, report, and presentation |

## Required Analysis Elements

Every capstone must include:

1. A clear decision question.
2. Dataset citation and data dictionary.
3. Data cleaning decisions.
4. Exploratory visualizations.
5. At least one uncertainty quantification method.
6. At least one hypothesis test, model comparison, or experimental analysis.
7. Assumption checks.
8. Limitations and data ethics note.
9. Recommendation supported by evidence.

## Choosing A Good Decision Question

A good capstone question is specific, answerable with the available data, and
connected to an action.

Strong examples:

1. Should the treatment page be launched if the observed conversion lift is
   small but statistically detectable?
2. Which house-price segment has the widest uncertainty, and how should that
   affect a pricing recommendation?
3. Which bike-demand conditions should trigger additional capacity planning?

Weak examples:

1. What is in this dataset?
2. Can we predict everything accurately?
3. Which variables are interesting?

Weak questions can become strong by naming a stakeholder, a decision, and a
measurable outcome.

## Suggested Project Tracks

| Track | Example question | Suggested dataset |
| --- | --- | --- |
| Risk classification | Which passenger profiles had higher survival probability? | Titanic |
| Price estimation | Which home characteristics most affect price uncertainty? | House Prices |
| Demand planning | What factors are associated with bike rental demand? | Bike Sharing Demand |
| Social indicators | Which country-level indicators differ by region or income group? | World Happiness Report |
| Experiment analysis | Did the treatment group produce a practically meaningful lift? | A/B Testing |

## Final Report Structure

1. Executive summary.
2. Decision question and context.
3. Data source and preparation.
4. Exploratory findings.
5. Statistical method and assumptions.
6. Results and uncertainty.
7. Recommendation.
8. Limitations, ethics, and next steps.
9. References.

## Capstone Rubric

Use `rubrics/capstone_rubric.md` for grading. The summary weights are:

| Criterion | Weight |
| --- | ---: |
| Decision question and data relevance | 15% |
| Reproducible Python workflow | 15% |
| Correct statistical modeling and assumptions | 25% |
| Interpretation under uncertainty | 20% |
| Technical report quality | 15% |
| Oral presentation quality | 10% |
