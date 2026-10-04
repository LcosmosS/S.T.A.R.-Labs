df_mangahi = pd.read_csv('mangaHIall.csv')
df_mangahi.columns = df_mangahi.columns.str.strip()  # Remove leading/trailing spaces
print("Columns in mangaHIall.csv after stripping:", df_mangahi.columns.tolist())
if 'mangaid' not in df_mangahi.columns:
    # Look for similar names
