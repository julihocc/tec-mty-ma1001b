# MA1001B - Statistical Modeling for Decision Making

This repository contains a data-science-oriented teaching package for
`MA1001B - Statistical Modeling for Decision Making`, built from the official
course source in `docs/MA1001B - Analítico.pdf`.

The course preserves the official probability and statistics spine while making
Python, Jupyter notebooks, real datasets, reproducible analysis, and
decision-oriented communication the central learning experience.

## Structure

- `syllabus.md`: course orientation, schedule, grading model, and official topic alignment.
- `course_design.md`: pedagogical design, lesson rhythm, and instructor guidance.
- `lessons/`: Jupyter notebooks organized as weekly topic lessons.
- `assignments/`: applied notebook assignments and rubrics.
- `capstone/`: final real-data project brief, proposal template, and rubrics.
- `data/README.md`: dataset download instructions, Kaggle guidance, and file placement rules.
- `rubrics/`: reusable notebook, assignment, and capstone assessment rubrics.
- `pyproject.toml` and `uv.lock`: uv-managed Python environment for the notebooks.
- `scripts/`: utility scripts used to generate or validate course artifacts.

## Quick Start

This project uses `uv` for Python version and dependency management.

```powershell
uv sync
uv run jupyter lab
```

Datasets are not committed to this repository. Follow `data/README.md` to
download the required files and place them under `data/raw/`.

## Maintenance

Regenerate the lesson notebooks after editing the lesson source:

```powershell
uv run python scripts\generate_lesson_notebooks.py
```

Validate notebook structure and Python syntax:

```powershell
uv run python scripts\validate_notebooks.py
```

## Teaching Model

Each lesson is designed around the same data-science reasoning cycle:

```text
decision question -> data -> statistical model -> uncertainty -> recommendation
```

The notebooks are not intended to be short code demos. They combine conceptual
explanation, guided Python walkthroughs, common mistakes, interpretation
prompts, and independent practice. The course deliberately uses fallback
simulated data so lessons remain runnable before students download Kaggle files,
but graded work should use the real datasets whenever required by the assignment
or capstone brief.
