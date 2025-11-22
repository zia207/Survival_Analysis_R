#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Batch repair Jupyter notebooks missing 'outputs' in code cells.
Usage: python repair_all_notebooks.py [directory]
       (default directory: current folder)
"""

import json
import sys
from pathlib import Path

def repair_notebook(file_path: Path) -> bool:
    """Repair a single notebook file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ [JSON ERROR] {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ [READ ERROR] {file_path}: {e}")
        return False

    # Ensure it's a notebook with cells
    if not isinstance(data, dict) or "cells" not in data:
        print(f"❌ [NOT A NOTEBOOK] {file_path}")
        return False

    fixed = False
    for cell in data["cells"]:
        if isinstance(cell, dict) and cell.get("cell_type") == "code":
            if "outputs" not in cell:
                cell["outputs"] = []
                fixed = True
            if "execution_count" not in cell:
                cell["execution_count"] = None
                fixed = True

    if fixed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # Use compact JSON like Jupyter does
                json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
            print(f"✅ [FIXED] {file_path}")
        except Exception as e:
            print(f"❌ [WRITE ERROR] {file_path}: {e}")
            return False
    else:
        print(f"✔️ [OK] {file_path}")
    return True

def main(target_dir: str = "."):
    root = Path(target_dir).resolve()
    if not root.is_dir():
        print(f"❌ Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    notebook_files = list(root.rglob("*.ipynb"))
    if not notebook_files:
        print(f"ℹ️ No .ipynb files found in '{root}'.")
        return

    print(f"🔧 Found {len(notebook_files)} notebook(s) in '{root}'. Repairing...\n")
    success_count = 0
    for nb_file in notebook_files:
        if repair_notebook(nb_file):
            success_count += 1

    print(f"\n✅ Repaired {success_count}/{len(notebook_files)} notebooks.")

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    main(directory)