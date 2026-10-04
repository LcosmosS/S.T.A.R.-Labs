python3 .grok/skills/generate2dmap/scripts/extract_prop_pack.py \
  --input assets/props/raw/<name>-sheet.png \
  --rows 3 --cols 3 \
  --labels <comma-separated-labels> \
  --output-dir assets/props \
  --manifest assets/props/<name>-prop-pack.json \
  --component-mode largest
