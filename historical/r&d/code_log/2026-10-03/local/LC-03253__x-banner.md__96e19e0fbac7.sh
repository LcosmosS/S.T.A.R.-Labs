ffmpeg -y -i banner-raw.jpg \
  -vf "scale=1200:264:force_original_aspect_ratio=increase,crop=1200:264" \
  -q:v 4 /workspace/.grok/x-banner.jpg.tmp
node scripts/write-atomic.mjs /workspace/.grok/x-banner.jpg.tmp public/x-banner.jpg
