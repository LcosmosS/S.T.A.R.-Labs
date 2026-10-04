import  plotly.graph_objects  as  go  
import  matplotlib.pyplot  as  plt  
import  seaborn  as  sns  
import  os  
 
pd.set_option('mode.chained_assignment',  None)  
os.makedirs("visualizations",  exist_ok=True)  
chunksize  =  10000  
 
#  Process  chunk  
def  process_chunk(chunk):  
    chunk  =  chunk.copy()  
    chunk.replace(-9999,  np.nan,  inplace=True)  
    key_cols  =  ['z',  'Fg',  'Fr',  'Fz',  'EBV',  'plx',  'pmRA',  'pmDE',  'Chi2',  'delChi2',  'TSNR2_ELG',  
'TSNR2_LRG',
 
'Morph',
