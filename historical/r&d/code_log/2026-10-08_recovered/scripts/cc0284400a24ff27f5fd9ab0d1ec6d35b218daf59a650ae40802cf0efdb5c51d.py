import os

for root, dirs, files in os.walk("/"):
 for file in files:
  if "best_gb_model.pkl" in file:
   print(os.path.join(root, file))
