# MA1001B - Statistical Modeling for Decision Making

This repository contains a data-science-oriented course scaffold for
`MA1001B - Statistical Modeling for Decision Making`, built from the official
course source in `docs/MA1001B - Analítico.pdf`.

The course preserves the official probability and statistics spine while making
Python, Jupyter notebooks, real datasets, reproducible analysis, and
decision-oriented communication the central learning experience.

## Structure

- `syllabus.md`: course orientation, schedule, grading model, and official topic alignment.
- `lessons/`: Jupyter notebooks organized as weekly topic lessons.
- `assignments/`: applied notebook assignments and rubrics.
- `capstone/`: final real-data project brief, proposal template, and rubrics.
- `data/README.md`: dataset download instructions, Kaggle guidance, and file placement rules.
- `requirements.txt`: Python packages for the notebooks.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter lab
```

Datasets are not committed to this repository. Follow `data/README.md` to
download the required files and place them under `data/raw/`.
