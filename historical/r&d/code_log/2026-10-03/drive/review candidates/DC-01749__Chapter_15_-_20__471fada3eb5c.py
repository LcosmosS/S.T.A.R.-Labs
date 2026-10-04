   # 2. Create L_cosmo_s features
   s_values = [0.5, 1.0, 1.5, 2.0]
   alpha = -1.5
   M_star = df['logmass'].median()
   
   df['a_n'] = (10**df['logmass'])**(1 + alpha) * np.exp(-10**df['logmass'] / (10**M_star))
   df['z_bin'] = pd.qcut(df['z'], q=20, labels=False, duplicates='drop')
   
   for s in s_values:
       l_cosmo_means = df.groupby('z_bin')['a_n'].transform('mean')
       df[f'L_cosmo_s{s}'] = l_cosmo_means / (df['z_bin']**s)
       df[f'L_cosmo_s{s}'].fillna(0, inplace=True)

   return df

# --- Block 3: Model Training and Evaluation ---
def train_and_evaluate(X, y):
