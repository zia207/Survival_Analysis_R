#!/usr/bin/env python3
"""
Batch convert Quarto Markdown (.qmd) files to Google Colab-ready .ipynb notebooks.
Supports R code chunks via %%R magic and enforces user-specified formatting rules.
"""

import re
import argparse
from pathlib import Path
import nbformat as nbf


def remove_knitr_quarto_options(content: str) -> str:
    """Remove Quarto/knitr option lines starting with '#|'."""
    lines = content.splitlines()
    return "\n".join(line for line in lines if not line.strip().startswith("#|"))


def remove_layout_block(content: str) -> str:
    """Remove the specific ::: {layout-ncol="3"} block with image links."""
    pattern = r":::\s*\{layout-ncol=\"3\"\}.*?:::"
    return re.sub(pattern, "", content, flags=re.DOTALL)


def convert_qmd_to_ipynb(qmd_path: Path, output_dir: Path):
    with open(qmd_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Apply cleaning rules
    content = remove_layout_block(content)
    content = remove_knitr_quarto_options(content)

    # Prepare notebook
    cells = []

    # Rule 5: First cell = image
    image_md = '![All-test](http://drive.google.com/uc?export=view&id=1bLQ3nhDbZrCCqy_WCxxckOne2lgVvn3l)'
    cells.append(nbf.v4.new_markdown_cell(image_md))

    # Parse chunks
    lines = content.splitlines()
    i = 0
    first_r_seen = False
    chunk_start_re = re.compile(r"^```{(\w+)}")
    chunk_end_re = re.compile(r"^```$")

    while i < len(lines):
        line = lines[i].rstrip()
        start_match = chunk_start_re.match(line)

        if start_match:
            lang = start_match.group(1)
            i += 1
            code_lines = []
            while i < len(lines):
                l = lines[i].rstrip()
                if chunk_end_re.match(l):
                    break
                code_lines.append(lines[i])  # keep original, including indent
                i += 1
            i += 1  # skip closing ```

            code_body = "\n".join(code_lines)

            if lang.lower() == "r":
                if not first_r_seen:
                    # Rule 6: Insert Colab setup before FIRST R chunk (with duplicate mount)
                    setup_code = '''# Install rpy2
from google.colab import drive
drive.mount('/content/drive')

## Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')'''
                    cells.append(nbf.v4.new_code_cell(setup_code))
                    first_r_seen = True
                cells.append(nbf.v4.new_code_cell("%%R\n" + code_body))
            else:
                # e.g., {python}, {bash}, etc.
                cells.append(nbf.v4.new_code_cell(code_body))
        else:
            # Accumulate markdown lines
            md_lines = []
            while i < len(lines):
                l = lines[i].rstrip()
                if chunk_start_re.match(l):
                    break
                md_lines.append(lines[i])
                i += 1
            md_content = "\n".join(md_lines)
            cells.append(nbf.v4.new_markdown_cell(md_content))

    # Write notebook
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    output_path = output_dir / (qmd_path.stem + ".ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"✅ Converted: {qmd_path.name} → {output_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert .qmd (Quarto Markdown) files to Colab-ready .ipynb notebooks."
    )
    parser.add_argument("input_dir", help="Directory containing .qmd files")
    parser.add_argument("output_dir", help="Directory to save .ipynb files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    qmd_files = list(input_dir.glob("*.qmd"))
    if not qmd_files:
        print(f"⚠️ No .qmd files found in {input_dir}")
        return

    for qmd_file in qmd_files:
        convert_qmd_to_ipynb(qmd_file, output_dir)

    print(f"\n🎉 Done! Converted {len(qmd_files)} .qmd file(s) to {output_dir}")


if __name__ == "__main__":
    main()