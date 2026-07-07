# MA1001B Analitico Findings

Source: `docs/MA1001B - Analítico.pdf`

Analyzed file: `MA1001B - Analítico.pdf`, official course plan for `MA1001B - Statistical Modeling for Decision Making`.

PDF metadata:

- Title: `SAMP | Vista preliminar`
- Creator: `wkhtmltopdf 0.12.2.1`
- Producer: `Qt 4.8.6`
- Creation date: February 26, 2026
- Pages: 4
- Page size: Letter

## Course Identity

- Course code: `MA1001B`
- Course title: `Statistical Modeling for Decision Making`
- Discipline: Mathematics
- School: Engineering and Sciences
- Academic department: Sciences
- CIP: `270501 Statistics, General`
- Programs: `IFI19`, `IDM19`, `ICI19`
- Prerequisite: `MA1031`
- Equivalences: None

## Course Orientation

The course is centered on statistical modeling for decision making under uncertainty. The program emphasizes:

- Making decisions in uncertain contexts related to natural and exact sciences.
- Building stochastic and deterministic models adapted to a given problem context.
- Interpreting model information with decision making as the final objective.
- Extracting relevant data from large structured databases using statistical methods and technological tools.
- Using inductive-deductive reasoning to solve problems with objective criteria.
- Communicating arguments and technical analysis in writing.

The main implication for lecture notes is that the course should not be framed only as a sequence of probability and statistics techniques. Each unit should connect technical methods to modeling, interpretation, and decision justification.

## Topic Structure

The official topic sequence has seven major blocks.

1. Probability theory
   - Set theory and probability calculation.
   - Counting techniques.
   - Conditional probability and Bayes' rule.
   - Random sampling.

2. Discrete random variables
   - Discrete probability distributions.
   - Bernoulli trials and binomial distribution.
   - Multinomial distribution.
   - Geometric and negative binomial distributions.
   - Hypergeometric distribution.
   - Poisson distribution.
   - Relation between discrete random variables and data science.

3. Continuous random variables
   - Density functions.
   - Expected value for continuous variables.
   - Uniform distribution.
   - Normal distribution.
   - Gamma-type distributions.
   - Moment-generating functions.

4. Sampling distributions
   - Transformation of variables.
   - Probability distributions of functions of random variables.
   - Sampling distribution of the mean.
   - Chi-square distribution.
   - t distribution.
   - F distribution.
   - Relation between sampling distributions and data science.

5. Estimation and its relation to data science
   - Point estimation methods.
   - Interval estimation.
   - Estimation of one mean and difference between two means.
   - Standard error.
   - Estimation of one proportion and difference between two proportions.
   - Estimation of variance and ratio of two variances.
   - Sample size estimation.

6. Hypothesis testing
   - Hypothesis testing elements.
   - Relationship between confidence intervals and hypothesis tests.
   - P-values for decision making.
   - Tests for one mean with unknown variance.
   - Tests for two means.
   - Tests for proportions.
   - Tests for variances.
   - Goodness-of-fit tests.
   - Tests of independence.
   - Tests of homogeneity.
   - Tests of several proportions.

7. Experimental design elements
   - Experimental strategies.
   - Single-factor experiments and analysis of variance.
   - Fixed effects model analysis.
   - Model adaptation through residual analysis.
   - Randomized complete blocks, Latin squares, and Graeco-Latin squares.
   - Introduction to factorial designs.

## Suggested Structure for Lecture Notes

A practical lecture-note structure can follow the seven official blocks, while making the modeling and decision thread explicit:

1. Probability foundations for uncertainty.
2. Discrete models for counts and events.
3. Continuous models for measurements.
4. Sampling distributions and model behavior.
5. Estimation and uncertainty quantification.
6. Hypothesis testing for decision making.
7. Experimental design and model validation.

Recommended recurring elements in each unit:

- Conceptual motivation tied to decisions under uncertainty.
- Formal definitions and assumptions.
- Worked examples with interpretation, not only calculation.
- Data-oriented examples using structured datasets when appropriate.
- Short computational activities or notebooks.
- A closing decision-making task where students justify a conclusion.

## Assessment Implications

The official evaluation policy suggests:

- 75%: activities, assignments, cases, and module exams assessing theoretical and practical knowledge in probability, random variables, estimation, hypothesis testing, and experimental design.
- 25%: challenge process and outcomes, including oral presentation of findings and a written technical report justifying the model or models used.

This supports separating course artifacts into:

- Technical practice: exercises, quizzes, and module exams.
- Applied cases: contextual problems where students choose and interpret models.
- Challenge support: templates or guidance for oral findings and technical reports.

Lecture notes should therefore include both computational/statistical fluency and written interpretation expectations.

## Bibliographic Anchors

The official bibliography lists:

- Devore, J. L. `Probability and Statistics for Engineers and Scientists`, 9th edition, Cengage Learning, 2016.
- Reinhart, Alex. `Statistics Done Wrong: The Woefully Complete Guide`, No Starch Press, 2015.
- Lohr, Sharon L. `Sampling: Design and Analysis`, 2nd edition, Brooks/Cole Cengage Learning, 2009.

These references suggest a balance between engineering statistics, statistical reasoning pitfalls, and sampling design.

## Quality Notes and Errata

The PDF appears usable as a source document, but it contains several empty fields and formatting issues:

- The `Course intention within the general study plan context` field is empty.
- `Modules` is empty.
- `Specific learning objectives by topic` is empty.
- `Teaching and learning technique` is listed as `Not Specified`.
- `Estimated timing per topic` is empty.
- `Support material` is empty.
- In topic 3, numbering repeats `3.2` and `3.3`.
- The heading `Dokimasia` is used for topic 6, but the contents are hypothesis testing. For teaching materials, `Hypothesis Testing` is clearer.
- The phrase `Teaching and learning tecnique` contains a typo in the source.
- In supervised learning activities, items 3 and 4 are visually joined without a clean line break.
- The source is in English, while parts of the bibliography metadata indicate Spanish-language editions.

When creating derived course materials, treat these as source-document defects rather than intentional curricular distinctions.
