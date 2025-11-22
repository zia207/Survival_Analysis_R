#!/bin/bash
# Convert all .qmd files in R_Markdown → Colab-ready .ipynb with %%R cells

INPUT_DIR="$HOME/Dropbox/WebSites/R_Website/Survival_Analysis_R/R_Markdown"
OUTPUT_DIR="$HOME/Dropbox/WebSites/R_Website/Survival_Analysis_R/Colab_Notebook"

mkdir -p "$OUTPUT_DIR"

python batch_qmd_to_ipynb.py \
  "$INPUT_DIR" \
  --output "$OUTPUT_DIR" \
  --add-r-magic \
  --recursive \
  --verbose

echo "Conversion complete!"
echo "Output folder: $OUTPUT_DIR"