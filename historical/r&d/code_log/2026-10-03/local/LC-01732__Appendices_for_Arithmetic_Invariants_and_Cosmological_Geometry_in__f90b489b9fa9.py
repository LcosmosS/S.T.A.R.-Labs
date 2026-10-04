axis=1)
         chunk[['coeff_a',  'coeff_b']]  =  pd.DataFrame(coeffs.tolist(),  
index=chunk.index)
                  def  process_curve(row):              if  pd.isna(row['coeff_a'])  or  pd.isna(row['coeff_b']):  return  np.nan              try:  return  EllipticCurve(QQ,  [0,  0,  0,  row['coeff_a'],  
