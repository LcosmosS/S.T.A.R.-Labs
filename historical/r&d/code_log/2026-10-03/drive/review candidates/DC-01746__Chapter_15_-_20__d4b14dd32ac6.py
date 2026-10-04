   df = pd.read_csv(filepath)
   # Basic cleaning: handle missing values
   for col in df.select_dtypes(include=np.number).columns:
       if df[col].isnull().any():
           df[col].fillna(df[col].median(), inplace=True)
   return df

# --- Block 2: Theory-Driven Feature Engineering ---
def create_symbolic_features(df):
