# Course Design Notes

This document explains the pedagogical design for the MA1001B data science
version. It is written for instructors and course developers who will extend or
teach from the notebooks.

## Design Principle

The course uses Python to make statistical reasoning visible. Python is not the
end goal. The end goal is for students to make defensible decisions under
uncertainty using data, models, assumptions, and clear communication.

Each lesson should answer four student questions:

1. What decision or problem motivates this topic?
2. What statistical idea helps with that decision?
3. How do we implement the idea in Python?
4. What can and cannot be concluded from the result?

## Lesson Rhythm

Each notebook follows this rhythm:

1. Learning goals.
2. Decision scenario.
3. Conceptual explanation.
4. Data and workflow setup.
5. Worked example.
6. Guided checkpoint.
7. Common mistakes.
8. Independent practice.
9. Exit ticket.

The rhythm is intentionally repeated. Students should learn to recognize the
shape of a statistical analysis: define the question, inspect data, choose a
model, quantify uncertainty, and write a conclusion.

## Progression Across The Semester

Weeks 1-3 are highly guided. Students learn the notebook workflow, probability
language, event definitions, conditional probabilities, and sampling.

Weeks 4-7 move from probability language to random-variable modeling. Students
learn to decide when a discrete or continuous distribution is a useful
approximation and when the assumptions are too weak.

Weeks 8-11 build inference. Students move from one sample to sampling
distributions, bootstrap reasoning, confidence intervals, variance, and sample
size planning.

Weeks 12-14 focus on decisions from evidence: hypothesis tests, categorical
inference, experiments, ANOVA, and residual checks.

Week 15 consolidates the workflow through the capstone.

## Instructor Guidance

Use the notebooks as class scripts, not as homework dumps. A typical 75-minute
class can use:

1. 10 minutes for the decision scenario and prior knowledge.
2. 15 minutes for conceptual explanation.
3. 20 minutes for the worked example.
4. 15 minutes for a guided checkpoint in pairs.
5. 10 minutes for discussion of limitations.
6. 5 minutes for the exit ticket.

For longer sessions, add the independent practice section during class. For
shorter sessions, assign it as homework.

## Feedback Priorities

When grading notebooks, prioritize reasoning quality over decorative output.
The strongest notebooks:

1. Define the decision question before the analysis.
2. Explain assumptions in context.
3. Use readable, reproducible code.
4. Interpret uncertainty instead of only reporting numbers.
5. State limitations without weakening every conclusion into vagueness.

## Capstone Readiness

The capstone should not appear suddenly at the end. By week 6, students should
have seen enough examples to propose a dataset and decision question. By week
10, they should be able to produce intervals or bootstrap uncertainty. By week
13, they should be able to choose a test, comparison, or model-based analysis.
