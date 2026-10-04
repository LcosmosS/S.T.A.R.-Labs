python star_docgen_v0-2.py \
  --corpus /home/kepler/star_docgen/corpus \
  --output /home/kepler/star_docgen/output \
  --model llama3:latest \
  --docs \
    Arithmetic_Invariants_and_Cosmological_Geometry_in_Cartography_.pdf \
    Appendices_for_Arithmetic_Invariants_and_Cosmological_Geometry_in_Cartography.pdf \
    Origins.pdf \
  --analyze \
  --max-pages 300 \
  --chunk-pages 4 \
  --overlap-pages 1
