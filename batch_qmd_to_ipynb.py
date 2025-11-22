#!/usr/bin/env python3
"""
Quarto (.qmd / .Rmd) → Colab R Notebook converter + auto-repair
Features:
- Smart insertion of rpy2 + Google Drive mount before first %%R cell
- Banner image
- Clean headings & layout blocks removal
- Guarantees every code cell has "outputs": [] and "execution_count": null
- Batch processing with nice feedback
"""

import re
import json
from pathlib import Path

# ------------------- Banner -------------------
BANNER = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "![Survival Analysis with R](http://drive.google.com/uc?export=view&id=1bLQ3nhDbZrCCqy_WCxxckOne2lgVvn3l)",
        "",
        "<br>"
    ]
}

# ------------------- Colab Setup Cells -------------------
RPY2_MD = {"cell_type": "markdown", "metadata": {}, "source": ["## Install rpy2"]}
RPY2_CODE = {
    "cell_type": "code",
    "metadata": {},
    "source": [
        "!pip uninstall rpy2 -y -q",
        "!pip install rpy2==3.5.1 -q",
        "%load_ext rpy2.ipython"
    ],
    "outputs": [],
    "execution_count": None
}

DRIVE_MD = {"cell_type": "markdown", "metadata": {}, "source": ["## Mount Google Drive"]}
DRIVE_CODE = {
    "cell_type": "code",
    "metadata": {},
    "source": [
        "from google.colab import drive",
        "drive.mount('/content/drive')"
    ],
    "outputs": [],
    "execution_count": None
}

SEPARATOR = {"cell_type": "markdown", "metadata": {}, "source": ["", "---", ""]}

# ------------------- Regexes -------------------
CHUNK_RE = re.compile(
    r"^(?P<indent>[ \t]*)```\{?\s*(?P<engine>[a-zA-Z0-9_+.-]*)\b(?P<options>.*?)\n(?P<code>[\s\S]*?)\n(?P=indent)```",
    re.MULTILINE
)
LAYOUT_BLOCK_RE = re.compile(r":::\s*\{layout-ncol.*?:::", re.DOTALL)

# ------------------- Helpers -------------------
def split_headings(lines):
    blocks = []
    current = []
    for line in lines:
        line = line.rstrip()
        if re.match(r"^\s*#+\s+", line) and current:
            blocks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))

    cleaned = []
    for b in blocks:
        if b.strip().startswith(("## Original Notebook Starts Here", "## Overview")):
            continue
        cleaned.append(b.rstrip())
    return [b for b in cleaned if b.strip()]

def ensure_code_cell_structure(cell):
    """Force correct empty output fields – essential for Colab"""
    if cell.get("cell_type") == "code":
        if "outputs" not in cell:
            cell["outputs"] = []
        if "execution_count" not in cell:
            cell["execution_count"] = None
    return cell

# ------------------- Core conversion -------------------
def qmd_to_cells(content: str):
    content = LAYOUT_BLOCK_RE.sub("", content)
    cells = [BANNER]
    pos = 0
    first_r_chunk_found = False

    for m in CHUNK_RE.finditer(content):
        # Markdown before chunk
        md_text = content[pos:m.start()].strip()
        if md_text:
            for block in split_headings(md_text.splitlines()):
                if block.strip():
                    cells.append(ensure_code_cell_structure({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": block.splitlines()
                    }))

        # Code chunk
        engine = m.group("engine").strip().lower()
        options_str = m.group("options")
        code = m.group("code").rstrip()

        option_comments = [
            p.strip() for p in re.split(r',\s*', options_str.strip())
            if p.strip().startswith("#|")
        ]

        is_r = engine in {"r", ""} or engine.startswith("r")

        if is_r and not first_r_chunk_found:
            cells.extend([RPY2_MD, RPY2_CODE, DRIVE_MD, DRIVE_CODE, SEPARATOR])
            first_r_chunk_found = True

        if is_r:
            source = ["%%R"]
            source.extend(option_comments)
            if code:
                source.append("")
                source.extend(code.splitlines())
            cell = {
                "cell_type": "code",
                "metadata": {},
                "source": source,
                "outputs": [],
                "execution_count": None
            }
        else:
            source = [f"```{engine}"] + code.splitlines() + ["```"]
            cell = {
                "cell_type": "code",
                "metadata": {},
                "source": source,
                "outputs": [],
                "execution_count": None
            }

        cells.append(ensure_code_cell_structure(cell))
        pos = m.end()

    # Remaining markdown
    final_md = content[pos:].strip()
    if final_md:
        for block in split_headings(final_md.splitlines()):
            if block.strip():
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": block.splitlines()
                })

    return cells

# ------------------- Convert single file -------------------
def convert_file(in_path: Path, out_path: Path):
    try:
        content = in_path.read_text(encoding="utf-8")
        cells = qmd_to_cells(content)

        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "R", "language": "R", "name": "ir"},
                "colab": {"toc_visible": True}
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }

        out_path.write_text(
            json.dumps(notebook, indent=1, ensure_ascii=False, separators=(',', ':')),
            encoding="utf-8"
        )
        print(f"Success: {in_path.name} → {out_path.name}")
    except Exception as e:
        print(f"Failed: {in_path.name} | {e}")

# ------------------- Slugify filename -------------------
def slug(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"\s+", "_", name).strip("_") + ".ipynb"

# ------------------- Main -------------------
def main():
    print("Quarto → Colab R Notebook Converter (with auto-repair)\n")
    folder = input("Folder with .qmd/.Rmd files: ").strip().strip('"\'')
    out = input("Output folder [Colab_Notebooks]: ").strip() or "Colab_Notebooks"

    in_dir = Path(folder)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list(in_dir.rglob("*.qmd")) + list(in_dir.rglob("*.Rmd"))
    if not files:
        print("No .qmd or .Rmd files found.")
        return

    print(f"\nConverting {len(files)} file(s)...\n")
    for f in sorted(files):
        convert_file(f, out_dir / slug(f.stem))

    print(f"\nAll done! Output → {out_dir.resolve()}")

if __name__ == "__main__":
    main()