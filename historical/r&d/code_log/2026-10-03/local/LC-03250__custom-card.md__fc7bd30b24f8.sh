   ffmpeg -y -i card-raw.jpg \
     -vf "scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630" \
     -q:v 4 /workspace/.grok/og.jpg.tmp
   node scripts/write-atomic.mjs /workspace/.grok/og.jpg.tmp public/og.jpg
