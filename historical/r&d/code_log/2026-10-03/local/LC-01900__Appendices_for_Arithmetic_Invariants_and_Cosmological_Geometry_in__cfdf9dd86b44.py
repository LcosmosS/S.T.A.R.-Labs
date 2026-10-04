os.makedirs("visualizations",  exist_ok=True)  
 
#  Load/Clean  
df  =  pd.read_csv("1760769987443A.csv")  
df.replace(-9999,  np.nan,  inplace=True)  
key_cols  =  ['z',  'Fg',  'Fr',  'Fz',  'EBV',  'plx',  'pmRA',  'pmDE']  
df.dropna(subset=key_cols,  inplace=True)  
df  =  df[(df['Fg']  >  0)  &  (df['Fr']  >  0)  &  (df['Fz']  >  0)]  
 
#  Features  
df['flux_gr']  =  df['Fg']  /  df['Fr']  
df['flux_rz']  =  df['Fr']  /  df['Fz']  
df['log_EBV']  =  np.log(df['EBV']  +  1e-6)  
df['pm_mag']  =  np.sqrt(df['pmRA']**2  +  df['pmDE']**2)  
 
#  Regime  split  with  imputation  for  small  sets  
from  sklearn.impute  import  SimpleImputer  
imputer  =  SimpleImputer(strategy='mean')  
df_gal  =  df[df['z']  <  0.1]  