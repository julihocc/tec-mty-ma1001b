import json
from pathlib import Path


def main():
    files = sorted(Path("lessons").glob("*.ipynb"))
    if len(files) != 15:
        raise SystemExit(f"Expected 15 notebooks, found {len(files)}")

    for path in files:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cells = notebook.get("cells", [])
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
