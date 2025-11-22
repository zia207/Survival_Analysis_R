# fix_r_notebooks.py
import json
from pathlib import Path
import re

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip())

def process_notebook(filepath: Path):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed = False

    for cell in nb.get('cells', []):
        if cell['cell_type'] != 'code':
            continue

        lines = cell['source']
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # 1. Remove any #| lines completely
            if line.strip().startswith('#|'):
                changed = True
                i += 1
                continue

            # 2. & 3. Look for the two R blocks (very tolerant matching)
            if i + 6 < len(lines) and lines[i].strip() == '%%R':
                block = ''.join(lines[i:i+10])  # grab enough lines

                # — Install packages block —
                if ('Install missing packages' in block and 
                    'installed.packages()' in block and 
                    'install.packages(new_packages' in block or 'install.packages(new.packages' in block):

                    print(f"  → Found & replacing install block in {filepath.name}")
                    new_lines.extend([
                        '%%R\n',
                        '# Install missing packages\n',
                        "new.packages <- packages[!(packages %in% installed.packages(lib='drive/My Drive/R/')[,'Package'])]\n",
                        "if(length(new.packages)) install.packages(new.packages, lib='drive/My Drive/R/')\n",
                        '\n'
                    ])
                    changed = True
                    # skip the old block (usually 4–6 lines)
                    while i < len(lines) and not lines[i].strip().startswith('%%R') and 'install.packages' in lines[i]:
                        i += 1
                    i += 1
                    continue

                # — Library loading block —
                if ('Load packages with suppressed messages' in block and 
                    'invisible(lapply' in block and 
                    'suppressPackageStartupMessages' in block):

                    print(f"  → Found & replacing library block in {filepath.name}")
                    new_lines.extend([
                        '%%R\n',
                        '# set library path\n',
                        ".libPaths('drive/My Drive/R')\n",
                        '# Load packages with suppressed messages\n',
                        'invisible(lapply(packages, function(pkg) {\n',
                        '  suppressPackageStartupMessages(library(pkg, character.only = TRUE))\n',
                        '}))', '\n', '\n'
                    ])
                    changed = True
                    # skip old block
                    i += 1
                    while i < len(lines) and '}))' not in lines[i]:
                        i += 1
                    i += 1  # skip the }}) line
                    continue

            new_lines.append(line)
            i += 1

        cell['source'] = new_lines

    if changed:
        # Jupyter standard: indent=1 + trailing newline
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print(f"Successfully MODIFIED: {filepath.name}\n")
    else:
        print(f"No changes needed in: {filepath.name}")

    return changed


# —————————————————————— RUN ——————————————————————
if __name__ == '__main__':
    folder = Path(".")  # ← Change this if your notebooks are elsewhere
    # folder = Path("/path/to/your/notebooks")

    notebooks = [p for p in folder.glob("*.ipynb") 
                 if not p.name.startswith('.') and 'checkpoint' not in p.name.lower()]

    if not notebooks:
        print("No .ipynb files found!")
    else:
        print(f"Found {len(notebooks)} notebooks → starting...\n")
        modified = sum(process_notebook(nb) for nb in notebooks)
        print(f"\nFinished! {modified} notebook(s) updated.")