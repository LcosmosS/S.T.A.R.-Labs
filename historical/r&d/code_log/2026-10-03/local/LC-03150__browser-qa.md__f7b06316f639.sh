mkdir -p /workspace/screenshots
node scripts/browser-smoke.mjs http://127.0.0.1:8080/ /workspace/screenshots/app-builder-preview.png
# Writes app-builder-preview.png (desktop), -mobile.png, and .json (verdict).
# Then Read BOTH PNGs in one batched read if you have an image tool, and iterate if either looks wrong.
