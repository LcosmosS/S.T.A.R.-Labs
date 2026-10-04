import pandas as pd
df = pd.read_csv('galaxies.csv')
masses = [10**lm for lm in df['log_mass']]
with open('masses.txt', 'w') as f:
   *     f.write(', '.join(map(str, masses)))
* Redshifts (redshifts.txt):
   * Use z values directly (e.g., 0.0213, 0.0157, ...).
   * Python:
   * python
with open('redshifts.txt', 'w') as f:
   *     f.write(', '.join(map(str, df['z'])))
* Place files in your PARI/GP directory.
