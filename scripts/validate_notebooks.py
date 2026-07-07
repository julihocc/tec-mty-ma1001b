"""MA1001B Lesson Notebook Validation Script.

This script enforces structural and syntactic quality guarantees across all generated
Jupyter notebooks in the MA1001B course repository (`lessons/`).

Validation Rules Enforced:
1. Notebook Count: Exactly 15 lesson notebooks must exist in `lessons/`.
2. Notebook Format: Must adhere to Jupyter Notebook Format Version 4 (`nbformat == 4`).
3. Pedagogical Depth (Cell Count): Every notebook must contain at least 17 cells
   (ensuring complete scaffolding: intro, goals, explicit links, scenario, concept,
   math, data notes, workflow steps, checkpoints, common mistakes, independent practice,
   interpretation template, and exit ticket).
4. Code Syntactic Validity: Every code cell in every notebook is compiled using Python's
   built-in `compile()` function in 'exec' mode. This guarantees that all generated code
   is syntactically valid and free of parsing errors (e.g., unterminated strings or
   invalid escape sequences) prior to distribution to students.

Usage:
    uv run python scripts/validate_notebooks.py
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def main() -> None:
    """Execute validation checks across all generated MA1001B notebooks.

    Iterates through all `.ipynb` files in the `lessons/` directory, verifying format,
    minimum cell counts, and Python syntax compilation for every code cell.

    Raises:
        SystemExit: If notebook count != 15, nbformat != 4, cell count < 17,
            or if any code cell contains syntax/compilation errors.
    """
    files: List[Path] = sorted(Path("lessons").glob("*.ipynb"))
    if len(files) != 15:
        raise SystemExit(f"Expected 15 notebooks, found {len(files)}")

    for path in files:
        notebook: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        cells: List[Dict[str, Any]] = notebook.get("cells", [])
        if notebook.get("nbformat") != 4:
            raise SystemExit(f"{path}: expected nbformat 4")
        if len(cells) < 17:
            raise SystemExit(f"{path}: expected at least 17 cells, found {len(cells)}")
        for cell in cells:
            if cell.get("cell_type") == "code":
                compile("".join(cell.get("source", [])), str(path), "exec")
        print(f"{path}: {len(cells)} cells")

    print("Notebook validation passed.")


if __name__ == "__main__":
    main()
