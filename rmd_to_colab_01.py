#!/usr/bin/env python3
"""
Convert .qmd (Quarto Markdown) files to Google Colab-ready .ipynb notebooks.
- First cell: specified image
- All headings (#, ##, etc.) → individual Markdown cells
- R chunks → %%R, with Colab setup inserted once before first R chunk
- Remove #| options and layout block
"""

import re
import argparse
from pathlib import Path
import nbformat as nbf


def remove_knitr_quarto_options(content: str) -> str:
    lines = content.splitlines()
    return "\n".join(line for line in lines if not line.strip().startswith("#|"))


def remove_layout_block(content: str) -> str:
    pattern = r":::\s*\{layout-ncol=\"3\"\}.*?:::"
    return re.sub(pattern, "", content, flags=re.DOTALL)


def is_heading_line(line: str) -> bool:
    """Check if line is a Markdown heading (atx style: # Heading)."""
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return False
    # Must have a space after #s or end of line (valid heading)
    after_hash = stripped.lstrip("#")
    return after_hash.startswith(" ") or after_hash == ""


def split_markdown_into_heading_cells(md_lines):
    """Split a list of Markdown lines into cells, isolating each heading into its own cell."""
    cells = []
    current_block = []

    for line in md_lines:
        if is_heading_line(line):
            # Flush current block if not empty
            if current_block:
                cells.append("\n".join(current_block))
                current_block = []
            # Add heading as its own cell
            cells.append(line)
        else:
            current_block.append(line)

    # Flush remaining
    if current_block:
        cells.append("\n".join(current_block))

    return cells


def convert_qmd_to_ipynb(qmd_path: Path, output_dir: Path):
    with open(qmd_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = remove_layout_block(content)
    content = remove_knitr_quarto_options(content)

    cells = []

    # Rule: First Markdown cell = image
    image_md = '![All-test](http://drive.google.com/uc?export=view&id=1bLQ3nhDbZrCCqy_WCxxckOne2lgVvn3l)'
    cells.append(nbf.v4.new_markdown_cell(image_md))

    # Parse content into chunks
    lines = content.splitlines()
    i = 0
    first_r_seen = False
    chunk_start_re = re.compile(r"^```{(\w+)}")
    chunk_end_re = re.compile(r"^```$")

    while i < len(lines):
        line = lines[i]
        if chunk_start_re.match(line.rstrip()):
            # --- Handle code chunk ---
            lang = chunk_start_re.match(line.rstrip()).group(1)
            i += 1
            code_lines = []
            while i < len(lines):
                l = lines[i].rstrip()
                if chunk_end_re.match(l):
                    break
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```

            code_body = "\n".join(code_lines)

            if lang.lower() == "r":
                if not first_r_seen:
                    # Insert Colab setup in its own code cell
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
                cells.append(nbf.v4.new_code_cell(code_body))
        else:
            # --- Accumulate consecutive non-code lines for Markdown processing ---
            md_buffer = []
            while i < len(lines):
                l = lines[i]
                if chunk_start_re.match(l.rstrip()):
                    break
                md_buffer.append(l)
                i += 1

            # Split buffer into heading-separated cells
            heading_cells = split_markdown_into_heading_cells(md_buffer)
            for cell_content in heading_cells:
                # Only add non-empty or meaningful cells
                if cell_content.strip() != "" or (
                    "\n" in cell_content or cell_content.strip()
                ):
                    cells.append(nbf.v4.new_markdown_cell(cell_content))

    # Write notebook
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    output_path = output_dir / (qmd_path.stem + ".ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"✅ Converted: {qmd_path.name} → {output_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert .qmd files to Colab-ready .ipynb with heading isolation."
    )
    parser.add_argument("input_dir", help="Directory containing .qmd files")
    parser.add_argument("output_dir", help="Output directory for .ipynb files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    qmd_files = list(input_dir.glob("*.qmd"))
    if not qmd_files:
        print(f"⚠️ No .qmd files found in {input_dir}")
        return

    for qmd_file in qmd_files:
        convert_qmd_to_ipynb(qmd_file, output_dir)

    print(f"\n🎉 Done! Converted {len(qmd_files)} file(s).")


if __name__ == "__main__":
    main()