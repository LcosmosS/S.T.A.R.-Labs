   python3 -c "
   from PIL import Image; import os
   im = Image.open('public/og.jpg')
   kb = os.path.getsize('public/og.jpg') // 1024
   print(im.size, f'{kb} KB')"
   # expect: (1200, 630) and under 600 KB (keeps X and other scrapers
   # reliable; target <= 300 KB — if over, bump -q:v up a step and re-encode)
