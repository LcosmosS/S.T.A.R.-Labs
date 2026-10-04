# --target is ONLY: player | npc | creature | asset
# Map character/spell/projectile/prop/summon/fx → --target asset (or player/npc/creature).
# --mode must be a known grid mode (idle/walk/attack/shoot/jump/…) OR pass both --rows and --cols.
python3 .grok/skills/generate2dsprite/scripts/generate2dsprite.py process \
  --input <run-dir>/raw-sheet.png \
  --target <player|npc|creature|asset> \
  --mode <idle|walk|run|attack|shoot|jump|cast|hurt|projectile|impact|fx|player_sheet|…> \
  --output-dir <run-dir> \
  --shared-scale \
  --align feet
# Custom grid example:
#   --mode sheet --rows 2 --cols 3 --label-prefix frame
