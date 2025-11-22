import json

with open('/home/zia207/Dropbox/WebSites/R_Website/Survival_Analysis_R/Colab_Notebook/02_07_01_01_survival_analysis_kaplan_meier_r.ipynb', 'r', encoding='utf-8') as f:
    content = f.read()

# Try to parse
try:
    data = json.loads(content)
    print("✅ Valid JSON")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON at line {e.lineno}, col {e.colno}: {e.msg}")
    exit(1)

# Check every code cell
for i, cell in enumerate(data.get('cells', [])):
    if cell.get('cell_type') == 'code':
        if 'outputs' not in cell:
            print(f"❌ Cell {i}: missing 'outputs'")
        if 'execution_count' not in cell:
            print(f"⚠️ Cell {i}: missing 'execution_count' (not fatal, but should be added)")