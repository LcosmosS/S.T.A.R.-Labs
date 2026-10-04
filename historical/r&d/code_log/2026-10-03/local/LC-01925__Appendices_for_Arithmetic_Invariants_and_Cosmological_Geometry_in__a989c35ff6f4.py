os.makedirs("visualizations",  exist_ok=True)  
chunksize  =  10000  
 
#  Process  chunk  with  enhanced  real  parameters  
def  process_chunk(chunk):  
    chunk  =  chunk.copy()  
    chunk.replace(-9999,  np.nan,  inplace=True)  
    key_cols  =  ['z',  'Fg',  'Fr',  'Fz',  'EBV',  'plx',  'pmRA',  'pmDE',  'Chi2',  'delChi2',  'TSNR2_ELG',  
'TSNR2_LRG',
 
'Morph',
