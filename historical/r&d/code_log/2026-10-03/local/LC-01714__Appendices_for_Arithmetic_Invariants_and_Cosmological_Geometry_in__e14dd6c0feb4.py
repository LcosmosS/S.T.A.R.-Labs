 def  run_predictive_modeling(df):      features  =  ['discriminant',  'z',  'logmass',  'petrorad_r',  'density_kg_m3']      target  =  'virial_energy_j'           X  =  df[features]      y  =  df[target]           X_train,  X_test,  y_train,  y_test  =  train_test_split(X,  y,  test_size=0.25,  
random_state=42)
          print(f"   -  Data  split  into  {len(X_train)}  training  samples  and  {len(X_test)}  test  
