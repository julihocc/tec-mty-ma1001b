# Copilot Instructions

## Repository shape

- This repository is a course-material/document repository, not an application codebase.
- The only tracked content artifact is `docs/MA1001B - Analítico.pdf`; the root-level tracked files are repository metadata (`README.md`, `LICENSE.md`, `.gitignore`).
- `README.md` only declares the repository name, so the main project content currently lives in the PDF under `docs/`.

## Build, test, and lint commands

- No build, test, or lint commands are defined in tracked files.
- There is no checked-in package manifest, Python project file, Makefile, or test runner configuration to derive project automation from.
- There is no single-test command available in the current repository state.

## High-level architecture

- The repository is organized around a single published course document stored in `docs/`.
- `docs/MA1001B - Analítico.pdf` is a binary deliverable rather than editable source, so content changes normally require replacing the file with a newly exported PDF instead of editing text in place.
- There are no tracked source files for regenerating the PDF, which means requests to update document contents may require first locating the authoring source outside this repository.

## Key conventions

- Keep course deliverables in `docs/`; avoid adding generated artifacts at the repository root.
- Track PDFs through Git LFS; do not commit large PDF binaries as normal Git blobs.
- Treat `docs/MA1001B - Analítico.pdf` as a binary asset. Do not attempt line-oriented edits inside the PDF; use a PDF-aware tool or replace the file wholesale.
- Preserve the existing PDF filename exactly, including spaces and the accented character, unless the user explicitly asks for a rename.
- Do not infer Python tooling from `.gitignore` alone. The ignore file is a generic Python-oriented template, but the repository currently has no tracked Python source or Python project configuration.
