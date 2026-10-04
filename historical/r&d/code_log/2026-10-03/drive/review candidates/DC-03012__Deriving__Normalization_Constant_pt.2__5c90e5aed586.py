import pandas as pd df = pd.read_csv('galaxies.csv') masses = [10**lm for lm in df['log_mass']] with open('masses.txt', 'w') as f: f.write(', '.join(map(str, masses)))
